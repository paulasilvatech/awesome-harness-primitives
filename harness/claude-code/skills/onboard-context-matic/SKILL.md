---
name: onboard-context-matic
description: >-
  Guided onboarding tour for the context-matic MCP server. Use this skill when the user asks what
  ContextMatic can do, wants a first-time tour, asks to show available APIs, asks how to use the
  context-matic server, or wants live model_search and endpoint_search demonstrations before
  integration.
---

<!-- Generated from harness/github-copilot/skills/onboard-context-matic/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# ContextMatic MCP onboarding

Guide the user through a conversational tour of the `context-matic` MCP server: detect the project language, list available APIs, let the user choose one, explain it with version-aware guidance, demonstrate `model_search` and `endpoint_search`, and finish with concrete follow-up prompts.

## When to invoke

- "What can this MCP do?"
- "Show me the available APIs in context-matic."
- "Onboard me to the context-matic server."
- "How do I use the ContextMatic MCP server?"
- "Give me a tour before integrating an API."

## Conduct rules

- Never narrate the skill structure. Do not say phase names, step numbers, or "as per the skill".
- Announce every tool call before making it with one short sentence explaining what you will look up and why.
- Stop at every interaction point and wait for the user's reply before continuing.
- Keep the tour focused on `fetch_api`, `ask`, `model_search`, and `endpoint_search`; do not turn it into a full integration unless the user explicitly asks.
- All tool calls are read-only. Do not modify the project, install packages, or write files during the tour.

## ContextMatic explanation

Explain that `context-matic` is a live, version-aware grounding layer for SDK integration. General models may know outdated public examples; ContextMatic returns the exact SDK models, endpoints, auth patterns, and runnable samples for the current API version and project language.

| Tool | What it is | Use it when | Output |
| --- | --- | --- | --- |
| `fetch_api` | API catalog lookup by `key` and language. | The user asks "What APIs can I use?" or "Do you have the PayPal SDK?" | A full catalog for the language, or one exact API match. The `key` is machine-readable, such as `paypal`, not the display name "PayPal Server SDK". |
| `ask` | Version-grounded integration Q&A. | The user asks "How do I authenticate?", "Show me the quickstart", or "What's the right way to do X?" | Step-by-step guidance and runnable code samples. |
| `model_search` | SDK model/object definition search. | The user asks "What fields does an Order have?" or "Is this property required?" | Model name, description, typed property list, required/optional markers, and nested types. |
| `endpoint_search` | SDK endpoint/method lookup. | The user asks "Show me how to call createOrder" or "What does getTrack return?" | Method signature, parameter types, response type, and copy-paste-ready sample code. |

## Language detection

Detect the project language before calling `fetch_api`, then reuse the same language for every later call.

| Evidence | Language |
| --- | --- |
| `package.json` plus `.ts` or `.tsx` files | `typescript` |
| `*.csproj` or `*.sln` | `csharp` |
| `requirements.txt`, `pyproject.toml`, or `*.py` | `python` |
| `pom.xml` or `build.gradle` | `java` |
| `go.mod` | `go` |
| `Gemfile` or `*.rb` | `ruby` |
| `composer.json` or `*.php` | `php` |
| No project files found | `typescript` fallback |

## Procedure

1. Open with a plain-language explanation of ContextMatic and the four tools.
2. Detect the project language, then say which language you detected.
3. Call `fetch_api` with `language` set to the detected language and `key` set to `""` to list all APIs.
4. Show every returned API as a numbered list with name and one-sentence description; do not truncate or skip entries.
5. Ask: "Which of these APIs would you like to explore? Just say the name or the number." Wait for the reply.
6. Store the chosen API's `key` from the `fetch_api` response and its display name. If the user picks an unavailable API, say it is not currently available and offer to continue with a listed API.
7. Announce the overview lookup, then call `ask` with the chosen `key`, detected `language`, and query: `Give me a high-level overview of this API: what it does, what the main controllers or modules are, how authentication works, and what the first step to start using it is.`
8. Present the overview conversationally, highlighting use cases, authentication, SDK controllers or namespaces, and package names such as NPM, pip, NuGet, or equivalent package managers.
9. Ask: "Is there a specific part of the [API name] you want to learn how to use — for example, creating an order, searching tracks, or managing subscriptions? Or should I show you the complete integration quickstart?" Wait for the reply.
10. Call `ask` with the user's stated goal, or use `Show me a complete integration quickstart: install the SDK, configure credentials, and make the first API call.` when they ask for the full guide. Present returned code samples exactly in fenced code blocks with the correct language tag.
11. Demonstrate `model_search` with a representative model: for `paypal`, use `Order`; for `spotify`, use `TrackObject`; otherwise choose a representative model from the API overview. Explain exact model name, description, required vs optional properties, and nested references such as `PurchaseUnit[] | undefined`.
12. Demonstrate `endpoint_search` with an explicit argument object: `key`, `query`, and `language`. For `paypal`, use `createOrder`; for `spotify`, use `getTrack`; otherwise choose a representative endpoint from the API overview. Explain method name, parameters, response type, and full returned code sample.
13. Close with a menu of concrete follow-up requests the user can ask next.

## Closing menu

Use these examples as the final menu, adapting only the API name or language when the tour context calls for it.

| Category | Example requests |
| --- | --- |
| Quickstart | `/integrate-context-matic Set up the Spotify TypeScript SDK and fetch my top 5 tracks.`<br>`/integrate-context-matic How do I authenticate with the Twilio API and send an SMS? Give me the full PHP setup including the SDK client and the send call.`<br>`/integrate-context-matic Walk me through initializing the Slack API client in a Python script and posting a message to a channel.` |
| Framework-specific integration | `/integrate-context-matic I'm building a Next.js app. Integrate the Google Maps Places API to search for nearby restaurants and display them on a page. Use the TypeScript SDK.`<br>`/integrate-context-matic I'm using Laravel. Show me how to send a Twilio SMS when a user registers. Include the PHP SDK setup, client initialization, and the controller code.`<br>`/integrate-context-matic I have an ASP.NET Core app. Add Twilio webhook handling so I can receive delivery status callbacks when an SMS is sent.` |
| Chaining tools | `/integrate-context-matic I want to add real-time order shipping notifications to my Next.js store. Use Twilio to send an SMS when the order status changes to "shipped".`<br>`/integrate-context-matic I need to post a Slack message every time a Spotify track changes in my playlist monitoring app. Walk me through integrating both APIs in TypeScript.`<br>`/integrate-context-matic In my ASP.NET Core app, I want to geocode user addresses using Google Maps and cache the results. Look up the geocode endpoint and response model, then generate the C# code including error handling.` |
| Debugging | `/integrate-context-matic My Spotify API call is returning 401. What OAuth flow should I be using and how does the TypeScript SDK handle token refresh automatically?`<br>`/integrate-context-matic My Slack message posts are failing intermittently with rate limit errors. How does the Python SDK expose rate limit information and what's the recommended retry pattern?` |

End with: "That's the tour! Ask me any of the above or just tell me what you want to build — I'll use this server to give you accurate, version-specific guidance."

## Limits

- Do not use this skill to integrate an API end-to-end; use the `integrate-context-matic` skill for implementation.
- Do not claim an API exists unless it appears in the live `fetch_api` response for the detected language.
- Do not summarize away code samples returned by `ask` or `endpoint_search`; preserve them exactly.


## Terminology to preserve

Use these terms naturally when relevant because they are part of the original ContextMatic tour vocabulary: `version-accurate`, `case-sensitive`, `human-readable`, `identifier/key`, `one-line`, `REST`, `Music/podcast`, `NPM/pip/NuGet/etc.`, `[model name]`, `[endpoint name]`, `"typescript"`, and `"python"`.

## Output template

```markdown
## ContextMatic tour result

**Status:** complete | waiting for user | blocked
**Detected language:** `<typescript|csharp|python|java|go|ruby|php>`
**Selected API:** `<API name>` (`<key>`)

### APIs shown
1. `<API name>` — <one-sentence description>

### Demonstrations
- `fetch_api`: listed <count> APIs for `<language>`
- `ask`: explained overview and quickstart/topic guidance
- `model_search`: `<model query>` → `<model name>`
- `endpoint_search`: `<endpoint query>` → `<method name>` / `<response type>`

### Next requests offered
- `<example request>`
```

## Quality gate

- [ ] The project language was detected from workspace evidence or explicitly defaulted to `typescript`.
- [ ] `fetch_api` was called with `key` equal to `""` before API selection.
- [ ] Every API returned by `fetch_api` was shown without truncation.
- [ ] The chosen API `key` came from the live `fetch_api` response.
- [ ] `ask`, `model_search`, and `endpoint_search` used the same `key` and `language`.
- [ ] The user was asked before API selection and before topic/quickstart selection.
- [ ] Every tool call was announced before invocation.
- [ ] Returned code samples were shown exactly in fenced code blocks.
