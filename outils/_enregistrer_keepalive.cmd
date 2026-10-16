@echo off
REM Enregistre la tache planifiee du keep-alive Supabase, l'execoute une fois,
REM puis affiche son etat. A lancer une seule fois.
schtasks /Create /F /TN "Supabase keepalive suivi-septfons" /TR "C:\Users\Admin\Desktop\Stellantis_SeptFons\outils\supabase_keepalive.cmd" /SC DAILY /ST 09:17
schtasks /Run /TN "Supabase keepalive suivi-septfons"
timeout /t 4 /nobreak > NUL
schtasks /Query /TN "Supabase keepalive suivi-septfons" /FO LIST
