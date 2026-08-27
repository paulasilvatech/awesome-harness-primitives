---
name: ssma-console
description: >-
  Generate XML configuration and execute Microsoft SQL Server Migration Assistant for Oracle
  console operations without wrapper scripts. Use when asked to create an SSMA project, assess
  Oracle to SQL Server migration, convert schema, synchronize target schema, migrate data, or
  troubleshoot SSMAforOracleConsole.exe XML scripts.
---

<!-- Generated from harness/github-copilot/plugins/data-engineering/skills/ssma-console/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# SSMA console

Create resolved SSMA XML files for Oracle to SQL Server migration operations, then invoke `SSMAforOracleConsole.exe` directly with variables, servers, and operation scripts.

## When to invoke

- "Create an SSMA console project for Oracle to SQL Server."
- "Generate the SSMA assessment report XML."
- "Convert and deploy Oracle schema with SSMAforOracleConsole.exe."
- "Migrate Oracle data to SQL Server using SSMA console."
- "Fix ORA-12505 or Source namespace was not found in SSMA XML."

## Inputs

Collect every placeholder before writing final XML.

| Group | Required values and defaults |
| --- | --- |
| Oracle | Host `localhost`, Port `1521`, Instance required service name, User, Password, Schema. |
| SQL Server | Server, Database, User, Password, Encrypt `true`, Trust Server Certificate `true`, Target Schema `dbo`. |
| Project | Name `ssma-migration`, Folder `.`, Type `sql-server-2022` with allowed `2016`, `2017`, `2019`, `2025`, `sql-azure`, SSMA Path `C:\Program Files\Microsoft SQL Server Migration Assistant for Oracle\bin\SSMAforOracleConsole.exe`. |

Preserve placeholders while collecting: `{PROJECT_FOLDER}`, `{PROJECT_TYPE}`, `{PROJECT_NAME}`, `{ORACLE_HOST}`, `{ORACLE_INSTANCE}`, `{ORACLE_PORT}`, `{ORACLE_USER}`, `{ORACLE_PASSWORD}`, `{ORACLE_SCHEMA}`, `{SQL_SERVER}`, `{SQL_DATABASE}`, `{SQL_USER}`, `{SQL_PASSWORD}`, `{ENCRYPT}`, `{TRUST_CERT}`, `{TARGET_SCHEMA}`, `{SSMA_CONSOLE_PATH}`, `{SCRIPT_XML}`, and `{OPERATION}`.

## Operation sequence

| Operation | File | Commands after preamble |
| --- | --- | --- |
| create-project | `ssma-create-project.xml` | `connect-target-database` then `map-schema source-schema="$OracleSchemaName$" sql-server-schema="$SQLServerDb$.{TARGET_SCHEMA}"`. |
| generate-report | `ssma-assessment.xml` | `generate-assessment-report object-name="$OracleSchemaName$" object-type="Schemas" write-summary-report-to="$SummaryReportFile$" verbose="true" report-errors="true"`. |
| migrate-schema | `ssma-schema.xml` | `connect-target-database`, `map-schema`, `convert-schema` to `$ConversionReportFile$`, then `synchronize-target object-name="$SQLServerDb$.{TARGET_SCHEMA}"`. |
| migrate-data | `ssma-data.xml` | Same as migrate-schema plus `refresh-from-database`, `migrate-data object-name="$OracleSchemaName$.Tables" object-type="category"` to `$DataMigrationReportFile$`, then `close-project`. |

For full migration, run create-project → generate-report → migrate-schema → migrate-data.

## XML requirements

Generate `ssma-variables.xml` with `$WorkingFolder$`, `$ProjectType$`, `$ProjectName$`, `OracleConnection`, `SQLServerConnection`, and `ReportSettings` variables including `$SummaryReportFile$`, `$ConversionReportFile$`, `$ConversionReportFolder$`, `$DataMigrationReportFile$`, and `$SynchronizationReportFolder$`.

Generate `ssma-servers.xml` using `tns-name-mode`; `standard-mode` treats the Oracle instance as SID and can fail with `ORA-12505`.

```xml
<oracle name="source_oracle">
  <tns-name-mode>
    <connection-provider value="OracleClient" />
    <service-name value="(DESCRIPTION =(ADDRESS_LIST =(ADDRESS = (PROTOCOL = TCP)(HOST = $OracleHostName$)(PORT = $OraclePort$)))(CONNECT_DATA =(SERVICE_NAME = $OracleInstance$)))" />
    <user-id value="$OracleUserName$" />
    <password value="$OraclePassword$" />
  </tns-name-mode>
</oracle>
```

All operation scripts use this preamble:

```xml
<create-new-project project-folder="$WorkingFolder$" project-name="$ProjectName$"
                    overwrite-if-exists="true" project-type="$ProjectType$" />
<connect-source-database server="source_oracle">
  <object-to-collect object-name="$OracleSchemaName$" />
</connect-source-database>
```

Always include `<object-to-collect>`; without it, `map-schema` fails with "Source namespace was not found". Use `<object-overwrite action="overwrite" />` for `migrate-schema` and `migrate-data`. Add `<data-migration-connection source-use-last-used="true" target-server="target_sqlserver" />` for `migrate-data`. Use `every-10%` progress in the common config and `every-5%` progress for schema/data operations.

## Execution

Show resolved XML and command to the user before running. Do not create external `.ps1`, `.bat`, or `.sh` wrappers.

```powershell
New-Item -ItemType Directory -Force -Path "Reports\Assessment","Reports\Conversion","Reports\Migration","Reports\Synchronization","Logs" | Out-Null
& "{SSMA_CONSOLE_PATH}" -s "{SCRIPT_XML}" -c "ssma-servers.xml" -v "ssma-variables.xml" -l "Logs\{OPERATION}.log"
```

After execution, check exit code `0`, logs in `Logs\{OPERATION}.log`, and reports under `Reports\Assessment\`, `Reports\Conversion\`, `Reports\Migration\`, and `Reports\Synchronization`.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `ORA-12505: SID not registered` | Used `standard-mode` for a service-name connection. | Use `tns-name-mode`. |
| `Source namespace was not found` | `connect-source-database` did not collect the schema. | Add `<object-to-collect>`. |
| `not found in metabase` on `force-load` | `force-load` is unreliable for this flow. | Use `object-to-collect` instead. |
| `SQL Server Agent is not running` | SSMA emits a warning. | Treat as warning; BCP client-side migration still works. |

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- ` (to `
- ` = success), read logs and reports (`
- ` for migrate-data, use `
- ` — also `
- `) → `
- `), Type (`
- `2017`
- `2019`
- `2025`
- `<config>`
- `<save-project />`
- `<script-commands>`
- `CRITICAL`
- `PLACEHOLDER`
- `end-to-end`
- `log-verbosity`
- `migrate-schema/migrate-data`
- `output-providers`
- `output-window`
- `progress-reporting`
- `report-messages`
- `report-progress`
- `save-project`
- `script-commands`
- `sql-server`
- `sql-server-authentication`
- `suppress-messages`
- `trust-server-certificate`
- `upgrade-project`
- `user-input-popup`
- `variable-group`
- `{PLACEHOLDER}`

Report file names to preserve in generated XML: AssessmentReport, ConversionReport, and DataMigrationReport.

## Output template

```markdown
## SSMA console result

**Status:** generated | executed | blocked
**Operation:** create-project | generate-report | migrate-schema | migrate-data

### Files
- `ssma-variables.xml`
- `ssma-servers.xml`
- `<operation script>.xml`

### Command
`& "{SSMA_CONSOLE_PATH}" -s "{SCRIPT_XML}" -c "ssma-servers.xml" -v "ssma-variables.xml" -l "Logs\{OPERATION}.log"`

### Validation
- Placeholders resolved: <yes/no>
- Exit code: <0/nonzero/not run>
- Reports reviewed: <paths>
```

## Quality gate

- [ ] All `{...}` placeholders are resolved before final XML execution.
- [ ] `ssma-servers.xml` uses `tns-name-mode`, not `standard-mode`.
- [ ] Every source connection includes `<object-to-collect>`.
- [ ] Operation order is respected for full migration.
- [ ] No external wrapper script is created.
- [ ] Output directories are created before execution.
- [ ] Logs, reports, and exit code are summarized.
