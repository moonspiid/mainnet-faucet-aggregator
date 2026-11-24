#!/usr/bin/env python3
"""Ask every faucet link for an answer, then write status.json.

A browser cannot do this job: stakely.io answers with
Cross-Origin-Resource-Policy: same-origin, so a fetch from the page is
rejected before the status is readable. These checks run server side, in the
scheduled workflow, and the page only displays the result.
"""

import concurrent.futures
import datetime
import json
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
TIMEOUT = 12
UA = (
    "Mozilla/5.0 (compatible; mainnet-faucet-aggregator/1.0; "
    "+https://github.com/moonspiid/mainnet-faucet-aggregator)"
)
# 401/403/405/429: the host answered, it just refuses automated clients
BLOCKED = {401, 403, 405, 429}
GONE = {404, 410}


def probe(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "text/html,*/*"}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return {"state": "up", "code": response.status}
    except urllib.error.HTTPError as error:
        if error.code in BLOCKED:
            return {"state": "up", "code": error.code, "blocked": True}
        return {"state": "gone" if error.code in GONE else "down", "code": error.code}
    except Exception as error:  # DNS, TLS, timeout, reset
        return {"state": "down", "code": 0, "error": type(error).__name__}


def links_of(faucets):
    urls = set()
    for faucet in faucets:
        urls.add(faucet["url"])
        urls.update(extra["url"] for extra in faucet.get("extra", []))
    return sorted(urls)


def main():
    faucets = json.loads((ROOT / "tools" / "faucets.json").read_text(encoding="utf-8"))
    urls = links_of(faucets)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(zip(urls, pool.map(probe, urls)))

    status = {
        "checked": datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "links": results,
    }
    (ROOT / "status.json").write_text(
        json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    counts = {}
    for result in results.values():
        counts[result["state"]] = counts.get(result["state"], 0) + 1
    print("%d links: %s" % (len(results), counts))


if __name__ == "__main__":
    main()
