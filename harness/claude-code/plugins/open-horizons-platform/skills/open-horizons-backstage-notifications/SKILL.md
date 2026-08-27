---
name: open-horizons-backstage-notifications
description: >-
  Install, configure, emit, process, route, and troubleshoot Backstage notifications and optional
  real-time signals. Use when handling user or group notifications, external emitters, email or
  Slack processors, scaffolder notifications, settings, topics, or delivery failures.
---

<!-- Generated from harness/github-copilot/plugins/open-horizons-platform/skills/open-horizons-backstage-notifications/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Backstage notifications

Deliver user-facing messages through the notifications service, not as inter-process messaging.

## When to invoke

- "Add Backstage notifications and signals."
- "Send a notification from a backend plugin or template."
- "Configure email or Slack delivery."
- "Fix notification preferences or delivery."

## Procedure

1. Confirm Backstage version and frontend mode. Notifications and signals are included by default
   in create-app from Backstage 1.42.0, but navigation and settings may still require app wiring.
2. Install or verify frontend and backend notification packages.
3. Add the notifications page or sidebar item through the target frontend system.
4. Use `notificationService` from `@backstage/plugin-notifications-node` inside backend plugins;
   do not call the REST API from a backend plugin.
5. Use authenticated REST calls only for external services.
6. Choose broadcast or entity recipients and validate catalog entity references.
7. Add signals only when near-real-time push improves the experience.
8. Add processors for decoration or external delivery; keep post-processing failures observable.
9. Configure user and default settings by channel, origin, or topic.
10. For email or Slack, store credentials externally, scope access, and test throttling and routing.
11. Test unread/read/saved behavior, preferences, signals, processor failure, and delivery to users
    or groups.

## Open Horizons integration

- Scope notifications to the Developer IDP or Agent IDP objective and current Horizon stage.
- Preserve Open Horizons Backstage ownership, identity, delivery, and evidence boundaries where applicable.
- Route cross-domain sequencing through `open-horizons-orchestration` (`skill`).

## Output template

```markdown
## Backstage notifications result

| Origin | Recipients | Topic | Processor | Signal | Validation |
| --- | --- | --- | --- | --- | --- |

### External configuration
- `<ENV_NAME>`: <purpose only>
```

## Quality gate

- [ ] Notifications are user-facing, not inter-process messages.
- [ ] Backend plugins use the node service rather than their own REST calls.
- [ ] External emitters authenticate with least privilege.
- [ ] Recipients resolve to catalog users or groups.
- [ ] Processor credentials remain external and failures are observable.
- [ ] Preferences, signals, routing, and delivery are tested.

## References

- [Backstage Notifications](https://backstage.io/docs/notifications/)
- [Notification usage](https://backstage.io/docs/notifications/usage)
- [Notification processors](https://backstage.io/docs/notifications/processors)
