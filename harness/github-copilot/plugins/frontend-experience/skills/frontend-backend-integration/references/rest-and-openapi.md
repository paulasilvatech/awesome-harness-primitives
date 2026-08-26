# REST and OpenAPI adapter

- Detect the OpenAPI version and compatible validator or generator already used.
- Validate paths, methods, parameters, headers, cookies, content types, encodings, request bodies, responses, error shapes, callbacks, links, security, uploads, and streaming consumed by the frontend.
- Preserve unknown response fields and backward-compatible additions.
- Test removed required fields, enum expansion, nullable values, partial data, numeric precision, and date formats.
- Keep schema validation distinct from Pact or other interaction contracts.
- Resolve external references only through approved roots and protocols; reject path escape and unrestricted network fetching.
- Generate clients only under explicit repository ownership and review generated diffs.

OpenAPI 3.2.0 is an available released specification, not an instruction to upgrade an existing contract.
