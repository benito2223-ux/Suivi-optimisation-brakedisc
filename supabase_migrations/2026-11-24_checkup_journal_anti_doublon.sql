-- Appliquee le 24/11/2026 (migrations « checkup_journal_anti_doublon » puis « …_trigger »).
-- L'essai ON CONFLICT (id_local) a echoue : il exige un droit SELECT pour anon + une policy de lecture. Remplace par un trigger.
revoke select (id_local) on public.checkup_journal from anon;
create or replace function public.checkup_journal_ignorer_doublon() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.id_local is not null and exists (select 1 from public.checkup_journal j where j.id_local = new.id_local) then
    return null;
  end if;
  return new;
end $$;
revoke all on function public.checkup_journal_ignorer_doublon() from public, anon, authenticated;
create trigger checkup_journal_doublon before insert on public.checkup_journal
  for each row execute function public.checkup_journal_ignorer_doublon();
