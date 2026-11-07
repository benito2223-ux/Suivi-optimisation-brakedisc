-- ============================================================================
-- Suivi d'optimisation — synchronisation v2 (par enregistrement, hors ligne d'abord)
-- Projet : xlpfwvipdmgslwpbbfxs (hébergé avec l'app Fellow : on n'ajoute QUE des objets suivi_* / sync_*)
--
-- Principes
--  · accès = appartenance à l'équipe (code d'équipe, vérifié côté serveur, haché) — PAS « tout compte
--    connecté » : l'inscription est ouverte sur ce projet, donc « authenticated » ne prouve rien ;
--  · aucune écriture directe sur les tables : tout passe par des fonctions security definer ;
--  · un « shard » = un petit enregistrement JSON (un scénario, une extraction Marposs, un réglage…) ;
--    écriture à concurrence optimiste (rev) ; le client fusionne les conflits ;
--  · espaces séparés (prod / dev / test) : le développement ne pollue plus la production ;
--  · pièces volumineuses (photos, plans) en table à part, adressées par leur empreinte.
-- ============================================================================

create extension if not exists pgcrypto with schema extensions;

-- ---------------------------------------------------------------- équipe ----
create table if not exists public.suivi_membres (
  user_id    uuid primary key,
  email      text not null default '',
  rejoint_le timestamptz not null default now()
);
create table if not exists public.suivi_code (
  id    int primary key default 1 check (id = 1),
  hache text not null
);
create table if not exists public.suivi_tentatives (
  user_id uuid not null,
  le      timestamptz not null default now()
);
create index if not exists suivi_tentatives_idx on public.suivi_tentatives (user_id, le);
alter table public.suivi_membres    enable row level security;
alter table public.suivi_code       enable row level security;
alter table public.suivi_tentatives enable row level security;
-- aucune policy : seules les fonctions security definer ci-dessous y accèdent

create or replace function public.suivi_est_membre() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.suivi_membres m where m.user_id = auth.uid());
$$;
revoke all on function public.suivi_est_membre() from public, anon;
grant execute on function public.suivi_est_membre() to authenticated;

-- rejoindre l'équipe avec le code (8 essais par heure et par compte, contre la force brute)
create or replace function public.suivi_rejoindre(p_code text) returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare h text; n int;
begin
  if auth.uid() is null then raise exception 'connexion requise' using errcode = '42501'; end if;
  if exists (select 1 from public.suivi_membres where user_id = auth.uid()) then
    return jsonb_build_object('ok', true, 'deja', true);
  end if;
  select count(*) into n from public.suivi_tentatives where user_id = auth.uid() and le > now() - interval '1 hour';
  if n >= 8 then raise exception 'trop de tentatives, réessayez dans une heure' using errcode = '42501'; end if;
  insert into public.suivi_tentatives(user_id) values (auth.uid());
  select hache into h from public.suivi_code where id = 1;
  if h is null or extensions.crypt(coalesce(p_code, ''), h) <> h then
    return jsonb_build_object('ok', false, 'raison', 'code incorrect');
  end if;
  insert into public.suivi_membres(user_id, email) values (auth.uid(), coalesce(auth.jwt() ->> 'email', ''));
  return jsonb_build_object('ok', true, 'deja', false);
end $$;
revoke all on function public.suivi_rejoindre(text) from public, anon;
grant execute on function public.suivi_rejoindre(text) to authenticated;

create or replace function public.suivi_statut() returns jsonb
language sql stable security definer set search_path = public as $$
  select jsonb_build_object('membre', public.suivi_est_membre(), 'email', coalesce(auth.jwt() ->> 'email', ''));
$$;
revoke all on function public.suivi_statut() from public, anon;
grant execute on function public.suivi_statut() to authenticated;

-- -------------------------------------------------------------- shards ------
create sequence if not exists public.sync_seq;
create table if not exists public.sync_shards (
  espace     text    not null default 'prod',
  id         text    not null,
  kind       text    not null default '',
  body       jsonb,
  rev        integer not null default 1,
  seq        bigint  not null default nextval('public.sync_seq'),
  supprime   boolean not null default false,
  modifie_par text   not null default '',
  modifie_le timestamptz not null default now(),
  primary key (espace, id)
);
create index if not exists sync_shards_seq_idx on public.sync_shards (espace, seq);
alter table public.sync_shards enable row level security;

create table if not exists public.sync_historique (
  espace text not null, id text not null, rev integer not null,
  body jsonb, supprime boolean not null default false,
  modifie_par text not null default '', modifie_le timestamptz not null default now(),
  primary key (espace, id, rev)
);
alter table public.sync_historique enable row level security;

create table if not exists public.sync_blobs (
  sha     text primary key,
  data    text not null,
  taille  integer not null,
  cree_par text not null default '',
  cree_le timestamptz not null default now()
);
alter table public.sync_blobs enable row level security;

-- historique : on garde les 10 dernières révisions de chaque shard
create or replace function public.sync_garder_historique() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.sync_historique(espace, id, rev, body, supprime, modifie_par, modifie_le)
  values (old.espace, old.id, old.rev, old.body, old.supprime, old.modifie_par, old.modifie_le)
  on conflict do nothing;
  delete from public.sync_historique h
   where h.espace = old.espace and h.id = old.id and h.rev <= old.rev - 10;
  return new;
end $$;
drop trigger if exists sync_shards_hist on public.sync_shards;
create trigger sync_shards_hist before update on public.sync_shards
  for each row execute function public.sync_garder_historique();

-- push : une liste d'enregistrements ; chaque élément {id, kind, body, base_rev, supprime}
-- réussit si base_rev = rev du serveur (0 = « je le crois nouveau »), sinon renvoie le conflit
create or replace function public.sync_push(p_espace text, p_items jsonb) returns jsonb
language plpgsql security definer set search_path = public as $$
declare it jsonb; cur public.sync_shards%rowtype; res jsonb := '[]'::jsonb; qui text; base int; sup boolean;
begin
  if not public.suivi_est_membre() then raise exception 'accès refusé' using errcode = '42501'; end if;
  if jsonb_typeof(p_items) <> 'array' then raise exception 'liste attendue'; end if;
  if length(p_items::text) > 8000000 then raise exception 'envoi trop volumineux'; end if;
  qui := coalesce(auth.jwt() ->> 'email', '');
  for it in select * from jsonb_array_elements(p_items) loop
    base := coalesce((it ->> 'base_rev')::int, 0);
    sup  := coalesce((it ->> 'supprime')::boolean, false);
    select * into cur from public.sync_shards where espace = p_espace and id = it ->> 'id' for update;
    if not found then
      insert into public.sync_shards(espace, id, kind, body, rev, supprime, modifie_par)
      values (p_espace, it ->> 'id', coalesce(it ->> 'kind', ''), it -> 'body', 1, sup, qui)
      returning * into cur;
      res := res || jsonb_build_array(jsonb_build_object('id', cur.id, 'ok', true, 'rev', cur.rev, 'seq', cur.seq));
    elsif cur.rev = base then
      update public.sync_shards
         set body = it -> 'body', kind = coalesce(it ->> 'kind', cur.kind), supprime = sup,
             rev = cur.rev + 1, seq = nextval('public.sync_seq'), modifie_par = qui, modifie_le = now()
       where espace = p_espace and id = cur.id
       returning * into cur;
      res := res || jsonb_build_array(jsonb_build_object('id', cur.id, 'ok', true, 'rev', cur.rev, 'seq', cur.seq));
    else
      res := res || jsonb_build_array(jsonb_build_object(
        'id', cur.id, 'ok', false, 'conflit', true, 'rev', cur.rev, 'seq', cur.seq,
        'body', cur.body, 'supprime', cur.supprime, 'modifie_par', cur.modifie_par));
    end if;
  end loop;
  return res;
end $$;
revoke all on function public.sync_push(text, jsonb) from public, anon;
grant execute on function public.sync_push(text, jsonb) to authenticated;

-- pull : tout ce qui a bougé depuis le curseur, dans l'ordre (par paquets)
create or replace function public.sync_pull(p_espace text, p_depuis bigint, p_limite int default 100) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare r jsonb;
begin
  if not public.suivi_est_membre() then raise exception 'accès refusé' using errcode = '42501'; end if;
  select coalesce(jsonb_agg(x order by x.seq), '[]'::jsonb) into r from (
    select s.id, s.kind, s.body, s.rev, s.seq, s.supprime, s.modifie_par
      from public.sync_shards s
     where s.espace = p_espace and s.seq > coalesce(p_depuis, 0)
     order by s.seq
     limit greatest(1, least(coalesce(p_limite, 100), 500))
  ) x;
  return r;
end $$;
revoke all on function public.sync_pull(text, bigint, int) from public, anon;
grant execute on function public.sync_pull(text, bigint, int) to authenticated;

-- pièces volumineuses adressées par empreinte : on n'envoie que ce qui manque
create or replace function public.sync_blobs_manquants(p_shas jsonb) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare r jsonb;
begin
  if not public.suivi_est_membre() then raise exception 'accès refusé' using errcode = '42501'; end if;
  select coalesce(jsonb_agg(v.sha), '[]'::jsonb) into r
    from jsonb_array_elements_text(p_shas) as v(sha)
   where not exists (select 1 from public.sync_blobs b where b.sha = v.sha);
  return r;
end $$;
revoke all on function public.sync_blobs_manquants(jsonb) from public, anon;
grant execute on function public.sync_blobs_manquants(jsonb) to authenticated;

create or replace function public.sync_blob_put(p_sha text, p_data text) returns boolean
language plpgsql security definer set search_path = public as $$
begin
  if not public.suivi_est_membre() then raise exception 'accès refusé' using errcode = '42501'; end if;
  if length(p_data) > 12000000 then raise exception 'pièce trop volumineuse'; end if;
  insert into public.sync_blobs(sha, data, taille, cree_par)
  values (p_sha, p_data, length(p_data), coalesce(auth.jwt() ->> 'email', ''))
  on conflict (sha) do nothing;
  return true;
end $$;
revoke all on function public.sync_blob_put(text, text) from public, anon;
grant execute on function public.sync_blob_put(text, text) to authenticated;

create or replace function public.sync_blob_get(p_sha text) returns text
language plpgsql stable security definer set search_path = public as $$
declare d text;
begin
  if not public.suivi_est_membre() then raise exception 'accès refusé' using errcode = '42501'; end if;
  select data into d from public.sync_blobs where sha = p_sha;
  return d;
end $$;
revoke all on function public.sync_blob_get(text) from public, anon;
grant execute on function public.sync_blob_get(text) to authenticated;

-- ------------------------------------------- l'existant : fini « tout compte connecté » ----
-- (ancienne synchro v4.8 et photos d'essai : réservées aux membres de l'équipe)
drop policy if exists "etat equipe" on public.etat;
create policy "etat equipe" on public.etat for all to authenticated
  using (public.suivi_est_membre()) with check (public.suivi_est_membre());
drop policy if exists "etat_historique equipe" on public.etat_historique;
create policy "etat_historique equipe" on public.etat_historique for all to authenticated
  using (public.suivi_est_membre()) with check (public.suivi_est_membre());
drop policy if exists "photos equipe select" on storage.objects;
create policy "photos equipe select" on storage.objects for select to authenticated
  using (bucket_id = 'photos' and public.suivi_est_membre());
drop policy if exists "photos equipe insert" on storage.objects;
create policy "photos equipe insert" on storage.objects for insert to authenticated
  with check (bucket_id = 'photos' and public.suivi_est_membre());
drop policy if exists "photos equipe update" on storage.objects;
create policy "photos equipe update" on storage.objects for update to authenticated
  using (bucket_id = 'photos' and public.suivi_est_membre()) with check (bucket_id = 'photos' and public.suivi_est_membre());
drop policy if exists "photos equipe delete" on storage.objects;
create policy "photos equipe delete" on storage.objects for delete to authenticated
  using (bucket_id = 'photos' and public.suivi_est_membre());
