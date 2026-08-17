---
name: "geofeed-tuner"
description: >-
  Use this skill whenever the user mentions IP geolocation feeds, RFC 8805, geofeeds, or wants help
  creating, tuning, validating, or publishing a self-published IP geolocation feed in CSV format.
  Intended user audience is a network operator, ISP, mobile carrier, cloud provider, hosting company,
  IXP, or satellite provider asking about IP geolocation accuracy, or geofeed authoring best
  practices. Helps create, refine, and improve CSV-format IP geolocation feeds with opinionated
  recommendations beyond RFC 8805 compliance. Do NOT use for private or internal IP address management
  — applies only to publicly routable IP addresses.
license: "Apache-2.0"
metadata:
  author: "Sid Mathur <support@getfastah.com>"
  compatibility: "Requires Python 3"
  version: "0.0.9"
---
# Geofeed Tuner – Create Better IP Geolocation Feeds

This skill helps you create and improve IP geolocation feeds in CSV format by:
- Ensuring your CSV is well-formed and consistent
- Checking alignment with [RFC 8805](references/rfc8805.txt) (the industry standard)
- Applying **opinionated best practices** learned from real-world deployments
- Suggesting improvements for accuracy, completeness, and privacy

## When to Use This Skill

- Use this skill when a user asks for help **creating, improving, or publishing** an IP geolocation feed file in CSV format.
- Use it to **tune and troubleshoot CSV geolocation feeds** — catching errors, suggesting improvements, and ensuring real-world usability beyond RFC compliance.
- **Intended audience:**
  - Network operators, administrators, and engineers responsible for publicly routable IP address space
  - Organizations such as ISPs, mobile carriers, cloud providers, hosting and colocation companies, Internet Exchange operators, and satellite internet providers
- **Do not use** this skill for private or internal IP address management; it applies **only to publicly routable IP addresses**.

## Prerequisites

- **Python 3** is required.

## Directory Structure and File Management

This skill uses a clear separation between **distribution files** (read-only) and **working files** (generated at runtime).

### Read-Only Directories (Do Not Modify)

The following directories contain static distribution assets. **Do not create, modify, or delete files in these directories:**

| Directory      | Purpose                                                    |
|----------------|------------------------------------------------------------|
| `assets/`      | Static data files (ISO codes, examples)                    |
| `references/`  | RFC specifications and code snippets for reference         |
| `scripts/`     | Executable code and HTML template files for reports        |

### Working Directories (Generated Content)

All generated, temporary, and output files go in these directories:

| Directory       | Purpose                                              |
|-----------------|------------------------------------------------------|
| `run/`          | Working directory for all agent-generated content    |
| `run/data/`     | Downloaded CSV files from remote URLs                |
| `run/report/`   | Generated HTML tuning reports                        |

### File Management Rules

1. **Never write to `assets/`, `references/`, or `scripts/`** — these are part of the skill distribution and must remain unchanged.
2. **All downloaded input files** (from remote URLs) must be saved to `./run/data/`.
3. **All generated HTML reports** must be saved to `./run/report/`.
4. **All generated Python scripts** must be saved to `./run/`.
5. The `run/` directory may be cleared between sessions; do not store permanent data there.
6. **Working directory for execution:** All generated scripts in `./run/` must be executed with the **skill root directory** (the directory containing `SKILL.md`) as the current working directory, so that relative paths like `assets/iso3166-1.json` and `./run/data/report-data.json` resolve correctly. Do not `cd` into `./run/` before running scripts.


## Processing Pipeline: Sequential Phase Execution

All phases must be executed **in order**, from Phase 1 through Phase 6. Each phase depends on the successful completion of the previous phase. For example, **structure checks** must complete before **quality analysis** can run.

The phases are summarized below. The agent must follow the detailed steps outlined further in each phase section.

| Phase | Name                       | Description                                                                       |
|-------|----------------------------|-----------------------------------------------------------------------------------|
| 1     | Understand the Standard    | Review the key requirements of RFC 8805 for self-published IP geolocation feeds   |
| 2     | Gather Input               | Collect IP subnet data from local files or remote URLs                            |
| 3     | Checks & Suggestions       | Validate CSV structure, analyze IP prefixes, and check data quality               |
| 4     | Tuning Data Lookup         | Use Fastah's MCP tool to retrieve tuning data for improving geolocation accuracy  |
| 5     | Generate Tuning Report     | Create an HTML report summarizing the analysis and suggestions                    |
| 6     | Final Review               | Verify consistency and completeness of the report data                            |

**Do not skip phases.** Each phase provides critical checks or data transformations required by subsequent stages.


### Execution Plan Rules

Before executing each phase, the agent MUST generate a visible TODO checklist.

The plan MUST:
- Appear at the very start of the phase
- List every step in order
- Use a checkbox format
- Be updated live as steps complete


### Phase 1: Understand the Standard

The key requirements from RFC 8805 that this skill enforces are summarized below. **Use this summary as your working reference.** Only consult the full [RFC 8805 text](references/rfc8805.txt) for edge cases, ambiguous situations, or when the user asks a standards question not covered here.

#### RFC 8805 Key Facts

**Purpose:** A self-published IP geolocation feed lets network operators publish authoritative location data for their IP address space in a simple CSV format, allowing geolocation providers to incorporate operator-supplied corrections.

**CSV Column Order (Sections 2.1.1.1–2.1.1.5):**

| Column | Field         | Required | Notes                                                      |
|--------|---------------|----------|------------------------------------------------------------|
| 1      | `ip_prefix`   | Yes      | CIDR notation; IPv4 or IPv6; must be a network address     |
| 2      | `alpha2code`  | No       | ISO 3166-1 alpha-2 country code; empty or "ZZ" = do-not-geolocate |
| 3      | `region`      | No       | ISO 3166-2 subdivision code (e.g., `US-CA`)               |
| 4      | `city`        | No       | Free-text city name; no authoritative validation set       |
| 5      | `postal_code` | No       | **Deprecated** — must be left empty or absent             |

**Structural rules:**
- Files may contain comment lines beginning with `#` (including the header, if present).
- A header row is optional; if present, it is treated as a comment if it starts with `#`.
- Files must be encoded in UTF-8.
- Subnet host bits must not be set (i.e., `192.168.1.1/24` is invalid; use `192.168.1.0/24`).
- Applies only to **globally routable** unicast addresses — not private, loopback, link-local, or multicast space.

**Do-not-geolocate:** An entry with an empty `alpha2code` or case-insensitive `ZZ` (irrespective of values of region/city) is an explicit signal that the operator does not want geolocation applied to that prefix.

**Postal codes deprecated (Section 2.1.1.5):** The fifth column must not contain postal or ZIP codes. They are too fine-grained for IP-range mapping and raise privacy concerns.


### Phase 2: Gather Input

- If the user has not already provided a list of IP subnets or ranges (sometimes referred to as `inetnum` or `inet6num`), prompt them to supply it. Accepted input formats:
  - Text pasted into the chat
  - A local CSV file
  - A remote URL pointing to a CSV file

- If the input is a **remote URL**:
  - Attempt to download the CSV file to `./run/data/` before processing.
  - On HTTP error (4xx, 5xx, timeout, or redirect loop), **stop immediately** and report to the user:
    `Feed URL is not reachable: HTTP {status_code}. Please verify the URL is publicly accessible.`
  - Do not proceed to Phase 3 with an incomplete or empty download.

- If the input is a **local file**, process it directly without downloading.

- **Encoding detection and normalization:**
  1. Attempt to read the file as UTF-8 first.
  2. If a `UnicodeDecodeError` is raised, try `utf-8-sig` (UTF-8 with BOM), then `latin-1`.
  3. Once successfully decoded, re-encode and write the working copy as UTF-8.
  4. If no encoding succeeds, stop and report: `Unable to decode input file. Please save it as UTF-8 and try again.`


### Phase 3: Checks & Suggestions

#### Execution Rules
- Generate a **script** for this phase.
- Do NOT combine this phase with others.
- Do NOT precompute future-phase data.
- Store the output as a JSON file at: `./run/data/report-data.json`

#### Schema Definition

The JSON structure below is **IMMUTABLE** during Phase 3. Phase 4 will later add a `TunedEntry` object to each object in `Entries` — this is the only permitted schema extension and happens in a separate phase.

JSON keys map directly to template placeholders like `{{.CountryCode}}`, `{{.HasError}}`, etc.

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
        {
          "ID": "",
          "Type": "",
          "Text": "",
          "Checked": false
        }
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

Field definitions:

**Top-level metadata:**
- `InputFile`: The original input source, either a local filename or a remote URL.
- `Timestamp`: Milliseconds since Unix epoch when the tuning was performed.
- `TotalEntries`: Total number of data rows processed (excluding comment and blank lines).
- `IpV4Entries`: Count of entries that are IPv4 subnets.
- `IpV6Entries`: Count of entries that are IPv6 subnets.
- `InvalidEntries`: Count of entries that failed IP prefix parsing and CSV parsing.
- `Errors`: Total entries whose `Status` is `ERROR`.
- `Warnings`: Total entries whose `Status` is `WARNING`.
- `OK`: Total entries whose `Status` is `OK`.
- `Suggestions`: Total entries whose `Status` is `SUGGESTION`.
- `CityLevelAccuracy`: Count of valid entries where `City` is non-empty.
- `RegionLevelAccuracy`: Count of valid entries where `RegionCode` is non-empty and `City` is empty.
- `CountryLevelAccuracy`: Count of valid entries where `CountryCode` is non-empty, `RegionCode` is empty, and `City` is empty.
- `DoNotGeolocate` (metadata): Count of valid entries where `CountryCode`, `RegionCode`, and `City` are all empty.

**Entry fields:**
- `Entries`: Array of objects, one per data row, with the following per-entry fields:
  - `Line`: 1-based line number in the original CSV (counting all lines including comments and blanks).
  - `IPPrefix`: The normalized IP prefix in CIDR slash notation.
  - `CountryCode`: The ISO 3166-1 alpha-2 country code, or empty string.
  - `RegionCode`: The ISO 3166-2 region code (e.g., `US-CA`), or empty string.
  - `City`: The city name, or empty string.
  - `Status`: Highest severity assigned: `ERROR` > `WARNING` > `SUGGESTION` > `OK`.
  - `IPVersion`: `"IPv4"` or `"IPv6"` based on the parsed IP prefix.
  - `Messages`: Array of message objects, each with:
    - `ID`: String identifier from the **Validation Rules Reference** table below (e.g., `"1101"`, `"3301"`).
    - `Type`: The severity type: `"ERROR"`, `"WARNING"`, or `"SUGGESTION"`.
    - `Text`: The human-readable validation message string.
    - `Checked`: `true` if the validation rule is auto-tunable (`Tunable: true` in the reference table), `false` otherwise. Controls whether the checkbox in the report is `checked` or `disabled`.
  - `HasError`: `true` if any message has `Type` `"ERROR"`.
  - `HasWarning`: `true` if any message has `Type` `"WARNING"`.
  - `HasSuggestion`: `true` if any message has `Type` `"SUGGESTION"`.
  - `DoNotGeolocate` (entry): `true` if `CountryCode` is empty or `"ZZ"` — the entry is an explicit do-not-geolocate signal.
  - `GeocodingHint`: Always empty string `""` in Phase 3. Reserved for future use.
  - `Tunable`: `true` if **any** message in the entry has `Checked: true`. Computed as logical OR across all messages' `Checked` values. This flag drives the "Tune" button visibility in the report.

#### Validation Rules Reference

When adding messages to an entry, use the `ID`, `Type`, `Text`, and `Checked` values from this table.

| ID     | Type         | Text                                                                                           | Checked | Condition Reference                    |
|--------|--------------|------------------------------------------------------------------------------------------------|---------|----------------------------------------|
| `1101` | `ERROR`      | IP prefix is empty                                                                             | `false` | IP Prefix Analysis: empty              |
| `1102` | `ERROR`      | Invalid IP prefix: unable to parse as IPv4 or IPv6 network                                     | `false` | IP Prefix Analysis: invalid syntax     |
| `1103` | `ERROR`      | Non-public IP range is not allowed in an RFC 8805 feed                                         | `false` | IP Prefix Analysis: non-public         |
| `3101` | `SUGGESTION` | IPv4 prefix is unusually large and may indicate a typo                                         | `false` | IP Prefix Analysis: IPv4 < /22         |
| `3102` | `SUGGESTION` | IPv6 prefix is unusually large and may indicate a typo                                         | `false` | IP Prefix Analysis: IPv6 < /64         |
| `1201` | `ERROR`      | Invalid country code: not a valid ISO 3166-1 alpha-2 value                                     | `true`  | Country Code Analysis: invalid         |
| `1301` | `ERROR`      | Invalid region format; expected COUNTRY-SUBDIVISION (e.g., US-CA)                              | `true`  | Region Code Analysis: bad format       |
| `1302` | `ERROR`      | Invalid region code: not a valid ISO 3166-2 subdivision                                        | `true`  | Region Code Analysis: unknown code     |
| `1303` | `ERROR`      | Region code does not match the specified country code                                          | `true`  | Region Code Analysis: mismatch         |
| `1401` | `ERROR`      | Invalid city name: placeholder value is not allowed                                            | `false` | City Name Analysis: placeholder        |
| `1402` | `ERROR`      | Invalid city name: abbreviated or code-based value detected                                    | `true`  | City Name Analysis: abbreviation       |
| `2401` | `WARNING`    | City name formatting is inconsistent; consider normalizing the value                           | `true`  | City Name Analysis: formatting         |
| `1501` | `ERROR`      | Postal codes are deprecated by RFC 8805 and must be removed for privacy reasons                | `true`  | Postal Code Check                      |
| `3301` | `SUGGESTION` | Region is usually unnecessary for small territories; consider removing the region value        | `true`  | Tuning: small territory region         |
| `3402` | `SUGGESTION` | City-level granularity is usually unnecessary for small territories; consider removing the city value | `true`  | Tuning: small territory city           |
| `3303` | `SUGGESTION` | Region code is recommended when a city is specified; choose a region from the dropdown         | `true`  | Tuning: missing region with city       |
| `3104` | `SUGGESTION` | Confirm whether this subnet is intentionally marked as do-not-geolocate or missing location data | `true`  | Tuning: unspecified geolocation        |

#### Populating Messages

When a validation check matches, add a message to the entry's `Messages` array using the values from the reference table:
```python
entry["Messages"].append({
    "ID": "1201",      # From the table
    "Type": "ERROR",   # From the table
    "Text": "Invalid country code: not a valid ISO 3166-1 alpha-2 value",  # From the table
    "Checked": True    # From the table (True = tunable)
})
```

After populating all messages for an entry, derive the entry-level flags:
```python
entry["HasError"] = any(m["Type"] == "ERROR" for m in entry["Messages"])
entry["HasWarning"] = any(m["Type"] == "WARNING" for m in entry["Messages"])
entry["HasSuggestion"] = any(m["Type"] == "SUGGESTION" for m in entry["Messages"])
entry["Tunable"] = any(m["Checked"] for m in entry["Messages"])
## Extended reference

Additional detailed guidance was moved to [references/extended-guide.md](references/extended-guide.md) to keep this skill within the progressive-disclosure budget.

