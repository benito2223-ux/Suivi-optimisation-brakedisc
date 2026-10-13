# AUDIT CLOUD / RLS — les 10 lignes (revue Claude P1)

- **Ce qui est poussé** : une table `etat`, une ligne = le suivi complet
  (~3,4 Mo : références, essais, prix, volumes, photos en base64), +
  `etat_historique` (20 versions, trim par trigger). Le catalogue et le Plan
  de conversion ne sont PAS encore dans le payload cloud (locale only).
- **Vers quelle table** : `etat` (une ligne), projet Supabase `suivi-septfons`
  (org « Sept Fons », région EU).
- **Quelle clé** : la clé `publishable` (anon) est dans le HTML public — par
  conception, elle ne donne aucun droit sans être authentifié.
- **RLS** : `authenticated` + GRANT sur les tables. **Quiconque crée un compte
  peut lire et écrire.** La porte est la page de login.
- **À décider par Benjamin** : fermer les inscriptions dans le dashboard
  Supabase (Authentication → Providers → Email : désactiver le signup) tant
  que l'accord client sur l'hébergement des données n'est pas écrit.
- **Le cloud est actuellement en 402** (quota egress épuisé) : aucun transfert
  ne passe tant que le quota n'est pas réinitialisé ou le plan pas upgradé.
- **Si le cloud est jugé incompatible** : il se désactive par défaut (le
  tooling tourne 100 % offline, la synchro est optionnelle et coupable par
  une constante).
- **Le calcul qui produit K et P_req n'est PAS dans ce fichier** — le secret
  thermique vit dans l'app conseiller (autre projet). L'aide qui l'exposait a
  été retirée en 4.89.1 et la porte hors-suite l'interdit.

*Z Code — 14/10/2026, Tour 73.*
