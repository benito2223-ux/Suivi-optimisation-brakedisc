@echo off
schtasks /Query /TN "Supabase keepalive suivi-septfons" /V /FO LIST
