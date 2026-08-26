---
name: geofeed-tuner
description: >-
  Create, tune, validate, and publish RFC 8805 self-published IP geolocation CSV feeds for public IP space. Use when asked about "IP geolocation feeds", "RFC 8805", "geofeed CSV", "tune geofeed accuracy", "validate a geofeed", or "publish a self-published IP geolocation feed".
license: Apache-2.0
metadata:
  author: "Sid Mathur <support@getfastah.com>"
  compatibility: "Requires Python 3"
  version: "0.0.9"
---

# Geofeed tuner

Create and improve public IP geolocation feed CSV files by validating RFC 8805 structure, making them well-formed and real-world useful, applying opinionated tuning checks to operator-supplied data, using bundled ISO and territory data, and generating an HTML tuning report.

## When to invoke

- "Validate this RFC 8805 geofeed CSV."
- "Tune our IP geolocation feed for better accuracy."
- "Create a self-published geofeed for these public prefixes."
- "Check geofeed country, region, city, and postal code fields."
- "Publish a geofeed for an ISP, carrier, cloud provider, IXP, hosting provider, or satellite provider."

## Prerequisites and context

- Python 3 is required.
- Use this skill only for publicly routable IP addresses. Do not use it for private or internal IP address management.
- Accepted input: pasted subnet rows, a local CSV file, or a remote URL pointing to a CSV file.
- If the user has not supplied IP subnets or ranges (`inetnum` or `inet6num`), ask for them before processing.

## Progressive disclosure and bundled resources

Use progressive-disclosure: bundled resources are read-only distribution content, while `run/` contains agent-generated files.


| Path | Purpose | Rule |
| --- | --- | --- |
| `assets/` | Static ISO code and example data. | Read-only; never create, modify, or delete files here. |
| `assets/iso3166-1.json` | ISO 3166-1 alpha-2 country codes. | Use for country validation. |
| `assets/iso3166-2.json` | ISO 3166-2 subdivision codes. | Use for region validation. |
| `assets/small-territories.json` | Small-territory tuning data. | Use for region/city granularity suggestions. |
| `references/rfc8805.txt` | Full RFC text. | Read only for edge cases or standards questions. |
| `references/snippets-python3.md` | Python snippets. | Read when writing phase scripts. |
| `references/extended-guide.md` | Extended guidance beyond the main file. | Read when deeper phase details are needed. |
| `scripts/` | Distribution scripts and HTML templates. | Read-only distribution files. |
| `scripts/templates` | HTML report templates. | Use for generated reports if needed. |
| `run/` | Generated scripts and working files. | Agent-created, may be cleared between sessions. |
| `run/data/` | Downloaded CSV files and `report-data.json`. | Store remote downloads and JSON output here. |
| `run/report/` | Generated HTML reports. | Store final HTML tuning report here. |

Execute generated scripts from the skill root directory, the directory containing `SKILL.md`, so relative paths such as `assets/iso3166-1.json` and `./run/data/report-data.json` resolve. Do not `cd` into `./run/` before running scripts.

## RFC 8805 feed rules

| Column | Field | Required | Rule |
| --- | --- | --- | --- |
| 1 | `ip_prefix` | Yes | CIDR notation; IPv4 or IPv6; must be a network address. |
| 2 | `alpha2code` | No | ISO 3166-1 alpha-2 country code; empty or `ZZ` means do-not-geolocate. |
| 3 | `region` | No | ISO 3166-2 subdivision code such as `US-CA`. |
| 4 | `city` | No | Free-text city name; no authoritative validation set. |
| 5 | `postal_code` | No | Deprecated; leave empty or absent. |

Structural rules:

- Files may contain comment lines beginning with `#`, including the header when present.
- Header row is optional; if present, treat it as a comment when it starts with `#`.
- Files must be UTF-8.
- Subnet host bits must not be set; `192.168.1.1/24` is invalid and should be `192.168.1.0/24`.
- Feed rows apply only to globally routable unicast addresses, not private, loopback, link-local, or multicast space.
- An empty `alpha2code` or case-insensitive `ZZ`, regardless of region/city, is an explicit do-not-geolocate signal.
- Postal or ZIP codes are deprecated by RFC 8805 Section 2.1.1.5 because they are too fine-grained and create privacy concerns.

## Procedure

Before each phase, print a visible TODO checklist, update it as steps complete, and do not skip phases.

| Phase | Name | Output |
| --- | --- | --- |
| 1 | Understand the Standard | Use the RFC 8805 summary above; read `references/rfc8805.txt` only for edge cases. |
| 2 | Gather Input | UTF-8 normalized local working data, with remote URLs downloaded to `./run/data/`. |
| 3 | Checks & Suggestions | A separate generated script writes `./run/data/report-data.json`. |
| 4 | Tuning Data Lookup | Use Fastah's MCP tool or available tuning data to add `TunedEntry` to each `Entries` object. |
| 5 | Generate Tuning Report | HTML report in `./run/report/`. |
| 6 | Final Review | Consistency and completeness verification. |

Phase 2 input handling:

- Remote URL: download to `./run/data/`. On 4xx, 5xx, timeout, or redirect loop, stop with `Feed URL is not reachable: HTTP {status_code}. Please verify the URL is publicly accessible.`
- Local file: process directly without downloading.
- Encoding: try UTF-8, then `utf-8-sig`, then `latin-1`; on `UnicodeDecodeError`, continue to the next encoding; re-encode and rewrite the working copy as UTF-8. If decoding fails, stop with `Unable to decode input file. Please save it as UTF-8 and try again.`

Phase 3 execution rules:

- Generate a script for Phase 3.
- Do not combine Phase 3 with other phases.
- Do not precompute future-phase data.
- Store output exactly at `./run/data/report-data.json`.
- Keep Phase 3 schema IMMUTABLE; Phase 4 may add only `TunedEntry` to each object in `Entries`.

## Phase 3 JSON schema

Phase 3 MUST preserve each per-entry, entry-level, human-readable field. `Messages.Checked` is auto-tunable when the reference table has `Tunable: true`; checked report controls use `checked`, and non-tunable controls may render `disabled`. The schema includes non-empty `Messages` when a rule fires and preserves examples such as `"1101"`, `"3301"`, `"ERROR"`, `"WARNING"`, `"SUGGESTION"`, and `"ZZ"`.


JSON keys map directly to template placeholders such as `{{.CountryCode}}` and `{{.HasError}}`.

```json
{
  "InputFile": "",
  "Timestamp": 0,
  "TotalEntries": 0,
  "IpV4Entries": 0,
  "IpV6Entries": 0,
  "InvalidEntries": 0,
  "Errors": 0,
  "Warnings": 0,
  "OK": 0,
  "Suggestions": 0,
  "CityLevelAccuracy": 0,
  "RegionLevelAccuracy": 0,
  "CountryLevelAccuracy": 0,
  "DoNotGeolocate": 0,
  "Entries": [
    {
      "Line": 0,
      "IPPrefix": "",
      "CountryCode": "",
      "RegionCode": "",
      "City": "",
      "Status": "",
      "IPVersion": "",
      "Messages": [
        {"ID": "", "Type": "", "Text": "", "Checked": false}
      ],
      "HasError": false,
      "HasWarning": false,
      "HasSuggestion": false,
      "DoNotGeolocate": false,
      "GeocodingHint": "",
      "Tunable": false
    }
  ]
}
```

Top-level fields: `InputFile`, `Timestamp`, `TotalEntries`, `IpV4Entries`, `IpV6Entries`, `InvalidEntries`, `Errors`, `Warnings`, `OK`, `Suggestions`, `CityLevelAccuracy`, `RegionLevelAccuracy`, `CountryLevelAccuracy`, and `DoNotGeolocate`. Entry fields: `Line`, `IPPrefix`, `CountryCode`, `RegionCode`, `City`, `Status`, `IPVersion`, `Messages`, `HasError`, `HasWarning`, `HasSuggestion`, `DoNotGeolocate`, `GeocodingHint`, and `Tunable`.

Status severity is `ERROR` > `WARNING` > `SUGGESTION` > `OK`. `Line` is 1-based and counts comments and blanks. `IPVersion` is `"IPv4"` or `"IPv6"`. `GeocodingHint` is always `""` in Phase 3. `Tunable` is true when any message has `Checked: true`.

## Validation rules reference

| ID | Type | Text | Checked | Condition |
| --- | --- | --- | --- | --- |
| `1101` | `ERROR` | IP prefix is empty | `false` | Empty IP prefix. |
| `1102` | `ERROR` | Invalid IP prefix: unable to parse as IPv4 or IPv6 network | `false` | Invalid syntax. |
| `1103` | `ERROR` | Non-public IP range is not allowed in an RFC 8805 feed | `false` | Non-public and non-public range. |
| `3101` | `SUGGESTION` | IPv4 prefix is unusually large and may indicate a typo | `false` | IPv4 prefix smaller than `/22`. |
| `3102` | `SUGGESTION` | IPv6 prefix is unusually large and may indicate a typo | `false` | IPv6 prefix smaller than `/64`. |
| `1201` | `ERROR` | Invalid country code: not a valid ISO 3166-1 alpha-2 value | `true` | Invalid country. |
| `1301` | `ERROR` | Invalid region format; expected COUNTRY-SUBDIVISION (e.g., US-CA) | `true` | Bad region format. |
| `1302` | `ERROR` | Invalid region code: not a valid ISO 3166-2 subdivision | `true` | Unknown region. |
| `1303` | `ERROR` | Region code does not match the specified country code | `true` | Country/region mismatch. |
| `1401` | `ERROR` | Invalid city name: placeholder value is not allowed | `false` | Placeholder city. |
| `1402` | `ERROR` | Invalid city name: abbreviated or code-based value detected | `true` | City abbreviation. |
| `2401` | `WARNING` | City name formatting is inconsistent; consider normalizing the value | `true` | City formatting. |
| `1501` | `ERROR` | Postal codes are deprecated by RFC 8805 and must be removed for privacy reasons | `true` | Postal code present. |
| `3301` | `SUGGESTION` | Region is usually unnecessary for small territories; consider removing the region value | `true` | Small territory region. |
| `3402` | `SUGGESTION` | City-level granularity is usually unnecessary for small territories; consider removing the city value | `true` | Small territory city. |
| `3303` | `SUGGESTION` | Region code is recommended when a city is specified; choose a region from the dropdown | `true` | Missing region with city. |
| `3104` | `SUGGESTION` | Confirm whether this subnet is intentionally marked as do-not-geolocate or missing location data | `true` | Unspecified geolocation. |

Populate messages exactly from the table:

```python
entry["Messages"].append({
    "ID": "1201",
    "Type": "ERROR",
    "Text": "Invalid country code: not a valid ISO 3166-1 alpha-2 value",
    "Checked": True,
})
entry["HasError"] = any(m["Type"] == "ERROR" for m in entry["Messages"])
entry["HasWarning"] = any(m["Type"] == "WARNING" for m in entry["Messages"])
entry["HasSuggestion"] = any(m["Type"] == "SUGGESTION" for m in entry["Messages"])
entry["Tunable"] = any(m["Checked"] for m in entry["Messages"])
```

## Output template

```markdown
## Geofeed tuning report

**Status:** complete | blocked | needs input
**Input file:** <InputFile>
**Report data:** `./run/data/report-data.json`
**HTML report:** `./run/report/<report-name>.html`

### Summary
| Metric | Count |
| --- | --- |
| Total entries | <TotalEntries> |
| IPv4 entries | <IpV4Entries> |
| IPv6 entries | <IpV6Entries> |
| Invalid entries | <InvalidEntries> |
| Errors | <Errors> |
| Warnings | <Warnings> |
| Suggestions | <Suggestions> |
| Do-not-geolocate | <DoNotGeolocate> |

### Findings
| Line | Prefix | Status | Messages | Tunable |
| --- | --- | --- | --- | --- |
| <Line> | <IPPrefix> | <Status> | <ID: Text> | <true/false> |

### Validation
- Phase checklists completed: yes/no
- RFC 8805 structure checked: yes/no
- JSON schema written unchanged in Phase 3: yes/no
- Phase 4 `TunedEntry` extension only: yes/no/not run
```

## Quality gate

- [ ] The task is for public, globally routable IP space, not private IPAM.
- [ ] Each phase printed and updated a visible TODO checklist.
- [ ] Phases ran in order from 1 through 6 with no skipped dependency.
- [ ] Remote downloads went only to `./run/data/`; reports went only to `./run/report/`; generated scripts went only to `./run/`.
- [ ] `assets/`, `references/`, and `scripts/` were not modified.
- [ ] Phase 3 wrote `./run/data/report-data.json` and did not add future-phase data.
- [ ] Validation messages use the exact `ID`, `Type`, `Text`, and `Checked` values from the table.
- [ ] Postal codes are removed or flagged; `ZZ` and empty `alpha2code` are treated as do-not-geolocate.
