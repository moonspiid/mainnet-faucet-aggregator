# Mainnet Faucet Aggregator

A single static page that links straight to the claim pages of official
faucets. No staking links, no intermediate redirects: one click and you are on
the faucet.

The site is an installable PWA and keeps working offline once loaded.

## What's in this repo

```
index.html               the whole page (design, content, filters)
manifest.webmanifest     PWA metadata (name, icons, colours)
sw.js                    service worker (caches the page and the icons)
icons/                   PNG + SVG icons (vector source)
donate-usdt-qr.png       QR code shown in the donation section
tools/make-icons.py      renders the PNGs from the geometry of icon.svg
tools/faucets.json       directory data (name, token, amount, link, network)
tools/build.py           rewrites the grid in index.html from faucets.json
```

The published site depends on nothing: `index.html` is self-contained and opens
as is. `tools/build.py` only rewrites the grid when the data changes, and uses
the standard library alone.

## Current directory

45 faucets, all checked on 24 November 2026: **34 mainnet** and **11 testnet**.
That covers the 42 Stakely pages plus three official pages (Polygon, BNB Chain,
Celo). The Stakely list comes from `stakely.io/sitemap.xml`, which exposes the
42 `/faucet/<network>-<token>` pages; each one was opened to record the amount it
prints ("You will get…") and its status.

The source of truth is `tools/faucets.json`: one object per faucet with `name`,
`token`, `provider`, `amount`, `url`, `host`, `network` (`mainnet`/`testnet`),
`status` (`active`/`inactive`) and optionally `note` and `extra` (secondary
links). The page is generated from that file, so the two counters next to the
title stay correct on their own.

Two faucets were marked **inactive** at the time of the check (Ethereum mainnet,
Solana mainnet): the card stays visible, with the amount struck through and a
dashed border, rather than silently sending someone to a dry page.

## Update a link

1. Edit `tools/faucets.json`: add, remove or fix an entry.
2. Run `python3 tools/build.py`: the grid between `<!-- grid:start -->` and
   `<!-- grid:end -->` is rewritten, along with the counters. Nothing else in
   `index.html` (CSS, JS, copy) is touched.
3. Update the check date in the footer.
4. Bump `VERSION` in `sw.js` so returning visitors pick up the new cache.

The "N mainnet" and "N testnet" counters next to the title are computed at load
from `data-network`: adding or removing a card updates them without further
work. The copyright year follows the visitor's clock.

## Social links

The footer shows X and GitHub, the two links verified on the `moonspiid`
profile. To add another, copy an `<li>` from the `<ul class="socials">` block and
replace the `href`, the `aria-label` and the SVG path (24 × 24, `fill` inherited
from `currentColor`). Adding Telegram, Discord or YouTube is one line per
network.

## Support this project

The site is free, has no account, no ads and no tracking, and there is no paid tier to upsell. If it saves you time, a donation pays for the hours behind it and the next features.

**Donate in USDT →** one crypto address, no card, no account, no payment processor in between.

<p align="center">
  <img src="donate-usdt-qr.png" alt="QR code of the EVM donation address" width="200">
  <br>
  <sub>Scan with any wallet app</sub>
</p>

```
0xA2700896E16BE762467D458F2b45260f8FAC9F3e
```

This is a plain EVM address, so **the same address works on every EVM network**. Send USDT on whichever one suits you:

| Network | Token |
| --- | --- |
| BNB Smart Chain (BEP20) | USDT |
| Ethereum (ERC20) | USDT |
| Polygon | USDT |
| Arbitrum One | USDT |
| Base | USDT |
| Optimism | USDT |

Two rules: send **USDT only** (another token sent to this address cannot be recovered), and keep a little of the network's own coin (BNB, ETH, POL) in your wallet to pay the transfer fee. A non-EVM network such as Tron (TRC20) uses a different address format, so nothing sent there reaches this one.

## Publish to GitHub Pages

```bash
# from the cloned repo, once the remote exists
git push -u origin main

# enable Pages on the main branch, repo root
gh api -X POST repos/<owner>/mainnet-faucet-aggregator/pages \
  -f 'source[branch]=main' -f 'source[path]=/'
```

The site is then served at `https://<owner>.github.io/mainnet-faucet-aggregator/`.
Every path in the project is relative, so the app works both at a domain root
and in a subfolder.

## Icons

```bash
python3 tools/make-icons.py
```

The script uses the standard library only (no Pillow). It writes
`icon-192.png`, `icon-512.png`, `icon-maskable-512.png` and
`apple-touch-icon.png`. `icons/icon.svg` remains the visual reference.

## Disclaimer

Faucets change networks, limits and rules without notice. Links are checked on
the date shown in the footer, with no guarantee. A faucet never asks for a
recovery phrase, and this page never connects a wallet.
