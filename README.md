# Mainnet Faucet Aggregator

Annuaire statique, en une seule page, qui pointe directement vers les pages de
réclamation des faucets officiels. Aucun lien de staking, aucune redirection
intermédiaire : un clic, vous êtes sur le faucet.

Le site est une PWA installable et fonctionne hors ligne une fois chargé.

## Ce que contient le dépôt

```
index.html               page unique (design, contenu, filtres)
manifest.webmanifest     métadonnées PWA (nom, icônes, couleurs)
sw.js                    service worker (cache de la page + icônes)
icons/                   icônes PNG + SVG (source vectorielle)
tools/make-icons.py      génère les PNG depuis la géométrie de icon.svg
tools/faucets.json       données de l'annuaire (nom, token, montant, lien, réseau)
tools/build.py           régénère la grille de index.html depuis faucets.json
```

Le site publié ne dépend de rien : `index.html` est autonome et s'ouvre tel
quel. `tools/build.py` sert uniquement à réécrire la grille quand les données
changent (bibliothèque standard uniquement).

## Annuaire actuel

45 faucets, tous relevés le 24/11/2026 : **34 mainnet** et **11 testnet**.
Cela couvre les 42 pages de Stakely plus trois pages officielles (Polygon, BNB
Chain, Celo). La liste Stakely vient de `stakely.io/sitemap.xml`, qui expose les
42 pages `/faucet/<réseau>-<token>` ; chacune a été ouverte pour relever le
montant affiché (« You will get… ») et son état.

La source de vérité est `tools/faucets.json` : un objet par faucet, avec
`name`, `token`, `provider`, `amount`, `url`, `host`, `network`
(`mainnet`/`testnet`), `status` (`active`/`inactive`) et éventuellement `note`
et `extra` (liens secondaires). La page est générée à partir de ce fichier, donc
les deux compteurs du titre restent justes automatiquement.

Deux faucets sont marqués **inactif** au relevé (Ethereum mainnet, Solana
mainnet) : la carte reste affichée, montant barré et bordure pointillée, pour
éviter d'envoyer quelqu'un sur une page à sec sans prévenir.

## Mettre à jour un lien

1. Éditer `tools/faucets.json` : ajouter, retirer ou corriger une entrée.
2. Lancer `python3 tools/build.py` : la grille entre `<!-- grid:start -->` et
   `<!-- grid:end -->` est réécrite, ainsi que les compteurs du titre. Le reste
   de `index.html` (CSS, JS, textes) n'est pas touché.
3. Mettre à jour la date de relevé dans le pied de page.
4. Incrémenter `VERSION` dans `sw.js` pour que les visiteurs récupèrent la
   nouvelle version du cache.

Les compteurs « N mainnet » et « N testnet » à côté du titre sont calculés au
chargement à partir de `data-network` : ajouter ou retirer une carte met les
compteurs à jour sans autre intervention. L'année du copyright suit l'horloge du
visiteur.

## Réseaux sociaux

Le pied de page affiche X et GitHub, les deux liens vérifiés sur le profil
`moonspiid`. Pour en ajouter un, copier un `<li>` du bloc `<ul class="socials">`
et remplacer le `href`, l'`aria-label` et le tracé SVG (24 × 24, `fill`
hérité de `currentColor`). Ajouter Telegram, Discord ou YouTube revient donc à
une ligne par réseau.

## Publier sur GitHub Pages

```bash
# depuis le dépôt cloné, une fois le dépôt distant créé
git push -u origin main

# activer Pages sur la branche main, racine du dépôt
gh api -X POST repos/<owner>/mainnet-faucet-aggregator/pages \
  -f 'source[branch]=main' -f 'source[path]=/'
```

Le site est alors servi sur `https://<owner>.github.io/mainnet-faucet-aggregator/`.
Tous les chemins du projet sont relatifs, l'application fonctionne aussi bien à
la racine d'un domaine que dans un sous-dossier.

## Icônes

```bash
python3 tools/make-icons.py
```

Le script n'utilise que la bibliothèque standard (pas de Pillow). Il produit
`icon-192.png`, `icon-512.png`, `icon-maskable-512.png` et
`apple-touch-icon.png`. `icons/icon.svg` reste la référence visuelle.

## Avertissement

Les faucets changent de réseaux, de limites et de règles sans préavis. Les liens
sont vérifiés à la date indiquée dans le pied de page, sans garantie. Un faucet ne
demande jamais de phrase de récupération, et cette page ne connecte aucun wallet.
