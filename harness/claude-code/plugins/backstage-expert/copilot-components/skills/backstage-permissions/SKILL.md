---
name: backstage-permissions
description: "Design, implement, test, and troubleshoot Backstage permission policies, basic and resource permissions, conditional decisions, rules, frontend authorization, and plugin integration. Use when implementing RBAC, ABAC, resource filtering, action visibility, or fixing authorization failures."
---

# Backstage permissions

Keep authentication and authorization separate and enforce permissions in backend data access,
not only in the UI.

## When to invoke

- "Add permissions to this Backstage plugin."
- "Write an RBAC or ABAC policy."
- "Implement conditional resource filtering."
- "Hide and deny unauthorized frontend or backend actions."

## Procedure

1. Confirm identity is established and inventory the action or resource being protected.
2. Choose a basic permission when the decision is action-wide, or a resource permission when the
   decision depends on resource attributes.
3. Put shared permission definitions in a common package consumable by backend, frontend, and
   policy code.
4. For resource permissions, define a resource reference, rules, `apply`, and `toQuery`.
5. Keep `apply` and `toQuery` logically equivalent.
6. Register permissions and resource types through the permissions registry.
7. Authenticate the request, authorize with credentials, and apply conditional filters in the
   data layer before loading or returning resources.
8. Add frontend permission checks for experience, but do not rely on them for enforcement.
9. Test allow, deny, conditional, missing resource, unauthenticated, and pagination behavior.
10. Document policy ownership and how adopters can compose exported condition helpers.

## Security criteria

- Backstage endpoints are not automatically protected merely because a sign-in page exists.
- Denied backend access must fail even when the frontend control is bypassed.
- Conditional filtering must occur before pagination so unauthorized resources do not distort
  result counts or leak through.

## Output template

```markdown
## Backstage permission result

| Permission | Type | Resource | Enforcement | Policy test |
| --- | --- | --- | --- | --- |

### Conditions
- Rule:
- `apply` / `toQuery` equivalence:
```

## Quality gate

- [ ] Authentication and authorization are treated separately.
- [ ] Permission definitions live in a reusable package.
- [ ] Backend enforcement cannot be bypassed through the frontend.
- [ ] Resource rules produce equivalent in-memory and query decisions.
- [ ] Conditional filtering and pagination do not leak unauthorized resources.
- [ ] Allow, deny, conditional, and unauthenticated tests pass.

## References

- [Permission framework overview](https://backstage.io/docs/permissions/overview)
- [Plugin author permissions](https://backstage.io/docs/permissions/plugin-authors/01-setup)
