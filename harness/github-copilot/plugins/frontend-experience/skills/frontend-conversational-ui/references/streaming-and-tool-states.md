# Streaming and tool states

## Stream lifecycle

`idle -> sending -> acknowledged -> streaming -> completed`

Alternative transitions may include `stopped`, `failed`, `disconnected`, `reconnecting`, `partial`, and `retried`. Define whether retry creates a new response, resumes, duplicates side effects, or discards partial output.

## Tool lifecycle

`proposed -> approval-required -> approved/denied -> queued -> running -> partial -> completed/failed/cancelled`

Expose:

- tool identity and purpose;
- requested permission and affected data;
- current state and progress when known;
- output provenance and trust boundary;
- cancellation and retry consequences;
- unavailable or policy-blocked behavior.

Do not simulate progress or tool success. Correlate duplicate, delayed, and out-of-order events safely.
