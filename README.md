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
```

Aucune dépendance, aucun build, aucun script tiers : le site s'ouvre tel quel.

## Annuaire actuel

| Faucet | Réseau | Lien |
| --- | --- | --- |
| Stakely Faucet | Mainnet (multi-chaînes) | https://stakely.io/faucet |
| Polygon Faucet | Mainnet (POL) | https://faucet.polygon.technology/ |
| BNB Chain Faucet | Testnet (tBNB) | https://www.bnbchain.org/en/testnet-faucet |
| Celo Faucet | Testnet (CELO Sepolia) | https://faucet.celo.org/ |

Les deux dernières entrées sont marquées **Testnet** : BNB Chain ne publie pas de
faucet mainnet, et la page Celo courante distribue du CELO de test. Le CELO
mainnet reste accessible via la page Stakely dédiée, liée depuis la carte.

## Mettre à jour un lien

1. Ouvrir `index.html`, section `<div class="grid" id="grid">`.
2. Chaque faucet est un `<article class="card" data-network="mainnet|testnet">`.
   Modifier le `href` du lien principal, le libellé, la description et le
   `<span class="host">` (domaine affiché en bas de carte).
3. Mettre à jour la date de vérification dans le pied de page.
4. Incrémenter `VERSION` dans `sw.js` pour que les visiteurs récupèrent la
   nouvelle version du cache.

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
