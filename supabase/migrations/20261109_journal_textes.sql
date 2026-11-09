-- 09/11/2026 — Journal permanent des textes d'essais : plus aucun texte écrit ne disparaît.
-- Cause : l'historique serveur ne garde que 10 versions par enregistrement ; un texte écrasé
-- (fusion entre appareils, essai supprimé ou déplacé, champ vidé) disparaissait pour de bon.
-- Ici : un trigger archive, AVANT toute mise à jour ou suppression d'un scénario, chaque texte
-- (observations, conclusion, objectif, détail d'arrêt, motif du scénario) qui n'est plus contenu
-- dans la nouvelle version. Table append-only, dédupliquée, jamais purgée.
-- Lecture : service_role / SQL uniquement (RLS activée sans politique, droits retirés).

create table if not exists public.sync_textes (
  id bigint generated always as identity primary key,
  espace text not null,
  shard_id text not null,
  essai_id text not null default '',
  champ text not null,
  texte text not null,
  empreinte text generated always as (md5(texte)) stored,
  archive_le timestamptz not null default now(),
  rev_source integer,
  modifie_par text,
  origine text not null default 'trigger'
);
create unique index if not exists sync_textes_uniq on public.sync_textes (espace, shard_id, essai_id, champ, empreinte);
create index if not exists sync_textes_recherche on public.sync_textes (espace, shard_id);
alter table public.sync_textes enable row level security;
revoke all on public.sync_textes from anon, authenticated;

create or replace function public.sync_norm(t text) returns text
language sql immutable as $$ select lower(regexp_replace(coalesce(t, ''), '\s+', ' ', 'g')) $$;

create or replace function public.sync_textes_de(b jsonb)
returns table(essai_id text, champ text, texte text)
language sql immutable as $$
  select ''::text, 'statutMotif'::text, trim(coalesce(b->>'statutMotif', ''))
  union all
  select coalesce(e->>'id', ''), c.champ,
         trim(coalesce(case c.champ when 'detail' then e->'cloture'->>'detail' else e->>c.champ end, ''))
  from jsonb_array_elements(case when jsonb_typeof(b->'essais') = 'array' then b->'essais' else '[]'::jsonb end) e,
       (values ('observations'), ('conclusion'), ('but'), ('detail')) c(champ)
$$;

create or replace function public.sync_archiver_textes() returns trigger
language plpgsql security definer set search_path = public as $$
declare
  r record;
  nouveau text;
  supprime boolean;
begin
  if OLD.id not like 'sc:%' or OLD.body is null then
    if TG_OP = 'DELETE' then return OLD; else return NEW; end if;
  end if;
  if TG_OP = 'DELETE' then supprime := true; else supprime := coalesce(NEW.supprime, false); end if;
  for r in select * from public.sync_textes_de(OLD.body) t where length(t.texte) >= 3 loop
    nouveau := null;
    if not supprime then
      select x.texte into nouveau from public.sync_textes_de(NEW.body) x
       where x.essai_id = r.essai_id and x.champ = r.champ limit 1;
    end if;
    if nouveau is null or position(public.sync_norm(r.texte) in public.sync_norm(nouveau)) = 0 then
      insert into public.sync_textes(espace, shard_id, essai_id, champ, texte, rev_source, modifie_par)
      values (OLD.espace, OLD.id, r.essai_id, r.champ, r.texte, OLD.rev,
              case when TG_OP = 'DELETE' then OLD.modifie_par else coalesce(NEW.modifie_par, OLD.modifie_par) end)
      on conflict do nothing;
    end if;
  end loop;
  if TG_OP = 'DELETE' then return OLD; else return NEW; end if;
end $$;

drop trigger if exists sync_shards_textes on public.sync_shards;
create trigger sync_shards_textes before update or delete on public.sync_shards
  for each row execute function public.sync_archiver_textes();

-- reprise : tout ce que l'historique et les sauvegardes du 09/11 contiennent déjà
insert into public.sync_textes(espace, shard_id, essai_id, champ, texte, rev_source, modifie_par, archive_le, origine)
select s.espace, s.id, t.essai_id, t.champ, t.texte, s.rev, s.modifie_par, s.modifie_le, 'reprise'
from (
  select espace, id, rev, modifie_par, modifie_le, body from public.sync_historique
  union all select espace, id, rev, modifie_par, modifie_le, body from public.sync_shards
  union all select espace, id, rev, modifie_par, modifie_le, body from public.sync_secours_20261109
  union all select espace, id, rev, modifie_par, modifie_le, body from public.sync_secours_hist_20261109
  union all select espace, id, rev, modifie_par, modifie_le, body from public.sync_secours_orphelins_20261109
) s, lateral public.sync_textes_de(s.body) t
where s.id like 'sc:%' and length(t.texte) >= 3
on conflict do nothing;
