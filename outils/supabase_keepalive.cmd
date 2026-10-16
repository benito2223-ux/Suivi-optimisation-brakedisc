@echo off
REM ============================================================================
REM keep-alive du projet Supabase suivi-septfons (cxjfyaorkkxemjnollnj)
REM ----------------------------------------------------------------------------
REM Supabase met en pause les projets gratuits sans activite pendant 7 jours.
REM Le cloud est inutilise en attendant le depot initial de Matis, donc il ne
REM genere aucune activite : cette tache en produit une, une fois par jour.
REM
REM Un simple GET REST (quelques octets) compte comme une activite base de
REM donnees. La cle est la cle publishable, publique par conception — c'est
REM la meme que celle embarquee dans bilan_economique.html.
REM
REM Tache planifiee : "Supabase keepalive suivi-septfons" (quotidienne, 09:17)
REM Supprimer : schtasks /Delete /TN "Supabase keepalive suivi-septfons" /F
REM Historique : le service est RESTREINT le 05/10/2026 pour
REM exceed_egress_quota (bande sortante) — tant que la restriction tient,
REM ces requetes recoivent un 402 ; elles redeviennent utiles apres
REM restauration. Voir ECHANGES.md, Tour 59, et la reponse a Benjamin.
REM ============================================================================

curl.exe -s -m 20 -o NUL -H apikey:sb_publishable_TQySmct-8qg3qMiS2WodbA_gQCcPp9Z https://cxjfyaorkkxemjnollnj.supabase.co/rest/v1/etat?id=eq.1
exit /b 0
