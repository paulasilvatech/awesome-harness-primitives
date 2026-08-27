# Async submission

Define:

- when the action becomes pending and whether fields remain editable;
- duplicate-click, Enter-key, navigation, and cancellation behavior;
- progress source and whether it is determinate;
- timeout, abort, retry, backoff, and idempotency behavior from the contract;
- optimistic change, rollback, conflict, and stale-data handling;
- final success confirmation, redirect, focus, announcement, and persisted result;
- uncertain outcomes where the client cannot know whether the server committed.

Never turn a network error into a silent reset. Preserve user work and explain the next safe action.
