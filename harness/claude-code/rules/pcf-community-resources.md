---
paths:
  - "**/*.{ts,tsx,js,jsx,json,xml,css,html}"
---

<!-- Generated from harness/github-copilot/instructions/pcf-community-resources.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Guides Power Apps Component Framework work toward PCF community resources, gallery discovery, videos, blogs, tools, contribution practices, and support channels.

# PCF Community Resource Conventions — Discovery and Contribution

These instructions apply to Power Apps Component Framework component code, manifests, styles, samples, and documentation. They are authoritative for using PCF community resources, PCF Gallery discovery, community videos, blogs, development tools, contribution hygiene, and support channels; official Microsoft Power Platform, project security, and repository-specific PCF engineering standards win for implementation details.

## PCF Gallery

Use PCF Gallery as the central hub for discovering, sharing, and learning from community Power Apps Component Framework components: https://pcf.gallery.

| Need | PCF Gallery convention |
| --- | --- |
| Discover components | Browse components by category and search for specific functionality. |
| Evaluate reuse | Review demonstrations, screenshots, source code links, installation instructions, component ratings, and reviews. |
| Learn patterns | Study real-world component implementations before designing similar controls. |
| Share work | Submit your own component with clear source code, screenshots, demos, and installation guidance. |
| Avoid duplication | Check the gallery before building a component that may already exist. |

## Community Videos and Blogs

Use community education sources to clarify patterns before inventing local conventions.

| Topic | Recommended community sources |
| --- | --- |
| Getting started | `Getting started with code components with OOB React and Fluent UI` by PowerfulDevs; `Getting Started With Power Apps Component Framework` by April Dunnam. |
| Manifest structure | `Power Apps Component Framework Manifest File Explained` by April Dunnam. |
| React and platform libraries | `Easier Development with React Controls and Platform Libraries` by Scott Durow; `Using React and the Fluent UI in Power Apps Component Framework` by Microsoft. |
| Framework overview | `Understanding the Power Apps Component Framework` and `Deep Dive: Power Apps Component Framework API` by PowerfulDevs. |
| Debugging | `How to Debug Power Apps Component Framework Components` by April Dunnam. |
| Advanced scenarios | `Power Apps Component Framework: Datasets with React and Azure Maps` by Nishant Rana; `How to Upload and Display Images with Power Apps Component Framework` by April Dunnam. |
| Styling and theming | `Using Fluent UI Components in Power Apps Component Framework` by Sancho Harker; `Power Apps Component Framework: Styling and Theming` by Microsoft. |
| End-to-end learning | `Power Apps Component Framework End to End Series` by April Dunnam plus community channels and Microsoft's official documentation. |

Follow community blogs for component development tutorials, best practices and patterns, performance optimization, external service integration, troubleshooting, feature announcements, and real-world use cases. Useful authors include Sancho Harker, Benedikt Bergmann, Andrew Butenko, Nishant Rana, OlivierFlying, Ramakrishnan Raman, Temmy Wahyu Raharjo, Scott Durow, Guido Preite, and Ulrikke Akerbæk.

## Community Tools

| Tool | Use it for | Best fit |
| --- | --- | --- |
| PCF Builder for XrmToolBox | Visual manifest editor, boilerplate generation, resource management, property configuration UI, quick component scaffolding, component testing, and XrmToolBox ecosystem integration. | Rapid prototyping, learning PCF structure, quick component setup, and manifest validation. |
| PCF Builder for VS Code | VS Code extension support, IntelliSense, code completion, command palette integration, manifest schema validation, code snippets, integrated terminal commands, and built-in debugging support. | Developers who prefer Visual Studio Code and a modern streamlined workflow. |

Use these tools to accelerate setup and validation, not to bypass code review, testing, or project standards.

## Community Engagement and Resource Selection

- Contribute components to PCF Gallery, publish source code on GitHub, and write blog posts when implementations teach reusable patterns.
- Learn from others by browsing PCF Gallery, watching community videos, and reading blogs before choosing an approach.
- Get help through Microsoft Learn Q&A forums, Power Apps Community forums, GitHub repository issues and discussions, and Twitter/LinkedIn Power Platform community channels.
- Stay updated by following community bloggers, subscribing to YouTube channels, joining Power Platform user groups, and attending community calls and events.
- Use Microsoft Learn for official documentation and tutorials, Power Platform Community for forums, GitHub for source repositories and samples, Power CAT (Customer Advisory Team) for enterprise guidance and patterns, and user groups for local or virtual meetups.

## Contribution Quality

When sharing PCF work, contribute components and knowledge back to the community, provide feedback, report issues, suggest improvements, answer questions, and help other developers. Include clear documentation, test across target platforms, follow established patterns and naming conventions, and ensure components work before sharing.

To prepare a component for PCF Gallery, create a well-documented component, test across target platforms, prepare screenshots and demos, submit to `pcf.gallery`, include a source code link with GitHub recommended, and provide clear installation instructions.

## Resource Decision Rules

| Situation | Preferred resource |
| --- | --- |
| Just starting | Watch April Dunnam's `Getting Started` video. |
| Need an existing component | Browse PCF Gallery. |
| Learning best practices | Read community blogs. |
| Want quick setup | Use PCF Builder tools. |
| Debugging issues | Watch debugging videos and read troubleshooting blogs. |
| Advanced techniques | Follow Scott Durow and PowerfulDevs content. |

## Good / Bad Examples

The examples below illustrate resource-driven component selection.

**Good:**

```text
Before creating a dataset map control, review PCF Gallery and Nishant Rana's dataset and Azure Maps material, then document why a custom implementation is still needed.
```

Why: The approach checks community prior art and records the implementation rationale.

**Bad:**

```text
Build a custom map control from scratch without checking existing gallery components or community debugging guidance.
```

Why: The approach risks duplicated work and misses known PCF patterns.

## PCF Community Vocabulary

Use the community terms `React/Fluent` and `platform-provided` when discussing OOB React, Fluent UI, React controls, and platform-provided libraries.


## Conventions

| Rule | Rationale |
| --- | --- |
| Check PCF Gallery before building reusable controls | Existing components and implementations can prevent duplicated work |
| Use community videos and blogs to learn concrete PCF patterns | Real-world examples expose manifest, debugging, styling, and API details |
| Use PCF Builder for XrmToolBox or VS Code for scaffolding and validation | Tooling reduces setup mistakes while preserving reviewability |
| Share components with source, screenshots, demos, and installation instructions | Community users need enough context to evaluate and install controls |
| Test thoroughly across target platforms before sharing | Components must work reliably in the environments users will adopt |
| Prefer official Microsoft Learn for authoritative platform behavior | Community guidance should not override official platform contracts |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Browse categories and search PCF Gallery for similar functionality | Assume no community component exists |
| Use GitHub source links and reviews to evaluate quality | Download components without inspecting source or installation guidance |
| Learn debugging from April Dunnam and community troubleshooting posts | Debug PCF issues without using known framework techniques |
| Use established naming conventions and documented patterns | Share undocumented or untested components |
| Ask for help in Microsoft Learn Q&A, Power Apps Community, or GitHub issues | Treat community support channels as a substitute for reproducible bug reports |

## Checklist Before Opening a PR

- [ ] PCF Gallery was checked for comparable components, demos, source links, and installation patterns.
- [ ] Relevant community videos, blogs, or official Microsoft documentation informed any unfamiliar PCF pattern.
- [ ] PCF Builder tooling was used where it improves manifest validation, scaffolding, or debugging.
- [ ] New or changed components include clear documentation, screenshots or demos when applicable, and installation notes.
- [ ] Components were tested across the target platforms before being shared or recommended.
- [ ] Support or contribution guidance points to Microsoft Learn Q&A, Power Apps Community, GitHub issues/discussions, or Power Platform community channels as appropriate.

## References

- PCF Gallery: <https://pcf.gallery>
