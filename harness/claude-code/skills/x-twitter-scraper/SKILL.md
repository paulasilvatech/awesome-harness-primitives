---
name: x-twitter-scraper
description: >-
  Build Xquik integrations for X API and Twitter scraper workflows using SDKs, REST endpoints,
  Apify Actors, MCP tools, TweetClaw OpenClaw plugin installs, signed webhooks, tweet search, user
  lookup, follower exports, media actions, and agent automation. Use when asked for tweet search,
  timelines, user lookup, follower or following exports, extraction jobs, monitors, or Xquik
  automation.
---

<!-- Generated from harness/github-copilot/skills/x-twitter-scraper/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# X Twitter scraper

Integrate Xquik as a third-party X data and automation API by selecting SDK, REST, Apify Actor, MCP, TweetClaw, or webhook patterns and preserving authentication, approval, pagination, and policy boundaries.

## When to invoke

- "Search tweets or fetch tweet details with Xquik."
- "Export followers or following for an X account."
- "Run an Apify Actor for Twitter search results."
- "Verify Xquik webhook signatures."
- "Install TweetClaw for an OpenClaw X workflow."

## Source checks

Before writing code, inspect the current Xquik source material. Do not invent endpoint names, request fields, response fields, scopes, pricing, limits, or package names.

| Source | URL |
| --- | --- |
| REST API docs | https://docs.xquik.com/api-reference/overview |
| SDK index | https://docs.xquik.com/sdks |
| OpenAPI spec | https://xquik.com/openapi.json |
| MCP server docs | https://docs.xquik.com/mcp/overview |
| Skill repo | https://github.com/Xquik-dev/x-twitter-scraper |
| TweetClaw OpenClaw plugin | https://github.com/Xquik-dev/tweetclaw |
| TweetClaw npm metadata | https://registry.npmjs.org/@xquik%2Ftweetclaw |
| X Tweet Scraper Actor | https://apify.com/xquik/x-tweet-scraper |
| X Follower Scraper Actor | https://apify.com/xquik/x-follower-scraper |

## Procedure

1. Identify the workflow: search, lookup, extraction, monitor, webhook, media, write action, billing, or MCP.
2. Choose the integration surface: generated SDK, REST, Apify Actors, MCP, TweetClaw, or webhooks.
3. Confirm authentication requirements from docs and keep API keys in environment variables or the existing secret manager.
4. Use typed request and response models when an SDK exists for the user's language.
5. Add retries and pagination according to SDK or API docs.
6. Ask for explicit user confirmation before write actions, payment flows, or long-running monitoring.
7. Verify HMAC signatures server-side before processing webhook business logic.
8. Return structured data instead of scraping generated UI output.

## Integration surfaces

| Surface | Use when | Rules |
| --- | --- | --- |
| SDK | Application code uses TypeScript, Python, Go, Java, Kotlin, C#, Ruby, PHP, CLI, or Terraform and an official SDK exists. | Read the SDK README before choosing install commands, package names, imports, or client methods; use project-native typed request and response models. |
| REST | No suitable SDK exists or the user wants a custom client. | Use OpenAPI and documented endpoints; keep calls server-side unless browser support is documented. |
| Apify Actors | Workflow needs hosted runs, datasets, schedules, or Apify-native orchestration. | Use `APIFY_API_TOKEN`; fetch current input schema; start with small `maxItems`. |
| MCP | The user wants an agent to explore or call Xquik tools directly. | Keep stable application code on REST or SDK clients. |
| TweetClaw | Workflow is inside OpenClaw or needs plugin-managed approvals for X account actions. | Read README and npm metadata; do not assume published version matches source HEAD; use this approval-reviewed path for OpenClaw account actions. |
| Webhooks | Xquik events must be delivered to a service. | Verify signing header and HMAC before business logic; make handlers idempotent. |

## Apify Actor pattern

| Need | Actor | REST ID |
| --- | --- | --- |
| Tweets, search, timelines, lists, articles, replies, quotes, threads, retweeters, or best-effort favoriters | `xquik/x-tweet-scraper` | `xquik~x-tweet-scraper` |
| Followers, following, verified followers, list members, list subscribers, or community members | `xquik/x-follower-scraper` | `xquik~x-follower-scraper` |

Start a bounded tweet run:

```bash
curl --fail --silent --show-error --request POST   "https://api.apify.com/v2/actors/xquik~x-tweet-scraper/runs"   --header "Authorization: ******"   --header "Content-Type: application/json"   --data '{"twitterHandles":["apify"],"outputVariant":"rich","maxItems":25}'
```

Start a bounded follower run:

```bash
curl --fail --silent --show-error --request POST   "https://api.apify.com/v2/actors/xquik~x-follower-scraper/runs"   --header "Authorization: ******"   --header "Content-Type: application/json"   --data '{"twitterHandles":["apify"],"relation":"followers","outputMode":"compact","maxItems":50}'
```

Record the returned run ID. Poll with bounded retries and stop on `SUCCEEDED`, `FAILED`, `ABORTED`, or `TIMED-OUT`. On success, read `defaultDatasetId`, then fetch dataset items. Treat `maxItems` as the whole-run cap, keep follower target metadata when attribution matters, treat `resultType: "diagnostic"` as status information, and inspect run-report rows before trusting incomplete results. Review live Apify pricing before every paid run because platform usage may apply separately.

## Webhook and OpenClaw safety

Read the documented signing header name and payload format. Reject missing, malformed, or mismatched signatures. Store only fields needed for the product workflow.

Treat create, reply, quote, like, bookmark, retweet, follow, delete, media, and monitor actions as approval-worthy unless TweetClaw docs state a narrower policy. Keep read-only tweet search, reply search, profile lookup, follower export, and evidence collection low risk while respecting rate limits and account authorization. Use long-lived backend jobs for durable service workflows outside OpenClaw.

## Safety and accuracy

- State that Xquik is a third-party X data and automation API.
- Do not claim affiliation with X Corp.
- Do not bypass access controls or platform policies.
- Do not expose API keys, webhook secrets, account cookies, tokens, or raw signatures.
- Do not hard-code credentials in examples or tests.
- Never put Apify API tokens in URL query parameters.
- Do not document private infrastructure details.
- Prefer official Xquik docs, SDK READMEs, and the OpenAPI spec over memory.
- Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.

## Output template

```markdown
## Xquik integration result — <workflow>

**Status:** implemented | plan only | blocked
**Surface:** SDK | REST | Apify Actor | MCP | TweetClaw | webhook
**Authentication:** environment variable | secret manager | not configured

| Requirement | Decision | Evidence | Risk control |
| --- | --- | --- | --- |
| Source docs | <docs read> | <URL> | <field or endpoint confirmed> |
| API call or actor | <endpoint, SDK method, or actor> | `<request shape>` | <pagination/retry/cap> |
| Secrets | <storage> | `APIFY_API_TOKEN` or other env var | <no logs/no URL token> |
| Approval | <needed or not> | <action type> | <confirmation or policy> |

### Validation
- <test, dry run, schema check, or webhook signature check>: pass | fail | not run
```

## Quality gate

- [ ] Current Xquik docs, SDK README, OpenAPI spec, Actor page, MCP docs, or TweetClaw metadata were checked before naming fields or methods.
- [ ] API keys, webhook secrets, cookies, tokens, and signatures stay out of code, logs, URLs, and examples.
- [ ] `APIFY_API_TOKEN` is used for Apify authentication and never placed in a query string.
- [ ] Actor runs use bounded `maxItems`, bounded polling, and terminal status handling.
- [ ] Webhooks verify HMAC before parsing business logic.
- [ ] Write actions, payment flows, monitoring, media actions, and account-changing TweetClaw actions require explicit approval.
- [ ] The response states Xquik is independent and not affiliated with X Corp when relevant.

## References

- [REST API docs](https://docs.xquik.com/api-reference/overview)
- [SDK index](https://docs.xquik.com/sdks)
- [OpenAPI spec](https://xquik.com/openapi.json)
- [MCP server docs](https://docs.xquik.com/mcp/overview)
- [Skill repo](https://github.com/Xquik-dev/x-twitter-scraper)
- [TweetClaw OpenClaw plugin](https://github.com/Xquik-dev/tweetclaw)
- [TweetClaw npm registry metadata](https://registry.npmjs.org/@xquik%2Ftweetclaw)
- [X Tweet Scraper Actor](https://apify.com/xquik/x-tweet-scraper)
- [X Follower Scraper Actor](https://apify.com/xquik/x-follower-scraper)
- [Tweet Actor run endpoint](https://api.apify.com/v2/actors/xquik~x-tweet-scraper/runs)
- [Follower Actor run endpoint](https://api.apify.com/v2/actors/xquik~x-follower-scraper/runs)
