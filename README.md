# Mainnet Faucet Aggregator — faucets without detours

<p>
  <img alt="45 faucets" src="https://img.shields.io/badge/faucets-45-ffd43b?labelColor=30363d">
  <img alt="34 mainnet" src="https://img.shields.io/badge/mainnet-34-2ea043?labelColor=30363d">
  <img alt="11 testnet" src="https://img.shields.io/badge/testnet-11-ea7a15?labelColor=30363d">
  <img alt="direct links" src="https://img.shields.io/badge/links-direct-1f6feb?labelColor=30363d">
  <br>
  <img alt="no staking" src="https://img.shields.io/badge/staking-zero-2ea043?labelColor=30363d">
  <img alt="installable PWA" src="https://img.shields.io/badge/pwa-installable-ea7a15?labelColor=30363d">
  <img alt="works offline" src="https://img.shields.io/badge/offline-ready-3fb950?labelColor=30363d">
  <img alt="price, free" src="https://img.shields.io/badge/price-free-2ea043?labelColor=30363d">
</p>

**Pick a network, land on the faucet, claim.** A one-page directory of official faucet claim pages — 42 Stakely networks plus Polygon, BNB Chain and Celo — with the amount each one pays printed on its card.

<h3 align="center">
  <a href="https://moonspiid.github.io/mainnet-faucet-aggregator/" target="_blank" rel="noopener noreferrer">↖ Open the directory</a>
</h3>

<p align="center">
  45 faucets, 34 mainnet and 11 testnet, checked on 24 November 2026.
  <br>
  Every link goes straight to the claim page — never to a staking page, never through a redirect.
</p>

## Contents

- [Why](#why)
- [Features](#features)
- [Quick start](#quick-start)
- [Install it as an app](#install-it-as-an-app)
- [How it works](#how-it-works)
- [Good to know](#good-to-know)
- [Contributors](#contributors)
- [Support this project](#support-this-project)

## Why

Faucet search results are full of pages that ask you to stake, connect a wallet or click through three redirects before a claim form shows up. This directory holds nothing but the direct claim links, the network each one serves and the amount it sends, so you can see where a click takes you before you take it.

## Features

- **45 faucets, amounts printed on the card** — 0.00088 APT on Aptos, 0.01 POL on Polygon, 10 SUI on Sui testnet, and so on. You know what a faucet pays before opening it.
- **Mainnet and testnet kept apart** — two counters next to the title (34 and 11), a filter for each, and a badge on every card.
- **Search across chains and tokens** — type `POL`, `SUI` or `SEPOLIA` and the grid narrows as you type; `/` focuses the field, `Esc` clears it.
- **Dead faucets are flagged, not hidden** — Ethereum and Solana mainnet were dry at the time of the check: their card shows the amount struck through, an `inactive` tag and a dashed border.
- **Direct links only** — no affiliate hop, no redirect domain, no wallet connection. The domain printed at the bottom of each card is the domain you land on.
- **Installable and offline** — the whole directory is one HTML file cached by a service worker, so it opens with no network.
- **Light and dark themes** — follows the system setting, with a manual toggle.

## Quick start

1. Open **[the directory](https://moonspiid.github.io/mainnet-faucet-aggregator/)**.
2. Press **Mainnet** or **Testnet**, or type a ticker in the search field.
3. Check the badge and the amount on the card, then press **Open the faucet**.
4. On Stakely: paste your address, solve the captcha, share the request ID on X when asked, and the drip arrives.

## Install it as an app

- **Android / Chrome** — ⋮ menu → *Install app* (or the install icon in the address bar), or *Add to home screen*.
- **iPhone / Safari** — Share → *Add to Home Screen*.
- **Desktop Chrome / Edge** — the install icon in the address bar.

It then runs in its own window and keeps the full directory available offline.

## How it works

- `index.html` — the whole page: hero, card grid, filters, donation section, footer, and one inline script for the theme, the counters and the copy buttons.
- `tools/faucets.json` — the data: one object per faucet with `name`, `token`, `provider`, `amount`, `url`, `host`, `network`, `status`, and optionally `note` and `extra` links.
- `tools/build.py` — rewrites the grid between `<!-- grid:start -->` and `<!-- grid:end -->` from that JSON, and refreshes the two counters. Standard library only; `python3 tools/build.py`.
- `sw.js` — the service worker: cache-first for the shell, revalidation of navigations so a new deploy is picked up. Bump `VERSION` when the page changes.
- `manifest.webmanifest` — the PWA metadata; icons come from `icons/`, and `tools/make-icons.py` redraws the PNGs from the geometry of `icon.svg`.
- Pushing to `main` republishes the site through GitHub Pages.

## Good to know

- The Stakely list comes from `stakely.io/sitemap.xml`, which exposes the 42 `/faucet/<network>-<token>` pages; the amount and status on each card were read from that page, not guessed.
- A mainnet faucet sends gas money — a fraction of a token to pay a fee, not a usable balance.
- BNB Chain keeps two entries: the Stakely mainnet page (0.00001 BNB) and the official testnet faucet (tBNB). Celo and Polygon work the same way, one card per source.
- Faucets change networks, limits and rules without notice, so the amounts are a snapshot of the date shown in the footer.
- A faucet never asks for a recovery phrase, and this page never connects a wallet.

## Contributors

<p>
  <a href="https://github.com/moonspiid" title="moonspiid">
    <img src="https://avatars.githubusercontent.com/moonspiid?s=96" alt="moonspiid" width="72" height="72">
  </a>
</p>

Built and maintained by **[moonspiid](https://github.com/moonspiid)**: the faucet list, the check behind every amount, and the hours behind each release. Spotted a dead link or a network that is missing? Open an [issue](https://github.com/moonspiid/mainnet-faucet-aggregator/issues) and you join the list.

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
