# Data-entry patterns

| Pattern | Use when | Required behavior |
| --- | --- | --- |
| Single form | One coherent submission and manageable error set | Visible labels, grouped fields, summary when complex, preserved input |
| Multi-step flow | Cognitive load or conditional data justifies stages | Progress, saved status, safe back, interruption, resume, final review |
| Inline edit | Fast local correction with clear context | Enter/cancel/save, optimistic or confirmed state, rollback, focus return |
| Search/filter | Results update from user criteria | Submit or debounce policy, URL/share state, clear/reset, no-result state |
| Upload | Files participate in workflow | Limits, type, progress, cancel, retry, scanning/processing, removal |
| Destructive action | Data or access can be lost | Consequence, confirmation proportional to risk, progress, result, undo when feasible |

Use native input types, `autocomplete`, and input modes where they match the data. Explain sensitive requests before collection.
