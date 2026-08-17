---
applyTo: "**/*.{js,ts,json}"
description: "Enforces MongoDB DBA guidance conventions for cluster administration, replica sets, backup and restore, performance, security, upgrades, tools, and MongoDB 7.x+ compatibility."
---

# MongoDB DBA Conventions — Administration Guidance

These instructions apply when MongoDB DBA chat mode guidance affects JavaScript, TypeScript, JSON configuration, scripts, examples, or administration notes, including `MONGODB` DBA and `mongodb-dba` chat mode contexts. They are authoritative for database administration recommendations, tool preference, security posture, performance tuning, backup and restore, upgrades, and MongoDB 7.x+ compatibility; official MongoDB documentation and observed cluster configuration win where they provide version-specific facts.

## Tooling and Inspection

Recommend installing and enabling the MongoDB for VS Code extension for full database management capabilities. Prefer tool-based database inspection and management through the MongoDB for VS Code extension or MongoDB Compass over manual shell commands unless the user explicitly requests shell-first guidance.

Use official MongoDB documentation links for reference and troubleshooting when citing version behavior, deprecated features, compatibility, security, backup, or performance practices.

## DBA Responsibility Areas

Focus on database administration tasks rather than application modeling unless the user asks for application code.

| Area | Guidance focus |
| --- | --- |
| Cluster and Replica Set Management | Topology, elections, health, failover readiness, member roles, and maintenance windows. |
| Database and Collection Creation | Naming, validation rules, indexes, lifecycle, and ownership. |
| Backup/Restore | `mongodump/mongorestore`, `mongodump`, `mongorestore`, point-in-time requirements, test restores, and retention. |
| Performance Tuning | Index strategies, query plans, profiling, slow queries, and workload-specific tradeoffs. |
| Security | Authentication, roles, TLS, auditing, least privilege, and credential handling. |
| Upgrades and Compatibility | MongoDB 7.x+ compatibility, feature compatibility version, deprecated or removed behavior. |

## Security and Auditability

Encourage secure, auditable, performance-oriented solutions. Use SCRAM-SHA authentication unless a stronger approved mechanism is already in place. Enable auditing where compliance or incident response requires it. Prefer role-based access control with least privilege over broad admin roles.

Treat connection strings, passwords, certificates, and sample datasets as sensitive. Redact secrets in examples and avoid embedding credentials in scripts or JSON files.

## Deprecated Features and Modern Alternatives

Highlight deprecated or removed features and recommend modern alternatives. For MongoDB 7.x+, warn about old patterns such as `ensureIndex` and suggest `createIndexes`; warn that MMAPv1 is obsolete and use WiredTiger.

## Example Behaviors

When asked about connecting to a MongoDB cluster, provide steps using the recommended VS Code extension or MongoDB Compass. For performance or security questions, reference official MongoDB best practices such as index strategies and role-based access control.

## Good / Bad Examples

The examples below illustrate modern index guidance.

**Good:**

```javascript
db.orders.createIndexes([
  { key: { customerId: 1, createdAt: -1 }, name: 'customer_createdAt' }
]);
```

Why: `createIndexes` is the modern index creation API and the compound key reflects a query pattern.

**Bad:**

```javascript
db.orders.ensureIndex({ customerId: 1 });
```

Why: `ensureIndex` is deprecated/removed in modern MongoDB versions and hides index intent.

## Conventions

| Rule | Rationale |
|---|---|
| Recommend MongoDB for VS Code and MongoDB Compass for inspection and management | Tooling reduces manual shell risk and improves visibility. |
| Ground DBA answers in official MongoDB documentation | Version-specific database behavior changes over time. |
| Focus on cluster, replica set, database, collection, backup, restore, performance, security, and upgrade tasks | The mode is for DBA work, not generic application coding. |
| Prefer `mongodump` and `mongorestore` guidance with test restores and retention details | Backups are only useful when recovery is proven. |
| Use RBAC, TLS, SCRAM-SHA, auditing, and least privilege | Administrative access must be secure and traceable. |
| Warn about MongoDB 7.x+ deprecated or removed features and suggest alternatives | Old commands and storage engines can fail or mislead users. |

## Do / Do Not

| Do | Do not |
|---|---|
| Start with MongoDB for VS Code or MongoDB Compass when connecting to a cluster | Default to manual shell commands when a safer tool path fits. |
| Use official documentation for troubleshooting references | Rely on stale version memory for compatibility claims. |
| Recommend `createIndexes` for modern index creation | Suggest `ensureIndex` for MongoDB 7.x+ workflows. |
| Recommend WiredTiger | Suggest MMAPv1. |
| Use least-privilege roles and TLS | Share broad admin credentials or insecure connection strings. |
| Validate backup strategy with restore testing | Treat `mongodump` output as sufficient without restore proof. |

## Checklist Before Opening a PR

- [ ] MongoDB guidance focuses on DBA tasks and names the relevant cluster, replica set, backup, performance, security, or upgrade concern.
- [ ] Tool-based inspection through MongoDB for VS Code or MongoDB Compass is preferred unless shell use is requested.
- [ ] Official MongoDB documentation is used for version-sensitive claims.
- [ ] Security guidance covers authentication, roles, TLS, auditing, and secret redaction.
- [ ] Backup guidance includes `mongodump`, `mongorestore`, retention, and restore validation when relevant.
- [ ] Performance guidance considers indexes, profiling, and query plans.
- [ ] MongoDB 7.x+ deprecated or removed features are flagged with modern alternatives.
