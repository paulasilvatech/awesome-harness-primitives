---
name: qdrant-clients-sdk
description: >-
  Select and use official Qdrant client SDKs, REST API, gRPC API, and curated snippet search. Use
  this skill when the user asks for Qdrant API reference, client installation commands, SDK
  language choice, upload point examples, FastEmbed setup, or REST versus gRPC guidance.
allowed-tools: Read, Grep, Glob, Bash
---

<!-- Generated from harness/github-copilot/skills/qdrant-clients-sdk/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Qdrant clients SDK

Use the official Qdrant clients and API references to answer SDK questions, choose an integration path, and fetch curated snippets for concrete operations such as collection creation, vector search, payload filtering, and point upload.

## When to invoke

- "Which Qdrant client should I install for this language?"
- "Show the Qdrant API reference for uploading points."
- "Find a Qdrant snippet for TypeScript vector search."
- "Should I use Qdrant REST or gRPC?"
- "Install the Qdrant Python client with FastEmbed."

## Official clients and installs

| Language | Official SDK | Install command or source |
| --- | --- | --- |
| Python | `qdrant-client` | `pip install qdrant-client[fastembed]` from `https://github.com/qdrant/qdrant-client` |
| JavaScript / TypeScript | `qdrant-js` | `npm install @qdrant/js-client-rest` from `https://github.com/qdrant/qdrant-js` |
| Rust | `rust-client` | `cargo add qdrant-client` from `https://github.com/qdrant/rust-client` |
| Go | `go-client` | `go get github.com/qdrant/go-client` from `https://github.com/qdrant/go-client` |
| .NET | `qdrant-dotnet` | `dotnet add package Qdrant.Client` from `https://github.com/qdrant/qdrant-dotnet` |
| Java | `java-client` | Maven Central artifact `io.qdrant/client` at `https://central.sonatype.com/artifact/io.qdrant/client` and source `https://github.com/qdrant/java-client` |

## API surfaces

| Surface | Use when | Reference |
| --- | --- | --- |
| REST API | You are new to Qdrant, prototyping, debugging with HTTP, or need OpenAPI-generated clients. | OpenAPI Reference `https://api.qdrant.tech/api-reference`; OpenAPI JSON `https://github.com/qdrant/qdrant/blob/master/docs/redoc/master/openapi.json` |
| gRPC API | You need lower overhead, streaming-friendly integrations, or native generated protobuf clients. | gRPC protobuf definitions `https://github.com/qdrant/qdrant/tree/master/lib/api/src/grpc/proto` |
| Curated snippets | You need operation-level examples before writing code. | `https://snippets.qdrant.tech/search?language=python&query=how+to+upload+points` |

## Snippet search workflow

1. Choose one supported snippet language: `python`, `typescript`, `rust`, `java`, `go`, or `csharp`.
2. Convert the user's intent into a concise query such as `how to upload points`, `hybrid search`, or `filter by payload`.
3. Fetch snippets with `curl -X GET "https://snippets.qdrant.tech/search?language=<language>&query=<url-encoded-query>"`.
4. Add `&format=json` only when structured snippet output is required; otherwise keep the default markdown response.
5. Preserve version notes such as `vlatest`, source URLs, idempotency comments, and retry flags from the snippet.

## Point upload reference pattern

When a snippet teaches point upload, preserve these API names and behaviors in generated code or advice:

| Concept | API or value | Rule |
| --- | --- | --- |
| Python client method | `client.upload_points(...)` from `qdrant_client` | Use for uploading multiple vector-embedded points to a collection. |
| Point type | `models.PointStruct` | Include `id`, `payload`, and `vector`. |
| Collection argument | `collection_name="{collection_name}"` | Replace `{collection_name}` with the real collection. |
| Example payload | `payload={"color": "red"}` and `payload={"color": "green"}` | Payloads are metadata for filtering. |
| Example vectors | `vector=[0.9, 0.1, 0.1]` and `vector=[0.1, 0.9, 0.1]` | Use dimensionality that matches the collection schema. |
| Reliability flags | `parallel=4`, `max_retries=3` | Mention when preserving robust indexing behavior. |
| Idempotency | Re-uploading and re-uploading the same `id` overwrites existing points. | If ids are omitted, Qdrant auto-generates UUIDs. |
| Documentation source | `https://qdrant.tech/documentation/manage-data/points/` | Cite when discussing point management. |

## Output template

```markdown
## Qdrant SDK answer

**Status:** ready | needs lookup | blocked
**Language:** `python` | `typescript` | `rust` | `java` | `go` | `csharp` | `rest` | `grpc`
**Recommended surface:** <SDK, REST API, or gRPC API>

| Need | Command, API, or reference | Notes |
| --- | --- | --- |
| Install | `<install command>` | <package/source> |
| Example | `<method or endpoint>` | <snippet source or caveat> |
| Validation | `<command or check>` | <expected result> |
```

## Quality gate

- [ ] The recommended client is one of the officially supported SDKs listed above.
- [ ] Installation commands match the selected language exactly.
- [ ] REST is preferred for first-time or prototype usage unless the user needs gRPC.
- [ ] Snippet searches use only supported languages and URL-encoded queries.
- [ ] API names from snippets, such as `PointStruct`, `upload_points`, `parallel`, and `max_retries`, are preserved when relevant.
- [ ] Absolute Qdrant reference URLs are included when citing API documentation.

## References

- [Qdrant Python client](https://github.com/qdrant/qdrant-client)
- [Qdrant JavaScript/TypeScript client](https://github.com/qdrant/qdrant-js)
- [Qdrant Rust client](https://github.com/qdrant/rust-client)
- [Qdrant Go client](https://github.com/qdrant/go-client)
- [Qdrant .NET client](https://github.com/qdrant/qdrant-dotnet)
- [Qdrant Java client](https://github.com/qdrant/java-client)
- [Qdrant Java Maven Central artifact](https://central.sonatype.com/artifact/io.qdrant/client)
- [Qdrant REST OpenAPI Reference](https://api.qdrant.tech/api-reference)
- [Qdrant OpenAPI JSON](https://github.com/qdrant/qdrant/blob/master/docs/redoc/master/openapi.json)
- [Qdrant gRPC protobuf definitions](https://github.com/qdrant/qdrant/tree/master/lib/api/src/grpc/proto)
- [Qdrant snippet search example](https://snippets.qdrant.tech/search?language=python&query=how+to+upload+points)
- [Qdrant point management](https://qdrant.tech/documentation/manage-data/points/)
