# Testing & Test Automation Plugin

Comprehensive collection for writing tests, test automation, and test-driven development including unit tests, integration tests, and end-to-end testing strategies.

## Installation

```bash
# Using Copilot CLI
copilot plugin install testing-automation@awesome-copilot
```

## What's Included

### Commands (Slash Commands)

| Command | Description |
|---------|-------------|
| `/testing-automation:ai-prompt-engineering-safety-review` | Review and improve AI prompts for safety, bias, security, privacy, effectiveness, robustness, and testability. |
| `/testing-automation:csharp-nunit` | Design, write, and review NUnit tests for .NET projects, including standard tests, data-driven tests, assertions, setup/teardown, categories, and isolation with mocks. |
| `/testing-automation:java-junit` | Apply JUnit 5 best practices for Java tests, including Maven or Gradle setup, standard and parameterized tests, lifecycle hooks, assertions, Mockito isolation, tags, nested tests, and test commands. |
| `/testing-automation:playwright-automation-fill-in-form` | Automate filling and reviewing a Microsoft Forms response with Playwright MCP. |
| `/testing-automation:playwright-explore-website` | Explore a website with Playwright MCP, identify 3-5 core user flows, capture locators and expected outcomes, close the browser context, and propose test cases. |
| `/testing-automation:playwright-generate-test` | Generate, save, run, and stabilize Playwright TypeScript tests from a user scenario using Playwright MCP exploration evidence. |
| `/testing-automation:webapp-testing` | Toolkit for interacting with and testing local web applications using Playwright. |

### Agents

| Agent | Description |
|-------|-------------|
| `tdd-red` | Guide test-first development by writing failing tests that describe desired behaviour from GitHub issue context before implementation exists. |
| `tdd-green` | Implement minimal code to satisfy GitHub issue requirements and make failing tests pass without over-engineering. |
| `tdd-refactor` | Improve code quality, apply security best practices, and enhance design whilst maintaining green tests and GitHub issue compliance. |
| `playwright-tester` | Testing mode for Playwright tests |

## Source

This plugin is part of [Awesome Copilot](https://github.com/github/awesome-copilot), a community-driven collection of GitHub Copilot extensions.

## License

MIT
