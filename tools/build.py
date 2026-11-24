"""Rebuilds the directory grid dans index.html à partir de tools/faucets.json.

    python3 tools/build.py

Le script ne touche qu'à ce qui est entre <!-- grid:start --> et <!-- grid:end -->,
plus les deux compteurs du titre. Le reste de la page (CSS, JS, textes) reste
édité à la main dans index.html.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
DATA = ROOT / "tools" / "faucets.json"

ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M7 17 17 7"/><path d="M9 7h8v8"/></svg>'
)
COPY = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="9" y="9" width="11" height="11" rx="2.5"/>'
    '<path d="M6.5 15H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v1.5"/></svg>'
)


def reward(item):
    flag = '<em class="flag">inactive</em>' if item.get("status") != "active" else ""
    if item.get("amount"):
        return (
            '          <p class="reward"><strong>%s</strong><span>per claim</span>%s</p>'
            % (item["amount"], flag)
        )
    return '          <p class="reward"><span>amount varies by network</span>%s</p>' % flag


def card(item):
    network = item["network"]
    extra = ""
    if item.get("extra"):
        links = "".join(
            '\n              <li><a class="alt" href="%s" target="_blank" rel="noopener noreferrer nofollow">%s ↗</a></li>'
            % (link["url"], link["label"])
            for link in item["extra"]
        )
        extra = '\n          <ul class="links">%s\n          </ul>' % links
    note = '\n          <p class="blurb">%s</p>' % item["note"] if item.get("note") else ""

    return """        <article class="card" data-network="{network}" data-status="{status}">
          <div class="card-head">
            <span class="mark" aria-hidden="true">{letter}</span>
            <div class="card-title">
              <h3>{name}</h3>
              <p>{token} · {provider} faucet</p>
            </div>
            <span class="badge {network}">{badge}</span>
          </div>
{reward}{note}
          <ul class="links">
            <li><a class="cta" href="{url}" target="_blank" rel="noopener noreferrer nofollow">Open the faucet{arrow}</a></li>
          </ul>{extra}
          <div class="card-foot">
            <span class="host">{host}</span>
            <button class="copy" type="button" data-copy="{url}" aria-label="Copy the {name} link">
              {copy}
              Copy
            </button>
          </div>
        </article>""".format(
        network=network,
        status=item.get("status", "active"),
        letter=item["name"][0].upper(),
        name=item["name"],
        token=item.get("token", ""),
        provider=item.get("provider", "Stakely"),
        badge=network.capitalize(),
        reward=reward(item),
        note=note,
        url=item["url"],
        arrow=ARROW,
        extra=extra,
        host=item["host"],
        copy=COPY,
    )


def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    cards = "\n\n".join(card(item) for item in items)
    html = HTML.read_text(encoding="utf-8")

    start, end = "<!-- grid:start -->", "<!-- grid:end -->"
    head, rest = html.split(start, 1)
    _, tail = rest.split(end, 1)
    html = "%s%s\n%s\n      %s%s" % (head, start, cards, end, tail)

    for network, label in (("mainnet", "mainnet"), ("testnet", "testnet")):
        count = sum(1 for item in items if item["network"] == network)
        html = re.sub(
            r'(<span class="count %s" id="count-%s">)[^<]*(</span>)' % (network, network),
            r"\g<1>%d %s\g<2>" % (count, label),
            html,
        )

    HTML.write_text(html, encoding="utf-8")
    mainnet = sum(1 for item in items if item["network"] == "mainnet")
    print("%d cards (%d mainnet, %d testnet)" % (len(items), mainnet, len(items) - mainnet))


if __name__ == "__main__":
    main()
