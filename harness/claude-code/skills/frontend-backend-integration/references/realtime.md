# Realtime and message adapter

Detect WebSocket, SSE, AsyncAPI, or custom message contracts plus protocol, channel, operation, message, binding, security, correlation, and version behavior.

Test:

- connect, authenticate, subscribe, initial state, stream, stop, unsubscribe, and close;
- reconnect, backoff, replay, resume token, heartbeat, and offline transition;
- duplicate, delayed, missing, out-of-order, unknown, and malformed events;
- correlation, causation, idempotency, optimistic state, rollback, and stale snapshots;
- partial messages, encoding, binary data, content type, and schema evolution;
- focus, announcements, rendering frequency, and reduced-update behavior.

Do not assume exactly-once delivery or ordering unless the contract guarantees it.
