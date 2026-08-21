---
applyTo: '**/*.{graphql,gql,vtl,ts,js,mjs,cjs,json,yml,yaml}'
description: 'Enforces production-grade AWS AppSync Event API handler conventions for APPSYNC_JS runtime restrictions, utilities, modules, data sources, IAM, batching, and observability.'
---

# AWS AppSync Event API Conventions — APPSYNC_JS Handlers

These instructions apply to AWS AppSync Event API handlers, namespace integrations, mapping code, schemas, configuration, and supporting JavaScript or TypeScript. They are authoritative for `onPublish` and `onSubscribe` behavior, `APPSYNC_JS` runtime limits, data source selection, IAM boundaries, batch semantics, and handler observability in matched files; broader AWS account, security, and deployment policies win when they impose stricter controls.

## Event API Contract and Data Sources

Design handlers around channel namespace flow: `onPublish` runs before broadcast, and `onSubscribe` runs on subscription attempts. Keep channel path, channel segments, and payload shape explicit and stable because they are API contracts; prefer additive payload fields and avoid breaking existing subscribers.

| Data source | Use when |
| --- | --- |
| Lambda | Custom compute, transformation, orchestration, and external AWS or service integrations. |
| DynamoDB | Low-latency event/state persistence and key-based reads or writes. |
| RDS (Aurora) | Relational checks, joins, and stronger relational integrity use cases. |
| EventBridge | Routing events into broader event-driven architectures. |
| OpenSearch | Search and analytics over event data. |
| HTTP endpoints | External APIs or AWS service APIs over HTTP. |
| Bedrock | Model inference and AI enrichment in event pipelines. |

Combine multiple data sources only when each hop has a clear reason such as auth, persistence, enrichment, or routing.

## Data Source Setup and IAM

- Create data sources at the Event API level, then attach them as namespace integrations.
- If using a service role, grant only required actions.
- Use a trust policy principal that allows `appsync.amazonaws.com` to assume the role.
- Restrict trust with `aws:SourceAccount` and a specific AppSync API ARN or tightly scoped `aws:SourceArn` pattern when possible.
- Do not reuse broad, cross-service IAM roles for AppSync data source access.
- Enforce least-privilege IAM per data source.

## Runtime Restrictions

The `APPSYNC_JS` runtime is a constrained JavaScript subset, not full Node.js.

| Restriction | Required convention |
| --- | --- |
| Async | Do not use promises, `async/await`, or background async workflows. |
| Control flow | Do not use `try/catch/finally`, `throw`, `while`, C-style `for(;;)`, `continue`, labels, or unsupported unary operators. |
| I/O | Do not rely on network or file system access from runtime code; use AppSync data sources for I/O. |
| Language features | Do not use recursion, pass functions as function arguments, or rely on classes and advanced runtime features outside documented support. |
| Iteration | Prefer `for-of` and `for-in` loops when iteration is needed. |

## Handler Flow and Pipeline State

- For handlers without data source integration, return transformed `ctx.events` directly.
- For handlers with data sources, use object form with `request(ctx)` and `response(ctx)`.
- Use `runtime.earlyReturn(...)` when business logic skips data source invocation and response mapping.
- Use `ctx.info.channel.path`, `ctx.info.channel.segments`, `ctx.info.channelNamespace.name`, and `ctx.info.operation` for routing logic.
- For `onPublish` with data source integration, return the event list to broadcast from `response(ctx)`.
- For `onSubscribe` with data source integration, include `response(ctx)` even when no follow-up mapping is needed.
- Use `ctx.prev.result` as the default handoff between consecutive pipeline functions when the next step depends on the previous output.
- Use `ctx.stash` only for small shared metadata across multiple pipeline stages, such as flags, IDs, or correlation context.
- Do not duplicate large payloads or full previous results into `ctx.stash` when `ctx.prev.result` already carries the needed value.

## Errors, Authorization, and Data Safety

- Do not use `throw` in handlers; use `util.error(...)` and `util.appendError(...)` patterns supported by the runtime.
- For business-level authorization rejection, use the documented unauthorized utility in handler code.
- For publish failures, return explicit runtime errors with safe messages.
- Keep error payloads non-sensitive; never expose secrets, raw stack traces, or internal identifiers.
- Treat `ctx.identity`, headers, and payload fields as untrusted input.
- Add validation before write operations and before forwarding transformed events.
- Never hardcode secrets in handler code.
- For public usage, keep defaults conservative with deny or unauthorized behavior on invalid states.

## Utilities, Modules, and Data Source Requests

Use `util` and official modules from `@aws-appsync/utils` to keep code runtime-safe and declarative.

| Area | APIs and conventions |
| --- | --- |
| Encoding | Use `util.urlEncode`, `util.urlDecode`, `util.base64Encode`, and `util.base64Decode`. |
| Early return | Use `runtime.earlyReturn(obj)` to stop the current handler and skip data source plus response evaluation. |
| DynamoDB import | Use `import * as ddb from '@aws-appsync/utils/dynamodb'`. |
| RDS import | Use `import { ... } from '@aws-appsync/utils/rds'`. |
| DynamoDB helpers | Prefer `get`, `put`, `remove`, `update`, `query`, `scan`, `sync`, `batchGet`, `batchPut`, `batchDelete`, `transactGet`, and `transactWrite` over handwritten request objects where possible. |
| DynamoDB updates | Prefer operation helpers such as increment, append, add, and remove for safe patch-style mutations. |
| DynamoDB access | Model keys and indexes for query-first access; avoid `scan` unless justified. |
| DynamoDB correctness | Use conditions for correctness and optimistic concurrency when needed. |
| HTTP | Return `resourcePath`, `method`, and optional `params` with `headers`, `query`, and `body`; check `ctx.result.statusCode`, `ctx.result.body`, and `ctx.error`. |
| EventBridge | Use `operation: 'PutEvents'` and build deterministic event entries from `ctx.events`. |
| RDS | Prefer SQL helpers and `createPgStatement` or `createMySQLStatement`; do not interpolate unsafe SQL. |
| OpenSearch | Keep request path and params explicit and map only required fields from `ctx.result`. |
| Bedrock | Define `operation` as `InvokeModel` or `Converse` explicitly and include prompt-injection safeguards. |

## Lambda Integration

For Event API Lambda data source requests, use `operation: 'Invoke'`, optional `invocationType: 'RequestResponse' | 'Event'`, and a `payload` shaped explicitly for the Lambda contract.

- Use `RequestResponse` when handler flow depends on Lambda output.
- Use `Event` only for fire-and-forget side effects.
- Validate `ctx.result` in `response(ctx)` and map to the exact outgoing event shape.
- In Event API handlers, Lambda operation support is `Invoke`; do not rely on GraphQL-style `BatchInvoke`.
- When batching with Lambda in Event API flows, send an array payload in one `Invoke` and implement item-level aggregation or partial-failure handling inside Lambda.
- Direct Lambda integrations with `Behavior: DIRECT` may replace handler code when the entire namespace behavior can be centralized in Lambda and APPSYNC_JS request/response mapping is unnecessary.
- In `REQUEST_RESPONSE` mode, `onPublish` Lambda returns `{ events?: OutgoingEvent[], error?: string }`; `onSubscribe` Lambda returns `null` for success or `{ error: string }` for rejection.
- In `EVENT` mode, invocation is asynchronous, AppSync does not wait for a Lambda response, and publish events continue broadcasting as usual.
- If Lambda returns `error` in request/response mode, it is logged when logging is enabled and not sent as a detailed internal error payload.

## Batch Operations

- Prefer batching where the target data source natively supports it and event semantics allow grouping.
- Use DynamoDB `batchGet`, `batchPut`, and `batchDelete` for non-atomic bulk operations.
- Use DynamoDB `transactGet` and `transactWrite` when atomic all-or-nothing behavior is required.
- Validate and cap per-request item counts and chunk large batches deterministically.
- Event API JS handler requests use Lambda `operation: 'Invoke'` with optional `invocationType`; there is no Event API `BatchInvoke` operation in handler request objects.
- For pseudo-batch Lambda patterns, send list payloads to one invoke and return deterministic per-item result structures.
- Keep ordering guarantees explicit; preserve and document ordering keys when downstream consumers depend on order.
- For bursty publish flows, prefer `batchPut` or `batchDelete`, or `transactWrite` when atomicity is required, over many single-item operations.

## Tooling, TypeScript, and Operations

- Use `@aws-appsync/eslint-plugin` with `plugin:@aws-appsync/base` at minimum.
- Use `plugin:@aws-appsync/recommended` when TypeScript tooling is configured.
- Transpile TypeScript to supported JavaScript before deployment because AppSync runtime does not execute TypeScript directly.
- Bundle with externalized `@aws-appsync/utils` imports and source maps for debugging.
- Enable CloudWatch logging for handlers and datasource integration.
- Log structured, low-cardinality fields such as channel namespace/path, operation, and request id.
- Add alarmable signals for handler errors, datasource errors, and latency regression.
- Keep response transformations deterministic and test with multi-event payloads.

## Good / Bad Examples

The examples below illustrate Event API Lambda requests without unsupported batch operations.

**Good:**

```js
export function request(ctx) {
  return {
    operation: 'Invoke',
    invocationType: 'RequestResponse',
    payload: { events: ctx.events }
  };
}
```

Why: The handler uses the supported Event API Lambda operation and sends an explicit list payload for batching semantics.

**Bad:**

```js
export function request(ctx) {
  return { operation: 'BatchInvoke', payload: ctx.events };
}
```

Why: Event API handler request objects do not support GraphQL-style `BatchInvoke`.

## Compatibility Vocabulary

Preserve Event API terminology for `AWS/service`, `HTTP/EventBridge/RDS/OpenSearch/Bedrock`, `Lambda/DynamoDB`, `aggregation/partial-failure`, `deny/unauthorized`, `increment/append/add/remove`, `loop/control`, `low-latency`, `path/params`, `reads/writes.`, `resolver/functions`, `service/API`, `statements/operators`, and `step-by-step` because these names describe runtime and datasource constraints.


## Conventions

| Rule | Rationale |
| --- | --- |
| Treat channel paths and event payloads as stable API contracts | Subscribers break when event shapes change unexpectedly |
| Keep `APPSYNC_JS` handler code within documented runtime restrictions | Unsupported JavaScript constructs fail at deployment or runtime |
| Use AppSync data sources for I/O | Runtime code has no direct network or file system access |
| Use `ctx.prev.result` for adjacent pipeline handoff and `ctx.stash` for small shared metadata | Pipeline state stays clear without duplicating large payloads |
| Use `util.error(...)`, `util.appendError(...)`, and unauthorized utilities instead of `throw` | Error behavior stays compatible with AppSync runtime |
| Prefer official `@aws-appsync/utils` modules for DynamoDB and RDS | Request objects stay declarative and aligned with runtime support |
| Use least-privilege IAM and restricted trust policies | AppSync integrations cannot assume broad roles or access unrelated resources |
| Enable logging and alarmable signals | Handler and datasource failures become observable in production |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Return transformed `ctx.events` directly when no data source is needed | Add a data source hop without a clear auth, persistence, enrichment, or routing reason |
| Use `request(ctx)` and `response(ctx)` for data source integrations | Omit `response(ctx)` from `onSubscribe` integrations |
| Use `runtime.earlyReturn(...)` for deliberate short-circuiting | Simulate control flow with unsupported exceptions |
| Use `operation: 'Invoke'` for Lambda Event API handlers | Use `BatchInvoke` in Event API handler requests |
| Use DynamoDB batch or transaction helpers when semantics allow | Loop over many single-item writes in bursty publish flows |
| Validate untrusted identity, headers, and payload fields | Forward raw event payloads to writes or downstream APIs without checks |
| Transpile TypeScript before deployment | Assume AppSync executes TypeScript directly |

## Checklist Before Opening a PR

- [ ] Handlers use only `APPSYNC_JS`-supported runtime features.
- [ ] No `throw`, async/promise usage, unsupported loops, unsupported control constructs, recursion, or runtime file/network access remain.
- [ ] `onPublish` and `onSubscribe` behavior, channel paths, and payload shapes are explicit and tested.
- [ ] Data sources are attached at namespace level and IAM roles use least privilege with `appsync.amazonaws.com`, `aws:SourceAccount`, and `aws:SourceArn` where possible.
- [ ] Error and authorization flow uses runtime-supported utilities and non-sensitive messages.
- [ ] Data source request/response mapping is deterministic and schema-safe.
- [ ] Lambda and DynamoDB contracts, batching limits, and ordering guarantees are documented and validated.
- [ ] Linting with `@aws-appsync/eslint-plugin` is enabled and TypeScript is transpiled before deployment.
- [ ] CloudWatch logging and alarmable signals cover handler errors, datasource errors, and latency regression.
