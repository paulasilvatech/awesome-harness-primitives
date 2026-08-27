---
name: dotnet-timezone
description: >-
  Resolve .NET and C# timezone questions with TimeZoneInfo, DateTimeOffset, TimeZoneConverter,
  NodaTime, UTC conversion, daylight saving time, scheduling, Windows and IANA timezone IDs,
  location lookup, and copy-paste-ready code. Use this skill when a .NET user needs the timezone
  for a city, address, region, or country, or asks about cross-platform timezone handling.
---

<!-- Generated from harness/github-copilot/plugins/dotnet-desktop-development/skills/dotnet-timezone/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# .NET timezone

Resolve timezone IDs, conversions, scheduling, and persistence for .NET applications by selecting the right library, mapping Windows and IANA identifiers, and returning concise C# code that is safe across daylight saving time and platforms.

## When to invoke

- "What timezone should I use for this city in .NET?"
- "Convert UTC to local time with TimeZoneInfo."
- "Make this timezone code work on Windows and Linux."
- "Handle daylight saving time in a C# scheduler."
- "Should I use DateTimeOffset or NodaTime?"

## Prerequisites and context

- Read `references/timezone-index.md` for common Windows and IANA mappings.
- Read `references/code-patterns.md` for ready-to-use .NET timezone patterns.
- Default to `TimeZoneConverter` for cross-platform Windows/IANA compatibility when the target runtime is unclear.
- Prefer `NodaTime` for recurring schedules, strict timezone arithmetic, and DST-sensitive workflows.

## Request routing

| Request type | Recommended path |
| --- | --- |
| Address or location lookup | Resolve geography to IANA zone, map to Windows ID, then return both IDs and offset/DST notes. |
| Timezone ID lookup | Use `references/timezone-index.md`; always provide Windows and IANA formats. |
| UTC/local conversion | Use `TimeZoneInfo` for platform-specific IDs or `TimeZoneConverter` for cross-platform IDs. |
| Cross-platform compatibility | Use `TZConvert.GetTimeZoneInfo(...)` from `TimeZoneConverter`. |
| Scheduling or DST handling | Use `NodaTime` and explicitly handle ambiguous and invalid local times. |
| API or persistence design | Store instants in UTC and use `DateTimeOffset` for data transfer; persist a timezone ID when future local scheduling matters. |

## Location resolution output

For every address, city, region, country, or place name, return this block and then a C# snippet.

```text
Location: <resolved place>
Windows ID: <windows id>
IANA ID: <iana id>
UTC offset: <standard offset and DST offset when relevant>
DST: <yes/no>
```

If multiple locations are present, include one block per location and a combined multi-timezone snippet. If a location is ambiguous, list possible timezone matches and ask the user to choose.

## Code patterns

| Pattern | Use when | Core API |
| --- | --- | --- |
| `TimeZoneInfo` | Windows-only code or known platform-specific ID. | `TimeZoneInfo.FindSystemTimeZoneById()`, `TimeZoneInfo.ConvertTimeFromUtc(...)`. |
| `TimeZoneConverter` | Cross-platform conversion across Windows, Linux, containers, and Azure. | `TZConvert.GetTimeZoneInfo("Asia/Colombo")`. |
| `NodaTime` | Recurring schedules, strict arithmetic, DST-sensitive jobs. | `DateTimeZone`, `Instant`, `ZonedDateTime`, resolvers for skipped/repeated local times. |
| `DateTimeOffset` | APIs and data transfer where offset must travel with the value. | `DateTimeOffset` and UTC normalization. |
| ASP.NET Core persistence/presentation | Store UTC instants and display in user-selected zone. | Database UTC column plus user timezone ID. |
| Recurring jobs and schedulers | Future local time must stay local after DST changes. | Store local schedule + zone ID, compute next occurrence with timezone rules. |
| Ambiguous and invalid DST timestamps | Local time may repeat or not exist. | Validate with `TimeZoneInfo.IsAmbiguousTime()` and `TimeZoneInfo.IsInvalidTime()` or NodaTime resolvers. |

```csharp
using TimeZoneConverter;

TimeZoneInfo tz = TZConvert.GetTimeZoneInfo("Asia/Colombo");
DateTime local = TimeZoneInfo.ConvertTimeFromUtc(DateTime.UtcNow, tz);
```

## Pitfall warnings

| Pitfall | Corrective rule |
| --- | --- |
| `TimeZoneInfo.FindSystemTimeZoneById()` is platform-specific | Use Windows IDs on Windows, IANA IDs on Linux/containers, or `TimeZoneConverter` to bridge both. |
| Storing `DateTime.Now` in databases | Store UTC instants; convert only at boundaries and presentation. |
| `DateTimeKind.Unspecified` leaks into conversions | Treat it as a bug risk unless it deliberately represents user-entered local wall time. |
| DST transitions skip or repeat local times | Validate invalid and ambiguous local timestamps before scheduling or converting. |
| Azure Windows and Azure Linux differ | Use the ID format expected by the host OS or use `TimeZoneConverter`. |

Keep answers production-safe, code-first, and explicit about third-party package requirements.

## Output template

```markdown
## .NET timezone result

**Status:** resolved | ambiguous | blocked
**Recommended approach:** <TimeZoneInfo | TimeZoneConverter | NodaTime | DateTimeOffset>

| Location or scenario | Windows ID | IANA ID | Offset/DST | Notes |
| --- | --- | --- | --- | --- |
| `<place or code path>` | `<windows>` | `<iana>` | `<offsets>` | `<pitfall>` |

    <copy-paste-ready C# snippet>

**Package requirement:** `<none | TimeZoneConverter | NodaTime>`
**Warning:** <relevant pitfall>
```

## Quality gate

- [ ] The request type was identified before choosing a library.
- [ ] Location requests include Windows ID, IANA ID, UTC offset, and DST status for each resolved place.
- [ ] Cross-platform code uses `TimeZoneConverter` unless the platform-specific ID requirement is explicit.
- [ ] Recurring schedules or strict DST logic use or recommend `NodaTime`.
- [ ] API and persistence guidance stores UTC and preserves timezone IDs when future local scheduling matters.
- [ ] The response includes a minimal copy-paste-ready C# snippet and package guidance.
- [ ] Ambiguous locations or DST timestamps are not silently guessed.

## Progressive disclosure and bundled resources

- `references/timezone-index.md`: common Windows and IANA timezone mappings.
- `references/code-patterns.md`: ready-to-use .NET timezone patterns.
