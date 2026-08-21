#!/usr/bin/env python3
"""Validate reachability of official Backstage documentation fallback sources."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import urllib.error
import urllib.request


URLS = [
    "https://raw.githubusercontent.com/backstage/backstage/master/docs/frontend-system/building-plugins/01-index.md",
    "https://raw.githubusercontent.com/backstage/backstage/master/docs/backend-system/building-plugins-and-modules/01-index.md",
    "https://backstage.io/docs/plugins/create-a-plugin/",
    "https://backstage.io/docs/plugins/composability/",
    "https://github.com/backstage/community-plugins/blob/main/CONTRIBUTING.md",
    "https://github.com/backstage/backstage/blob/master/CONTRIBUTING.md",
]


def check_url(url: str, timeout: int) -> dict:
    request = urllib.request.Request(
        url, headers={"User-Agent": "backstage-plugin-builder-doc-check"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"url": url, "status": response.status, "ok": 200 <= response.status < 400}
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": exc.code, "ok": False, "error": str(exc)}
    except urllib.error.URLError as exc:
        return {"url": url, "status": None, "ok": False, "error": str(exc.reason)}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate official Backstage documentation fallback URLs")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON instead of text")
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    results = [check_url(url, args.timeout) for url in URLS]
    payload = {"checked_at": dt.datetime.now(
        dt.timezone.utc).isoformat(), "results": results}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for result in results:
            status = "PASS" if result["ok"] else "FAIL"
            print(f"{status} {result.get('status')} {result['url']}")
            if result.get("error"):
                print(f"  {result['error']}")
    return 0 if all(result["ok"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
