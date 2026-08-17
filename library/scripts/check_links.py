#!/usr/bin/env python3
"""Audit external links across the repository.

Extracts every http(s) URL from repository content, then checks each unique URL
concurrently and classifies the result. Intentional placeholders (example.com,
localhost, templating tokens, tenant-specific hosts) are excluded by design so
the report only contains links that are supposed to resolve.

Usage:
  python3 library/scripts/check_links.py                    # check everything
  python3 library/scripts/check_links.py --path library/skills  # limit to a subtree
  python3 library/scripts/check_links.py --json report.json # machine-readable output
  python3 library/scripts/check_links.py --cache .linkcache.json
  python3 library/scripts/check_links.py --only-problems    # hide OK rows

Exit codes: 0 = no broken links, 1 = at least one BROKEN url.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s<>\"')\]}`,;\\]+")
TEXT_EXT = {".md", ".json", ".yml", ".yaml", ".sh", ".py", ".ps1", ".ts", ".js", ".mjs"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

# Hosts and patterns that are deliberately not real endpoints.
PLACEHOLDER_HOST_RE = re.compile(
    r"^(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|host|hostname|server|"
    r"(?:[a-z0-9-]+\.)?example\.(?:com|org|net)|example|test|foo|bar|"
    r"my-?org\..*|my-?tenant\..*|yourorg\..*|your-?domain\..*|contoso\..*|"
    r"<[^>]*>|\{[^}]*\}|.*\$\{.*)$",
    re.I,
)
PLACEHOLDER_URL_RE = re.compile(
    r"[<>{}\u2026]|\$\{|\$\(|\$[A-Za-z_]\w*|%s|%d|\.\.\.|YOUR_|__[A-Z_]+__|xxx+"
    r"|/(?:owner|org|user|username|account)/(?:repo|repository|project)\b"
    r"|\b(?:my-?repo|my-?plugin|my-?skill|my-?marketplace|some-?repo|some-command)\b",
    re.I,
)

# XML/SOAP namespace URIs are identifiers, not navigable links. Never probe them.
NAMESPACE_URI_RE = re.compile(
    r"^https?://(?:schemas\.|www\.w3\.org/|purl\.org/|xmlns\.|docs\.oasis-open\.org/ns/"
    r"|schema\.org/?$|www\.opengis\.net/|ns\.adobe\.com/)",
    re.I,
)

# Local / non-routable hosts referenced in examples and dev instructions.
LOCAL_HOST_RE = re.compile(
    r"^(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|host\.docker\.internal"
    r"|[\w.-]+\.(?:local|internal|test|invalid|localhost))$",
    re.I,
)

# Hosts that are real but reject or throttle automated HEAD/GET traffic.
KNOWN_BOT_BLOCKERS = {
    "www.linkedin.com", "linkedin.com", "twitter.com", "x.com",
    "www.instagram.com", "medium.com", "www.reddit.com", "reddit.com",
    "stackoverflow.com", "www.udemy.com", "www.crunchbase.com",
}

# Deprecated domains that still resolve but should be migrated.
DEPRECATED_HOSTS = {
    "docs.microsoft.com": "learn.microsoft.com",
    "azure.microsoft.com/en-us/documentation": "learn.microsoft.com",
    "docs.azure.cn": "learn.microsoft.com",
    "msdn.microsoft.com": "learn.microsoft.com",
    "technet.microsoft.com": "learn.microsoft.com",
    "code.visualstudio.com/api/references/vscode-api": None,
}

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def find_repo_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / ".git").exists() or (candidate / "README.md").exists():
            return candidate
    return start.resolve()


def iter_files(root: Path, subpath: str | None) -> list[Path]:
    base = root / subpath if subpath else root
    if not base.exists():
        raise SystemExit(f"--path not found: {base}")
    if base.is_file():
        return [base]
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if Path(fn).suffix.lower() in TEXT_EXT:
                out.append(Path(dirpath) / fn)
    return sorted(out)


def clean_url(raw: str) -> str:
    url = raw.rstrip(".,;:!?")
    while url and url[-1] in ")]}\"'" and url.count(url[-1]) > url.count({")": "(", "]": "[", "}": "{"}.get(url[-1], url[-1])):
        url = url[:-1]
    return url


def host_of(url: str) -> str:
    return re.sub(r"^https?://", "", url).split("/")[0].split("?")[0]


def is_placeholder(url: str) -> bool:
    if NAMESPACE_URI_RE.match(url):
        return True
    host = host_of(url)
    # A public host always has a dot. Dotless hosts come from regex literals and
    # split strings in scripts (e.g. "https://hooks\.slack\.com/..."), not links.
    if host and "." not in host:
        return True
    if LOCAL_HOST_RE.match(host):
        return True
    return bool(PLACEHOLDER_URL_RE.search(url)) or bool(PLACEHOLDER_HOST_RE.match(host))


def collect(files: list[Path], root: Path) -> dict[str, list[str]]:
    refs: dict[str, list[str]] = defaultdict(list)
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(p.relative_to(root))
        for raw in URL_RE.findall(text):
            refs[clean_url(raw)].append(rel)
    return refs


def probe(url: str, timeout: float) -> tuple[str, int | None, str]:
    """Return (status_label, http_code, detail)."""
    ctx = ssl.create_default_context()
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={
            "User-Agent": UA,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                code = resp.getcode()
                final = resp.geturl()
                if final.rstrip("/") != url.rstrip("/"):
                    return "REDIRECT", code, final
                return "OK", code, ""
        except urllib.error.HTTPError as e:
            # HEAD is unreliable: many servers return 404/405/500 for HEAD on
            # pages that serve fine over GET. Never conclude from a HEAD failure.
            if method == "HEAD":
                continue
            if e.code in (405, 501):
                return "OK", e.code, "method not allowed (endpoint alive)"
            if e.code in (401, 403, 429) or host_of(url) in KNOWN_BOT_BLOCKERS:
                return "BLOCKED", e.code, e.reason or ""
            return "BROKEN", e.code, e.reason or ""
        except urllib.error.URLError as e:
            reason = str(getattr(e, "reason", e))
            if "timed out" in reason.lower():
                if method == "HEAD":
                    continue
                return "TIMEOUT", None, reason
            return "BROKEN", None, reason
        except Exception as e:  # noqa: BLE001 - never let one URL kill the run
            return "ERROR", None, f"{type(e).__name__}: {e}"
    return "TIMEOUT", None, "no response"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(find_repo_root(Path(__file__).resolve())), help="repository root (default: nearest parent containing .git or README.md)")
    ap.add_argument("--path", default=None, help="limit scan to this subdirectory or single file")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--cache", default=None, help="reuse/save probe results")
    ap.add_argument("--only-problems", action="store_true")
    ap.add_argument("--list-only", action="store_true", help="extract URLs, do not probe")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    files = iter_files(root, args.path)
    refs = collect(files, root)

    checkable = {u: f for u, f in refs.items() if not is_placeholder(u)}
    placeholders = {u: f for u, f in refs.items() if is_placeholder(u)}

    print(f"Scanned {len(files)} files")
    print(f"Unique URLs: {len(refs)}  (checkable {len(checkable)}, placeholders skipped {len(placeholders)})")

    if args.list_only:
        for u in sorted(checkable):
            print(u)
        return 0

    cache: dict[str, list] = {}
    cache_path = Path(args.cache) if args.cache else None
    if cache_path and cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text())
        except Exception:
            cache = {}

    todo = [u for u in checkable if u not in cache]
    print(f"Probing {len(todo)} URLs ({len(checkable) - len(todo)} from cache)...", flush=True)

    results: dict[str, list] = {u: cache[u] for u in checkable if u in cache}
    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(probe, u, args.timeout): u for u in todo}
        for fut in concurrent.futures.as_completed(futs):
            u = futs[fut]
            try:
                results[u] = list(fut.result())
            except Exception as e:  # noqa: BLE001
                results[u] = ["ERROR", None, str(e)]
            done += 1
            if done % 100 == 0:
                print(f"  ...{done}/{len(todo)}", flush=True)

    if cache_path:
        cache.update(results)
        cache_path.write_text(json.dumps(cache, indent=0))

    buckets: dict[str, list[tuple[str, list, list[str]]]] = defaultdict(list)
    for u, r in results.items():
        buckets[r[0]].append((u, r, refs[u]))

    # Deprecated-domain findings are independent of HTTP status.
    deprecated = [(u, refs[u]) for u in checkable
                  if any(host_of(u) == d or host_of(u).endswith("." + d) for d in DEPRECATED_HOSTS)]

    order = ["BROKEN", "ERROR", "TIMEOUT", "REDIRECT", "BLOCKED", "OK"]
    for label in order:
        rows = buckets.get(label, [])
        if not rows:
            continue
        if args.only_problems and label in ("OK", "BLOCKED"):
            print(f"\n## {label}: {len(rows)}")
            continue
        print(f"\n## {label}: {len(rows)}")
        if label == "OK":
            continue
        for u, r, where in sorted(rows)[:400]:
            code = f" [{r[1]}]" if r[1] else ""
            detail = f" -> {r[2]}" if r[2] else ""
            print(f"  {u}{code}{detail}")
            print(f"      in: {', '.join(sorted(set(where))[:4])}"
                  + (f" (+{len(set(where)) - 4} more)" if len(set(where)) > 4 else ""))

    if deprecated:
        print(f"\n## DEPRECATED DOMAIN: {len(deprecated)}")
        for u, where in sorted(deprecated)[:200]:
            print(f"  {u}")
            print(f"      in: {', '.join(sorted(set(where))[:4])}")

    print("\nSUMMARY")
    print("status | count")
    print("--- | ---:")
    for label in order:
        print(f"{label} | {len(buckets.get(label, []))}")
    print(f"DEPRECATED | {len(deprecated)}")
    print(f"PLACEHOLDER (skipped) | {len(placeholders)}")

    if args.json_out:
        payload = {
            "summary": {label: len(buckets.get(label, [])) for label in order},
            "deprecated": [{"url": u, "files": sorted(set(w))} for u, w in deprecated],
            "results": [
                {"url": u, "status": r[0], "code": r[1], "detail": r[2], "files": sorted(set(refs[u]))}
                for u, r in sorted(results.items())
            ],
            "placeholders": sorted(placeholders),
        }
        Path(args.json_out).write_text(json.dumps(payload, indent=2))
        print(f"\nJSON report written to {args.json_out}")

    return 1 if buckets.get("BROKEN") else 0


if __name__ == "__main__":
    sys.exit(main())
