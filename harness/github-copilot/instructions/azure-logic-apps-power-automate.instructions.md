---
applyTo: "**/*.json,**/*.logicapp.json,**/workflow.json,**/*-definition.json,**/*.flow.json"
description: "Enforces Azure Logic Apps and Power Automate workflow conventions for WDL structure, triggers, actions, reliability, security, integration patterns, DevOps, monitoring, and cost governance."
---

# Azure Logic Apps and Power Automate Conventions — Workflow Automation

These instructions apply to Azure Logic Apps and Microsoft Power Automate workflow JSON definitions that use the JSON-based Workflow Definition Language (WDL). They are authoritative for workflow structure, connector use, expressions, integration patterns, reliability, security, monitoring, deployment, migration, and cost discipline in matched workflow files; platform policy, tenant licensing, and organization-specific Azure governance win where they define stricter requirements.

## Workflow Definition Language Structure

Use the canonical WDL envelope for Logic Apps and flow definitions. Keep the top-level `definition` and deployment `parameters` separate so environment values do not leak into workflow logic.

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "actions": {},
    "contentVersion": "1.0.0.0",
    "outputs": {},
    "parameters": {},
    "staticResults": {},
    "triggers": {}
  },
  "parameters": {}
}
```

- Keep `actions`, `triggers`, `parameters`, `outputs`, `staticResults`, and `contentVersion` explicit in workflow definitions.
- Use clear action names such as `Get_Customer_Data`, `Parse_Customer_Response`, `Switch_Request_Type`, `Initialize_Response_Variable`, and `Return_Success_Response` because run history and alerts surface these names directly.
- Avoid hardcoded properties in trigger and action definitions; parameterize environment-specific values such as `apiEndpoint`, `serviceBusQueueName`, `slaThresholdSeconds`, `criticalAlertChannelId`, `warningAlertChannelId`, `subscriptionId`, `resourceGroupName`, `location`, `Environment`, `logicAppName`, and `version`.
- Keep workflows to roughly 50 actions or less for designer performance; split complex business logic into multiple smaller workflows when necessary.
- Use descriptive comments only where JSON comments are accepted by the surrounding artifact or tooling; otherwise encode context in names, metadata, run tracking, and documentation.

## Platform Selection and Workflow Types

Choose Azure Logic Apps or Power Automate intentionally even though both share the underlying workflow engine and language.

| Platform or type | Use when | Avoid when |
| --- | --- | --- |
| Power Automate | Business users need a user-friendly interface, Microsoft 365 and Dynamics 365 integration, Power Platform environments, desktop flow UI automation, or RPA capabilities. | Enterprise operations, advanced Azure integration, and deep monitoring are primary requirements. |
| Azure Logic Apps | Developers need enterprise-grade integration, Azure service integration, operational monitoring, API-style workflows, B2B/EDI, or source-controlled deployment. | Licensing, ownership, or citizen-developer requirements make a Power Platform Solution the right ALM boundary. |
| Consumption Logic Apps | Workloads are variable, unpredictable, serverless, and fit a pay-per-execution pricing model. | Predictable performance, local development support, VNet integration, or fixed plan economics are required. |
| Standard Logic Apps | Fixed App Service Plan pricing, predictable performance, local development support, shared workflows, deployment slots, and VNet integration are needed. | Pay-per-execution economics are better for the workload. |
| Integration Service Environment (ISE) | Dedicated deployment, isolated runtime, direct VNet access, higher throughput, or longer execution durations are required. | The scenario can use newer Standard networking and private endpoint patterns. |

Power Automate license decisions belong in the design record: `Power Automate per user plan`, `Power Automate per flow plan`, `Power Automate Process plan`, or `Power Automate included with Office 365`. Account for premium connectors, API call limits, per-user assignment, per-flow ownership, and Office 365 limitations before moving a flow into production.

## Triggers and API Entry Points

Select trigger types by integration style and protect every inbound boundary.

- Use a Request trigger for synchronous API-like workflows and return explicit `Response` actions with appropriate `statusCode`, headers, and body shape.
- Use a Recurrence trigger for scheduled operations; set recurrence intervals that avoid over-polling.
- Use event-based triggers for reactive patterns such as Service Bus and Event Grid.
- Use webhook-based triggers instead of polling triggers when the source supports callbacks.
- Configure timeout periods, pagination settings for high-volume data sources, authentication, IP restrictions, and OpenAPI schemas for HTTP triggers.
- For Workflow as API patterns, design request triggers with `method`, `required`, `enum`, field descriptions, and response contracts.

```json
"triggers": {
  "manual": {
    "type": "Request",
    "kind": "Http",
    "inputs": {
      "schema": {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
          "customerId": { "type": "string", "description": "The unique identifier for the customer" },
          "requestType": { "type": "string", "enum": ["Profile", "OrderSummary"], "description": "The type of request to process" },
          "requestParameter": { "type": "string" },
          "apiVersion": { "type": "string" }
        },
        "required": ["customerId", "requestType"]
      },
      "method": "POST"
    }
  },
  "When_a_message_is_received_in_a_queue": {
    "type": "ApiConnectionWebhook",
    "inputs": {
      "host": { "connection": { "name": "@parameters('$connections')['servicebus']['connectionId']" } },
      "body": { "isSessionsEnabled": true },
      "path": "/subscriptionListener",
      "queries": {
        "queueName": "@parameters('serviceBusQueueName')",
        "subscriptionType": "Main"
      }
    }
  }
}
```

When importing a Logic App through API Management, apply consistent URL structures, path versioning such as `/api/v1/resource`, request validation, rate limiting, and correlation headers before forwarding to the backend.

## Actions, Connectors, and Control Flow

Use the smallest reliable action set and choose the right action type for the operation.

- Use HTTP actions for direct REST calls, SOAP bridges, and protocol bridging when a connector does not provide a better contract.
- Use connector actions such as `ApiConnection` and `ApiConnectionWebhook` for built-in integrations with Key Vault, Service Bus, Office 365, Application Insights, Log Analytics, SQL, Teams, and Dataverse when the managed connector gives authentication, throttling, and schema benefits.
- Use data operation actions such as `Compose`, `ParseJson`, `InitializeVariable`, `SetVariable`, `AppendToArrayVariable`, `If`, `Switch`, `Scope`, `Foreach`, and `Response` to keep transformation and control flow explicit.
- Organize complex workflows with `Scope` actions such as `Try_Process_Order`, `Handle_Process_Error`, `Handle_Success`, `Handle_Failure`, `Handle_Connection_Errors`, and `Handle_Business_Logic_Errors`.
- Use conditions for branching logic, parallel branches for independent work, and `until` loops only with clear exit conditions and timeouts.
- Configure `runtimeConfiguration.concurrency.repetitions` for parallelizable `Foreach` loops; start with a conservative value such as `10` and adjust after observing connector limits.
- Use `runAfter` to make success, failure, timeout, and compensation paths explicit.

```json
"Process_Items": {
  "type": "Foreach",
  "foreach": "@body('Get_Items')",
  "actions": {
    "Process_Single_Item": { "type": "Scope", "actions": {} }
  },
  "runAfter": { "Get_Items": ["Succeeded"] },
  "runtimeConfiguration": {
    "concurrency": { "repetitions": 10 }
  }
}
```

## Expressions, Parameters, Variables, and Message Handling

Keep expressions readable and defensive. Use built-in expression functions instead of custom actions when the transformation is simple.

| Concern | Convention |
| --- | --- |
| String manipulation | Use `concat()`, `replace()`, `substring()`, and `toUpper()` for small string transforms. |
| Collection operations | Use `filter()`, `map()`, `select()`, `length()`, `sum()`, `max()`, `join()`, and `createArray()` when the expression remains readable. |
| Conditional logic | Use `if()`, `and()`, `or()`, `not()`, `equals()`, `greater()`, `less()`, and `contains()` for simple decisions; move complex branching into `If` or `Switch` actions. |
| Date/time | Use `formatDateTime()`, `addDays()`, `utcNow()`, `ticks()`, `div()`, `sub()`, and `mul()` for deterministic temporal calculations. |
| JSON handling | Use `json()`, `array()`, and `ParseJson` with schema validation before accessing structured payloads. |
| Safe access | Use `item()?['PropertyName']`, `triggerBody()?['customerId']`, `body('Parse_Message')?['data']?['items']`, `outputs('Calculate_Processing_Time')`, and `coalesce()` where missing data is possible. |

Power Automate conditions should use the designer for a single comparison and advanced expressions for multiple conditions:

```text
@or(equals(item()?['Status'], 'completed'), equals(item()?['Status'], 'unnecessary'))
@and(equals(item()?['Status'], 'blocked'), equals(item()?['Assigned'], 'John Wonder'))
@and(greater(item()?['Due'], item()?['Paid']), less(item()?['dueDate'], utcNow()))
@equals(item()?['Status'], 'blocked')
@greater(item()?['Due'], item()?['Paid'])
@less(item()?['dueDate'], addDays(utcNow(),1))
@empty(item()?['Status'])
@not(contains(item()?['Status'], 'Failed'))
```

Use the function names `equals`, `greater`, `less`, and `empty` consistently in Power Automate condition expressions so reviewers can map designer conditions to WDL expressions.
Preserve common condition snippets when refactoring: `@equals(item()?['Status'], 'blocked')`, `@greater(item()?['Due'], item()?['Paid'])`, `@less(item()?['dueDate'], addDays(utcNow(),1))`, `@empty(item()?['Status'])`, and `@not(contains(item()?['Status'], 'Failed'))`.

Parameterize workflows for reuse and keep temporary state local to the run:

```json
"parameters": {
  "apiEndpoint": {
    "type": "string",
    "defaultValue": "https://api.dev.example.com",
    "metadata": { "description": "The base URL for the API endpoint" }
  },
  "$connections": { "defaultValue": {}, "type": "Object" },
  "serviceBusQueueName": { "type": "string", "defaultValue": "orders" },
  "slaThresholdSeconds": { "type": "int" }
},
"actions": {
  "Initialize_Variables": {
    "type": "InitializeVariable",
    "inputs": {
      "variables": [
        { "name": "requestId", "type": "string", "value": "@{guid()}" },
        { "name": "processedItems", "type": "array", "value": [] },
        { "name": "validItems", "type": "array", "value": [] },
        { "name": "invalidItems", "type": "array", "value": [] },
        { "name": "responsePayload", "type": "object", "value": {} }
      ]
    }
  }
}
```

Validate message schemas, set `Content-Type` deliberately, and use `Parse JSON` actions before downstream transformations.

```json
"Parse_Response": {
  "type": "ParseJson",
  "inputs": {
    "content": "@body('HTTP_Request')",
    "schema": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "data": { "type": "array", "items": { "type": "object", "properties": {} } }
      }
    }
  }
}
```

## Reliability, Error Handling, and Exception Strategy

Design every workflow with explicit success, failure, timeout, fallback, and notification behavior.

- Configure retry policies for transient errors; use `fixed` retries for predictable short failures and `exponential` retries for unstable downstream services.
- Add timeouts for external service calls so runs do not hang indefinitely.
- Use `runAfter` with `Succeeded`, `Failed`, and `TimedOut` conditions for error branches.
- Add fallback mechanisms for critical operations, including `Invoke_Fallback_Endpoint` when a primary dependency fails.
- Use schema validation, defensive expressions with `coalesce()` and safe navigation (`?`), and pre-condition checks before critical operations.
- Use structured `try/catch`-style scopes: `Try_Primary_Action`, `Main_Operation`, `Handle_Connection_Errors`, `Handle_Business_Logic_Errors`, and `Switch_On_Error_Type`.
- Capture `ErrorCategory`, `StatusCode`, `ErrorMessage`, `ErrorDetails`, `Timestamp`, `EventId`, `OrderId`, `CustomerId`, and correlation IDs in logs.
- Categorize error types such as `ResourceNotFound`, `ValidationError`, and `PermissionDenied`; use specific recovery actions such as `Create_Resource`, `Resubmit_With_Defaults`, `Elevate_Permissions`, or `Send_To_Support_Queue` only when they are safe and intentional.

```json
"HTTP_Action": {
  "type": "Http",
  "inputs": { "method": "GET", "uri": "https://api.example.com/resource" },
  "retryPolicy": {
    "type": "fixed",
    "count": 3,
    "interval": "PT20S",
    "minimumInterval": "PT5S",
    "maximumInterval": "PT1H"
  }
},
"Get_Customer_Details": {
  "type": "Http",
  "inputs": { "method": "GET", "uri": "https://api.example.com/customers/@{body('Parse_Message')?['data']?['customerId']}" },
  "retryPolicy": {
    "type": "exponential",
    "count": 5,
    "interval": "PT10S",
    "minimumInterval": "PT5S",
    "maximumInterval": "PT1H"
  }
},
"Handle_Failure": {
  "type": "Scope",
  "actions": {
    "Log_Error": {
      "type": "ApiConnection",
      "inputs": {
        "host": { "connection": { "name": "@parameters('$connections')['loganalytics']['connectionId']" } },
        "method": "post",
        "body": {
          "LogType": "WorkflowError",
          "ErrorDetails": "@{actions('HTTP_Action').outputs.body}",
          "StatusCode": "@{actions('HTTP_Action').outputs.statusCode}"
        }
      }
    },
    "Send_Notification": {
      "type": "ApiConnection",
      "inputs": {
        "host": { "connection": { "name": "@parameters('$connections')['office365']['connectionId']" } },
        "method": "post",
        "path": "/v2/Mail",
        "body": {
          "To": "support@contoso.com",
          "Subject": "Workflow Error - HTTP Call Failed",
          "Body": "<p>The HTTP call failed with status code: @{actions('HTTP_Action').outputs.statusCode}</p>"
        }
      },
      "runAfter": { "Log_Error": ["Succeeded"] }
    }
  },
  "runAfter": { "HTTP_Action": ["Failed", "TimedOut"] }
}
```

For Service Bus processing, explicitly complete, abandon, or dead-letter messages by using `Complete_Message`, `Abandon_Message`, or `Dead_Letter_Message` with `lockToken`, `sessionId`, `queueName`, `deadLetterReason`, and `deadLetterDescription`. Use actions such as `Validate_Stock`, `Check_Product_Stock`, `Verify_Availability`, `Add_To_Valid_Items`, `Add_To_Invalid_Items`, `Check_Order_Validity`, `Process_Valid_Order`, `Send_Order_Confirmation`, and `Send_Invalid_Stock_Notification` to make business outcomes visible in run history.
When parsing Service Bus connector payloads, read message content from `ContentData` before applying a `ParseJson` schema so the workflow validates the actual brokered message body.

Use retry intervals such as `PT15S` or `PT30S` when the downstream connector needs a different cadence from the default `PT20S`; use `PT1S` only for explicit duration conversion logic, not as an aggressive retry interval.

```json
"Complete_Message": { "type": "ApiConnection", "inputs": { "path": "/messages/complete" } },
"Abandon_Message": { "type": "ApiConnection", "inputs": { "path": "/messages/abandon" } },
"Dead_Letter_Message": { "type": "ApiConnection", "inputs": { "path": "/messages/deadletter" } }
```

## Security, Identity, and Sensitive Data

Treat workflow definitions as production integration code that can expose data, credentials, and privileged actions.

- Use managed identities, especially `ManagedServiceIdentity`, for Azure service access when possible.
- In ARM templates, set the Logic App identity `type` to `SystemAssigned` when the workflow needs its own managed identity.
- Store secrets and credentials in Azure Key Vault; fetch `apiKey` and `database-connection-string` through the `keyvault` connector instead of embedding values.
- Apply least privilege to connections and Azure RBAC assignments; implement custom roles where built-in roles are too broad.
- Secure API endpoints with authentication and authorization; protect API Management frontends with `validate-jwt`, `openid-config`, and `required-claims`.
- Apply IP restrictions to HTTP triggers and content/action endpoints with `allowedCallerIpAddresses`, `addressRange`, `13.91.0.0/16`, and `40.112.0.0/13` only when those ranges are the intended callers.
- Apply encryption for sensitive parameters, messages, data at rest, and data in transit.
- Mask sensitive data in logs and monitoring; never emit raw connection strings, tokens, secrets, or full payloads containing sensitive data.
- Implement regular access reviews, Just-In-Time access for administrative operations, audit trails for access and configuration changes, private endpoints, and Virtual Network integration for Logic Apps Standard.

```json
"Get_Secret": {
  "type": "ApiConnection",
  "inputs": {
    "host": { "connection": { "name": "@parameters('$connections')['keyvault']['connectionId']" } },
    "method": "get",
    "path": "/secrets/@{encodeURIComponent('apiKey')}/value"
  }
},
"Call_Protected_API": {
  "type": "Http",
  "inputs": {
    "method": "POST",
    "uri": "https://api.example.com/protected",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "******'Get_Secret')?['value']}"
    },
    "body": { "data": "@variables('processedData')" }
  },
  "authentication": { "type": "ManagedServiceIdentity" },
  "runAfter": { "Get_Secret": ["Succeeded"] }
}
```

SQL connector calls that must execute a parameterized query should keep the dataset path and SQL shape explicit:

```json
"Execute_Database_Query": {
  "type": "ApiConnection",
  "inputs": {
    "host": { "connection": { "name": "@parameters('$connections')['sql']['connectionId']" } },
    "method": "post",
    "path": "/datasets/default/query",
    "body": {
      "query": "SELECT * FROM Customers WHERE CustomerId = @CustomerId",
      "parameters": { "CustomerId": "@triggerBody()?['customerId']" },
      "connectionString": "@body('Get_Database_Credentials')?['value']"
    }
  }
}
```

```xml
<policies>
  <inbound>
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401" failed-validation-error-message="Unauthorized">
      <openid-config url="https://login.microsoftonline.com/{tenant-id}/.well-known/openid-configuration" />
      <required-claims>
        <claim name="aud" match="any"><value>api://mylogicapp</value></claim>
      </required-claims>
    </validate-jwt>
    <rate-limit calls="5" renewal-period="60" />
    <set-header name="Correlation-Id" exists-action="override"><value>@(context.RequestId)</value></set-header>
    <log-to-eventhub logger-id="api-logger">@{ return new JObject(new JProperty("correlationId", context.RequestId), new JProperty("api", context.Api.Name), new JProperty("operation", context.Operation.Name), new JProperty("user", context.User.Email), new JProperty("ip", context.Request.IpAddress)).ToString(); }</log-to-eventhub>
  </inbound>
  <backend><forward-request /></backend>
  <outbound><set-header name="X-Powered-By" exists-action="delete" /></outbound>
  <on-error><base /></on-error>
</policies>
```

## Integration and Enterprise Patterns

Select integration patterns by business semantics, not by connector convenience.

| Pattern | Convention |
| --- | --- |
| Mediator Pattern | Use Logic Apps or Power Automate as an orchestration layer between systems when central routing adds clarity. |
| Content-Based Routing | Route messages based on content to different destinations with `If` or `Switch`. |
| Message Transformation | Transform between JSON, XML, EDI, and other formats with explicit schemas and maps. |
| Scatter-Gather | Distribute independent work in parallel and aggregate results after all branches finish. |
| Protocol Bridging | Connect systems with different protocols such as REST, SOAP, FTP, and B2B transports. |
| Claim Check | Store large payloads externally in blob storage or databases and move references through the workflow. |
| Saga Pattern | Manage distributed transactions with compensating actions for failures. |
| Choreography Pattern | Coordinate multiple services without creating an unnecessary central orchestrator. |
| Asynchronous Processing Pattern | Name long-running HTTP steps clearly, for example `LongRunningAction`, and use callbacks, durable status, and retries for operations such as `https://api.example.com/longrunning`. |
| Webhook Pattern | Name callback subscription steps clearly, for example `WebhookAction`, and use `ApiConnectionWebhook` with subscription paths such as `/subscribe/topics/@{encodeURIComponent('mytopic')}/subscriptions/@{encodeURIComponent('mysubscription')}` for callback-based processing. |
| B2B Message Exchange | Exchange EDI documents between trading partners with AS2, X12, and EDIFACT. |
| Integration Account | Store B2B artifacts such as agreements, schemas, and maps. |
| Rules Engine | Use the Azure Logic Apps Rules Engine for complex business rules. |
| Message Validation | Validate messages against schemas for compliance and data integrity. |
| Transaction Processing | Use compensating transactions and rollback semantics for business transaction failure paths. |

For API integration workflows, validate inputs, retrieve secrets, call external systems, parse responses, branch by request type, log success, and return a deterministic result. Preserve clear action names and telemetry fields such as `Validate_Input`, `Get_API_Key`, `Get_Customer_Data`, `Parse_Customer_Response`, `Prepare_Profile_Response`, `Calculate_Order_Statistics`, `Prepare_Order_Response`, `Set_Default_Response`, `Log_Successful_Request`, `Return_Validation_Error`, `Return_Success_Response`, `ApiRequestSuccess`, `RequestType`, and `ProcessingTime`.

```json
{
  "type": "Http",
  "inputs": {
    "method": "GET",
    "uri": "https://api.example.com/customers/@{triggerBody()?['customerId']}",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "******'Get_API_Key')?['value']}"
    }
  }
}
```

For order-processing examples, keep event fields and business fields explicit: `eventId`, `eventType`, `eventTime`, `dataVersion`, `data`, `orderId`, `orderDate`, `customerId`, `customerName`, `email`, `status`, `createdDate`, `orders`, `items`, `productId`, `quantity`, `unitPrice`, `availableStock`, `requestedQuantity`, `reason`, `Insufficient stock`, `InsufficientStock`, `processedTime`, `LockToken`, `SessionId`, `Importance`, `IsHtml`, and `Normal`.

## Monitoring, Observability, and Operations

Make workflows observable from the first production run.

- Configure diagnostic settings to capture workflow runs and metrics.
- Add tracking IDs and correlation IDs to correlate related workflow runs across systems.
- Implement comprehensive logging with appropriate detail levels and masked sensitive data.
- Set alerts for workflow failures, performance degradation, SLA breaches, dead-letter growth, and business KPI failures.
- Use Application Insights and Log Analytics for end-to-end tracing and operational analysis.
- Create dedicated health check workflows, heartbeat patterns, periodic check-ins, and dead letter handling workflows for operational monitoring.
- Track business metrics such as order processing times, approval rates, transaction IDs, and SLA compliance.
- Route alerts by business impact through email, SMS, or Teams and group related alerts to prevent alert fatigue.
- Use stable `LogType` values such as `ConnectionError` and `OrderProcessingError` for failure categories so dashboards and alerts can filter errors without parsing free-form messages.

```json
"Monitor_Transaction_SLA": {
  "type": "Scope",
  "actions": {
    "Calculate_Processing_Time": {
      "type": "Compose",
      "inputs": "@{div(sub(ticks(utcNow()), ticks(triggerBody()?['startTime'])), 10000000)}"
    },
    "Check_SLA_Breach": {
      "type": "If",
      "expression": "@greater(outputs('Calculate_Processing_Time'), parameters('slaThresholdSeconds'))",
      "actions": {
        "Log_SLA_Breach": {
          "type": "ApiConnection",
          "inputs": {
            "host": { "connection": { "name": "@parameters('$connections')['loganalytics']['connectionId']" } },
            "method": "post",
            "body": {
              "LogType": "SLABreach",
              "TransactionId": "@{triggerBody()?['transactionId']}",
              "ProcessingTimeSeconds": "@{outputs('Calculate_Processing_Time')}",
              "SLAThresholdSeconds": "@{parameters('slaThresholdSeconds')}",
              "BreachSeverity": "@if(greater(outputs('Calculate_Processing_Time'), mul(parameters('slaThresholdSeconds'), 2)), 'Critical', 'Warning')"
            }
          }
        },
        "Send_SLA_Alert": {
          "type": "ApiConnection",
          "inputs": {
            "host": { "connection": { "name": "@parameters('$connections')['teams']['connectionId']" } },
            "method": "post",
            "body": {
              "notificationTitle": "SLA Breach Alert",
              "message": "Transaction @{triggerBody()?['transactionId']} exceeded SLA by @{sub(outputs('Calculate_Processing_Time'), parameters('slaThresholdSeconds'))} seconds",
              "channelId": "@{if(greater(outputs('Calculate_Processing_Time'), mul(parameters('slaThresholdSeconds'), 2)), parameters('criticalAlertChannelId'), parameters('warningAlertChannelId'))}"
            }
          }
        }
      }
    }
  }
}
```

Cost metrics should record `WorkflowCostMetrics`, `WorkflowName`, `ExecutionId`, `ActionCount`, `TriggerType`, `DataProcessedBytes`, `ExecutionDurationSeconds`, `Timestamp`, `workflow().name`, `workflow().run.id`, `workflow().run.actions`, `workflow().triggers[0].kind`, `workflow().run.transferred`, and `workflow().run.duration` when the telemetry source provides those values.

## Performance and Cost Governance

Optimize for fewer reliable actions, bounded payloads, controlled concurrency, and predictable licensing.

| Area | Convention |
| --- | --- |
| Trigger optimization | Use batching in triggers to process multiple items in a single run, use webhook-based triggers where possible, and avoid over-polling recurrence schedules. |
| Action optimization | Reduce action count by combining related operations, using built-in functions instead of custom actions, and batching when connector APIs support it. |
| Data transfer | Minimize payload sizes in HTTP requests and responses; use local file operations or external blob storage for large payloads; apply data compression where supported. |
| Consumption Logic Apps | Watch execution count, trigger frequency, connector calls, action count, and data transfer. |
| Standard Logic Apps | Right-size App Service Plans, implement auto-scaling, consider reserved instances for predictable workloads, and consolidate compatible workflows in shared App Service Plans. |
| Shared resources | Use shared connections and integration resources without creating hidden coupling or violating least privilege. |
| Power Automate | Choose license types based on workflow complexity, premium connector use, user assignment, API call reduction, caching, batch processing, and trigger frequency. |
| Designer health | Limit workflows to 50 actions or less, avoid deep nesting of scopes and actions, and split workflow templates when complexity grows. |

Use deployment slots for mission-critical Logic Apps that require zero-downtime deployments, and keep post-deployment validation tests in the release pipeline.

## DevOps, Source Control, and ALM

Treat Logic Apps and Power Automate assets as versioned deployment artifacts.

- Store Logic App definitions in source control such as Git, Azure DevOps, or GitHub.
- Use ARM templates, Bicep, or supported deployment artifacts for multiple environments; the original examples use ARM templates.
- Use Azure DevOps pipelines or GitHub Actions for automated deployment.
- Implement branching strategies appropriate for release cadence.
- Version Logic Apps using tags, version properties, URI path versioning, parameter versioning, or side-by-side versioning.
- Include post-deployment validation tests in CI/CD.
- Use Power Platform Solutions for Power Automate ALM where flows belong to the Power Platform ecosystem.
- Reuse workflow templates for standard patterns across the organization.
- Label Azure DevOps examples as `YAML` when documentation distinguishes them from JSON workflow definitions.

```yaml
trigger:
  branches:
    include:
    - main
    - release/*

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: AzureResourceManagerTemplateDeployment@3
  inputs:
    deploymentScope: 'Resource Group'
    azureResourceManagerConnection: 'Your-Azure-Connection'
    subscriptionId: '$(subscriptionId)'
    action: 'Create Or Update Resource Group'
    resourceGroupName: '$(resourceGroupName)'
    location: '$(location)'
    templateLocation: 'Linked artifact'
    csmFile: '$(System.DefaultWorkingDirectory)/arm-templates/logicapp-template.json'
    csmParametersFile: '$(System.DefaultWorkingDirectory)/arm-templates/logicapp-parameters-$(Environment).json'
    deploymentMode: 'Incremental'
```

For ARM versioning, maintain `workflowDefinitionMap`, `v1Definition`, `v2Definition`, `v3Definition`, `fullLogicAppName`, and `allowedValues` such as `v1`, `v2`, and `v3`. Use `Microsoft.Logic/workflows`, `apiVersion` `2019-05-01`, `resourceGroup().location`, and `parameters('logicAppName')` consistently in ARM templates. For deployment schemas, preserve `https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#`.

```json
"Check_Request_Version": {
  "type": "Switch",
  "expression": "@triggerBody()?['apiVersion']",
  "cases": {
    "1.0": { "actions": { "Process_V1_Format": { "type": "Scope", "actions": {} } } },
    "2.0": { "actions": { "Process_V2_Format": { "type": "Scope", "actions": {} } } }
  },
  "default": {
    "actions": {
      "Return_Version_Error": {
        "type": "Response",
        "kind": "Http",
        "inputs": { "statusCode": 400, "body": { "error": "Unsupported API version", "supportedVersions": ["1.0", "2.0"] } }
      }
    }
  }
}
```

## Cross-Platform Compatibility and Migration

Plan platform movement before relying on connector or licensing behavior that exists only in one product.

- Export/Import compatibility is not guaranteed: flows can be exported from Power Automate and imported into Logic Apps, but modifications may be required.
- Some connectors exist in one platform but not the other; perform connector mapping and identify gaps before migration.
- Power Automate environments provide isolation and may have different policies.
- Use Azure DevOps for Logic Apps ALM and Solutions for Power Automate ALM unless the organization defines a different standard.
- Migration assessments should evaluate complexity, suitability, connector mapping, testing strategy, parallel testing before cutover, and documentation of configuration changes.

```json
{
  "SolutionName": "MyEnterpriseFlows",
  "Version": "1.0.0",
  "Flows": [
    {
      "Name": "OrderProcessingFlow",
      "Type": "Microsoft.Flow/flows",
      "Properties": {
        "DisplayName": "Order Processing Flow",
        "DefinitionData": {
          "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
          "triggers": {
            "When_a_new_order_is_created": {
              "type": "ApiConnectionWebhook",
              "inputs": {
                "host": {
                  "connectionName": "shared_commondataserviceforapps",
                  "operationId": "SubscribeWebhookTrigger",
                  "apiId": "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps"
                }
              }
            }
          },
          "actions": {}
        }
      }
    }
  ]
}
```

## Good / Bad Examples

The examples below illustrate a resilient API-style Logic App convention: validate input, use Key Vault, call the API with explicit content type, parse the response, branch on request type, log, and return a typed response. The bad example hardcodes secrets, skips validation, omits `runAfter`, and gives operators no failure path.

**Good:**

```json
{
  "actions": {
    "Validate_Input": {
      "type": "If",
      "expression": {
        "and": [
          { "not": { "equals": ["@triggerBody()?['customerId']", null] } },
          { "not": { "equals": ["@triggerBody()?['requestType']", null] } }
        ]
      },
      "actions": {
        "Get_API_Key": {
          "type": "ApiConnection",
          "inputs": {
            "host": { "connection": { "name": "@parameters('$connections')['keyvault']['connectionId']" } },
            "method": "get",
            "path": "/secrets/@{encodeURIComponent('apiKey')}/value"
          }
        },
        "Get_Customer_Data": {
          "type": "Http",
          "inputs": {
            "method": "GET",
            "uri": "https://api.example.com/customers/@{triggerBody()?['customerId']}",
            "headers": { "Content-Type": "application/json", "Authorization": "******'Get_API_Key')?['value']}" }
          },
          "runAfter": { "Get_API_Key": ["Succeeded"] }
        },
        "Parse_Customer_Response": {
          "type": "ParseJson",
          "inputs": {
            "content": "@body('Get_Customer_Data')",
            "schema": {
              "type": "object",
              "properties": {
                "id": { "type": "string" },
                "name": { "type": "string" },
                "email": { "type": "string" },
                "status": { "type": "string" },
                "createdDate": { "type": "string" },
                "orders": { "type": "array", "items": { "type": "object", "properties": { "orderId": { "type": "string" }, "orderDate": { "type": "string" }, "amount": { "type": "number" } } } }
              }
            }
          },
          "runAfter": { "Get_Customer_Data": ["Succeeded"] }
        }
      },
      "else": {
        "actions": {
          "Return_Validation_Error": {
            "type": "Response",
            "kind": "Http",
            "inputs": { "statusCode": 400, "body": { "error": "Invalid request", "message": "Request must include customerId and requestType", "timestamp": "@utcNow()" } }
          }
        }
      }
    }
  }
}
```

Why: The workflow validates input, resolves secrets at runtime, uses explicit dependencies, parses structured data, and returns a clear error response.

**Bad:**

```json
{
  "actions": {
    "CallApi": {
      "type": "Http",
      "inputs": {
        "method": "GET",
        "uri": "https://api.example.com/orders",
        "headers": { "Authorization": "hardcoded-secret" }
      }
    },
    "Return": {
      "type": "Response",
      "inputs": { "statusCode": 200, "body": "@body('CallApi')" }
    }
  }
}
```

Why: The workflow hardcodes a credential, has no validation, no schema, no retry policy, no failure branch, and no observable action names for support.

## Deployment and Connection Literals

Preserve provider paths and placeholder names exactly when converting examples into deployable ARM or connection-parameter artifacts.

```json
{
  "parameters": {
    "$connections": {
      "value": {
        "keyvault": {
          "connectionId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Web/connections/keyvault",
          "connectionName": "keyvault",
          "id": "/subscriptions/{subscription-id}/providers/Microsoft.Web/locations/{location}/managedApis/keyvault"
        },
        "servicebus": {
          "connectionId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Web/connections/servicebus",
          "connectionName": "servicebus",
          "id": "/subscriptions/{subscription-id}/providers/Microsoft.Web/locations/{location}/managedApis/servicebus"
        },
        "office365": {
          "connectionId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Web/connections/office365",
          "connectionName": "office365",
          "id": "/subscriptions/{subscription-id}/providers/Microsoft.Web/locations/{location}/managedApis/office365"
        },
        "applicationinsights": {
          "connectionId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Web/connections/applicationinsights",
          "connectionName": "applicationinsights",
          "id": "/subscriptions/{subscription-id}/providers/Microsoft.Web/locations/{location}/managedApis/applicationinsights"
        }
      }
    }
  }
}
```

Use this file for high-quality, cloud-based Apps/Power workflow definitions; keep multi-layered exception handling in named scopes instead of hiding it in a single opaque action. Treat HTTP requests/responses and connector requests/responses as separate contracts so API response shape does not drift from connector payload shape.

## Conventions

| Rule | Rationale |
|---|---|
| Keep the WDL envelope explicit with `definition`, `$schema`, `actions`, `triggers`, `parameters`, `outputs`, `staticResults`, and `contentVersion` | Tools, designers, and deployment pipelines depend on predictable workflow shape |
| Choose Logic Apps, Power Automate, Consumption, Standard, or ISE based on ownership, operations, networking, performance, and licensing needs | Platform mismatch creates avoidable cost, missing connectors, and operational gaps |
| Use Request, Recurrence, event-based, and webhook triggers according to integration semantics | Trigger choice controls latency, cost, reliability, and API behavior |
| Name actions descriptively and group complex paths with scopes | Run history, diagnostics, and support alerts become understandable |
| Parameterize environment values and use variables only for run-local temporary state | Definitions stay portable across environments without hiding mutable state |
| Keep expressions concise, safe, and schema-backed | Complex inline expressions are hard to debug and unsafe payload access fails at runtime |
| Use `runAfter`, retry policies, timeouts, fallback paths, and dead-letter handling | Transient and terminal failures are handled deliberately instead of becoming stuck runs |
| Use managed identities, Key Vault, least privilege, RBAC, IP restrictions, private networking, and masked logs | Workflow definitions often connect privileged systems and can leak sensitive data |
| Configure diagnostics, tracking IDs, Application Insights, Log Analytics, business metrics, and alerts | Operators need correlated evidence for failures, SLA breaches, and process health |
| Limit action count, avoid deep nesting, batch where possible, and control concurrency | Performance, designer usability, connector throttling, and execution cost stay bounded |
| Store definitions in source control and deploy through CI/CD with environment parameter files | Production changes remain reviewable, repeatable, and auditable |
| Version APIs and workflows with URI path, parameters, or side-by-side deployments | Consumers can migrate safely without breaking existing integrations |
| Use Integration Account, EDI, AS2, X12, EDIFACT, and Rules Engine features for B2B scenarios | Enterprise integration artifacts require platform support beyond ad hoc JSON transforms |

## Do / Do Not

| Do | Do not |
|---|---|
| Use the WDL schema `https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#` | Ship workflow JSON without an explicit schema and `contentVersion` |
| Use managed identity and Key Vault for secrets | Hardcode tokens, passwords, connection strings, or API keys in workflow definitions |
| Use `ParseJson` with schemas before accessing nested payloads | Navigate arbitrary payloads without validation or safe access |
| Use `runAfter` branches for `Succeeded`, `Failed`, and `TimedOut` outcomes | Assume the happy path is the only path that will run |
| Use batching, webhooks, and measured concurrency | Over-poll sources or run unbounded parallel loops |
| Use API Management policies for public API frontends | Expose unauthenticated HTTP triggers directly when governance requires an API gateway |
| Store Logic Apps in Git and deploy with ARM, Azure DevOps, or GitHub Actions | Make manual-only portal changes that cannot be reviewed or reproduced |
| Use Solutions for Power Automate ALM | Treat business flows as unowned personal automations |
| Track workflow runs, business metrics, and cost metrics | Operate production workflows without diagnostics or alerts |
| Split workflows that exceed the readability budget | Build deeply nested 50+ action workflows that the designer and reviewers cannot reason about |

## Checklist Before Opening a PR

- [ ] The workflow JSON keeps the WDL `definition`, `$schema`, `actions`, `triggers`, `parameters`, `outputs`, `staticResults`, and `contentVersion` structure.
- [ ] Trigger choice, authentication, pagination, timeout, IP restrictions, and request schema match the integration scenario.
- [ ] Actions have descriptive names, explicit `runAfter` dependencies, and scopes for complex success and failure branches.
- [ ] Environment values, connection IDs, endpoint URLs, queue names, channel IDs, and version values are parameterized.
- [ ] Expressions use safe access, schema validation, and built-in functions without becoming unreadable.
- [ ] External calls have timeout, retry, fallback, and error logging behavior appropriate to the downstream service.
- [ ] Secrets come from Key Vault or managed connections, and logs do not expose sensitive payloads or credentials.
- [ ] Managed identity, least privilege, Azure RBAC, API authentication, CORS or IP restrictions, and private networking are configured where required.
- [ ] Diagnostics, tracking IDs, Application Insights or Log Analytics, alerts, and business metrics cover failure and performance scenarios.
- [ ] Action count, nesting, batching, concurrency, and trigger frequency stay within performance and cost expectations.
- [ ] Source control, CI/CD deployment, environment parameter files, and post-deployment validation are updated with the workflow.
- [ ] Cross-platform connector differences, Power Automate licensing, and migration constraints are documented when a workflow moves between products.
- [ ] API Management policies, versioning, and response contracts are updated when the workflow is exposed as an API.
- [ ] No unrelated edits, leftover placeholders, hardcoded secrets, or unreviewed manual portal changes are included.

## References

- Azure Logic Apps Documentation: https://learn.microsoft.com/en-us/azure/logic-apps/
- Power Automate Documentation: https://learn.microsoft.com/en-us/power-automate/
- Workflow Definition Language Schema: https://learn.microsoft.com/en-us/azure/logic-apps/workflow-definition-language-schema
- Power Automate vs Logic Apps Comparison: https://learn.microsoft.com/en-us/azure/azure-functions/functions-compare-logic-apps-ms-flow-webjobs
- Enterprise Integration Patterns: https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-enterprise-integration-overview
- Logic Apps B2B Documentation: https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-enterprise-integration-b2b
- Azure Logic Apps Limits and Configuration: https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config
- Logic Apps Security Overview: https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-securing-a-logic-app
- API Management and Logic Apps Integration: https://learn.microsoft.com/en-us/azure/api-management/import-logic-app-as-api
- Logic Apps Standard Networking: https://learn.microsoft.com/en-us/azure/logic-apps/single-tenant-overview-compare
- JSON Schema draft-04 used in request-trigger examples: http://json-schema.org/draft-04/schema#
- Example development endpoint preserved from workflow samples: https://api.dev.example.com
- Example customer endpoint using trigger data: https://api.example.com/customers/@{triggerBody()?['customerId']}
- Example customer endpoint using parsed body data: https://api.example.com/customers/@{body('Parse_Message')?['data']?['customerId']}
- Example inventory endpoint: https://api.example.com/inventory/@{items('Validate_Stock')?['productId']}
- Example long-running endpoint: https://api.example.com/longrunning
- Example orders endpoint: https://api.example.com/orders
- Example protected endpoint: https://api.example.com/protected
- Example resource endpoint: https://api.example.com/resource
- Example fallback endpoint: https://fallback-api.example.com/resource
- Microsoft Entra OpenID configuration template: https://login.microsoftonline.com/{tenant-id}/.well-known/openid-configuration
- ARM deployment template schema: https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#
