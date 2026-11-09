-- ============================================================================
-- Garde-fou serveur contre les suppressions et les vidages en masse (09/11/2026)
--
-- Incident : un appareil dont l'état local était vide (mémoire pleine) s'est cru synchronisé et a envoyé, en
-- quelques secondes, 82 suppressions et plusieurs réglages remplacés par des listes vides. Rien n'a été perdu
-- (historique serveur), mais le serveur ne doit JAMAIS accepter un tel envoi : une personne ne supprime pas 80
-- scénarios d'un coup, et un envoi légitime ne vide pas des enregistrements remplis.
-- Règle : dans UN envoi, au plus 5 suppressions et 3 enregistrements remplis réécrits à vide ; sinon l'envoi
-- ENTIER est refusé (rien n'est écrit).
-- ============================================================================
create or replace function public.sync_push(p_espace text, p_items jsonb) returns jsonb
language plpgsql security definer set search_path = public as $$
declare it jsonb; cur public.sync_shards%rowtype; res jsonb := '[]'::jsonb; qui text; base int; sup boolean;
        nb_sup int; nb_vide int := 0; vide boolean;
begin
  if not public.suivi_est_membre() then raise exception 'accès refusé' using errcode = '42501'; end if;
  if jsonb_typeof(p_items) <> 'array' then raise exception 'liste attendue'; end if;
  if length(p_items::text) > 8000000 then raise exception 'envoi trop volumineux'; end if;
  select count(*) into nb_sup from jsonb_array_elements(p_items) x where coalesce((x ->> 'supprime')::boolean, false);
  if nb_sup > 5 then
    raise exception 'protection : % suppressions dans un seul envoi — refusé (aucune écriture)', nb_sup using errcode = '42501';
  end if;
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
      vide := (it -> 'body') is null or jsonb_typeof(it -> 'body') = 'null' or (it -> 'body')::text in ('[]', '{}');
      if not sup and vide and not cur.supprime and length(coalesce(cur.body::text, '')) > 20 then
        nb_vide := nb_vide + 1;
        if nb_vide > 3 then
          raise exception 'protection : plusieurs enregistrements remplis réécrits à vide dans un seul envoi — refusé (aucune écriture)' using errcode = '42501';
        end if;
      end if;
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
