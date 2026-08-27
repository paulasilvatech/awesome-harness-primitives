---
paths:
  - "**/*.py"
---

<!-- Generated from harness/github-copilot/instructions/dataverse-python-agentic-workflows.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Preview conventions for building agentic Python workflows that use Dataverse as an enterprise data source, including SDK usage, data agents, MCP/A2A patterns, governance, and ML integration.

# Dataverse Python Agentic Workflow Conventions — Preview Data Agents

These instructions apply to Python code that builds agentic workflows over Microsoft Dataverse with the Dataverse SDK for Python public preview capabilities and planned GA integrations. They are authoritative for Dataverse-backed data agents, data quality checks, form prediction, MCP and A2A design seams, secure impersonation concepts, governance conventions, and AI/ML integration in matched files; official Dataverse SDK documentation, platform security policy, and production compliance requirements win wherever they define stricter behavior or finalized APIs.

## Preview Status and API Stability

Treat the agentic workflow surface as preview. Keep conceptual patterns isolated from stable SDK calls, and label planned integrations so reviewers can distinguish available code from future-facing design.

| Item | Convention |
| --- | --- |
| `PREVIEW` / `FEATURE` / `NOTICE` | Preserve preview notices for feature stability and review context. |
| Status | Public Preview as of December 2025. |
| General Availability | GA date is TBD; do not promise final API compatibility. |
| Documentation | Complete implementation details are forthcoming; validate code against official docs before production use. |
| Current SDK posture | Use current SDK capabilities for CRUD, bulk operations, OData, SQL, metadata, pagination, file upload, and structured errors. |
| Planned posture | Design for native async/await, MCP integration, A2A collaboration primitives, enhanced authentication/impersonation, governance policy enforcement, and advanced caching strategies without hardcoding nonexistent APIs into production paths. |

## Agentic Workflow Model

Use Dataverse as the central source of truth and keep agents focused on one data responsibility. An agentic workflow combines decision-making agents, orchestration logic, and Dataverse records, not unbounded autonomous mutation.

| Concept | Convention |
| --- | --- |
| Agents | Implement autonomous components that make decisions and take actions based on data and rules. |
| Workflows | Orchestrate complex, multi-step operations without hiding side effects. |
| Dataverse | Treat as the enterprise system of record for tables, rows, metadata, documents, audit trails, and governance. |
| Python audience | Keep workflows approachable for data scientists and developers who do not have .NET expertise. |
| Autonomous Data Agents | Query, update, and evaluate data quality independently within explicit permission and audit boundaries. |
| Form Prediction & Autofill | Pre-fill forms from historical patterns and context only with clear confidence and review paths. |
| Model Context Protocol (MCP) | Use as the standard agent-to-tool communication shape when integration is available. |
| Agent-to-Agent (A2A) Collaboration | Let multiple agents collaborate through events or messages, not shared mutable state. |
| Semantic Modeling | Represent natural-language understanding of data relationships separately from raw table access. |
| Secure Impersonation | Run operations on behalf of specific users only through supported impersonation contexts and audit trails. |
| Compliance Built-in | Enforce data governance and retention policies instead of leaving them to caller discipline. |

## Dataverse SDK Access Patterns

Use current SDK features for working code. Keep data access explicit, paginated, and table-aware.

| API or package | Convention |
| --- | --- |
| `from PowerPlatform.Dataverse.client import DataverseClient` | Use the current SDK client for Dataverse access. |
| `from azure.identity import InteractiveBrowserCredential` | Use Azure Identity credentials for interactive development samples; production code should use the organization's approved credential flow. |
| `DataverseClient("https://<org>.crm.dynamics.com", InteractiveBrowserCredential())` | Keep the organization URL configurable; preserve the placeholder `https://<org>.crm.dynamics.com` only in samples. |
| `client.get(table_name, select=required_fields)` | Select only required fields for completeness and quality checks. |
| `client.get("account")` | Use logical table names such as `account` consistently. |
| `client.update("account", account['id'], enrichment)` | Update only fields owned by the agent's responsibility. |
| `client.create("account", {"name": "New Account"})` | Create records only inside an auditable user or service context. |
| `client.list_tables()` | Validate table existence before running health checks. |
| Pagination | Iterate pages returned by `client.get(...)`; do not assume a single list contains every record. |
| File Upload | Treat document attachment handling as data governance-sensitive. |
| Metadata Operations | Use table and column definitions instead of hardcoded assumptions when agents adapt to schema. |
| Error Handling | Preserve structured exception details in logs and return user-safe status objects. |

## Data Quality and Health Agents

Build data agents around measurable checks, bounded record sets, and reproducible reports.

| Agent or method | Convention |
| --- | --- |
| `DataQualityAgent` | Monitor and improve data quality without mixing enrichment, sync, or UI prediction logic into the same class. |
| `evaluate_data_quality(table_name)` | Return metrics such as `total_records`, `null_values`, and `duplicate_records`. |
| `auto_remediate(issues)` | Keep remediation decisions explicit, auditable, and reversible. |
| `analyze_completeness(table_name, required_fields)` | Count missing values per required field and calculate percentages. |
| `all_records` | Use a local aggregate only after paging deliberately; avoid unbounded memory growth. |
| `missing_by_field` | Track missing counts per required field before computing completeness. |
| `missing_counts` | Include missing-count details in quality reports. |
| `duplicate_count` | Report duplicate totals alongside duplicate details. |
| `detect_duplicates(table_name, key_fields)` | Use deterministic keys such as `name` and `emailaddress1`; report `original_id`, `duplicate_id`, and `key`. |
| `generate_quality_report(table_name)` | Return `timestamp`, `table`, `completeness`, and `duplicates`; use `pd.Timestamp.now().isoformat()` when pandas is already a dependency. |
| `SimpleDataAgent.check_health(table_name)` | Check table existence with `list_tables()`, cap exploratory counts such as `len(records) > 1000`, and return `status`, `message`, `record_count`, and `timestamp`. |
| `json.dumps(report, indent=2)` | Use for readable local reports; avoid dumping sensitive records. |
| Required fields | Use examples such as `name`, `telephone1`, and `emailaddress1` only when they match the target table. |

## Enrichment, Pipeline, and Agent Collaboration

Keep orchestration separate from individual agent behavior so agents can be tested independently and composed safely.

| Pattern | Convention |
| --- | --- |
| `DataEnrichmentAgent.enrich_accounts()` | Enrich account records with external market data only after ownership, source quality, and overwrite rules are explicit. |
| `multi-agent` | Keep multi-agent collaboration explicit through orchestration or events. |
| `DataPipeline` | Orchestrate `quality_agent`, `enrichment_agent`, and `sync_agent` instead of embedding all logic in one agent. |
| `run(table_name)` | Make orchestration state visible through events or logs such as quality check, enrichment, and external sync stages without requiring a numbered runbook in the instruction. |
| `sync_to_external_db` | Keep external sync as a named operation owned by synchronization agents. |
| `SyncAgent` | Keep external database synchronization separate from quality and enrichment logic. |
| `DataValidationAgent.validate_and_notify(data)` | Publish `data_validated` or `validation_failed` events after validation. |
| `DataProcessingAgent.process_data(data)` | Subscribe to validated events and process only already-validated data. |
| `publish_event(...)` / `subscribe(...)` | Use event-style collaboration for A2A flows; never couple agents through untracked shared objects. |

## MCP Tool Integration

Design MCP tools with stable names, clear descriptions, constrained parameters, and standard error handling. Keep MCP server code conceptual until the SDK provides the final API.

| MCP element | Convention |
| --- | --- |
| `from dataverse_mcp import DataverseMCPServer` | Treat as conceptual until the package and API are released. |
| `DataverseMCPServer(client, tools=tools)` | Build servers from an existing Dataverse client and a declarative tool list. |
| `query_accounts` | Define a query tool with `filter`, `select`, and `top` parameters. |
| `create_account` | Define create tools with required business fields such as `name` and bounded optional fields such as `credit_limit`. |
| `update_account` | Define update tools with `account_id` and `updates`; validate field ownership before writing. |
| `handle_tool_call("query_accounts", {...})` | Keep tool invocation explicit and validate OData filters such as `creditlimit gt 100000`. |
| `tools/capabilities` | Document available tools and capabilities before exposing them to agents. |
| Tool Definition | Describe available tools and parameters. |
| Tool Invocation | Allow LLMs to call tools only through validated parameters. |
| Context Management | Preserve context between agent and tools without leaking unrelated records. |
| Error Handling | Return standardized errors instead of raw exceptions. |
| Model Context Protocol docs | Preserve `https://modelcontextprotocol.io/` as the external protocol reference and avoid claiming any SDK is the go-to platform until GA documentation confirms it. |

## Prediction and AI/ML Integration

Separate predictive models from Dataverse write paths. Predictions should carry confidence and never silently overwrite user-entered data.

| API or class | Convention |
| --- | --- |
| `FormPredictionAgent` | Train and serve autofill suggestions for one bounded form or table scenario. |
| `RandomForestRegressor` | Use `sklearn.ensemble.RandomForestRegressor` only when tabular historical data and regression output fit the problem. |
| `pandas as pd` | Use `pd.DataFrame(records)` for feature preparation and `pd.Timestamp.now().isoformat()` for timestamps when pandas is already part of the workflow. |
| `train_on_historical_data(table_name, features, target)` | Collect training data with `select=features + [target]`, fill missing feature values deliberately, and return a model score. |
| `predict_field_values(table_name, record_id, features_data)` | Return `record_id`, `predicted_value`, and `confidence`; raise `ValueError("Model not trained. Call train_on_historical_data first.")` when no model exists. |
| `analyze_with_llm` | Keep LLM analysis in a named method that bounds samples and returns advisory insight. |
| `DataInsightAgent` | Use LLMs to summarize data samples without turning the LLM into the system of record. |
| `from openai import OpenAI` | Keep LLM integration behind a dedicated class and pass `openai_key` through secure configuration. |
| `OpenAI(api_key=openai_key)` | Never hardcode API keys. |
| `llm.chat.completions.create(...)` | Keep the model name, for example `gpt-4`, configurable. |
| `sample_size=100` | Bound data sent to the LLM and summarize records with `json.dumps(records[:5], indent=2, default=str)`. |
| `response.choices[0].message.content` | Return generated insights as advisory content, not verified facts. |

## Impersonation, Audit, and Governance

Do not simulate security features in production code. Use supported platform capabilities for impersonation, audit trails, retention, and classification.

| Capability | Convention |
| --- | --- |
| `GUID` | Treat user and record GUID values as identifiers that require audit and access-control checks. |
| `from dataverse_security import ImpersonationContext` | Treat as a planned conceptual API until released. |
| `with ImpersonationContext(client, user_id="user-guid")` | Run operations on behalf of a specific user only with explicit user identity and audit requirements. |
| `client.get_audit_trail(table="account", record_id="record-guid", action="create")` | Retrieve audit evidence for sensitive mutations. |
| `from dataverse_governance import DataGovernance` | Treat as a planned conceptual API until released. |
| `DataGovernance(client)` | Centralize retention and classification logic. |
| `set_retention_policy(table="account", retention_days=365)` | Keep retention days explicit and policy-driven. |
| `classify_columns(...)` | Classify fields such as `name` as `Public`, `telephone1` as `Internal`, and `creditlimit` as `Confidential` only when those labels match the organization's data policy. |
| `enforce_all_policies()` | Apply governance through a central mechanism, not scattered conditionals. |

## Current and Planned Capability Boundaries

Use available capabilities now and leave clean seams for planned features; agent-like systems are acceptable when they use stable CRUD and query APIs rather than unreleased hooks.

| Available now | Coming in GA |
| --- | --- |
| CRUD Operations | Full MCP integration |
| Bulk Operations | A2A collaboration primitives |
| Query Capabilities with OData and SQL | Enhanced authentication/impersonation |
| Metadata Operations | Governance policy enforcement |
| Error Handling with structured exception hierarchy | Native async/await support |
| Pagination for large result sets | Advanced caching strategies |
| File Upload for document attachments | More complete agentic workflow APIs |

## Good / Bad Examples

The examples below illustrate bounded, paginated Dataverse access with safe reporting.

**Good:**

```python
from PowerPlatform.Dataverse.client import DataverseClient
from azure.identity import InteractiveBrowserCredential
import json
import pandas as pd

class SimpleDataAgent:
    def __init__(self, org_url):
        self.client = DataverseClient(org_url, InteractiveBrowserCredential())

    def check_health(self, table_name):
        try:
            matching = [t for t in self.client.list_tables() if t["LogicalName"] == table_name]
            if not matching:
                return {"status": "error", "message": f"Table {table_name} not found"}

            records = []
            for page in self.client.get(table_name):
                records.extend(page)
                if len(records) > 1000:
                    break

            return {
                "status": "healthy",
                "table": table_name,
                "record_count": len(records),
                "timestamp": pd.Timestamp.now().isoformat(),
            }
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

agent = SimpleDataAgent("https://<org>.crm.dynamics.com")
print(json.dumps(agent.check_health("account"), indent=2))
```

Why: The agent uses the current SDK, validates table existence, paginates, bounds exploratory reads, and returns a structured status.

**Bad:**

```python
class Agent:
    def run(self):
        records = self.client.get("account")
        self.llm.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": str(records)}])
        self.client.update("account", "record-guid", {"creditlimit": 999999})
```

Why: The code ignores pagination, sends unbounded data to an LLM, hardcodes a record mutation, and lacks audit, validation, confidence, and governance checks.

## Conventions

| Rule | Rationale |
|---|---|
| Mark Public Preview and TBD GA assumptions in code comments or design docs when using planned features | Reviewers can separate stable SDK code from future-facing seams |
| Use `DataverseClient` with approved credentials and configurable organization URLs | Data agents remain deployable across environments |
| Iterate paginated `client.get(...)` results and select only needed columns | Large Dataverse tables do not overload memory or expose unnecessary data |
| Keep `DataQualityAgent`, `DataEnrichmentAgent`, `DataPipeline`, `DataValidationAgent`, and `DataProcessingAgent` responsibilities separate | Agents stay testable and side effects remain visible |
| Design MCP tools such as `query_accounts`, `create_account`, and `update_account` with validated parameters | LLM tool calls cannot mutate enterprise data through ambiguous inputs |
| Return confidence and record identity from prediction agents | Users can review autofill suggestions before trusting them |
| Use `ImpersonationContext`, audit trails, and `DataGovernance` only through supported APIs | Security and compliance are enforced by the platform, not simulated locally |
| Bound LLM samples and keep generated insights advisory | Sensitive data exposure and hallucinated decisions are reduced |

## Do / Do Not

| Do | Do not |
|---|---|
| Use current SDK capabilities for CRUD Operations, Bulk Operations, Query Capabilities, Metadata Operations, Error Handling, Pagination, and File Upload | Depend on planned GA-only APIs as if they were production-ready |
| Keep examples using `https://<org>.crm.dynamics.com` as placeholders | Commit a real organization URL, token, or credential |
| Validate tables with `client.list_tables()` before health checks | Assume every configured `table_name` exists |
| Publish `data_validated` and `validation_failed` events between agents | Share mutable state directly between A2A agents |
| Define MCP tool schemas with `filter`, `select`, `top`, `account_id`, and `updates` | Let an LLM pass arbitrary write payloads to Dataverse |
| Use `pd.DataFrame`, `RandomForestRegressor`, and `OpenAI` only where the dependency is justified | Add ML or LLM dependencies to simple CRUD workflows without need |
| Retrieve `audit_log` with `get_audit_trail` for sensitive writes | Perform impersonated or governed operations without evidence |
| Cite official documentation and release plans for preview behavior | Treat conceptual snippets as finalized SDK contracts |

## Checklist Before Opening a PR

- [ ] Preview-only APIs are labeled and isolated from production execution paths.
- [ ] Dataverse organization URLs, credentials, OpenAI keys, and user IDs are configurable and not committed as real values.
- [ ] Agents use `DataverseClient`, approved Azure Identity credentials, pagination, and field selection where applicable.
- [ ] Data quality reports include table, totals, completeness, missing counts, duplicates, and timestamps without dumping sensitive records.
- [ ] MCP tools have stable names, descriptions, validated parameters, and standardized error behavior.
- [ ] A2A collaboration uses events or messages such as `data_validated`, `validation_failed`, and `processing_complete`.
- [ ] Prediction and LLM flows bound sample sizes, preserve confidence, and avoid silent writes.
- [ ] Impersonation, audit, retention, classification, and governance logic rely on supported platform APIs or remain clearly conceptual.
- [ ] Current-versus-GA capability boundaries are explicit in code, comments, or documentation.

## References

- Dataverse SDK for Python Overview: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/overview
- Working with Data: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/sdk-python/work-data
- Release Plan: Agentic Workflows: https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave2/data-platform/build-agentic-flows-dataverse-sdk-python
- Model Context Protocol: https://modelcontextprotocol.io/
- Azure AI Services: https://learn.microsoft.com/en-us/azure/ai-services/
- Python async/await: https://docs.python.org/3/harness/github-copilot/asyncio.html
- SDK Source Code: https://github.com/microsoft/PowerPlatform-DataverseClient-Python
- Issues & Feature Requests: https://github.com/microsoft/PowerPlatform-DataverseClient-Python/issues
