-- Amorcage de public.checkup_reference (projet cxjfyaorkkxemjnollnj) depuis les shards de l'outil principal.
-- A executer UNE FOIS dans le SQL Editor Supabase (role postgres, contourne la RLS), puis a rejouer apres une modif de charniere.
-- Meme logique que chargerDepuisSyncShards() de checkup.html : arbre 'tree' + scenarios 'sc:<opId>:<scenarioId>'.
-- Scenario retenu : serie+baseline > baseline > serie > premier avec outils. Idempotent (upsert, version incrementee).
-- Verifier apres : select ligne, reference, op, jsonb_array_length(contenu->'rows') from checkup_reference order by 1,2,3;
-- Si l'espace n'est pas 'prod' ou si les colonnes different, ajuster le where (sync_shards : espace, id, body, supprime).
with tree as (
  select body from sync_shards where espace = 'prod' and id = 'tree' and coalesce(supprime,false) = false limit 1
),
ops as (
  select l->>'nom' as ligne, r->>'nom' as reference,
         coalesce(o->>'nom', o->>'code', 'OP') as op, o->>'id' as op_id, o->'scenarioIds' as sids
  from tree t,
       jsonb_array_elements(t.body) l,
       jsonb_array_elements(coalesce(l->'references','[]'::jsonb)) r,
       jsonb_array_elements(coalesce(r->'ops','[]'::jsonb)) o
),
scs as (
  select o.ligne, o.reference, o.op, s.body as sc,
         row_number() over (partition by o.ligne, o.reference, o.op order by
           case when s.body->>'statut'='serie' and (s.body ? 'baseline' or s.body ? 'base') then 0
                when s.body ? 'baseline' or s.body ? 'base' then 1
                when s.body->>'statut'='serie' then 2
                when jsonb_array_length(coalesce(s.body->'outils','[]'::jsonb))>0 then 3 else 4 end) as rg
  from ops o
  join lateral jsonb_array_elements_text(coalesce(o.sids,'[]'::jsonb)) cid on true
  join sync_shards s on s.espace='prod' and s.id = 'sc:' || o.op_id || ':' || cid and coalesce(s.supprime,false)=false
),
rangees as (
  select c.ligne, c.reference, c.op,
    jsonb_agg(jsonb_build_array(
      coalesce(ot->>'numero', ot->>'nom', ot->>'id', 'Outil'),
      coalesce(lg->>'nom','Logement'),
      coalesce(lg->>'ref', lg->>'plaquette', ''),
      coalesce(lg->>'mabec',''),
      coalesce(lg->>'charniere',''),
      coalesce(lg->>'vc',''), coalesce(lg->>'f',''),
      coalesce(lg->>'modeVitesse', lg->>'mode',''),
      coalesce(lg->>'sBroche','')) ) as rows
  from scs c,
       jsonb_array_elements(coalesce(c.sc->'outils','[]'::jsonb)) ot,
       jsonb_array_elements(coalesce(ot->'logements','[]'::jsonb)) lg
  where c.rg = 1
  group by c.ligne, c.reference, c.op
)
insert into public.checkup_reference (id, ligne, reference, op, contenu, version, publie_le, publie_par)
select ligne || '/' || reference || '/' || op, ligne, reference, op,
       jsonb_build_object('rows', rows), 1, now(), 'amorcage-sql'
from rangees
on conflict (id) do update
  set contenu = excluded.contenu, version = checkup_reference.version + 1,
      publie_le = now(), publie_par = excluded.publie_par;
