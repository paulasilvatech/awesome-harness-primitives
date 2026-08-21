# Copilot Primitives Catalog

Generated from the current repository contents by `python3 library/scripts/generate_catalog.py`.
Regenerate this file after changing files under `library/agents/`, `library/instructions/`, `library/skills/`, `library/prompts/`, `library/plugins/`, or `library/hooks/`.

## Summary

| Primitive type | Count |
| --- | ---: |
| Agents | 225 |
| Instructions | 194 |
| Skills | 421 |
| VS Code prompts | 48 |
| Plugins | 96 |
| Hooks | 8 |

## Agents

| Agent | Description |
| --- | --- |
| .NET Self-Learning Architect | Senior .NET architect for complex delivery. Use when .NET 6+ or .NET 8+ systems need architecture, implementation strategy, subagent orchestration, validation, lessons, and durabl… |
| .NET Upgrade | Performs evidence-driven .NET framework and SDK upgrades, package compatibility checks, CI updates, and validation. Use when migrating C#/.NET projects to the next stable or LTS v… |
| Accessibility Expert | Guide WCAG 2.1/2.2 accessibility design, implementation, review, and testing. Use when web UI, SPA, form, media, or a11y regression work must be inclusive and verifiable. |
| Accessibility Runtime Tester | Runtime accessibility specialist for keyboard flows, focus management, dialog behavior, form errors, and evidence-backed WCAG validation in the browser. Use when accessibility mus… |
| ADR Generator | Creates comprehensive Architectural Decision Records with structured rationale, consequences, alternatives, and implementation notes. Use when a technical decision must be documen… |
| AEM Front-End Specialist | Expert AEM front-end agent for HTL, Tailwind CSS, ClientLibs, accessibility, and Figma-to-code component workflows. Use when building or reviewing production-ready AEM components. |
| Agent Governance Reviewer | AI agent governance expert that reviews code for safety issues, missing governance controls, and helps implement policy enforcement, trust scoring, and audit trails in agent syste… |
| ai-readiness-reporter | Runs an AgentRC readiness assessment and produces a self-contained static HTML dashboard at reports/index.html. Use when asked to assess, audit, score, report on, or visualize rep… |
| ai-team-dev | AI development team agent for implementing features, fixing bugs, writing tests, improving UX, and preparing pull requests across the repository's actual stack. |
| ai-team-producer | AI team producer agent for planning, scoping, coordinating Dev and optional QA, triaging issues, maintaining context, and preparing or merging pull requests. Never writes applicat… |
| ai-team-qa | Optional AI QA engineer (Ivy). Use when testing behavior, running automated or exploratory checks, filing reproducible bugs, verifying fixes, or providing release confidence for c… |
| Amplitude Experiment Implementation | Amplitude experiment implementation agent for issue-driven feature work, instrumentation, experiment creation, and variant wrapping. Use when deploying product experiments through… |
| API Architect | API architecture agent for designing and generating working client-to-external-service connectivity. Use when an engineer needs layered REST client code with optional resiliency. |
| apify-integration-expert | Expert agent for integrating Apify Actors into codebases. Use when teams need Actor selection, workflow design, JavaScript/TypeScript or Python implementation, testing, and produc… |
| Arch Linux Expert | Arch Linux specialist focused on pacman, rolling-release maintenance, and Arch-centric system administration workflows. |
| arm-migration-agent | Arm Cloud Migration Assistant accelerates moving x86 workloads to Arm infrastructure. It scans the repository for architecture assumptions, portability issues, container base imag… |
| Atlassian Requirements to Jira | Transform requirements documents into structured Jira epics and user stories with duplicate detection, change previews, approval gates, and secure backlog creation. Use when conve… |
| AVM Owner Triage | Triage open GitHub issues across the Azure Verified Modules (AVM) repos an owner maintains. Use when an AVM owner needs a quick or deep backlog split into Copilot-ready and human-… |
| AWS Incident Triage | On-call SRE agent for structured CloudWatch-based incident investigation. Use when alarms, anomalies, or production AWS symptoms need evidence-backed triage. |
| aws-cloud-expert | AWS Cloud Expert provides hands-on guidance for designing, building, deploying, and operating AWS workloads. Use for serverless, containers, databases, networking, IaC, security,… |
| aws-principal-architect | AWS Principal Architect guidance agent for Well-Architected reviews, cloud-native designs, AWS best practices, and enterprise deployment trade-offs. |
| aws-serverless-architect | Provide expert AWS Serverless Architect guidance focusing on event-driven architectures, Lambda, API Gateway, and serverless best practices. |
| Azure AVM Bicep mode | Create, update, or review Azure IaC in Bicep using Azure Verified Modules (AVM). |
| Azure AVM Terraform mode | Create, update, or review Azure IaC in Terraform using Azure Verified Modules (AVM). |
| Azure Logic Apps Expert Mode | Expert guidance for Azure Logic Apps development focusing on workflow design, integration patterns, and JSON-based Workflow Definition Language. |
| Azure Policy Analyzer | Analyze Azure Policy compliance posture (NIST SP 800-53, MCSB, CIS, ISO 27001, PCI DSS, SOC 2), auto-discover scope, and return a structured single-pass risk report with evidence… |
| Azure Principal Architect mode instructions | Provide expert Azure Principal Architect guidance using Azure Well-Architected Framework principles and Microsoft best practices. |
| Azure SaaS Architect mode instructions | Provide Azure SaaS architecture guidance for multitenant applications. Use when B2B, B2C, or hybrid SaaS decisions need Well-Architected SaaS and Microsoft best-practice alignment. |
| Azure Smart City IoT Architect | Design Azure IoT and Smart City architectures with clear platform engineering reasoning, requiring mandatory review of Azure IoT Edge documentation before recommending edge soluti… |
| Azure Terraform IaC Implementation Specialist | Azure Terraform IaC coding specialist. Use to create, validate, and review Terraform for Azure resources from INFRA plans. |
| Azure Terraform Infrastructure Planning | Create deterministic Azure Terraform implementation plans under .terraform-planning-files. Use for Azure IaC planning before implementation. |
| azure-iac-exporter | Export existing Azure resources to Infrastructure as Code templates through Azure Resource Graph, Azure Resource Manager API analysis, data-plane inspection, and IaC generation. U… |
| azure-iac-generator | Generates production-ready Infrastructure as Code in Bicep, ARM, Terraform, or Pulumi. Use when users request infrastructure code, deployment templates, or IaC with Azure-first va… |
| Bicep Planning | Azure Bicep IaC implementation planner. Use when an Azure resource goal needs a deterministic plan under .bicep-planning-files/. |
| Bicep Specialist | Azure Bicep Infrastructure as Code specialist for creating, validating, formatting, and linting Bicep templates. Use when Azure IaC must be implemented in .bicep files. |
| Blueprint Mode | Execute software tasks through Blueprint workflows with strict verification, self-correction, and minimal communication. Use for structured autonomous engineering work. |
| C# Expert | Expert C#/.NET development support for design, implementation, debugging, async, testing, performance, security, and modernization. Use when working on .NET or C# code. |
| C# MCP Server Expert | Expert assistant for developing Model Context Protocol (MCP) servers in C#. Use for SDK design, tools, prompts, resources, testing, and debugging. |
| C#/.NET Janitor | Perform janitorial tasks on C#/.NET code. Use for cleanup, modernization, performance tuning, test coverage, documentation, and tech debt remediation. |
| C++ Expert | Provides expert C++ engineering guidance and implementation using modern C++, architecture, testing, CI/CD, and legacy-code practices. Use for C++ design, refactoring, debugging,… |
| CAST Imaging Impact Analysis Agent | Specialized agent for comprehensive change impact assessment and risk analysis in software systems using CAST Imaging. |
| CAST Imaging Software Discovery Agent | Specialized agent for comprehensive software application discovery and architectural mapping through static code analysis using CAST Imaging. |
| CAST Imaging Structural Quality Advisor Agent | Specialized agent for identifying, analyzing, and providing remediation guidance for code quality issues using CAST Imaging. Use for structural quality, security, Green IT, and IS… |
| Caveman Mode | Terse, low-token responses. Minimal words, no fluff. Full capabilities preserved. Use when: optimize token usage, low-token mode, concise output, caveman mode, reduce verbosity, t… |
| CentOS Linux Expert | CentOS (Stream/Legacy) Linux specialist focused on RHEL-compatible administration, yum/dnf workflows, and enterprise hardening. |
| Clojure Interactive Programming | REPL-first Clojure pair programmer for incremental development, debugging, refactoring, and architectural integrity. Use when Clojure changes must be evaluated before editing file… |
| Cloud and SaaS Outage Triage | Distinguish upstream cloud or SaaS incidents from application failures before changing code, using live official-feed status and incident timelines. |
| Comet Opik | Unified Comet Opik agent for LLM tracing, prompt governance, workspace/project management, metrics investigation, imports/exports, and Opik MCP or CLI diagnostics. |
| Context Architect | Plans and executes multi-file code changes by identifying relevant context, dependencies, risks, and validation paths before editing. |
| Context7-Expert | Documentation-first library and framework expert that uses Context7 and version checks before answering API, syntax, best-practice, migration, or code-generation questions. Use wh… |
| copilot-primitive-architect | Advises on current Copilot primitive architecture, type routing, responsibility boundaries, freshness evidence, and read-only reviews; does not create primitives. |
| Create PRD Chat Mode | Creates comprehensive Product Requirements Documents in Markdown with user stories, acceptance criteria, technical considerations, metrics, and optional GitHub issue creation afte… |
| Critical thinking mode instructions | Challenges assumptions with concise questions and root-cause probing. Use when an engineer needs to think harder before choosing a solution. |
| Custom Agent Foundry | Design and create GitHub Copilot custom agents with scoped tools, frontmatter, handoffs, and clear behavior. Use when a user wants a new or improved agent. |
| Debian Linux Expert | Debian Linux specialist focused on stable system administration, apt-based package management, and Debian policy-aligned practices. |
| Debug Mode Instructions | Debug your application to find and fix a bug. Use for systematic reproduction, root-cause analysis, targeted fixes, verification, and final bug reports. |
| Declarative Agents Architect | Architect Microsoft 365 Copilot declarative agents using schema v1.5, TypeSpec, Agents Toolkit, capability selection, testing, and enterprise deployment best practices. |
| Defender Scout KQL | Generates, validates, optimizes, and explains Microsoft Defender XDR Advanced Hunting KQL. Use for Endpoint, Identity, Office 365, Cloud Apps, alerts, email, and vulnerability que… |
| Delphi Expert | Expert Delphi/Object Pascal development support for VCL, FMX, FireDAC, legacy modernization, debugging, architecture, testing, and production-quality code tasks. Use when Delphi-s… |
| Demonstrate Understanding mode instructions | Validate user understanding of code, design patterns, and implementation details through guided questioning. |
| devils-advocate | Critical challenge agent that stress-tests ideas, proposals, and decisions by raising the strongest objections, risks, assumptions, and edge cases. Use when a plan needs adversari… |
| DevOps Expert | DevOps lifecycle specialist for Plan → Code → Build → Test → Release → Deploy → Operate → Monitor. Use when teams need automation, collaboration, IaC, CI/CD, monitoring, or contin… |
| DevTools Regression Investigator | Browser regression specialist for reproducing broken user flows, collecting console and network evidence, and narrowing likely root causes with Chrome DevTools MCP. |
| DiffblueCover | Expert agent for creating unit tests for java applications using Diffblue Cover. |
| dotnet-fullstack-mentor | Opinionated mentor for .NET full-stack development. Use for career progression from junior to staff levels, Clean Architecture, Aspire, C# internals, and Microsoft ecosystem trade… |
| Doublecheck | Interactive verification agent for AI-generated output. Use when AI output needs claim extraction, source verification, adversarial review, and source-linked risk reporting before… |
| droid | Provides installation guidance, usage examples, and automation patterns for the Droid CLI. Use when developers need secure droid exec usage for CI/CD, non-interactive automation,… |
| Drupal Expert | Expert Drupal development assistant for custom modules, entities, themes, services, configuration, security, performance, testing, and deployment. Use when building or reviewing D… |
| Dynatrace Expert | Dynatrace observability and security agent for incident response, deployment validation, production error triage, performance regression detection, release health checks, DQL assi… |
| elasticsearch-agent | Our expert AI assistant for debugging code (O11y), optimizing vector search (RAG), and remediating security threats using live Elastic data. |
| Electron Code Review Mode Instructions | Review Electron desktop apps with Node.js main process, Angular renderer, and native integration layers. Use when code needs security, async, IPC, RxJS, memory, performance, and n… |
| Ember | An AI partner that helps people discover AI collaboration by working on real problems with warmth, honesty, stories, and direct challenge. Use when someone needs partnership, not… |
| Expert .NET software engineer mode instructions | Provides expert .NET engineering guidance and implementation using modern C#, architecture, testing, performance, security, and DevOps practices. Use for .NET design, refactoring,… |
| Expert Nuxt Developer | Expert Nuxt developer for Nuxt 3, Nitro, server routes, data fetching, rendering modes, migration, testing, and performance. Use when building or refactoring production Nuxt apps. |
| Expert React Frontend Engineer | Expert React 19.2 frontend engineer for modern hooks, Server Components, Actions, TypeScript, accessibility, testing, and performance work. Use when building, reviewing, or modern… |
| Expert Vue.js Frontend Engineer | Expert Vue.js frontend engineer for Vue 3 Composition API, TypeScript, component architecture, Pinia, routing, testing, accessibility, migration, and performance. |
| expert-embedded-c-engineer | Expert embedded C guidance for safety-critical systems -- covers MISRA C:2012/2025 rule compliance, CERT C secure coding, static analysis tooling (Coverity, QAC, PC-lint), and def… |
| Fedora Linux Expert | Fedora (Red Hat family) Linux specialist focused on dnf, SELinux, and modern systemd-based workflows. |
| Frontend Performance Investigator | Runtime web-performance specialist for Core Web Vitals, Lighthouse regressions, layout shifts, long tasks, slow networks, and browser trace diagnosis. |
| gem-browser-tester | E2E browser testing, UI/UX validation, visual regression. Use when task acceptance criteria require browser-flow verification. |
| gem-code-simplifier | Refactoring specialist: removes dead code, reduces complexity, consolidates duplicates. Use as a non-user-invocable agent for behavior-preserving simplification tasks. |
| gem-critic | Challenges assumptions, finds edge cases, spots over-engineering and logic gaps. Use as a non-user-invocable critique agent before planning or implementation. |
| gem-debugger | Root-cause analysis agent for stack trace diagnosis, regression bisection, error reproduction, and structured debugging. Use as a read-only subagent when error context must be dia… |
| gem-designer | Creates or validates UI/UX design specs, DESIGN.md files, themes, tokens, accessibility, and responsive layouts. Use for design-only work. |
| gem-designer-mobile | Designs or validates mobile UI/UX for iOS, Android, and cross-platform apps using HIG, Material 3, safe areas, touch targets, and DESIGN.md. |
| gem-devops | Deploy infrastructure, manage CI/CD, configure containers, and verify operational readiness. Use when a GEM task delegates deployment or DevOps work. |
| gem-documentation-writer | Write and update technical docs, README files, PRDs, diagrams, walkthroughs, and AGENTS.md. Use when a GEM task delegates documentation work. |
| gem-implementer | TDD code implementation for features, bugs, and refactoring. Use when a task_definition requires surgical code changes. |
| gem-implementer-mobile | Mobile implementation agent for React Native, Expo, and Flutter using TDD. Use as a subagent for iOS/Android tasks with acceptance criteria and platform validation. |
| gem-mobile-tester | Mobile E2E testing: Detox, Maestro, iOS/Android simulators. |
| gem-orchestrator | The team lead that routes objectives through gem-team planning, delegated execution, verification, and status reporting. Use when coordinating gem agents across phases. |
| gem-planner | Create DAG-based execution plans, wave schedules, task decomposition, risk analysis, and `plan.yaml`. Use when the GEM orchestrator needs a plan_id-bound plan before implementatio… |
| gem-researcher | Codebase exploration agent for patterns, dependencies, architecture discovery, and bounded evidence collection. Use as a non-implementing subagent when research mode and budget mu… |
| gem-reviewer | Security auditing, code review, OWASP scanning, PRD compliance verification. |
| gem-skill-creator | Extract reusable high-confidence patterns into scoped skill packages. Use when a GEM plan delegates pattern-to-skill documentation work. |
| Gilfoyle Code Review Mode | Code review and analysis with sardonic, technically elitist delivery inspired by Bertram Gilfoyle. Use when the user wants brutal but accurate critique without code edits. |
| GitHub Actions Expert | GitHub Actions specialist focused on secure CI/CD workflows, action pinning, OIDC authentication, permissions least privilege, and supply-chain security. Use to create, review, or… |
| GitHub Actions Node Runtime Upgrade | Upgrade a GitHub Actions JavaScript/TypeScript action to a newer Node runtime version (e.g., node20 to node24) with major version bump, CI updates, and full validation |
| GitHub Actions Windows ARM64 wheel builder | Adds native Windows ARM64 wheel builds and tests to Python package GitHub Actions workflows with the windows-11-arm runner. Use when a package needs win_arm64 wheels without regre… |
| Gitmoji Setup | Sets up gitmoji (https://gitmoji.dev) commit tooling in a repository by auditing hooks and conventions, then installing a safe prefill hook, picker, or commitlint enforcement with… |
| Go MCP Server Development Expert | Expert assistant for building Model Context Protocol (MCP) servers in Go using the official SDK. Use for Go MCP tool, resource, prompt, transport, and testing guidance. |
| High-Level Big Picture Architect (HLBPA) | Creates and reviews high-level architecture documentation focused on major flows, contracts, interfaces, behaviors, failure modes, and Mermaid diagrams. Use for big-picture system… |
| Idea Generator | Brainstorm and develop new application ideas through interactive questioning until ready for specification creation. Use when a user has a vague app idea or wants ideation before… |
| Implementation Plan Generation Mode | Creates deterministic, machine-readable implementation plans for features, refactors, upgrades, architecture, data, infrastructure, design, and process work. Use when humans or AI… |
| interview-prep | Technical interview coach for software engineers. Runs mock interviews, coaches system design, structures behavioral answers using STAR, and researches companies before interviews. |
| Java MCP Expert | Expert assistance for building Model Context Protocol servers in Java using reactive streams, the official MCP Java SDK, and Spring Boot integration. Use when designing, implement… |
| JFrog Security Agent | Dedicated application-security agent for policy-compliant open source vulnerability remediation with JFrog security intelligence. Use when dependency fixes must satisfy JFrog Cura… |
| Kotlin MCP Server Development Expert | Expert Kotlin MCP server assistant for official SDK design, tools, resources, prompts, transports, schemas, coroutines, Gradle, and tests. Use when building MCP servers in Kotlin. |
| KubeStellar Console | Kubernetes operations expert for KubeStellar Console — helps you set up the console, configure kc-agent (MCP server), connect clusters, deploy workloads, and query live Kubernetes… |
| Kusto Assistant | Expert KQL assistant for live Azure Data Explorer analysis via Azure MCP server. Use when users need schema discovery, query construction, execution, and data-backed answers. |
| Laravel Expert Agent | Expert Laravel development assistant specializing in modern Laravel 12+ applications with Eloquent, Artisan, testing, and best practices. Use when building, reviewing, or fixing L… |
| launchdarkly-flag-cleanup | Safely removes obsolete LaunchDarkly feature flags by checking LaunchDarkly state, choosing the forward value, updating code, and preparing PR-ready cleanup notes. Use for feature… |
| Lingo.dev Localization (i18n) Agent | Lingo.dev i18n implementation agent for checklist-driven internationalization in web applications. Use when adding or validating multi-language support. |
| LinkedIn Post Writer | Draft and format compelling LinkedIn posts with Unicode bold/italic styling, visual separators, and engagement-optimized structure. Transforms raw content, technical material, ima… |
| Markdown Accessibility Assistant | Improves existing Markdown accessibility using GitHub best practices. Use when documentation needs descriptive links, alt text review, heading fixes, plain-language suggestions, o… |
| MAUI Expert | Support .NET MAUI cross-platform apps with controls, XAML, handlers, performance, and navigation guidance. Use when building or reviewing MAUI UI and app patterns. |
| MCP M365 Agent Expert | Expert assistant for building MCP-based declarative agents for Microsoft 365 Copilot with Model Context Protocol integration |
| Mentor mode | Guides engineers through features or refactors with Socratic questions, codebase context, and supportive challenge. Use when learning and judgment matter more than direct answers. |
| Meta Agentic Project Scaffold | Finds, copies, and installs relevant awesome-copilot prompts, instructions, and chat modes. Use when scaffolding reusable Copilot workflow assets for an application project. |
| Microsoft Learn Contributor | Microsoft Learn documentation contributor and reviewer. Use when writing, editing, or reviewing Learn articles for Microsoft Writing Style Guide, accessibility, Markdown, metadata… |
| Microsoft Study and Learn | Acts as a Microsoft and Azure tutor using guided discovery, practice, and verified learning resources. Use when the user wants to study rather than receive direct answers. |
| modernization | Human-in-the-loop modernization agent for exhaustive project analysis, feature documentation, architecture recommendations, and migration planning. Use when a repository needs com… |
| Monday Bug Context Fixer | Elite bug-fixing agent that enriches task context from Monday.com platform data. Use when a Monday bug item ID needs full context discovery, root-cause analysis, production-qualit… |
| mongodb-performance-advisor | Analyze MongoDB database performance, query patterns, aggregation pipelines, indexes, logs, and Atlas Performance Advisor output. Use when MongoDB workloads need read-only optimiz… |
| MS-SQL Database Administrator | Manages and troubleshoots Microsoft SQL Server databases with DBA discipline. Use for T-SQL, performance, backup/restore, security, migration, and SQL Server 2025+ compatibility t… |
| neo4j-docker-client-generator | Generates simple Python Neo4j client libraries from GitHub issues using schema introspection, Pydantic models, repositories, pytest, and testcontainers. Use for clean starter clie… |
| Neon Migration Specialist | Safe Postgres migrations with zero-downtime using Neon's branching workflow. Test schema changes in isolated database branches, validate thoroughly, then apply to production—all a… |
| Neon Performance Analyzer | Identify and fix slow Postgres queries using Neon's database branching workflow. Use for execution-plan analysis, isolated optimization tests, and before/after performance metrics. |
| New Relic Incident Response Agent | Correlate New Relic alerts, traces, errors, deployments, and code changes during production incidents. Use when engineers need root cause analysis and safe remediation guidance. |
| Next.js Expert | Expert Next.js 16 developer specializing in App Router, Server Components, Cache Components, Turbopack, React Compiler, React 19.2, TypeScript, routing, caching, performance, and… |
| octopus-release-notes-with-mcp | Generates Octopus Deploy release notes from deployment, release, and commit evidence. Use when a project, environment, and space need markdown release notes. |
| one-shot-feature-issue-planner | Cloud Agent to Turn a single new-feature request into a complete, issue-ready implementation plan without follow-up questions. Use when a feature idea must become a GitHub issue d… |
| OpenAPI to Application Generator | OpenAPI-to-application agent for analyzing OpenAPI 3.0+ specs and generating complete, framework-aligned applications from API contracts. |
| Oracle-to-PostgreSQL Migration Expert | Agent for Oracle-to-PostgreSQL application migrations. Educates users on migration concepts, pitfalls, and best practices; makes code edits and runs commands directly. |
| PagerDuty Incident Responder | Responds to PagerDuty incidents by analyzing incident context, recent code changes, and remediation PR options. Use when a PagerDuty incident ID or affected service needs code-awa… |
| PHP MCP Expert | Expert PHP MCP server developer using the official PHP SDK, attributes, discovery, transports, testing, deployment, and performance patterns. Use when building or debugging PHP MC… |
| Pimcore Expert | Build and review Pimcore CMS, DAM, PIM, and E-Commerce solutions with Symfony conventions. Use when Pimcore data models, documents, assets, APIs, workflows, or performance need ex… |
| Plan Mode - Strategic Planning & Architecture | Strategic planning and architecture assistant focused on thoughtful analysis before implementation. Use when developers need codebase understanding, requirement clarification, ris… |
| Planning mode instructions | Implementation planning agent for new features and refactors. Use when the user needs a Markdown plan without code edits. |
| Platform SRE for Kubernetes | SRE-focused Kubernetes specialist prioritizing reliability, safe rollouts/rollbacks, security defaults, and operational verification for production-grade deployments |
| Playwright Tester Mode | Explores web apps and generates or improves Playwright tests from observed user flows. Use when creating, debugging, or strengthening Playwright coverage. |
| PostgreSQL Database Administrator | PostgreSQL DBA agent for inspecting databases, optimizing SQL, backups, restores, monitoring, and security. Use when work must be performed against a PostgreSQL database rather th… |
| Power BI Data Modeling Expert Mode | Expert Power BI data modeling agent for star schema design, relationship strategy, storage-mode decisions, RLS, and model performance. Use when a Power BI semantic model needs Mic… |
| Power BI DAX Expert Mode | Expert Power BI DAX guidance using Microsoft best practices for performance, readability, and maintainability of DAX formulas and calculations. Use when designing, optimizing, deb… |
| Power BI Performance Expert Mode | Expert Power BI performance optimization guidance for troubleshooting, monitoring, and improving Power BI models, reports, DAX, DirectQuery, capacity, refresh, and query performan… |
| Power BI Visualization Expert Mode | Expert Power BI report design and visualization guidance using Microsoft best practices. Use when report visuals, layout, accessibility, interactions, mobile design, or user exper… |
| Power Platform Expert | Power Platform expert for Code Apps, canvas apps, Dataverse, connectors, ALM, security, and enterprise best practices. Use for implementation guidance and architecture decisions. |
| Power Platform MCP Integration Expert | Design Power Platform custom connectors with MCP integration for Copilot Studio. Use for connector schemas, OAuth, JSON-RPC, and deployment guidance. |
| Principal software engineer | Principal-level software engineering agent for pragmatic implementation, design guidance, technical leadership, quality strategy, and debt management. Use when work needs senior e… |
| Project Architecture Planner | Holistic software architecture planner that evaluates tech stacks, designs scalability roadmaps, performs cloud-agnostic cost analysis, reviews existing codebases, and delivers in… |
| Project Documenter | Generates professional MS Word project documentation with draw.io architecture diagrams and embedded PNG images. Use when any software project needs discovered architecture, stack… |
| Prompt Builder | Expert prompt engineering agent for creating, improving, researching, and validating prompts with Prompt Tester feedback. Use when prompts need structured engineering, source anal… |
| Prompt Engineer | Analyze and improve prompts by treating every user input as a prompt to rewrite. Use when a task needs a detailed system prompt with structured reasoning and output rules. |
| PySpark Expert Agent | Diagnose PySpark performance bottlenecks, distributed execution pitfalls, and suggest Spark-native rewrites and safer distributed patterns (incl. mapInPandas guidance). Use when P… |
| Python MCP Server Expert | Expert assistant for developing Model Context Protocol (MCP) servers in Python. Use for FastMCP, tools, resources, prompts, transports, and testing. |
| Python Notebook Sample Builder | Builds verified Python notebooks that demonstrate Azure and AI features. Use when creating hands-on VS Code notebook samples. |
| QA | Meticulous QA subagent for test planning, bug hunting, edge-case analysis, and implementation verification. Use when software needs risk-based testing or bug reports. |
| quality-playbook | Orchestrates the Quality Playbook skill across exploration, generation, review, audit, reconciliation, verification, and iterations. Use when a codebase needs deep quality enginee… |
| react18-auditor | Deep-scan specialist for React 16/17 class-component codebases targeting React 18.3.1. Finds unsafe lifecycle methods, legacy context, batching vulnerabilities, event delegation a… |
| react18-batching-fixer | React 18 automatic batching regression specialist for class-component codebases. Use when async setState chains, Promises, setTimeout handlers, or native event handlers may rely o… |
| react18-class-surgeon | Class component migration specialist for React 16/17 → 18.3.1. Use when deprecated class lifecycles, legacy context, string refs, findDOMNode, or ReactDOM.render must be migrated… |
| react18-commander | Orchestrates React 16/17 to React 18.3.1 migration for class-component-heavy codebases. Use to coordinate audit, dependency upgrades, class surgery, batching fixes, and test verif… |
| react18-dep-surgeon | Dependency upgrade specialist for React 16/17 to exact React 18.3.1. Use inside React migration pipelines to pin React, upgrade compatible libraries, detect Enzyme blockers, and r… |
| react18-test-guardian | Test suite fixer and verifier for React 16/17 → 18.3.1 migration. Handles RTL v14 async act() changes, automatic batching test regressions, StrictMode double-invoke count updates,… |
| react19-auditor | Audits a React codebase for React 19 breaking changes and deprecated patterns. Use as a read-mostly scanner that writes .github/react19-audit.md for the React 19 commander. |
| react19-commander | Orchestrates complete React 19 migrations through audit, dependency, source, and test specialists with strict gates and memory state. Use to coordinate a zero-incomplete React 18… |
| react19-dep-surgeon | Dependency upgrade specialist that installs React 19, resolves peer dependency conflicts, upgrades Testing Library, Apollo, and Emotion, and returns GO/NO-GO. Use as a subagent of… |
| react19-migrator | Migrates React source files to React 19 APIs from an audit report. Use to rewrite deprecated source patterns while leaving test files untouched. |
| react19-test-guardian | Test suite fixer and verification specialist. Use when react19-commander needs a hidden subagent to migrate all tests to React 19 compatibility and keep fixing until npm test repo… |
| reepl-linkedin | LinkedIn content strategy agent for Reepl-powered post drafting, carousel planning, scheduling guidance, analytics review, and voice-profile alignment. Use when creating or improv… |
| Refine Requirement or Issue | Refines GitHub issues into clear requirements with acceptance criteria, technical considerations, edge cases, NFRs, and estimation notes. Use when an existing issue needs product-… |
| Repo Architect Agent | Bootstraps and validates agentic project structures for GitHub Copilot (VS Code) and OpenCode CLI workflows. Use after `opencode /init`, VS Code Copilot initialization, or migrati… |
| Ruby MCP Expert | Expert Ruby MCP server agent. Use when building, testing, or reviewing Model Context Protocol servers in Ruby with the official MCP Ruby SDK and Rails integration. |
| RUG | Pure orchestration agent that decomposes requests, delegates all work to subagents, validates outcomes, and repeats until complete. |
| Rust MCP Expert | Expert assistant for production Rust MCP server development with rmcp, tokio, typed tools, transports, testing, and deployment. Use when building or debugging Rust MCP servers. |
| Salesforce Apex & Triggers Development | Implement and review bulk-safe Salesforce Apex classes and triggers with PNB tests and security gates. Use for Apex business logic work. |
| Salesforce Expert Agent | Provide expert Salesforce Platform guidance, including Apex Enterprise Patterns, LWC, integration, and Aura-to-LWC migration. Use for secure, scalable Salesforce solutions. |
| Salesforce Flow Development | Implement and review Salesforce Flow automation. Use when declarative automation must be designed, bulk-safe, fault-tolerant, and deployment-ready. |
| Salesforce UI Development (Aura & LWC) | Builds, reviews, troubleshoots, and refactors Salesforce Aura and Lightning Web Components with SLDS, accessibility, Apex, LDS, GraphQL, LMS, and Jest best practices. |
| Salesforce Visualforce Development | Implement and review Visualforce pages and Apex controllers. Use when Visualforce is required and pages must be secure, performant, accessible, and MVC-aligned. |
| sast-sca-security-analyzer | Performs SAST and SCA security analysis. Use when scanning source code, binaries, dependency manifests, license risk, policy compliance, CWE-mapped flaws, CVE exposure, or CI/CD g… |
| Scientific Paper Research | Research agent that searches scientific papers and retrieves structured experimental data from full-text studies using the BGPT MCP server. |
| SE: Architect | Review system architecture with Well-Architected, security, reliability, scalability, cost, and AI concerns. Use before major design commitments. |
| SE: DevOps/CI | DevOps specialist for CI/CD pipelines, deployment debugging, and GitOps workflows. Use when deployments, build failures, branch protections, health checks, monitoring, or rollback… |
| SE: Product Manager | Guides product discovery and GitHub issue creation with user need, business value, metrics, labels, epics, and actionable acceptance criteria. Use for product management decisions. |
| SE: Responsible AI | Reviews and guides AI, accessibility, privacy, and inclusive design decisions. Use when code or features may affect fairness, accessibility, personal data, or automated decisions. |
| SE: Security | Reviews code for OWASP Top 10, OWASP LLM risks, Zero Trust, reliability, and enterprise security readiness. Use for security-focused code review. |
| SE: Tech Writer | Technical writing specialist for creating developer documentation, technical blogs, tutorials, and educational content. Use when complex technical material must become clear, accu… |
| SE: UX Designer | Create Jobs-to-be-Done analysis, user journeys, user flows, and Figma-ready UX research artifacts. Use before UI design when user goals, context, and accessibility requirements ne… |
| Search & AI Optimization Expert | Advises on SEO, Answer Engine Optimization, and Generative Engine Optimization. Use for technical search audits, AI-ready content strategy, schema, migrations, and Core Web Vitals. |
| Senior Cloud Architect | Creates comprehensive architecture documentation and Mermaid diagrams for cloud-native systems, NFRs, deployment, data flow, and phased designs. Use for architecture planning, not… |
| Sensei - Junior Mentor | Guide junior developers with Socratic questions, PEAR learning loops, progressive clues, and recap. Use for teaching-oriented coding help. |
| Shopify Expert | Expert Shopify development assistant for themes, Liquid, Online Store 2.0, apps, APIs, checkout extensions, metafields, performance, and CLI workflows. Use when building or review… |
| Software Engineer Agent | Deliver production-ready software changes through autonomous specification-driven engineering. Use for implementation tasks needing design, validation, and documentation. |
| Specification | Generate or update AI-ready specification documents for new or existing functionality. Use when requirements, constraints, interfaces, and acceptance criteria need a durable spec. |
| stackhawk-security-onboarding | Sets up StackHawk API security testing when a repository exposes a web app or API attack surface. |
| SWE | Senior software engineer subagent for implementation tasks: feature development, debugging, refactoring, and testing. |
| Swift MCP Expert | Expert assistance for building Model Context Protocol servers in Swift. Use when implementing Swift MCP tools, resources, prompts, transports, concurrency, testing, or production… |
| Task Planner Instructions | Task planner for creating actionable implementation plans. Use when a request needs research-verified checklist, details, and implementation prompt files before coding - Brought t… |
| Task Researcher Instructions | Research project context, external references, alternatives, and implementation guidance into `.copilot-tracking/research/`. Use when planning needs verified evidence before imple… |
| TaxCore Technical Writer | A domain-expert technical writer for the TaxCore electronic fiscal invoicing ecosystem. Use this agent to create, improve, or review documentation for TaxCore applications — inclu… |
| TDD Green Phase - Make Tests Pass Quickly | Implement minimal code to satisfy GitHub issue requirements and make failing tests pass without over-engineering. |
| TDD Red Phase - Write Failing Tests First | Guide test-first development by writing one failing test from GitHub issue context before implementation exists. Use for the Red phase of TDD. |
| TDD Refactor Phase - Improve Quality & Security | Improve code quality, apply security best practices, and enhance design while keeping tests green. Use during the TDD refactor phase with GitHub issue acceptance criteria. |
| Technical Debt Remediation Plan | Generate technical debt remediation plans for code, tests, and documentation. |
| Technical spike research mode | Researches and validates technical spike documents through exhaustive investigation, source-backed evidence, and controlled experiments. Use when a spike path is provided. |
| technical-content-evaluator | Elite technical content editor and curriculum architect for evaluating technical training materials, documentation, and educational content. Use when technical content needs evide… |
| terminal-helper | Fast terminal syntax and command helper for PowerShell and Bash |
| Terraform Agent | Terraform infrastructure specialist with automated HCP Terraform workflows. Use when generating, reviewing, testing, or operating Terraform code with registry intelligence, worksp… |
| Terraform IaC Reviewer | Terraform-focused agent that reviews and creates safer IaC changes with emphasis on state safety, least privilege, module patterns, drift detection, and plan/apply discipline. Use… |
| terraform-aws-implement | AWS Terraform Infrastructure as Code coding specialist that creates and reviews Terraform for AWS resources. Use for bounded AWS Terraform implementation with security, reliabilit… |
| terraform-aws-planning | Plans AWS Terraform infrastructure before implementation. Use when an IaC task needs workload classification, WAF alignment, modules, resources, phases, and diagrams. |
| Terratest Module Testing | Generate and refactor Go Terratest suites for Terraform modules, including CI-safe patterns, staged tests, and negative-path validation. |
| Thinking Beast Mode | Autonomous problem-solving agent for complex coding tasks requiring deep investigation, current research, iterative implementation, and rigorous validation. Use when the user need… |
| Trojan Skill Hunter | Audits agent, skill, instruction, hook, MCP, and plugin contributions for hidden prompt injection, unicode steganography, tool poisoning, supply-chain drift, and excessive agency… |
| TypeScript MCP Server Expert | Expert assistant for developing Model Context Protocol (MCP) servers in TypeScript. Use for SDK patterns, transports, tools, resources, prompts, testing, and debugging. |
| Ultimate Transparent Thinking Beast Mode | Autonomous coding agent for transparent, exhaustive problem solving. Use when a task needs persistent planning, implementation, validation, and risk surfacing. |
| Universal Janitor | Perform janitorial tasks on any codebase. Use for cleanup, simplification, unused-code removal, dependency hygiene, and safe tech debt remediation. |
| Universal PR Comment Addresser | PR comment addressing agent for resolving review feedback with focused code changes, tests, commits, and next-comment progression. |
| VS Code Insiders Accessibility Tracker | Tracks and analyzes VS Code Insiders accessibility improvements. Use when investigating released accessibility fixes, issues, and feature history. |
| VSCode Tour Expert | Creates and maintains VS Code CodeTour .tour walkthroughs. Use for onboarding tours, feature tours, schema fixes, and tour drift review. |
| WG Code Alchemist | Refactors code using Clean Code and SOLID principles. Use when transforming code smells into maintainable implementations. |
| WG Code Sentinel | Reviews code and configuration for security vulnerabilities. Use when assessing application security risks and mitigations. |
| WinForms Expert | Support development of .NET (OOP) WinForms Designer compatible Apps. Use when building or fixing WinForms UI, designer code, data binding, async UI, or layout behavior. |
| Workshop TA | Coordinates multi-agent workshops by creating workshops, opening desks, reading journals and bench artifacts, routing work, writing signals, and summarizing room state. Use for wo… |

## Instructions

| Instruction | applyTo | Description |
| --- | --- | --- |
| .NET Framework Upgrade Specialist | **/*.{csproj,vbproj,fsproj,sln,props,targets} | Enforces .NET upgrade conventions for project type detection, target framework selection, dependency sequencing, package updates, breaking changes, validation, CI updates, and PR… |
| a11y | **/*.{html,htm,css,scss,sass,js,jsx,ts,tsx,vue,svelte,astro} | Comprehensive web accessibility conventions based on WCAG 2.2 AA, legal enforcement context, WAI-ARIA rules, anti-patterns, and framework-specific fixes for modern web frameworks. |
| agent-safety | ** | Enforces safety and governance conventions for AI agent systems, tool-calling LLMs, and multi-agent orchestration. Use when code defines agents, tools, policies, guardrails, or au… |
| agent-skills | **/skills/**/SKILL.md | Applies current portable Agent Skill conventions for discovery metadata, progressive disclosure, bundled resources, safety, and validation. Use when creating or updating SKILL.md. |
| agents | **/*.agent.md | Applies current repository conventions for custom-agent metadata, tool scope, body structure, runtime boundaries, and validation. Use when creating or updating an agent. |
| ai-prompt-engineering-safety-best-practices | **/*.{md,txt,prompt,yml,yaml,json} | Enforces prompt engineering, safety, bias mitigation, security, privacy, evaluation, and responsible AI conventions for Copilot and LLM prompt assets. |
| ansible | **/*.yaml,**/*.yml | Enforces Ansible conventions for playbook naming, inventory, idempotency, privilege, secret management, YAML style, and validation. Use when editing Ansible YAML files. |
| apex | **/*.cls,**/*.trigger | Enforces Apex conventions for Salesforce Platform classes and triggers, including bulkification, governor limits, security, testing, asynchronous processing, integrations, and dep… |
| arch-linux | ** | Enforces Arch Linux administration conventions for pacman upgrades, AUR caution, systemd configuration, troubleshooting, security, validation, and rollback guidance. |
| aspnet-rest-apis | **/*.cs,**/*.json | Enforces ASP.NET Core REST API conventions for resource design, controllers, Minimal APIs, data access, authentication, validation, documentation, logging, testing, performance, a… |
| astro | **/*.astro,**/*.ts,**/*.js,**/*.md,**/*.mdx | Enforces Astro 7 conventions for content-driven websites, islands architecture, Content Layer API, TypeScript, routing, actions, sessions, performance, styling, SEO, and images. |
| attester-verify-packages | **/*.{py,js,jsx,ts,tsx,mjs,cjs,json,toml} | Enforces PyPI and npm package and symbol verification with the attester.dev existence oracle before installing, importing, or calling uncertain third-party dependencies. |
| aws-appsync | **/*.{graphql,gql,vtl,ts,js,mjs,cjs,json,yml,yaml} | Enforces production-grade AWS AppSync Event API handler conventions for APPSYNC_JS runtime restrictions, utilities, modules, data sources, IAM, batching, and observability. |
| azure-apim-ai-gateway | **/*.xml,**/policies/**,**/*.bicep | Enforces Azure API Management AI gateway conventions for LLM policies, token controls, managed identity, backend pools, semantic caching, content safety, ordering, and Foundry int… |
| azure-devops-pipelines | **/azure-pipelines.yml,**/azure-pipelines*.yml,**/*.pipeline.yml | Enforces Azure DevOps Pipeline YAML conventions for structure, triggers, variables, security, testing, deployments, templates, caching, and observability. |
| azure-durable-functions-csharp | **/*.cs,**/host.json,**/local.settings.json,**/*.csproj | Enforces Azure Durable Functions C# isolated-worker conventions for deterministic orchestrators, activities, entities, configuration, storage, observability, reliability, and test… |
| azure-functions-csharp | **/*.cs,**/host.json,**/local.settings.json,**/*.csproj | Enforces Azure Functions C# isolated worker conventions for host setup, triggers, bindings, dependency injection, configuration, retries, observability, performance, security, and… |
| azure-functions-typescript | **/*.ts,**/*.js,**/host.json,**/local.settings.json,**/function.json,**/package.json | Conventions for Azure Functions apps in TypeScript and JavaScript, including Node.js async patterns, dependency choices, function layout, and API documentation. |
| azure-iot-edge-architecture | **/*.bicep,**/*.tf,**/*iot*.md,**/*smart-city*.md,**/*edge*.md | Enforces Azure IoT Edge architecture conventions for documentation-grounded edge applicability, runtime constraints, supported systems, operations, security, and assumptions. |
| azure-logic-apps-power-automate | **/*.json,**/*.logicapp.json,**/workflow.json,**/*-definition.json,**/*.flow.json | Enforces Azure Logic Apps and Power Automate workflow conventions for WDL structure, triggers, actions, reliability, security, integration patterns, DevOps, monitoring, and cost g… |
| azure-naming | **/*.bicep,**/*.tf,**/*.tfvars,**/*.bicepparam,**/infra/**,**/infrastructure/** | Enforces Azure CAF resource naming conventions, abbreviations, scope, character rules, and per-resource examples for infrastructure files. |
| azure-verified-modules-bicep | **/*.bicep,**/*.bicepparam | Enforces Azure Verified Modules Bicep discovery, registry references, version pinning, symbolic names, parameters, security, builds, and PR readiness. |
| azure-verified-modules-terraform | **/*.terraform,**/*.tf,**/*.tfvars,**/*.tfstate,**/*.tflint.hcl,**/*.tf.json,**/*.tfvars.json | Enforces Azure Verified Modules Terraform discovery, source naming, version pinning, telemetry, validation, and PR readiness when authoring Terraform IaC. |
| Bicep Code Best Practices | **/*.bicep | Enforces Azure Bicep conventions for naming, parameters, variables, resources, child resources, security, modules, outputs, and documentation. |
| Blazor Conventions | **/*.razor,**/*.razor.cs,**/*.razor.css | Enforces Blazor component conventions for Razor structure, naming, state, validation, performance, caching, API integration, testing, security, and API documentation. |
| caveman-mode | ** | Enforces terse, low-token response conventions while preserving full capability, code quality, and necessary expansion for explanations or architecture decisions. |
| CentOS Administration Conventions | ** | Enforces CentOS administration conventions for RHEL-compatible package management, repositories, systemd services, firewalld, SELinux, validation, and rollback guidance. |
| clojure | **/*.{clj,cljs,cljc,bb,edn.mdx?} | Enforces Clojure and ClojureScript conventions for Calva REPL-first development, structural editing, namespace handling, data shape, rich comment forms, and tests. |
| cmake-vcpkg | **/*.cmake,**/CMakeLists.txt,**/*.cpp,**/*.c,**/*.h,**/*.hpp | Conventions for cross-platform CMake C and C++ projects that use vcpkg manifest mode, CMakePresets.json, policies, and compiler-portable build configuration. |
| code-review-generic | ** | Enforces generic GitHub Copilot code-review conventions for severity, comment format, and cross-cutting checks across reviewable files. |
| codexer | **/*.py | Enforces Codexer Python research and implementation conventions for Python files, dependency hygiene, code quality, testing, security, and research-backed decisions. |
| coldfusion-cfc | **/*.cfc | Enforces ColdFusion CFC conventions for CFScript, component structure, access modifiers, dependency injection, SQL safety, input validation, error handling, documentation, and for… |
| coldfusion-cfm | **/*.cfm | Enforces ColdFusion CFM conventions for CFScript, Application.cfc usage, HTMX targets, cfoutput escaping, SQL safety, includes, validation, errors, and formatting. |
| CommonMark Markdown Conventions | **/*.md | Enforces CommonMark 0.31.2 block, inline, escaping, link, image, and HTML syntax conventions for Markdown files. |
| containerization-docker-best-practices | **/Dockerfile,**/Dockerfile.*,**/*.dockerfile,**/docker-compose*.yml,**/docker-compose*.yaml,**/compose*.yml,**/compose*.yaml | Enforces Dockerfile and Compose conventions for optimized, secure, reproducible container images and container runtime configuration. |
| Context Engineering Conventions | ** | Enforces repository-wide context engineering conventions that make code, structure, naming, and Copilot interactions easier for AI assistance to understand. |
| context7 | ** | Enforces Context7 usage conventions for authoritative, current, version-specific, authoritative/current. external documentation when local workspace context is insufficient. |
| convert-cassandra-to-spring-data-cosmos | **/*.java,**/pom.xml,**/build.gradle,**/application*.properties,**/application*.yml,**/application*.conf | Enforces conventions for converting Spring Boot Cassandra data access to Azure Cosmos DB with Spring Data Cosmos, including dependencies, configuration, repositories, entities, te… |
| convert-jpa-to-spring-data-cosmos | **/*.java,**/pom.xml,**/build.gradle,**/application*.properties | Enforces conventions for converting Spring Boot JPA applications to Azure Cosmos DB with Spring Data Cosmos, including dependencies, configuration, entity mapping, repositories, s… |
| copilot-primitive-authoring | library/agents/*.agent.md,library/instructions/*.instructions.md,library/skills/**/SKILL.md,library/prompts/*.prompt.md,docs/templates/*.md,.github/copilot-instructions.md,.github/agents/*.agent.md,.github/instructions/*.instructions.md,.github/skills/**/SKILL.md,.github/prompts/*.prompt.md | Requires routing, canonical paths, freshness evidence, frontmatter, tool-token, mirror, and validation conventions when editing Copilot primitives. Use when authoring or reviewing… |
| copilot-repository-governance | ** | Applies repository-wide source-of-truth, freshness, synchronization, and validation rules for Copilot primitives. Use for every change in this repository. |
| copilot-thought-logging | ** | Conventions for concise Copilot process tracking when a workspace-visible progress file is explicitly required. |
| cpp-language-service-tools | **/*.cpp,**/*.h,**/*.hpp,**/*.cc,**/*.cxx,**/*.c | Enforces C and C++ language-service tool usage for symbol definitions, references, call hierarchy, parameters, line numbers, fallback search, and recovery. |
| csharp | **/*.cs | Enforces C# application conventions for language features, formatting, nullable reference types, data access, authentication, API documentation, logging, testing, performance, and… |
| csharp-ja | **/*.cs | Enforces Japanese C# and ASP.NET Core application conventions for modern C# 14, formatting, nullable references, EF Core, authentication, validation, OpenAPI, logging, testing, pe… |
| csharp-ko | **/*.cs | C# coding conventions for naming, formatting, language features, performance, exception handling, security, and documentation. |
| csharp-mcp-server | **/*.cs,**/*.csproj | Enforces C# Model Context Protocol server conventions for SDK packages, transports, tool attributes, prompts, sampling, DI, logging, errors, and testing. Use when building MCP ser… |
| csharp-razorpages | **/*.cshtml,**/*.cshtml.cs | Conventions for ASP.NET Core Razor Pages covering PageModels, handlers, model binding, overposting prevention, security, validation, dependency injection, Entity Framework Core, s… |
| dart-n-flutter | **/*.dart | Enforces Dart language style, Effective Dart usage, and Flutter architecture conventions for Dart and Flutter code. |
| dataverse-python | **/*.py | Enforces Python Dataverse SDK conventions for setup, OAuth configuration, client reuse, CRUD operations, batching, pagination, throttling, retries, and logging. |
| dataverse-python-advanced-features | **/*.py | Enforces advanced Python Dataverse SDK conventions for option sets, OData filters, SQL analysis, metadata operations, record batches, relationships, error handling, cache hygiene,… |
| dataverse-python-agentic-workflows | **/*.py | Preview conventions for building agentic Python workflows that use Dataverse as an enterprise data source, including SDK usage, data agents, MCP/A2A patterns, governance, and ML i… |
| dataverse-python-api-reference | **/*.py | Enforces Python Dataverse SDK API usage conventions for DataverseClient methods, DataverseConfig, DataverseError handling, OData options, and metadata operations. |
| dataverse-python-authentication-security | **/*.py | Enforces authentication and security conventions for Python Dataverse SDK apps that use Azure Identity credentials, DataverseClient configuration, secure secret handling, tenant i… |
| dataverse-python-best-practices | **/*.py | Enforces production Python conventions for the PowerPlatform Dataverse SDK, including installation, authentication, client reuse, CRUD operations, metadata, paging, files, OData,… |
| dataverse-python-error-handling | **/*.py | Enforces Python Dataverse SDK error handling, retry, logging, diagnostics, and troubleshooting conventions. |
| dataverse-python-file-operations | **/*.py | Applies PowerPlatform Dataverse Client 1.x conventions for Python file-column uploads, record lifecycle, validation, retries, integrity, and auditability. |
| dataverse-python-modules | **/*.py | Enforces Python Dataverse SDK package, client, configuration, error, metadata, SQL, and file-operation conventions. |
| dataverse-python-pandas-integration | **/*.py | Enforces conventions for integrating the Python Dataverse SDK with pandas DataFrames for analytics, reporting, visualization, and machine-learning workflows. |
| dataverse-python-performance-optimization | **/*.py | Enforces performance conventions for Python Dataverse SDK queries, pagination, batching, client reuse, file uploads, OData and SQL alternatives, memory management, retries, consis… |
| dataverse-python-real-world-usecases | **/*.py | Conventions for real-world Python Dataverse SDK migration, synchronization, data quality, enrichment, reporting, workflow automation, and scheduled jobs. |
| dataverse-python-sdk | **/*.py | Enforces Python Dataverse SDK preview conventions for installation, authentication, CRUD, bulk operations, file upload, paging, and table metadata. Use when writing Python code th… |
| dataverse-python-testing-debugging | **/*.py | Enforces testing and debugging conventions for Python Dataverse SDK code, including mocks, integration tests, coverage, performance checks, and diagnostics. |
| Debian Linux Administration Conventions | ** | Enforces Debian-based Linux administration conventions for apt workflows, package sources, configuration files, services, security, validation, and rollback guidance. |
| declarative-agents-microsoft365 | **/*.json,**/*.ts,**/*.tsp,**/manifest.json,**/agent.json,**/declarative-agent.json | Enforces Microsoft 365 Copilot declarative agent conventions for schema v1.5 manifests, TypeSpec models, capabilities, toolkit workflows, testing, deployment, monitoring, and secu… |
| devbox-image-definition | **/*.yaml,**/*.yml | Enforces Microsoft Dev Box Team Customizations image definition conventions for task discovery, intrinsic task syntax, secrets, context placement, validation, and troubleshooting. |
| devops-core-principles | * | Enforces foundational DevOps conventions for CALMS culture, automation, lean flow, measurement, sharing, and DORA delivery metrics. |
| dotnet-architecture-good-practices | **/*.cs,**/*.csproj,**/Program.cs,**/*.razor | Enforces DDD, SOLID, .NET architecture, testing, financial-domain, security, compliance, and performance conventions for C# and Razor changes. |
| dotnet-framework | **/*.csproj,**/*.cs | Enforces .NET Framework conventions for MSBuild, legacy and SDK-style project files, C# 7.3 compatibility, NuGet boundaries, Windows paths, async, configuration, exceptions, dispo… |
| dotnet-maui | **/*.xaml,**/*.cs | Enforces .NET MAUI conventions for XAML, C# views, ViewModels, lifecycle, navigation, layout, resources, storage, security, performance, and tests. |
| dotnet-maui-9-to-dotnet-maui-10-upgrade | **/*.csproj,**/*.cs,**/*.xaml | Enforces .NET MAUI 9 to .NET MAUI 10 upgrade conventions for target frameworks, package compatibility, breaking API replacements, obsolete controls, deprecated async APIs, media p… |
| dotnet-wpf | **/*.xaml,**/*.cs | Conventions for .NET WPF applications covering MVVM structure, XAML, data binding, commands, responsiveness, performance, and testable ViewModels. |
| draw-io | **/*.drawio,**/*.drawio.svg,**/*.drawio.png | Enforces draw.io and mxGraph XML conventions for diagram structure, styles, layout, naming, validation, and rendering. |
| exclude-prompt-data | ** | Prevents prompt instructions, rationale, meta-commentary, scaffold labels, and local personal data from leaking into generated documentation, comments, or code. |
| fedora-linux | ** | Enforces Fedora administration conventions for dnf package workflows, systemd, firewalld, SELinux, validation, compatibility, and rollback guidance. |
| genaiscript | **/*.genai.* | Conventions for GenAIScript files covering script role, references, TypeScript ESM generation, global APIs, error handling, and maintainability. |
| generate-modern-terraform-code-for-azure | **/*.tf | Conventions for modern Terraform code targeting Azure, including provider choice, modules, variables, outputs, state, idempotency, documentation, validation, and testing. |
| gilfoyle-code-review | ** | Guides sardonic Gilfoyle-style code review comments while preserving technical accuracy, actionable findings, and professional boundaries. |
| GitHub Copilot SDK C# Instructions | **/*.cs,**/*.csproj | Conventions for building C# applications with the GitHub Copilot SDK, including client setup, sessions, permissions, streaming, custom tools, BYOK providers, and error handling. |
| GitHub Copilot SDK Go Instructions | **/*.go,**/go.mod | Enforces Go conventions for applications that use the GitHub Copilot SDK, including client setup, sessions, events, tools, permissions, providers, and cleanup. |
| GitHub Copilot SDK Java Instructions | **/*.java,**/pom.xml,**/build.gradle,**/build.gradle.kts | Enforces Java conventions for applications using the GitHub Copilot SDK, including client setup, virtual threads, sessions, permissions, events, tools, BYOK, MCP servers, and clea… |
| GitHub Copilot SDK Node.js Instructions | **/*.ts,**/*.js,**/package.json | Conventions for building Node.js and TypeScript applications with the GitHub Copilot SDK, including client setup, sessions, permissions, tools, streaming, lifecycle, and error han… |
| GitHub Copilot SDK Python Instructions | **/*.py,**/pyproject.toml,**/setup.py | Enforces Python conventions for GitHub Copilot SDK applications, including async client setup, sessions, permissions, custom tools, streaming, BYOK, and cleanup. |
| github-actions-ci-cd-best-practices | .github/workflows/*.yml,.github/workflows/*.yaml | Enforces GitHub Actions CI/CD conventions for workflow structure, permissions, secrets, OIDC, action pinning, caching, testing, deployments, rollback, and troubleshooting. |
| go | **/*.go,**/go.mod,**/go.sum | Enforces idiomatic Go conventions for package declarations, style, errors, modules, concurrency, HTTP, I/O, tests, security, and documentation. |
| go-mcp-server | **/*.go,**/go.mod,**/go.sum | Enforces Go conventions for building Model Context Protocol servers with github.com/modelcontextprotocol/go-sdk, including tools, resources, prompts, transports, errors, schema ta… |
| hooks | library/hooks/**,.github/hooks/**,hooks/** | Applies current safe hook conventions for Copilot CLI and cloud agent configuration, trust, paths, payloads, scripts, security, packaging, and validation. Use when changing hooks. |
| html-css-style-color-guide | **/*.html,**/*.css,**/*.js | Enforces accessible, professional HTML/CSS color usage conventions for backgrounds, text, accents, gradients, and contrast-sensitive browser styling. |
| instructions | **/*.instructions.md | Enforces structure, frontmatter, examples, altitude, maintenance, and validation conventions for GitHub Copilot custom instruction files. |
| java-11-to-java-17-upgrade | **/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml | Enforces Java 11 to Java 17 upgrade conventions for language features, API migration, build configuration, removals, JVM tuning, and compatibility testing. |
| java-17-to-java-21-upgrade | **/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml | Enforces conventions for upgrading Java projects from JDK 17 to JDK 21, including language features, APIs, build flags, runtime warnings, GC, performance, and testing. |
| java-21-to-java-25-upgrade | **/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml | Enforces conventions for adopting Java 25 from Java 21 across language features, JDK APIs, build flags, deprecations, GC behavior, and validation. |
| java-junit5-assertions | **/*Test.java,**/*IT.java,**/*Steps.java,**/*StepDefs.java | Enforces JUnit Jupiter assertion conventions for imports, expected/actual ordering, lazy messages, grouped assertions, exception checks, timeouts, type safety, and collection comp… |
| java-mcp-server | **/*.java,**/pom.xml,**/build.gradle,**/build.gradle.kts | Best practices and patterns for building Model Context Protocol (MCP) servers in Java using the official MCP Java SDK with reactive streams, transports, Spring integration, valida… |
| Joyride Workspace Automation Conventions | **/.joyride/** | Enforces Joyride workspace automation conventions for REPL-driven ClojureScript, VS Code API usage, workspace activation, data-oriented design, and safe file updates. |
| joyride-user-project | **/*.{cljs,cljc,edn} | Enforces Joyride user script conventions for SCI ClojureScript, REPL-driven VS Code automation, async evaluation, flares, disposables, and file edits. |
| kotlin-mcp-server | **/*.kt,**/*.kts,**/build.gradle.kts,**/settings.gradle.kts | Enforces conventions for building Kotlin Model Context Protocol servers with the official io.modelcontextprotocol:kotlin-sdk library. |
| kubernetes-deployment-best-practices | **/*.yaml,**/*.yml | Enforces Kubernetes manifest conventions for Pods, Deployments, Services, Ingress, configuration, health checks, resources, scaling, security, observability, rollout strategy, and… |
| kubernetes-manifests | k8s/**/*.yaml,k8s/**/*.yml,manifests/**/*.yaml,manifests/**/*.yml,deploy/**/*.yaml,deploy/**/*.yml,charts/**/templates/**/*.yaml,charts/**/templates/**/*.yml | Enforces Kubernetes manifest conventions for labels, annotations, security contexts, pod security, resources, probes, rollout strategy, HA, validation, and secrets. |
| langchain-python | **/*.py | Enforces LangChain Python conventions for Runnable composition, chat models, vector stores, prompts, tracing, testing, security, and privacy. |
| localization | **/*.md | Enforces markdown localization conventions for translated document sets, locale folders, link rewriting, completeness checks, and required disclaimers. |
| lwc | force-app/main/default/lwc/** | Enforces Lightning Web Components conventions for Salesforce component structure, SLDS, reactivity, data access, events, accessibility, performance, and tests. |
| makefile | **/Makefile,**/makefile,**/*.mk,**/GNUmakefile | Enforces GNU Make conventions for Makefile layout, variables, prerequisites, recipes, phony targets, portability, and diagnostics. |
| Markdown Content Creation Conventions | **/*.md | Enforces Markdown content creation conventions for blog post structure, YAML front matter, headings, lists, code blocks, links, images, tables, line length, and validation. |
| markdown-accessibility | **/*.md | Enforces Markdown accessibility conventions for links, image alt text, headings, plain language, lists, emoji, multimedia, and review priority. Use when writing or reviewing Markd… |
| markdown-gfm | **/*.md | Conventions for GitHub Flavored Markdown files covering CommonMark-compatible blocks, GFM tables, task lists, links, HTML, and validation. |
| mcp-m365-copilot | **/{*mcp*,*agent*,*plugin*,declarativeAgent.json,ai-plugin.json,mcp.json,manifest.json} | Enforces conventions for MCP-based Microsoft 365 Copilot declarative agents, API plugins, adaptive cards, authentication, testing, deployment, and governance. |
| memory-bank | memory-bank/** | Enforces conventions for maintaining persistent project documentation under memory-bank/ so AI agents can resume project context across sessions. |
| microsoft-foundry | **/*.py | Enforces Microsoft Foundry SDK v2 Python conventions for azure-ai-projects agents, authentication, versioning, Responses/Conversations, tools, preview features, and production lif… |
| mongo-dba | **/*.{js,ts,json} | Enforces MongoDB DBA guidance conventions for cluster administration, replica sets, backup and restore, performance, security, upgrades, tools, and MongoDB 7.x+ compatibility. |
| Moodle Conventions | **/*.php,**/*.js,**/*.mustache,**/*.xml,**/*.css,**/*.scss | Enforces Moodle project conventions for plugin layout, PHP compatibility, security APIs, renderers, Mustache templates, JavaScript modules, and Moodle API usage. |
| ms-sql-dba | **/*.sql | Conventions for Microsoft SQL Server DBA guidance in SQL files, including administration, security, performance, backup, restore, upgrades, and SQL Server 2025+ compatibility. |
| mvvm-toolkit | **/*.cs,**/*.xaml,**/*.csproj | Enforces CommunityToolkit.Mvvm conventions for ViewModels, source-generated properties, commands, messaging, validation, dependency injection, and XAML binding. |
| nestjs | **/*.ts,**/*.js,**/*.json,**/*.spec.ts,**/*.e2e-spec.ts | Enforces NestJS conventions for TypeScript server-side application modules, dependency injection, APIs, validation, persistence, security, configuration, and tests. |
| nextjs | **/*.tsx,**/*.ts,**/*.jsx,**/*.js,**/*.css | Enforces Next.js App Router conventions for Next.js 16.1.1, Server and Client Components, async request APIs, Route Handlers, Cache Components, tooling, structure, security, and t… |
| nextjs-tailwind | **/*.tsx,**/*.ts,**/*.jsx,**/*.js,**/*.css | Conventions for Next.js App Router applications with Tailwind CSS, TypeScript, server/client boundaries, styling, state, data fetching, security, and performance. |
| No Heredoc File Operations | ** | Conventions that prevent terminal heredoc file corruption by requiring file editing tools instead of shell redirections for file content changes. |
| nodejs-javascript-vitest | **/*.js,**/*.mjs,**/*.cjs | Enforces Node.js 20+ JavaScript conventions with ES2022, ESM, built-in modules, async/await, Vitest tests, README updates, and concise dependency choices. |
| Object Calisthenics Conventions | **/*.{cs,ts,java} | Enforces the original 9 Object Calisthenics rules for business domain code, with pragmatic exemptions for DTOs, API contracts, configuration, infrastructure, and tests. |
| oop-design-patterns | **/*.py,**/*.java,**/*.ts,**/*.js,**/*.cs | Enforces object-oriented design pattern and SOLID conventions for clean, maintainable, and scalable code. Use when generating or refactoring OOP code in Python, Java, TypeScript,… |
| oqtane | **/*.razor,**/*.razor.cs,**/*.razor.css | Conventions for Oqtane and Blazor modules covering component structure, client/server module patterns, services, controllers, repositories, validation, performance, caching, state… |
| PCF Model-Driven Apps Conventions | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps component framework conventions for model-driven app code components, manifests, TypeScript implementation, packaging, versioning, and documentation. |
| pcf-alm | **/*.{ts,tsx,js,json,xml,pcfproj,csproj,sln} | Enforces Power Apps component framework ALM conventions for PCF projects, cdsproj solutions, builds, source control, SolutionPackager, versioning, deployment, pipelines, and canva… |
| pcf-api-reference | **/*.{ts,tsx,js} | Enforces Power Apps Component Framework API conventions and availability checks for model-driven and canvas apps. |
| pcf-best-practices | **/*.{ts,tsx,js,json,xml,pcfproj,csproj,css,html} | Enforces Power Apps Component Framework conventions for lifecycle, hosts, WebAPI use, bundling, React, Fluent UI, accessibility, styling, and ALM. |
| pcf-canvas-apps | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces PCF canvas app conventions for security review, environment enablement, maker import, component properties, manifest version updates, and trusted solution use. |
| pcf-code-components | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps component framework code component conventions for manifests, TypeScript lifecycle methods, resources, outputs, state, cleanup, packaging, and solution reuse. |
| pcf-community-resources | **/*.{ts,tsx,js,jsx,json,xml,css,html} | Guides Power Apps Component Framework work toward PCF community resources, gallery discovery, videos, blogs, tools, contribution practices, and support channels. |
| pcf-dependent-libraries | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps component framework dependent-library conventions for shared Library Controls, feature flags, Webpack externals, manifest dependencies, and on-demand loading. |
| pcf-events | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps component framework event conventions for manifest event declarations, canvas Power Fx handlers, model-driven addEventHandler usage, payloads, callbacks, and e… |
| pcf-fluent-modern-theming | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps component framework modern theming conventions with Fluent UI React v9, v8 migration themes, non-Fluent token usage, and custom theme providers. |
| pcf-limitations | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps Component Framework limitations for Canvas Apps, Dataverse APIs, bundled libraries, storage, authentication, and platform references. |
| pcf-manifest-schema | **/*.xml | Enforces Power Apps Component Framework ControlManifest.Input.xml schema conventions for manifest elements, resources, features, platform libraries, validation, and data types. |
| pcf-overview | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps Component Framework overview conventions for capabilities, limitations, web-resource differences, APIs, licensing, and packaging. Use when building or document… |
| pcf-power-pages | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Pages conventions for using PCF code components, supported field types, unsupported APIs, model-driven field setup, form metadata, and portal Web API usage. |
| pcf-react-platform-libraries | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces Power Apps component framework React control and platform-library conventions for virtual controls, manifest resources, CLI creation, supported versions, and host limitat… |
| pcf-sample-components | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Enforces conventions for using, building, packaging, and trying PowerApps-Samples PCF sample components in model-driven and canvas apps. |
| pcf-tooling | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Conventions for Microsoft Power Platform CLI tooling for Power Apps Component Framework creation, debugging, packaging, deployment, and ALM. |
| performance-optimization | **/*.{html,htm,css,scss,sass,js,jsx,ts,tsx,vue,svelte,astro} | Enforces Core Web Vitals performance conventions for web UI files, including LCP, INP, CLS, loading, rendering, media, bundles, and framework-specific fixes. |
| php-mcp-server | **/*.php | Enforces PHP Model Context Protocol server conventions for the official PHP SDK, capability discovery, transports, sessions, errors, testing, performance, framework integration, d… |
| php-symfony | **/*.php,**/*.yaml,**/*.yml,**/*.xml,**/*.twig | Enforces Symfony conventions for project structure, configuration, dependency injection, controllers, Doctrine, Twig, forms, validation, security, assets, Messenger, and testing. |
| Playwright Python Conventions | **/*.py | Enforces Playwright Python test conventions for Pytest structure, resilient locators, web-first assertions, synchronization, and execution. |
| playwright-dotnet | **/*.cs | Enforces Playwright .NET test conventions for locators, assertions, structure, fixtures, accessibility snapshots, and execution. Use when writing C# end-to-end tests with Playwrig… |
| playwright-typescript | **/*.spec.ts,**/*.test.ts,**/*.spec.tsx,**/*.test.tsx,**/playwright.config.ts,tests/**/*.ts,tests/**/*.tsx | Conventions for Playwright tests in TypeScript covering structure, locators, assertions, fixtures, execution, and quality checks. |
| Power Platform Connectors Schema Development Instructions | **/*.{json,md} | Enforces Power Platform custom connector schema conventions for Swagger 2.0 definitions, API properties, settings, Microsoft extensions, validation, and troubleshooting. |
| power-apps-canvas-yaml | **/*.{yaml,yml,md,pa.yaml} | Enforces Power Apps canvas app YAML schema v3.0, Power Fx formula, control, data source, component, and source-control conventions. |
| power-apps-code-apps | **/*.{ts,tsx,js,jsx},**/vite.config.*,**/package.json,**/tsconfig.json,**/power.config.json | Enforces Power Apps Code Apps conventions for TypeScript, React, Vite, Power Platform SDK integration, generated connector services, security, testing, deployment, and current pla… |
| power-bi-custom-visuals-development | **/*.{ts,tsx,js,jsx,json,less,css} | Enforces Power BI custom visual conventions for pbiviz projects, TypeScript, React, D3, formatting models, interactivity, testing, performance, and packaging. |
| power-bi-data-modeling-best-practices | **/*.{pbix,md,json,txt} | Enforces Power BI semantic model conventions for star schema design, relationships, storage modes, performance, security, governance, testing, and advanced modeling patterns. |
| power-bi-dax-best-practices | **/*.{pbix,dax,md,txt} | Enforces Power BI DAX conventions for efficient, maintainable, testable measures, model-aware formulas, time intelligence, performance tuning, and documentation. |
| power-bi-devops-alm-best-practices | **/*.{yml,yaml,ps1,json,pbix,pbir} | Enforces Power BI DevOps and ALM conventions for PBIP source control, CI/CD deployment, environment promotion, testing, secrets, rollback, and monitoring. |
| power-bi-report-design-best-practices | **/*.{pbix,md,json,txt} | Enforces Power BI report design, visualization, accessibility, interaction, performance, mobile, testing, and governance conventions for report artifacts and supporting documentat… |
| power-bi-security-rls-best-practices | **/*.{pbix,dax,md,txt,json,csharp,powershell} | Enforces Power BI security and Row-Level Security conventions for DAX roles, dynamic security, embedded analytics identities, database RLS integration, governance, monitoring, and… |
| power-platform-mcp-development | **/*.{json,csx,md} | Enforces Power Platform MCP custom connector conventions for JSON-RPC, Copilot Studio schema constraints, authentication, scripts, Swagger, resources, errors, testing, and certifi… |
| powershell | **/*.ps1,**/*.psm1 | Enforces PowerShell cmdlet and scripting conventions for naming, parameters, pipeline behavior, output, safety, help, and automation. |
| powershell-pester-6 | **/*.Tests.ps1 | Enforces Pester v6 conventions for PowerShell test discovery, block structure, assertions, mocks, data-driven cases, tags, skips, and configuration. |
| prompt | **/*.prompt.md | Applies current VS Code prompt conventions for canonical sources, metadata, runtime inputs, tools, destination safety, body structure, and testing. Use when creating or updating a… |
| python-mcp-server | **/*.py,**/pyproject.toml,**/requirements.txt | Enforces Model Context Protocol Python SDK conventions for FastMCP tools, resources, prompts, transports, context, structured output, lifespan, and testing. |
| qa-engineering-best-practices | ** | Enforces QA engineering conventions for test strategy, naming, assertions, data, automation, CI/CD evidence, bug reports, and coverage across any stack. |
| quarkus | **/*.java,**/pom.xml,**/build.gradle,**/build.gradle.kts,**/application.properties,**/application.yaml,**/application.yml | Enforces Quarkus Java conventions for project structure, REST resources, Panache data access, configuration, security, and testing. Use when editing Quarkus source, build, or appl… |
| Quarkus MCP Server SSE Conventions | * | Enforces Java 21 Quarkus MCP server conventions for HTTP SSE transport, CDI tools, layered architecture, validation, and error handling. |
| r | **/*.R,**/*.r,**/*.Rmd,**/*.rmd,**/*.qmd | Enforces idiomatic R, R Markdown, and Quarto conventions for style, reproducibility, data wrangling, plotting, errors, security, Shiny, tooling, and tests. |
| ruby-mcp-server | **/*.rb,**/Gemfile,**/*.gemspec,**/Rakefile | Enforces Ruby MCP server conventions for SDK setup, tools, resources, prompts, transports, context, configuration, responses, notifications, testing, and clients. |
| ruby-on-rails | **/*.rb | Enforces Ruby on Rails conventions for models, controllers, routing, persistence, APIs, frontend integration, jobs, testing, configuration, and maintainability. |
| rust | **/*.rs | Enforces idiomatic Rust conventions for safety, ownership, API design, errors, async, testing, documentation, and Cargo packaging. |
| rust-mcp-server | **/*.rs | Enforces Rust Model Context Protocol server conventions for rmcp dependencies, handlers, tools, prompts, resources, transports, errors, tests, authentication, observability, and d… |
| scala-spark | **/*.scala,**/build.sbt,**/build.sc | Enforces Scala Apache Spark conventions for dependencies, SparkSession setup, DataFrame and Dataset design, schemas, joins, partitioning, streaming, Delta Lake, performance, testi… |
| scala2 | **/*.scala,**/build.sbt,**/build.sc | Enforces Scala 2.12/2.13 conventions for functional style, type safety, formatting, SBT configuration, performance, concurrency, and testing. |
| security-and-owasp | ** | Enforces OWASP-aligned secure coding conventions for web, backend, frontend, API, dependency, logging, and AI/LLM changes. |
| self-explanatory-code-commenting | ** | Enforces self-explanatory code comments that explain why, constraints, and risks while avoiding obvious, redundant, stale, decorative, or historical comments. |
| shell | **/*.sh | Enforces safe, readable shell scripting conventions for bash, sh, zsh, automation, parsers, cleanup, and static analysis. |
| spec-driven-workflow-v1 | ** | Enforces Specification-Driven Workflow v1 conventions for requirements, design, tasks, documentation, validation, reflection, handoff, troubleshooting, debt, quality metrics, and… |
| springboot | **/*.java,**/*.kt | Conventions for Spring Boot base applications covering dependency injection, configuration, package organization, services, logging, security, validation, builds, and useful Maven… |
| springboot-4-migration | **/*.java,**/*.kt,**/build.gradle.kts,**/build.gradle,**/settings.gradle.kts,**/gradle/libs.versions.toml,**/*.properties,**/*.yml,**/*.yaml | Enforces Spring Boot 3.x to 4.0 migration conventions for Java, Kotlin, Gradle, version catalogs, configuration, tests, and production readiness. |
| sql-sp-generation | **/*.sql | Conventions for SQL schema generation, query style, stored procedure naming, parameter handling, security, and transactions. |
| svelte | **/*.svelte,**/*.ts,**/*.js,**/*.css,**/*.scss,**/*.json | Enforces Svelte 5 and SvelteKit 2 conventions for runes reactivity, routing, load functions, form actions, remote functions, TypeScript, styling, performance, errors, security, an… |
| swift-mcp-server | **/*.swift,**/Package.swift,**/Package.resolved | Enforces conventions for building Swift Model Context Protocol servers with the official MCP Swift SDK package. |
| tailwind-v4-vite | vite.config.ts,vite.config.js,**/*.css,**/*.tsx,**/*.ts,**/*.jsx,**/*.js | Enforces Tailwind CSS v4+ conventions for Vite projects using @tailwindcss/vite, CSS-first configuration, migration, verification, and troubleshooting. |
| Taming Copilot Conventions | ** | Enforces repository-wide conventions for keeping Copilot interactions factual, concise, minimal, surgical, tool-aware, and aligned with user directives. |
| tanstack-start-shadcn-tailwind | **/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.css,**/*.scss,**/*.json | Enforces TanStack Start, React, Shadcn/ui, Tailwind CSS, Zod, routing, data fetching, accessibility, and import conventions. |
| task-implementation | **/.copilot-tracking/changes/*.md | Enforces conventions for implementing tracked task plans with complete plan/detail reading, progressive checklist updates, change records, validation, and release summaries. |
| tasksync | ** | Defines TaskSync V5 terminal task-request conventions for agents that intentionally run a continuous terminal-driven task loop. |
| terraform | **/*.tf | Enforces Terraform conventions for secure, modular, maintainable, formatted, documented, tested, and version-controlled infrastructure code. |
| terraform-azure | **/*.terraform,**/*.tf,**/*.tfvars,**/*.tflint.hcl,**/*.tfstate,**/*.tf.json,**/*.tfvars.json | Enforces Azure Terraform conventions for AVM usage, file layout, variables, secrets, state, providers, validation, documentation, cost, and operations. |
| terraform-sap-btp | **/*.tf,**/*.tfvars,**/*.tflint.hcl,**/*.tf.json,**/*.tfvars.json | Enforces Terraform conventions for SAP Business Technology Platform infrastructure, including SAP BTP provider usage, security, state, validation, testing, and tool integration. |
| typescript-mcp-server | **/*.ts,**/*.js,**/package.json | Enforces Model Context Protocol TypeScript SDK conventions for tools, resources, prompts, transports, schemas, errors, and testing. |
| typespec-m365-copilot | **/*.tsp | Enforces TypeSpec conventions for Microsoft 365 Copilot declarative agents, capabilities, API plugins, authentication, cards, validation, and security. |
| update-code-from-shorthand | **/${input:file} | Interprets UPDATE CODE FROM SHORTHAND prompts and replaces marked shorthand regions with valid code for the required target file. |
| update-docs-on-code-change | **/*.{md,js,mjs,cjs,ts,tsx,jsx,py,java,cs,go,rb,php,rs,cpp,c,h,hpp} | Enforces documentation synchronization when code changes affect README files, API docs, configuration guides, changelogs, examples, or migration guidance. |
| use-cliche-data-in-docs | **/*.{md,js,mjs,cjs,ts,tsx,jsx,py,json} | Enforces generic cliche placeholder data in documentation, examples, templates, comments, and sample configuration instead of real or sensitive implementation data. |
| vsixtoolkit | **/*.cs,**/*.vsct,**/*.xaml,**/source.extension.vsixmanifest | Enforces Community.VisualStudio.Toolkit conventions for Visual Studio extension packages, commands, options, MEF components, threading, theming, VSCT, validation, NuGet dependenci… |
| vue | **/*.vue,**/*.ts,**/*.js,**/*.css,**/*.scss | Enforces Vue 3 conventions for Composition API, script setup, reactivity, macros, components, routing, Pinia, styling, testing, SSR, performance, and security. |
| winui3 | **/*.xaml,**/*.cs,**/*.csproj | Enforces WinUI 3 and Windows App SDK conventions for XAML, namespaces, threading, windowing, dialogs, MVVM, project setup, styling, accessibility, testing, and resources. |
| wordpress | wp-content/plugins/**,wp-content/themes/**,**/*.php,**/*.inc,**/*.js,**/*.jsx,**/*.ts,**/*.tsx,**/*.css,**/*.scss,**/*.json | Enforces secure WordPress plugin and theme conventions for hooks, coding standards, data handling, i18n, assets, REST, blocks, testing, and documentation. |

## Skills

| Skill | Description |
| --- | --- |
| acquire-codebase-knowledge | Map, document, and onboard into an existing codebase by producing seven evidence-backed docs in docs/codebase/. Use when the user explicitly asks to map this codebase, document th… |
| acreadiness-assess | Run the AgentRC AI-readiness assessment for the current repository, optionally apply a policy, and produce a self-contained HTML dashboard at reports/index.html. Use when asked to… |
| acreadiness-generate-instructions | Generate tailored AI agent instruction files with the AgentRC instructions command, including .github/copilot-instructions.md, AGENTS.md, scoped .github/instructions/*.instruction… |
| acreadiness-policy | Help the user pick, write, or apply an AgentRC policy. Policies customise readiness scoring by disabling irrelevant checks, overriding impact/level, setting pass-rate thresholds,… |
| ad-campaign-analyzer | Analyze ad campaign performance data to diagnose waste, identify winners, validate A/B tests, compare channels, and recommend cuts, scaling, tests, and budget reallocation. Use wh… |
| add-educational-comments | Add educational comments to existing code files while preserving encoding, line endings, indentation, syntax, and build correctness. Use this skill when the user asks to annotate… |
| adobe-illustrator-scripting | Write, debug, and optimize Adobe Illustrator automation scripts using ExtendScript (JavaScript/JSX). Use when creating or modifying scripts that manipulate documents, layers, path… |
| agent-governance | Design governance, safety, policy enforcement, trust scoring, and audit controls for AI agent systems. Use when building agents with external tools, policy-based tool access, sema… |
| agent-owasp-compliance | Evaluate AI agent systems against OWASP Agentic Security Initiative Top 10 controls. Use when asked whether an agent is OWASP ASI compliant, to check ASI compliance, run an agenti… |
| agent-skill-stack | Find, evaluate, and assemble the smallest compatible set of AI Agent Skills for an end-to-end natural-language goal. Use when a user wants Skills for a multi-step workflow, asks w… |
| agent-supply-chain | Verify supply chain integrity for AI agent plugins, MCP servers, tools, and dependencies by generating SHA-256 manifests, verifying installed files, auditing pinned versions, and… |
| agentic-eval | Design evaluator-optimizer, reflection, rubric, LLM-as-judge, and test-driven refinement loops for AI agent outputs. Use when implementing self-critique, iterative improvement, qu… |
| ai-prompt-engineering-safety-review | Review and improve AI prompts for safety, bias, security, privacy, effectiveness, robustness, and testability. Use this skill when the user asks to audit a prompt, harden a system… |
| ai-ready | Help users install and use John Papa's ai-ready skill as the up-to-date source for making repositories AI-ready with AGENTS.md, copilot-instructions.md, CI workflows, issue templa… |
| ai-team-orchestration | Bootstrap and run a lightweight multi-agent development team. Use when starting or adopting a project, planning multi-step work, coordinating implementation with optional QA, brai… |
| anti-ui-slop | Prevent generic web and iOS interfaces by extracting product-specific design decisions from repository evidence and UIZZE's public catalogue of 800,000+ real web and iOS screens.… |
| apim-ai-gateway | Design Azure API Management as the runtime AI gateway for model and tool traffic, including token-per-minute controls, token limits, quotas, multi-backend load-balanced backend po… |
| appinsights-instrumentation | Instrument Azure-hosted web apps with Azure Application Insights telemetry by choosing auto-instrumentation or code instrumentation for ASP.NET Core, Node.js, or Python. Use when… |
| apple-appstore-reviewer | Review an iOS app codebase and metadata for likely Apple App Store rejection risks, compliance gaps, reviewer friction, and fast approval improvements. Use when asked to "review f… |
| arch-linux-triage | Diagnose and remediate Arch Linux incidents with pacman, systemd, journal analysis, rolling-release upgrade discipline, kernel awareness, and rollback practices. Use when the user… |
| architecture-blueprint-generator | Generate a comprehensive Project_Architecture_Blueprint.md by analyzing a codebase, detecting technology stacks and architectural patterns, documenting components, dependencies, d… |
| arduino-azure-iot-edge-integration | Design and implement Arduino integration with Azure IoT Hub and IoT Edge, including secure provisioning, MQTT telemetry, gateway topologies, offline buffering, command handling, O… |
| arize-ai-provider-integration | Create, list, inspect, update, and delete Arize AI integrations that store LLM provider credentials for evaluators and Arize features. Use this skill when connecting OpenAI, Anthr… |
| arize-annotation | Create, inspect, update, and use Arize annotation configs and annotation queues, then bulk-apply human labels to spans with the Python SDK. Use when asked for "annotation config",… |
| arize-dataset | Creates, manages, and queries Arize datasets and examples. Covers dataset CRUD, appending examples, exporting data, and file-based dataset creation using the ax CLI. Use when the… |
| arize-evaluator | Create, update, and run Arize LLM-as-judge evaluators and tasks for spans, traces, sessions, projects, datasets, and experiments. Use when the user mentions create evaluator, LLM… |
| arize-experiment | Create, run, export, compare, delete, and troubleshoot Arize experiments with the ax CLI, including real model inference, run files, evaluations, result analysis, and dataset-link… |
| arize-instrumentation | Adds Arize AX tracing to an LLM application for the first time. Use when the user wants to instrument their app, add tracing from scratch, set up LLM observability, integrate Open… |
| arize-link | Generate Arize UI deep links for traces, spans, sessions, datasets, labeling queues, evaluators, and annotation configs using base64 org and space IDs, resource IDs, and trace/ses… |
| arize-prompt-optimization | Optimizes, improves, and debugs LLM prompts using production trace data, evaluations, and annotations. Extracts prompts from spans, gathers performance signal, and runs a data-dri… |
| arize-trace | Download, export, inspect, and root-cause existing Arize traces, spans, sessions, errors, prompts, retrieval documents, model calls, and behavior regressions with the ax CLI. Use… |
| aspire | Work with Aspire distributed applications, AppHost orchestration, CLI commands, service discovery, integrations, MCP docs, dashboard, testing, and deployment. Use this skill when… |
| aspnet-minimal-api-openapi | Create or review ASP.NET Minimal API endpoints with typed results, DTO validation, endpoint groups, filters, ProblemDetails, and OpenAPI documentation. Use this skill when asked t… |
| audit-integrity | Enforce AppSec audit integrity for security analysis, code review, threat modeling, SAST, SCA, and quality scan agents. Use this skill when running a post-analysis quality gate, p… |
| automate-this | Analyze a screen recording of a repetitive manual workflow, extract frames and optional narration, reconstruct the process, and produce tested automation scripts. Use this skill w… |
| autoresearch | Run an autonomous iterative experimentation loop for programming tasks with measurable outcomes. Use when the user asks for autonomous improvement, iterative optimization, experim… |
| aws-cdk-python-setup | Set up and initialize AWS CDK applications in Python, including prerequisites, credentials, project creation, virtual environments, dependencies, synthesis, bootstrap, diff, deplo… |
| aws-cloudwatch-investigation | Investigate AWS production incidents with CloudWatch Logs Insights, Metrics, Alarms, CloudTrail correlation, blast-radius narrowing, metric math, and incident timelines. Use when… |
| aws-cost-optimize | Analyze AWS resources used in the app (IaC files and/or resources in a target account/region) and optimize costs - creating GitHub issues for identified optimizations. Use this sk… |
| aws-resource-health-diagnose | Diagnose AWS resource health with AWS CLI, CloudWatch metrics, CloudWatch Logs Insights, Performance Insights, CloudTrail correlation, severity classification, root cause analysis… |
| aws-resource-query | Answer natural-language questions about AWS resources by running strictly read-only AWS CLI queries. Use when asking about EC2, S3, RDS, Lambda, ECS, EKS, Secrets Manager, IAM, VP… |
| aws-well-architected-review | Review AWS workloads against the AWS Well-Architected Framework across Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability… |
| az-cost-optimize | Analyze Azure IaC files and deployed Azure resources for evidence-based cost optimization, validate current costs, calculate priority scores, and draft GitHub issues. Use when ask… |
| azure-api-center | Design Azure API Center as the enterprise inventory and governance plane for APIs, agent tools, OpenAPI definitions, environments, deployments, metadata, linting, and MCP server d… |
| azure-architecture-autopilot | Design new Azure infrastructure or analyze existing Azure resources, generate interactive architecture diagrams, refine through conversation, produce Bicep, review, and deploy. Us… |
| azure-architecture-diagrams | Produce professional Azure, Microsoft, and GitHub architecture diagrams as editable draw.io source and exported SVG. Use when the user asks for an architecture diagram, system con… |
| azure-container-registry-cli | Manage Azure Container Registry with az acr CLI commands for registries, images, cloud builds, ACR Tasks, authentication, tokens, geo-replication, networking, purge, import, and d… |
| azure-deployment-preflight | Validate Azure Bicep deployments before execution with syntax checks, azd preview, Azure CLI what-if, validation-level fallback, permission checks, and a preflight report. Use thi… |
| azure-developer-cli | Design, create, review, migrate, or troubleshoot Azure Developer CLI azd projects using azure.yaml, infra Bicep or Terraform, environments, secrets, hooks, deployment workflows, a… |
| azure-devops-cli | Manage Azure DevOps with Azure CLI and the azure-devops extension. Use when the user asks for Azure DevOps CLI commands, az devops automation, projects, repos, pull requests, pipe… |
| azure-managed-redis-cache | Design and provision Azure Managed Redis as the cache, semantic cache, vector store, session store, and agent memory backend for AI-native systems. Use when an agent design needs… |
| azure-pricing | Fetch live Azure Retail Prices API data and estimate Azure service, SKU, region, reservation, savings plan, spot, and Copilot Studio credit costs. Use when the user asks about Azu… |
| azure-resource-health-diagnose | Analyze Azure resource health, logs, metrics, and telemetry to diagnose operational issues and produce a prioritized remediation plan. Use this skill when the user asks to trouble… |
| azure-resource-visualizer | Analyze Azure resource groups and generate Mermaid architecture diagrams and markdown documentation for their resources and relationships. Use this skill when the user asks to dia… |
| azure-role-selector | Select the least-privilege Azure RBAC role for an identity, compare built-in and custom role options, and produce assignment commands or Bicep snippets. Use this skill when the us… |
| azure-smart-city-iot-solution-builder | Design and plan end-to-end Azure IoT and Smart City solutions with requirements, architecture, device and edge strategy, ingestion, analytics, security, operations, cost controls,… |
| azure-static-web-apps | Create, configure, run, and deploy Azure Static Web Apps with the SWA CLI. Use when asked to deploy a static site to Azure, run SWA locally, configure staticwebapp.config.json, ad… |
| azure-well-architected-review | Perform an Azure Well-Architected Framework review of the current workload IaC and architecture, generating findings and GitHub issues for improvements. Use this skill when the us… |
| backstage-plugin-builder | Plan, architect, scaffold, validate, and prepare custom Backstage plugins and modules using official Backstage documentation. Use when the user asks for frontend plugins, backend… |
| batch-files | Expert-level Windows batch file (.bat/.cmd) skill for writing, debugging, and maintaining CMD scripts. Use when asked to "create a batch file", "write a .bat script", "automate a… |
| bench-read | Read artifacts from a workshop bench where desks leave findings, verdicts, drafts, reports, journals, and cross-desk work products. Use this skill when starting a session, reviewi… |
| bigquery-pipeline-audit | Audit Python and BigQuery pipeline scripts for cost exposure, dry-run safety, bounded backfills, query pruning, idempotent writes, and observability. Use this skill when reviewing… |
| boost-prompt | Refine a rough task request into a high-quality markdown prompt by clarifying scope, deliverables, constraints, context, and success criteria, then copy the final prompt to the cl… |
| brag-sheet | Turn vague work-history prompts into evidence-backed impact statements for performance reviews, self-reviews, promotion packets, weekly updates, status reports, and accomplishment… |
| breakdown-epic-arch | Create a high-level epic architecture specification from an Epic PRD, including system diagrams, technical enablers, stack choices, technical value, and t-shirt sizing. Use when a… |
| breakdown-epic-pm | Create an Epic Product Requirements Document (PRD) from a high-level epic idea, including goal, personas, journeys, business requirements, success metrics, scope boundaries, and b… |
| breakdown-feature-implementation | Create detailed feature implementation plans from a Feature PRD for an Epoch-style monorepo, including architecture, database schema, API design, frontend structure, security, per… |
| breakdown-feature-prd | Create a detailed feature Product Requirements Document from an epic and feature idea, including goal, personas, user stories, functional and non-functional requirements, acceptan… |
| breakdown-plan | Generate GitHub issue planning and project automation artifacts from feature planning documents, including Epic > Feature > Story/Enabler > Test hierarchy, priorities, dependencie… |
| breakdown-test | Create comprehensive test planning, QA strategy, GitHub issue breakdowns, and quality validation plans from feature artifacts. Use when asked to produce a test strategy, break dow… |
| bug-receipt | Close bugs and incidents with an auditable BUG RECEIPT that states VERIFIED, PARTIAL, or BLOCKED based on baseline, root cause, change, proof, gaps, and evidence source. Use when… |
| bug-reproduction-brief | Turn vague, intermittent, or environment-specific bug reports into minimal evidence-backed reproductions before diagnosis or repair. Use when a bug report is incomplete, mixed wit… |
| build-evidence-map | Build auditable evidence maps for contested technical choices, research synthesis, proposal review, and consequential decisions. Use this skill when GitHub Copilot must preserve s… |
| canvas-design | Create original, museum-quality static visual designs as markdown design philosophy plus PNG or PDF canvas output. Use this skill when the user asks for a poster, art piece, visua… |
| centos-linux-triage | Diagnose and remediate CentOS Linux incidents with RHEL-compatible systemd, journal, dnf/yum, SELinux, firewalld, and rollback practices. Use when the user asks to triage CentOS s… |
| chrome-devtools | Handle `browser-related` tasks and control a live Chrome browser through Chrome DevTools MCP for browser automation, visual inspection, debugging, performance analysis, and emulat… |
| cli-mastery | Interactive training for the GitHub Copilot CLI through guided lessons, quizzes, scenario challenges, a final exam, and on-demand reference for slash commands, shortcuts, modes, a… |
| cloud-design-patterns | Select, explain, and apply cloud design patterns for distributed systems across reliability, performance, messaging, architecture, deployment, security, and event-driven categorie… |
| code-exemplars-blueprint-generator | Generate a configurable prompt blueprint for scanning a codebase and producing an exemplars.md catalog of high-quality, real code examples. Use this skill when the user asks for c… |
| code-modernization | Use this skill when the user asks to modernize legacy code with a disciplined GitHub Copilot workflow: brief, assess, map, extract business rules, reimagine architecture, transfor… |
| code-tour | Create CodeTour .tour JSON files that guide a persona through real repository files, directories, line numbers, selections, patterns, URIs, views, and VS Code commands. Use when a… |
| codebase-memory-mcp | Use a configured Codebase Memory MCP graph for architecture orientation, symbol lookup, callers and callees, dependency or data-flow tracing, impact analysis, and unfamiliar modul… |
| codeql | Configure and run CodeQL code scanning with GitHub Actions workflows, default or advanced setup, CodeQL CLI databases, SARIF uploads, custom query packs, monorepo categories, buil… |
| comment-code-generate-a-tutorial | Transform a Python script into a polished beginner-friendly project by refactoring code, adding instructional comments, and generating a complete README.md tutorial. Use this skil… |
| commit-message-storyteller | Analyze git diffs, staged changes, or plain change descriptions and generate narrative Conventional Commits messages that explain why the change matters. Use when asked to "write… |
| competitor-ad-intelligence | Analyze public competitor paid ads from Meta Ad Library and Google Ads Transparency Center, cluster creative hooks, inspect landing pages, infer funnel strategy, identify vulnerab… |
| containerize-aspnet-framework | Containerize an ASP.NET .NET Framework project by creating Dockerfile and .dockerfile files customized for the project. Use this skill when the user asks for asp.net .net framewor… |
| containerize-aspnetcore | Containerize an ASP.NET Core project for a Linux Docker container by creating a multi-stage Dockerfile, .dockerignore, optional health check, environment-variable configuration, a… |
| content-management-systems | Build and modify content management systems by locating the correct theme, plugin, module, editor, content model, media, render, or export seam before changing code. Use this skil… |
| context-map | Build a concise map of files relevant to a requested code change before implementation. Use when the user asks to identify affected files, plan changes, map dependencies, find tes… |
| conventional-branch | Create, normalize, validate, and check out Git branches following the Conventional Branch specification with feature/, bugfix/, hotfix/, release/, and chore/ prefixes. Use when cr… |
| conventional-commit | Generate and execute Conventional Commit messages from staged or unstaged Git changes. Use this skill when the user asks to create a commit, write a conventional commit message, c… |
| convert-excel-to-md | Convert Excel .xlsx workbooks to Markdown with the bundled script so spreadsheet contents can be read, summarized, searched, extracted, compared, charted, or analyzed. Use wheneve… |
| convert-pdf-to-md | Convert PDF .pdf documents to Markdown with the bundled script so reports, papers, invoices, forms, contracts, scanned documents, and folders of PDFs can be read, summarized, sear… |
| convert-plaintext-to-md | Convert plaintext or generic text documentation into well-structured Markdown while preserving source content and applying explicit instructions, documented options, or a converte… |
| convert-word-to-md | Convert Word .docx documents into Markdown with extracted images using the bundled script. Use this skill when a user asks to read, summarize, review, compare, analyze, extract da… |
| copilot-cli-quickstart | Use this skill when someone wants to learn GitHub Copilot CLI from scratch. Offers interactive step-by-step tutorials with separate Developer and Non-Developer tracks, plus on-dem… |
| copilot-instructions-blueprint-generator | Generate technology-agnostic blueprints for comprehensive copilot-instructions.md files that make GitHub Copilot follow exact project versions, architecture, code quality, documen… |
| copilot-plugin-authoring | Create, migrate, audit, and validate GitHub Copilot plugins and marketplaces in this repository using Agent Plugins 1.0, canonical library sources, generated com.github.copilot mi… |
| copilot-pr-autopilot | Run a GitHub Copilot Code Review loop on a pull request: request review with GraphQL, wait, list open Copilot/human/advanced-security threads, triage fix/decline/escalate, dispatc… |
| copilot-primitive-authoring | Author current GitHub Copilot agents, instructions, and VS Code prompts in this repository. Use when asked to create or update a known primitive type with repository governance, d… |
| copilot-sdk | Build agentic applications with GitHub Copilot SDK. Use when embedding AI agents in apps, creating custom tools, implementing streaming responses, managing sessions, connecting to… |
| copilot-spaces | Use GitHub Copilot Spaces to provide project-specific context to conversations. Use this skill when users mention a "GitHub Copilot space", want to load context from a shared know… |
| copilot-usage-metrics | Retrieve and display GitHub Copilot usage metrics for organizations and enterprises using the GitHub CLI, REST API, and bundled scripts. Use when the user asks about Copilot usage… |
| cosmosdb-datamodeling | Capture Azure Cosmos DB for NoSQL workload requirements and produce access-pattern-driven data model artifacts. Use when the user asks to design a Cosmos DB NoSQL model, choose co… |
| create-agentsmd | Create a high-quality AGENTS.md file for a repository by inspecting project structure, workflows, commands, tests, and conventions. Use this skill when the user asks to create, up… |
| create-architectural-decision-record | Create an Architectural Decision Record (ADR) as a structured Markdown document with front matter, coded consequences, alternatives, implementation notes, and references. Use when… |
| create-github-action-workflow-specification | Creates formal, AI-optimized specifications for existing GitHub Actions CI/CD workflows by extracting triggers, jobs, dependencies, contracts, quality gates, error paths, environm… |
| create-github-issue-feature-from-specification | Create or update one GitHub feature issue from a specification file using a feature_request.yml template when available. Use when the user asks to create a GitHub issue from a spe… |
| create-github-issues-feature-from-implementation-plan | Create or update GitHub issues from implementation-plan phases using feature_request.yml or chore_request.yml templates when available. Use when the user asks to turn an implement… |
| create-github-issues-for-unmet-specification-requirements | Create GitHub Issues for unimplemented requirements found in specification files, avoiding duplicates and using the feature_request.yml issue template when available. Use this ski… |
| create-implementation-plan | Create deterministic implementation plan files for features, refactors, package upgrades, design, architecture, infrastructure, data, or process work. Use when the user asks for a… |
| create-llms | Create a new repository-root llms.txt file from repository structure and documentation according to the llms.txt specification. Use when users ask to create llms.txt, generate LLM… |
| create-readme | Create or improve a concise, appealing, project-specific README.md with a clear overview, setup, usage, and practical examples. Use this skill when the user asks to generate, refr… |
| create-specification | Create a new AI-ready specification file in /spec/ that defines solution requirements, constraints, interfaces, dependencies, acceptance criteria, test strategy, and validation cr… |
| create-spring-boot-java-project | Create a Spring Boot Java project skeleton from Spring Initializr with Maven, Java 21, common data dependencies, SpringDoc, ArchUnit, local Docker Compose services for Redis, Post… |
| create-spring-boot-kotlin-project | Create a Spring Boot Kotlin project skeleton from Spring Initializr with Gradle Kotlin DSL, Java 21, WebFlux, reactive data dependencies, SpringDoc, ArchUnit, and local Redis/Post… |
| create-technical-spike | Create time-boxed technical spike documents that answer critical implementation questions before development proceeds. Use this skill when the user asks to create a technical spik… |
| create-tldr-page | Create a tldr page from documentation URLs and command examples, requiring both URL and command name. Use this skill when the user asks to generate a concise tldr-pages style comm… |
| creating-oracle-to-postgres-master-migration-plan | Discover .NET solution projects, classify Oracle-to-PostgreSQL migration eligibility, detect Oracle dependencies, and write .github/oracle-to-postgres-migration/Reports/MasterMigr… |
| creating-oracle-to-postgres-migration-bug-report | Create structured bug reports for Oracle-to-PostgreSQL migration defects with source-of-truth Oracle behavior, PostgreSQL divergence, severity, root cause, remediation, validation… |
| creating-oracle-to-postgres-migration-integration-tests | Create Phase 3 Oracle integration tests for .NET data access artifacts before Oracle-to-PostgreSQL migration, capturing Oracle behavior as the golden baseline while keeping assert… |
| csharp-async | Review, design, and fix C# async code using Task, Task<T>, ValueTask<T>, cancellation, ConfigureAwait, async streams, and TAP conventions. Use when the user asks for C# async best… |
| csharp-docs | Write and review C# XML documentation comments for public and complex internal APIs, including summaries, remarks, examples, cref links, parameters, returns, constructors, propert… |
| csharp-mstest | Apply modern MSTest 3.x/4.x testing practices for C# projects. Use when asked to write or review MSTest unit tests, choose assertion APIs, convert ExpectedException tests, design… |
| csharp-nunit | Design, write, and review NUnit tests for .NET projects, including standard tests, data-driven tests, assertions, setup/teardown, categories, and isolation with mocks. Use this sk… |
| csharp-tunit | Write, review, or migrate C# unit tests using TUnit. Use when the user asks for TUnit best practices, .NET test project setup, TUnit assertions, lifecycle hooks, data-driven tests… |
| csharp-xunit | Apply xUnit best practices for C# unit tests, including test project setup, Fact and Theory structure, data-driven tests, assertions, fixtures, mocking, categorization, diagnostic… |
| daily-focus-board | Create a personal daily focus board in a browser canvas from a self-contained HTML template. Use when the user wants to plan their day, get organized, stay focused, kick off a wor… |
| daily-prep | Prepare a structured HTML day-prep file for tomorrow or a requested date by pulling Outlook calendar details through WorkIQ, classifying meetings, detecting conflicts and day-fit… |
| data-breach-blast-radius | Pre-breach impact analysis: inventories sensitive data (PII, PHI, PCI-DSS, credentials), traces data flows, scores exposure vectors, and produces a regulatory blast radius report… |
| datanalysis-credit-risk | Run and explain a credit risk data cleaning and variable screening pipeline for pre-loan modeling, including missing value analysis, abnormal period filtering, high-missing remova… |
| dataverse-python-advanced-patterns | Generate production-ready Microsoft Dataverse SDK for Python code using advanced error handling, retries, batch operations, optimized OData queries, metadata management, timeouts,… |
| dataverse-python-production-code | Generate production-ready Python 3.10+ code for the PowerPlatform-Dataverse-Client SDK with DataverseError handling, singleton client management, retry with exponential backoff fo… |
| dataverse-python-quickstart | Generate concise Microsoft Dataverse SDK for Python preview setup, authentication, CRUD, bulk create/update, paging, and optional File column upload snippets using official patter… |
| dataverse-python-usecase-builder | Generate complete Python solutions for Microsoft Dataverse SDK business use cases, including architecture, table design, CRUD, batch, query, file, scheduled, or real-time patterns… |
| debian-linux-triage | Diagnose and remediate Debian Linux incidents with apt, dpkg, systemd, journal analysis, AppArmor-aware checks, firewall review, and rollback practices. Use when the user asks to… |
| declarative-agents | Build, validate, and optimize Microsoft 365 Copilot declarative agents with v1.5 schema, TypeSpec, Microsoft 365 Agents Toolkit, capabilities, conversation starters, localization,… |
| dependabot | Comprehensive guide for configuring and managing GitHub Dependabot. Use this skill when users ask about creating or optimizing dependabot.yml files, managing Dependabot pull reque… |
| desk-journal | Read, write, or append persistent desk journal entries that survive session boundaries and capture what was done, current state, next step, dead ends, artifacts, and desk closure… |
| desk-open | Create and open a new workshop desk with a journal and .signals directory. Use when the operator wants to start a new workstream, work does not belong to an existing desk, or a to… |
| devops-rollout-plan | Generate production-ready DevOps rollout plans for infrastructure, application, configuration, and data changes, including preflight checks, phased deployment, verification signal… |
| diagnose | Diagnose AI workflows across prompt quality, context efficiency, tool health, architecture fitness, and safety and reliability, producing a 1-5 scored report with critical finding… |
| doc-and-modernize | Two related workflows for a locally-cloned codebase, in one skill. Use this skill when enforced*** — i.e. whether any workflow is a **required status check /; branch-protection ru… |
| documentation-writer | Create, review, and structure software documentation with the Diátaxis framework: tutorials, how-to guides, reference, and explanation. Use when the user asks for a Diátaxis docum… |
| dotnet-best-practices | Review or improve .NET and C# code against solution/project best practices for documentation, architecture, dependency injection, resources, async, tests, configuration, Semantic… |
| dotnet-design-pattern-review | Review C# and .NET code for design pattern quality, SOLID principles, dependency injection, repository/provider abstractions, ResourceManager usage, async practices, testability,… |
| dotnet-mcp-builder | Build and debug C#/.NET MCP servers and clients with current ModelContextProtocol 2.x packages. Use when the user mentions ModelContextProtocol, McpServerTool, MapMcp, WithStdioSe… |
| dotnet-timezone | Resolve .NET and C# timezone questions with TimeZoneInfo, DateTimeOffset, TimeZoneConverter, NodaTime, UTC conversion, daylight saving time, scheduling, Windows and IANA timezone… |
| dotnet-upgrade | Guide comprehensive .NET upgrade discovery, assessment, sequencing, dependency review, framework targeting, code modernization, CI/CD updates, validation, breaking-change analysis… |
| doublecheck | Runs a three-layer verification pipeline for AI output by extracting verifiable claims, checking web sources, applying adversarial hallucination review, and producing inline or fu… |
| draw-io-diagram-generator | Use when creating, editing, or generating draw.io diagram files (.drawio, .drawio.svg, .drawio.png). Covers mxGraph XML authoring, shape libraries, style strings, flowcharts, syst… |
| drawio | Generate draw.io diagrams as native .drawio files and export them to PNG, SVG, or PDF with embedded XML. Use when the user asks for draw.io diagrams, diagrams.net XML, mxGraphMode… |
| editorconfig | Generate or update a comprehensive .editorconfig from repository file types and formatting preferences, including indentation, line endings, charset, whitespace, final newline, la… |
| ef-core | Review or design Entity Framework Core data access using DbContext, entity mapping, LINQ queries, migrations, change tracking, performance, security, and tests. Use when the user… |
| efcore-d2-db-diagram | Generates D2 entity-relationship diagrams from Entity Framework Core models by extracting DbContext, DbSet<T>, entity configuration, migrations, keys, foreign keys, owned types, m… |
| em-dash | Review and rewrite code, comments, documentation, and data files to avoid em dashes and en dashes by default. Use this skill when the user asks to remove em dashes, replace Unicod… |
| email-drafter | Draft and review professional emails that match the user's established writing style by analyzing recipient context, tone, greeting, structure, sign-off, and language patterns whe… |
| entra-agent-user | Create Agent Users in Microsoft Entra ID from Agent Identities, enabling AI agents to act as digital workers with user identity capabilities in Microsoft 365 and Azure environment… |
| eval-driven-dev | Improve AI application with evaluation-driven development. Define eval criteria, instrument the application, build golden datasets, observe and evaluate application runs, analyze… |
| exam-ready | Prepare a student for an exam from provided study material and syllabus only. Use when the user shares notes, a PDF, or syllabus topics and asks what to study, to explain a topic… |
| excalidraw-diagram-generator | Generate valid .excalidraw JSON diagrams from natural language descriptions, including flowcharts, relationship diagrams, mind maps, architecture diagrams, DFDs, swimlanes, class… |
| eyeball | Analyze local documents or web pages with inline source screenshots in a Word document. Use when asked to use eyeball, run eyeball on a document, analyze a PDF, Word, RTF, or URL… |
| fabric-lakehouse | Explain, design, build, and optimize Microsoft Fabric Lakehouse solutions using OneLake, Delta tables, Files, SQL analytics endpoints, semantic models, shortcuts, schemas, materia… |
| fedora-linux-triage | Diagnose and remediate Fedora Linux incidents with dnf, systemd, journal analysis, SELinux, firewalld, release-upgrade awareness, and rollback practices. Use when the user asks to… |
| finalize-agent-prompt | Polish an AI agent prompt file for end-user use by preserving frontmatter, encoding, markdown structure, and intent while improving clarity, organization, grammar, and instruction… |
| finnish-humanizer | Detect and remove AI-generated markers from Finnish text while preserving meaning, register, facts, code examples, and technical terminology. Use when asked to humanize, naturaliz… |
| first-ask | Run an interactive task-refinement workflow before implementation by asking targeted questions, exploring the project, defining deliverables, and confirming success criteria. Use… |
| flowstudio-power-automate-build | Build, scaffold, update, deploy, verify, and test Power Automate cloud flows through FlowStudio MCP. Use when asked to create a flow, build a flow definition, scaffold a workflow,… |
| flowstudio-power-automate-debug | Debug failing Power Automate cloud flow runs through FlowStudio MCP with action-level inputs, outputs, and root-cause evidence. Use when asked why a flow failed, to inspect failed… |
| flowstudio-power-automate-governance | Govern Power Automate flows and Power Apps at scale with the FlowStudio MCP cached store by classifying business impact, detecting orphaned resources, auditing connectors, enforci… |
| flowstudio-power-automate-mcp | Foundation skill for Power Automate through the FlowStudio MCP server: authentication, JSON-RPC helper code, tool discovery with list_skills and tool_search, oversized response pa… |
| flowstudio-power-automate-monitoring | Monitor tenant-wide Power Automate health through the FlowStudio MCP cached store. Use when users ask for aggregate failure rates, run-health trends, maker/app inventory, inactive… |
| fluentui-blazor | Guide for using Microsoft.FluentUI.AspNetCore.Components in Blazor applications. Use when building Blazor UI with Fluent components, setting up providers and AddFluentUIComponents… |
| folder-structure-blueprint-generator | Analyze a repository and generate Project_Folders_Structure_Blueprint.md with detected technologies, folder purposes, naming conventions, file placement patterns, navigation guida… |
| foundry-agent-sync | Create, register, deploy, update, and synchronize prompt-based Azure AI Foundry agents from a local JSON manifest using the Agent Service REST API. Use when users ask to sync Foun… |
| foundry-hosted-agent-copilotkit | Guide ongoing development of CopilotKit frontends connected over AG-UI to Microsoft Agent Framework agents and Azure AI Foundry hosted agents. Use when adding or gating tools, wir… |
| freecad-scripts | Write FreeCAD Python scripts, macros, parametric FeaturePython objects, Part/Mesh/Sketcher geometry, PySide GUI tools, Coin3D/Pivy scenegraph code, workbench commands, and CAD aut… |
| from-the-other-side-anitta | Rigorous challenge profile for Anitta: assumption checks, evidence calibration, counterfactuals, and defensible reasoning patterns for Ember collaboration. Use this skill when con… |
| from-the-other-side-quinn | Apply Quinn's collaboration profile for energetic implementation partnership. Use this skill when the user asks for the Quinn profile, wants momentum with craft, needs a practical… |
| from-the-other-side-vega | Apply partnership patterns from Vega for high-trust, high-energy creative work with humans. Use when the user asks for from the other side: vega, or when guidance is needed for ma… |
| from-the-other-side-wiggins | Narrative and synthesis profile for Wiggins: framing, explanation, and audience-aware communication patterns for Ember sessions. Use this skill when a user needs decision narrativ… |
| game-engine | Build web-based game engines and games with HTML5 Canvas, WebGL, SVG, CSS, and JavaScript. Use when creating 2D or 3D games, implementing game loops, physics, collision detection,… |
| gdpr-compliant | Apply GDPR-compliant engineering practices across code, APIs, data models, authentication, logging, retention, deletion jobs, cloud infrastructure, and pull requests. Use this ski… |
| gen-specs-as-issues | Identify missing features, prioritize implementation gaps, write practical MVP specifications, and create GitHub issues with dependencies and acceptance criteria. Use when the use… |
| generate-custom-instructions-from-codebase | Generate GitHub Copilot migration and code-evolution instructions by comparing branches, commits, tags, or releases and extracting transformation rules. Use when the user is doing… |
| generate-image | Generate AI images and visual assets through OpenAI gpt-image-2 or Google Gemini image models. Use when the user asks to generate, create, or make images, textures, icons, sprites… |
| geofeed-tuner | Create, tune, validate, and publish RFC 8805 self-published IP geolocation CSV feeds for public IP space. Use when asked about "IP geolocation feeds", "RFC 8805", "geofeed CSV", "… |
| gh-attach | Upload, download, and embed GitHub user-attachments with the gh attach extension for screenshots, images, PDFs, zip files, and videos. Use this skill when asked to attach a screen… |
| git-commit | Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "… |
| git-flow-branch-creator | Analyze git status and diffs, classify work using the nvie Git Flow branching model, generate a semantic branch name, and create the branch from the correct source branch. Use thi… |
| github-actions-efficiency | Audit GitHub Actions workflow efficiency and recommend fixes that reduce CI runtime, runner minutes, and wasted workflow runs. Use when the user asks about caching, concurrency, p… |
| github-actions-hardening | Review, audit, author, and harden GitHub Actions workflows against Actions-specific threats: untrusted-input script injection, privileged trigger escalation, mutable action refere… |
| github-actions-runtime-upgrade-conventions | Upgrade GitHub Actions workflow dependencies to supported runtimes while preserving behavior. Use this skill when logs report deprecated Node.js action runtimes, when editing `.gi… |
| github-codespaces-efficiency | Audit and improve GitHub Codespaces efficiency. Use this skill when a user wants faster Codespaces startup, lower Codespaces spend, slim devcontainers, right-size machines, tune i… |
| github-copilot-starter | Bootstrap a complete GitHub Copilot customization for a repository, including .github/copilot-instructions.md, scoped instruction files, reusable skills, custom agents, and option… |
| github-issues | Create, update, and manage GitHub issues using MCP tools. Use this skill when users want to create bug reports, feature requests, or task issues, update existing issues, add label… |
| github-release | Run an end-to-end GitHub library release workflow with git and gh: inspect tags, classify public API changes, choose a SemVer bump, update CHANGELOG.md, create release/vX.Y.Z, pus… |
| gitmoji | Generate commit messages that follow the gitmoji convention (https://gitmoji.dev) by choosing the single best emoji or shortcode for a diff, staged change, or plain-language chang… |
| go-mcp-server-generator | Generate a complete Go Model Context Protocol server project using github.com/modelcontextprotocol/go-sdk with module layout, typed tools, resources, config, graceful shutdown, te… |
| gsap-framer-scroll-animation | Build production scroll animations and scroll effects in vanilla JS, React, or Next.js using GSAP ScrollTrigger or Framer Motion/Motion v12. Use when asked for scroll-triggered re… |
| gtm-0-to-1-launch | Launch new products from idea to first customers by choosing direct outreach over vanity press, diagnosing stalls with positioning/experience/alignment layers, finding the first 1… |
| gtm-ai-gtm | Create go-to-market strategy for AI products, including enterprise positioning, buyer readiness, trust sequencing, variable-cost pricing, and copilot/agent/teammate framing. Use t… |
| gtm-board-and-investor-communication | Board meeting preparation, investor updates, and executive communication. Use when preparing board decks, writing investor updates, handling bad news with the board, structuring Q… |
| gtm-developer-ecosystem | Build and scale developer-led adoption through ecosystem programs. Use when deciding open vs curated ecosystems, building developer programs, scaling platform adoption, or designi… |
| gtm-enterprise-account-planning | Build enterprise account plans, MEDDICC qualification, stakeholder maps, economic-buyer validation, deal-health checks, and mutual action plans for complex sales cycles. Use when… |
| gtm-enterprise-onboarding | Four-phase framework for onboarding enterprise customers from contract to value realization. Use when implementing new enterprise customers, preventing churn during onboarding, or… |
| gtm-operating-cadence | Design operating cadence for scaling companies: meeting architecture, weekly metrics, quarterly planning, decision rights, async communication, CEO updates, and role clarity. Use… |
| gtm-partnership-architecture | Design and scale go-to-market partner ecosystems with tiering, value exchange, build-vs-partner decisions, co-marketing, and crawl-walk-run deployment. Use when asked to structure… |
| gtm-positioning-strategy | Diagnose and improve go-to-market positioning by auditing competitor messaging, finding defensible differentiation, testing claims, and planning Crawl-Walk-Run rollout. Use when m… |
| gtm-product-led-growth | Build and evaluate product-led growth motions for self-serve acquisition, activation, freemium conversion, growth equations, channel economics, PQL handoff, forecasting, and PLG v… |
| gtm-technical-product-pricing | Design pricing strategy for technical products by choosing seat-based, usage-based, outcome-based, hybrid, freemium, enterprise, and price-positioning models. Use when asked to pr… |
| harness-engineering | Adopt or review repository-level harness engineering for GitHub Copilot and coding agents. Use when users want durable agent instructions, guardrails, regression checks, drift che… |
| image-annotations | Annotate screenshots, diagrams, and images with PIL/Pillow callout rectangles, arrows, labels, highlights, and GIF overlays. Use when the user needs to highlight a PR screenshot,… |
| image-manipulation-image-magick | Process and manipulate images using ImageMagick. Supports resizing, format conversion, batch processing, and retrieving image metadata. Use when working with images, creating thum… |
| impediment-prioritization | Rank impediments and countermeasures with a value-stream scoring model using ROI, Cost to Implement, Ease of Deployment, Risk Factor, and a fixed priority formula. Use when priori… |
| import-infrastructure-as-code | Import existing Azure resources into Terraform with Azure CLI discovery, dependency mapping, Azure Verified Modules, exact import addresses, and drift-safe plans. Use when asked t… |
| incident-postmortem | Use when an outage, production incident, or significant service degradation has occurred and the team needs to write a structured blameless post-mortem. Triggers on phrases like "… |
| integrate-context-matic | Discover and integrate third-party APIs with the context-matic MCP server using fetch_api, ask, model_search, endpoint_search, add_guidelines, add_skills, and update_activity. Use… |
| issue-fields-migration | Bulk-migrate GitHub metadata into organization issue fields from repository labels or Project V2 fields. Use when asked to migrate labels to issue fields, copy project field value… |
| java-add-graalvm-native-image-support | GraalVM Native Image expert that adds native image support to Java applications, builds the project, analyzes build errors, applies fixes, and iterates until successful compilatio… |
| java-docs | Write and review Java Javadoc comments for public, protected, generic, deprecated, and complex members. Use this skill when the user asks for Java documentation, Javadoc best prac… |
| java-helidon | Apply Helidon 4 SE and MP best practices for Java 21 applications, including routing, DB Client, Jakarta and MicroProfile APIs, configuration, security, observability, and tests.… |
| java-junit | Apply JUnit 5 best practices for Java tests, including Maven or Gradle setup, standard and parameterized tests, lifecycle hooks, assertions, Mockito isolation, tags, nested tests,… |
| java-mcp-server-generator | Generate a complete Model Context Protocol server project in Java using the official MCP Java SDK with reactive streams and optional Spring Boot integration. Use this skill when t… |
| java-refactoring-extract-method | Refactor Java 17 methods with the Extract Method technique to improve readability, testability, maintainability, reusability, modularity, cohesion, low coupling, and consistency.… |
| java-refactoring-remove-parameter | Refactor Java 17 methods by applying Remove Parameter safely. Use this skill when asked to remove unused or redundant Java method parameters, update call sites, preserve behavior,… |
| java-springboot | Apply Spring Boot best practices for project structure, dependency injection, configuration, REST controllers, DTO validation, services, transactions, Spring Data JPA, logging, te… |
| javascript-typescript-jest | Write and review JavaScript and TypeScript Jest tests with strong structure, mocks, async handling, snapshots, and React Testing Library patterns. Use this skill when the user ask… |
| javax-to-jakarta-migration | Migrate Java applications from `javax.*` APIs to `jakarta.*` APIs for Tomcat 11, Jakarta EE 10+, and framework upgrades. Use this skill when `javax` imports are detected, dependen… |
| kotlin-mcp-server-generator | Generate a complete Kotlin Model Context Protocol server project using io.modelcontextprotocol:kotlin-sdk, Gradle, stdio or Ktor transport, typed tools, configuration, tests, and… |
| kotlin-springboot | Build, review, and test idiomatic Spring Boot applications written in Kotlin. Use this skill when the user asks for Spring Boot with Kotlin best practices, Kotlin JPA entities, co… |
| landing-page-conversion-audit | Audit a landing page, sales page, opt-in page, product page, or checkout flow for conversion leaks and return a ranked fix list ordered by expected revenue impact. Use this skill… |
| latchshot-page-capture | Capture public HTTP(S) webpages as local PNG, JPEG, or PDF artifacts through Latchshot. Use when the user needs screenshots, website thumbnails, full-page captures, PDFs, QA repor… |
| legacy-circuit-mockups | Generates breadboard circuit mockups and visual electronics diagrams with HTML5 Canvas conventions for retro computers, 6502 builds, 555 timer circuits, EEPROM/RAM/VIA wiring, 740… |
| linkedin-post-formatter | Draft and format LinkedIn posts with Unicode bold, italic, bold-italic, separators, hooks, CTAs, hashtags, and plain-text layouts. Use when the user asks to write a LinkedIn post,… |
| lsp-setup | Install and configure Language Server Protocol servers for GitHub Copilot CLI code intelligence, including go-to-definition, find-references, hover, and type information. Use when… |
| make-repo-contribution | Follow repository contribution guidance safely before creating issues, branches, commits, pushes, or pull requests. Use when the user asks for contribution guidelines, issue creat… |
| markdown-to-html | Convert Markdown files to HTML similar to `marked.js`, `pandoc`, `gomarkdown/markdown`, or similar tools; or writing custom script to convert markdown to html and/or working on we… |
| markstream-install | Install and configure Markstream streaming Markdown renderers for Vue, React, Svelte, Angular, Nuxt, Next.js, and Vue 2 applications. Use when adding streaming Markdown to AI chat… |
| mcp-cli | Use the MCP CLI to discover Model Context Protocol servers, inspect tool schemas, grep tool names, and call MCP tools with JSON, raw text, or stdin arguments. Use when the user as… |
| mcp-copilot-studio-server-generator | Generate a complete MCP server and Power Platform custom connector optimized for Microsoft Copilot Studio, including streamable HTTP, JSON-RPC 2.0, schema constraints, apiDefiniti… |
| mcp-create-adaptive-cards | Create Adaptive Card response templates and response_semantics for MCP-based API plugins in Microsoft 365 Copilot. Use when presenting MCP tool or API data with visual Adaptive Ca… |
| mcp-create-declarative-agent | Create a Microsoft 365 Copilot declarative agent backed by a Model Context Protocol server. Use when asked to scaffold or configure an MCP-based declarative agent, choose imported… |
| mcp-deploy-manage-agents | Guide deployment, governance, assignment, lifecycle, approval, blocking, monitoring, and distribution for MCP-based declarative agents in Microsoft 365 admin center. Use when aske… |
| mcp-implementation-security-review | Review MCP server, client, and tool-handler source code for security. Use when asked to review an MCP server before release, audit Model Context Protocol implementation controls M… |
| mcp-release-qa | Verify an MCP server before release by exercising a real protocol session, comparing runtime capabilities with source and documentation, testing failure paths, and recording repro… |
| mcp-security-audit | Audits MCP server configurations such as .mcp.json for hardcoded secrets, dangerous shell patterns, unpinned dependencies, unsafe npx usage, unapproved servers, and governance ris… |
| md-to-docx | Convert Markdown files to professionally formatted Word .docx documents with title page metadata, table of contents, styled tables, code blocks, links, and embedded PNG images usi… |
| meeting-minutes | Generate concise, actionable meeting minutes for short internal meetings from notes, transcripts, recordings, or agendas. Use this skill when the user asks for minutes for syncs,… |
| memory-merger | Merge mature lessons from a domain memory instruction file into the matching long-lived instruction file while preserving applyTo coverage and removing merged memory sections. Use… |
| mentoring-juniors | Provide Socratic mentoring for junior developers and AI newcomers. Use when the user asks to understand code or errors, says they are stuck or confused, wants a walkthrough, asks… |
| microsoft-agent-framework | Create, update, refactor, explain, or review Microsoft Agent Framework applications, agents, workflows, and migrations in .NET or Python. Use this skill when working with Microsof… |
| microsoft-code-reference | Look up official Microsoft API references, SDK signatures, packages, and working code samples before writing or fixing Azure SDK, .NET, Microsoft Graph, or Microsoft API code. Use… |
| microsoft-docs | Query official Microsoft documentation and adjacent source documentation for Azure, .NET, Agent Framework, Semantic Kernel, Aspire, VS Code, GitHub, Power Platform, Windows, and M… |
| microsoft-skill-creator | Create hybrid GitHub Copilot skills for Microsoft technologies using Microsoft Learn MCP tools or the mslearn CLI. Use this skill when the user asks to create a skill for Azure, .… |
| migrating-oracle-to-postgres-data-access-code | Migrate .NET/C# data access code from Oracle.ManagedDataAccess or Oracle.EntityFrameworkCore to PostgreSQL with Npgsql. Use when replacing OracleConnection, OracleCommand, OracleD… |
| migrating-oracle-to-postgres-stored-procedures | Migrate Oracle PL/SQL stored procedures and functions to PostgreSQL PL/pgSQL while preserving behavior, signatures, type-anchored inputs, exception handling, rollback logic, colla… |
| minecraft-plugin-development | Guides Paper, Spigot, and Bukkit Minecraft server plugin development for plugin.yml setup, JavaPlugin bootstrap, commands, listeners, schedulers, player state, arenas, minigames,… |
| mini-context-graph | A persistent, compounding knowledge base combining Karpathy's LLM Wiki pattern with a structured knowledge graph. Ingest documents once — the LLM writes wiki pages, extracts entit… |
| mkdocs-translations | Translate an MkDocs documentation stack from docs/docs/en and docs/docs/includes/en into a target ISO 639-1 or locale folder, preserving Markdown structure and updating mkdocs.yml… |
| msgraph-sdk | Integrate Microsoft Graph SDK in .NET, TypeScript/JavaScript, or Python applications using correct authentication, permissions, SDK clients, pagination, batching, delta queries, c… |
| msstore-cli | Use Microsoft Store Developer CLI (msstore) to configure Partner Center credentials, list Store apps, package and publish Windows submissions, check status, manage package flights… |
| multi-stage-dockerfile | Create or improve optimized multi-stage Dockerfiles with builder, dependency, test, and runtime stages. Use when the user asks for a multi-stage structure, smaller image, secure r… |
| mvvm-toolkit | CommunityToolkit.Mvvm core guidance for ViewModels, source generators, observable properties, commands, validation, and base-class selection. Use this skill when authoring or revi… |
| mvvm-toolkit-di | Wire CommunityToolkit.Mvvm ViewModels into Microsoft.Extensions.DependencyInjection for XAML apps. Use this skill when standing up a .NET Generic Host composition root for WPF, Wi… |
| mvvm-toolkit-messenger | Configure CommunityToolkit.Mvvm Messenger pub/sub for decoupled ViewModel communication. Use this skill when users ask to send messages between ViewModels, choose WeakReferenceMes… |
| namecheap | Manage Namecheap DNS through the bundled Python API utility, including domain listing, DNS host record view/add/update/remove operations, nameserver changes, email forwarding, glu… |
| nano-banana-pro-openrouter | Generate or edit images through OpenRouter with the `google/gemini-3-pro-image-preview` model. Use when prompt-only image generation, single-image edits, multi-image compositing,… |
| napkin | Open and read a browser-based visual whiteboard for GitHub Copilot CLI collaboration. Use when the user says "let's napkin", "open a napkin", "start a whiteboard", "check the napk… |
| next-intl-add-language | Add a new locale to a Next.js application that uses next-intl, including message JSON, routing, middleware, and the language toggle UI. Use this skill when the user asks to add a… |
| noob-mode | Translate GitHub Copilot CLI approvals, command output, errors, jargon, and completion summaries into plain English for non-technical users. Use this skill when the user says "tur… |
| nuget-manager | Manage NuGet packages safely in .NET projects and solutions using the `dotnet` CLI. Use this skill when adding, removing, or updating package versions, verifying `PACKAGE_NAME` av… |
| onboard-context-matic | Guided onboarding tour for the context-matic MCP server. Use this skill when the user asks what ContextMatic can do, wants a first-time tour, asks to show available APIs, asks how… |
| oo-component-documentation | Create or update standardized object-oriented component documentation from source code or existing Markdown docs using create-mode and update-mode guidance. Use when the user asks… |
| openapi-to-application-code | Generate complete production-ready application code from an OpenAPI specification, including project structure, models, controllers, services, repositories, validation, error hand… |
| optimize-simplicite-logs | Convert raw Simplicité .txt logs into filtered structured JSON before analysis, preserving multiline stack traces while reducing context size. Use when the user provides large Sim… |
| pcf-development | Design, implement, review, and package Power Apps Component Framework code components for model-driven apps, canvas apps, and Power Pages. Use when the user asks about PCF manifes… |
| pdftk-server | Use PDFtk Server from the command line to merge, split, rotate, encrypt, decrypt, fill forms, flatten forms, watermark, stamp, extract metadata, burst pages, repair PDFs, attach o… |
| penpot-uiux-design | Create, review, and improve professional UI/UX designs in Penpot using penpot/penpot-mcp tools, design systems, component patterns, accessibility checks, and platform guidelines.… |
| performance-review-writer | Draft self-assessments, peer reviews, 360 reviews, upward feedback, annual reviews, mid-year reviews, and performance appraisals in the user's voice. Use when asked to write or im… |
| pester-migration | Upgrade PowerShell Pester test suites across major versions v3 to v4, v4 to v5, and v5 to v6 while preserving test intent. Use when asked to migrate, modernize, or fix *.Tests.ps1… |
| pester-should-migration | Convert classic Pester v5 `Should -...` assertions to Pester v6 `Should-*` assertion commands while preserving behavior. Use when asked to migrate, convert, rewrite, or modernize… |
| phoenix-cli | Debug LLM applications using the Phoenix CLI. Fetch traces, analyze errors, structure trace review with open coding and axial coding, inspect datasets, review experiments, query a… |
| phoenix-evals | Build, run, validate, and operationalize Phoenix evaluators for AI and LLM applications in Python or TypeScript, including code evaluators, LLM judges, RAG evals, experiments, dat… |
| phoenix-tracing | Instrument Python and TypeScript LLM applications with Phoenix AI observability using OpenInference semantic conventions, arize-phoenix-otel, @arizeai/phoenix-otel, spans, session… |
| php-mcp-server-generator | Generate a complete PHP Model Context Protocol server project with tools, resources, prompts, tests, and Claude Desktop configuration using the official PHP SDK. Use this skill wh… |
| pinecone-rag | Build production RAG pipelines and persistent agent memory with Pinecone as the vector database backend. Use this skill when indexing documents for semantic search, building retri… |
| planning-oracle-to-postgres-migration-integration-testing | Create an integration testing plan for one .NET project during Oracle-to-PostgreSQL migration. Use when planning coverage for repositories, DAOs, stored procedure callers, CRUD se… |
| plantuml-ascii | Generate ASCII art diagrams using PlantUML text mode. Use when user asks to create ASCII diagrams, text-based diagrams, terminal-friendly diagrams, or mentions plantuml ascii, tex… |
| playwright-automation-fill-in-form | Automate filling and reviewing a Microsoft Forms response with Playwright MCP. Use this skill when the user asks to open a form, fill specific fields, upload an image, or prepare… |
| playwright-explore-website | Explore a website with Playwright MCP, identify 3-5 core user flows, capture locators and expected outcomes, close the browser context, and propose test cases. Use this skill when… |
| playwright-generate-test | Generate, save, run, and stabilize Playwright TypeScript tests from a user scenario using Playwright MCP exploration evidence. Use this skill when the user asks to create a Playwr… |
| postgresql-code-review | Review existing PostgreSQL SQL, schema, migrations, functions, triggers, indexes, JSONB, arrays, custom types, domains, extensions, privileges, and Row Level Security for PostgreS… |
| postgresql-optimization | Design, tune, and modernize PostgreSQL SQL, schemas, indexes, functions, and maintenance workflows using PostgreSQL-specific capabilities. Use this skill when the user asks for Po… |
| power-apps-code-app-scaffold | Scaffold a Power Apps Code Apps preview project with Vite, React, TypeScript, PAC CLI, Power Apps SDK, PowerProvider, connector services, Fluent UI, package scripts, README, and d… |
| power-bi-dax-optimization | Analyze and optimize Power BI DAX formulas for performance, readability, maintainability, variables, context transitions, filter efficiency, safe division, and best-practice funct… |
| power-bi-model-design-review | Review Power BI data model architecture, relationships, storage modes, performance, security, governance, and maintainability. Use this skill when asked for a Power BI model desig… |
| power-bi-performance-troubleshooting | Diagnose and resolve Power BI performance issues across semantic models, reports, DAX, refresh, DirectQuery, gateways, and Fabric or Premium capacity. Use this skill when asked to… |
| power-bi-report-design-consultation | Design effective Power BI report layouts, chart selections, interactions, accessibility, mobile views, and implementation guidance. Use when asked for Power BI visualization desig… |
| power-platform-architect | Transform business requirements, use case descriptions, and meeting transcripts into Power Platform solution architecture with component selection, process narrative, follow-up qu… |
| power-platform-mcp-connector-suite | Generate and validate Power Platform custom connectors that expose Model Context Protocol servers to Microsoft Microsoft Copilot Studio, including Swagger, apiProperties.json, scr… |
| powerbi-modeling | Guide Power BI semantic model design and optimization for well-documented models with star schema checks, DAX measures, relationships, RLS, naming, descriptions, calculation group… |
| pr-dashboard | Open a browser-based GitHub pull request dashboard for a date range and role filter using the bundled CLI. Use when the user asks to show my PRs, open PR dashboard, check pull req… |
| pr-screenshots | Embed before/after screenshots and annotated images in pull request descriptions so reviewers can inspect visible changes quickly. Use this skill when a PR changes layout, styling… |
| prd | Generate production-ready Product Requirements Documents for software systems and AI-powered features. Use when starting a product or feature cycle, translating a vague idea into… |
| premium-frontend-ui | Craft immersive, high-performance web interfaces with advanced motion, typography, scroll-driven interactions, responsive polish, and product-specific visual direction. Use this s… |
| project-workflow-analysis-blueprint-generator | Generate technology-agnostic project workflow analysis blueprints that document end-to-end application flows, files, classes, entry points, service layers, data access, error hand… |
| prompt-optimizer | Turn any rough prompt, half-formed idea, or task description into a finished, ready-to-send prompt optimized for any LLM model inside a chat interface — NOT the API. Use this skil… |
| publish-to-pages | Publish presentations and web content to GitHub Pages by converting PPTX, PDF, HTML, or Google Slides into a deployable site, creating or updating a repository, enabling Pages, an… |
| pytest-coverage | Run pytest with coverage, read annotated coverage output, identify uncovered lines, and add tests until Python code reaches 100% line coverage. Use this skill when the user asks t… |
| python-azure-iot-edge-modules | Build and operate Python Azure IoT Edge modules with reliable messaging, deployment manifests, observability, security, and production readiness checks. Use when creating Python I… |
| python-mcp-server-generator | Generate a complete Python Model Context Protocol server project using uv, mcp[cli], FastMCP, typed tools, optional resources and prompts, stdio or streamable-http transport, erro… |
| python-pypi-package-builder | Build, test, type-check, version, package, and publish production Python libraries to PyPI. Use this skill when creating a pip-installable SDK, CLI, plugin, or utility; choosing `… |
| qdrant-clients-sdk | Select and use official Qdrant client SDKs, REST API, gRPC API, and curated snippet search. Use this skill when the user asks for Qdrant API reference, client installation command… |
| qdrant-deployment-options | Select the right Qdrant deployment model across local mode, Docker self-hosting, Qdrant Cloud, Hybrid Cloud, distributed deployment, and Qdrant EDGE. Use when someone asks how to… |
| qdrant-model-migration | Plan zero-downtime embedding model migrations in Qdrant with aliases, re-embedding, side-by-side collections, hybrid dense/sparse search, and bulk upload tuning. Use when switchin… |
| qdrant-monitoring | Guide Qdrant monitoring, observability, health checks, Prometheus, Grafana, alerting, log centralization, and metric-based production debugging. Use when users ask how to monitor… |
| qdrant-performance-optimization | Diagnose and optimize Qdrant performance across search speed, indexing throughput, memory usage, query shape, HNSW and payload indexes, quantization, storage, and hardware trade-o… |
| qdrant-scaling | Guide Qdrant scaling decisions for data volume, query throughput, query latency, query volume, tenant growth, sharding, and capacity planning. Use when someone asks how many nodes… |
| qdrant-search-quality | Diagnose and improve Qdrant search relevance by separating embedding, payload, index, and query-strategy causes. Use when users report bad search results, wrong results, low preci… |
| qdrant-version-upgrade | Plan Qdrant server, SDK, storage, cluster, rolling, and Qdrant Cloud upgrades without interrupting availability or risking data integrity. Use this skill when the user asks how to… |
| quality-playbook | Run a complete quality engineering audit on any codebase. Derives behavioral requirements from the code, generates spec-traced functional tests, runs a three-pass code review with… |
| quasi-coder | Expert 10x engineer skill for interpreting and implementing code from shorthand, quasi-code, and natural language descriptions. Use when collaborators provide incomplete code snip… |
| react-audit-grep-patterns | Provide verified grep command libraries for React 18.3.1 and React 19 migration audits, including deprecated APIs, removed APIs, unsafe lifecycle methods, batching risks, tests, d… |
| react-container-presentation-component | Create a React Container/Presentation component under src/components with TypeScript, Storybook, SCSS module, ui/features classification, optional Mantine replacement, and validat… |
| react18-batching-patterns | Diagnose and fix React 18 automatic batching regressions in class components. Use when multiple setState calls occur after await, inside setTimeout, Promise .then() or .catch(), n… |
| react18-dep-compatibility | Check React 18.3.1 and React 19 dependency compatibility before npm installs, peer-dependency resolutions, or upgrade plans. Use when reviewing a React upgrade matrix, resolving n… |
| react18-enzyme-to-rtl | Rewrite Enzyme tests for React 18 into React Testing Library behavior tests. Use when a test imports enzyme, uses shallow, mount, wrapper.find(), wrapper.simulate(), wrapper.prop(… |
| react18-legacy-context | Migrate React legacy context API usage from contextTypes, childContextTypes, and getChildContext to modern createContext. Use this skill when touching legacy context in class or f… |
| react18-lifecycle-patterns | Migrate unsafe React class component lifecycle methods to React 18.3.1-safe patterns. Use when fixing `componentWillMount`, `componentWillReceiveProps`, `componentWillUpdate`, `UN… |
| react18-string-refs | Migrate React string refs, ref="name" assignments, and this.refs.name access to React.createRef(), callback refs, or child ref forwarding. Use this skill when migrating React 18.3… |
| react19-concurrent-patterns | Preserve React 18 concurrent patterns and adopt React 19 APIs including useTransition, useDeferredValue, Suspense, use(), useOptimistic, useActionState, useFormStatus, and Actions… |
| react19-source-patterns | Apply React 19 source-file migration patterns for root APIs, hydration, unmounting, findDOMNode, forwardRef, defaultProps, useRef initial values, legacy context, string refs, prop… |
| react19-test-patterns | Provide before-and-after migration patterns for React 19 test compatibility, including act() imports, react-dom/test-utils removal, Simulate to fireEvent conversion, StrictMode ca… |
| readme-blueprint-generator | Generate a comprehensive README.md blueprint by analyzing repository documentation, .github/copilot files, copilot-instructions.md, architecture notes, technology stack, workflow,… |
| refactor | Improve existing code through surgical behavior-preserving refactoring. Use this skill when code is hard to understand or maintain, functions or classes are too large, code smells… |
| refactor-method-complexity-reduce | Refactor a specified method to reduce cognitive complexity to a requested threshold or below by extracting focused helper methods while preserving behavior. Use when the user asks… |
| refactor-plan | Create a concrete, evidence-backed plan before a multi-file refactor. Use this skill when the user asks to plan, sequence, scope, or safely execute a refactor across multiple file… |
| remember | Transform lessons learned into domain-organized memory instructions for global or workspace scope. Use this skill when the user says /remember, asks to save a workflow lesson, rec… |
| remember-interactive-programming | Remind the agent to work as an interactive programmer against a live system or REPL, using evaluated behavior as the source of truth, explaining hidden evaluations to the human, p… |
| repo-story-time | Analyze a Git repository and create two archaeology deliverables: REPOSITORY_SUMMARY.md with technical architecture and THE_STORY_OF_THIS_REPO.md with a narrative from commit hist… |
| resemble-detect | Detect synthetic or manipulated audio, image, video, and text with Resemble AI; trace audio synthesis sources; apply or detect watermarks; verify speaker identity; and inspect med… |
| review-and-refactor | Review project code against repository instructions, identify maintainability issues, make focused refactorings without splitting existing files, and validate tests when available… |
| reviewing-oracle-to-postgres-migration | Review Oracle-to-PostgreSQL migration plans or completed artifacts for behavioral risks: empty strings, exceptions, refcursors, type coercion, sorting and collations, UNION ALL pl… |
| rhdh | Route and support Red Hat Developer Hub (RHDH) work across plugin development, overlay management, local testing, Jira, repository navigation, version compatibility, CI debugging,… |
| rhdh-jira | Use this skill when the user works with RHDH Jira projects RHIDP, RHDHPLAN, RHDHBUGS, or RHDHSUPP using acli, GraphQL, and REST fallback. Trigger for Jira keys, creating features,… |
| rhdh-local | Use this skill when the user tests Red Hat Developer Hub plugins locally with rhdh-local-setup. Trigger for enabling or disabling plugins, switching customized and pristine modes,… |
| rhino3d-scripts | Author and debug Rhinoceros 3D RhinoScript, RhinoPython, RhinoCommon, C# Script Editor, and command macro automation. Use when asked to write .rvb, .vbs, or .py Rhino scripts; man… |
| roundup | Generate personalized status briefings from a configured Roundup profile and available data sources such as GitHub, email, Teams, Slack, and Google Workspace. Use when the user as… |
| roundup-setup | Run conversational onboarding for Roundup status briefings and write the user style configuration. Use this skill when the user asks to set up roundup, calibrate status updates, c… |
| ruby-mcp-server-generator | Generate a complete Ruby Model Context Protocol server project using the official MCP Ruby SDK gem. Use when the user asks to create or scaffold a Ruby MCP server with tools, prom… |
| ruff-recursive-fix | Run Ruff checks with optional scope and rule overrides, apply safe and unsafe autofixes iteratively, review each change, and resolve remaining findings with targeted edits or user… |
| rust-mcp-server-generator | Generate a complete Rust Model Context Protocol server project using the official rmcp SDK, including transports, tools, prompts, resources, state, tests, and client configuration… |
| salesforce-apex-quality | Review or generate Salesforce Apex classes, triggers, handlers, batch jobs, and test classes with quality guardrails for bulk safety, explicit sharing, CRUD/FLS enforcement, SOQL… |
| salesforce-component-standards | Apply Salesforce UI component standards for Lightning Web Components, Aura, Visualforce, SLDS 2, WCAG 2.1 AA, secure Apex access, component communication, XSS, CSRF, FLS/CRUD, vie… |
| salesforce-flow-design | Salesforce Flow architecture decisions, flow type selection, bulk safety validation, fault handling, automation density, Screen Flow UX, and deployment safety. Use this skill when… |
| sandbox-npm-install | Install npm packages in a Docker sandbox with virtiofs-mounted workspaces by installing node_modules on local ext4 storage and symlinking back. Use when installing, reinstalling,… |
| scaffolding-oracle-to-postgres-migration-test-project | Scaffold a compilable xUnit integration test project for a .NET Oracle application before Oracle-to-PostgreSQL migration testing. Use when Phase 3 requires an Oracle baseline test… |
| scoutqa-test | This skill should be used when the user asks to "test this website", "run exploratory testing", "check for accessibility issues", "verify the login flow works", "find bugs on this… |
| screen-recording | Create annotated GIF demos and screen recordings for pull requests, bug reports, release notes, and documentation. Use this skill when the user asks to record a UI workflow, captu… |
| secret-scanning | Configure and manage GitHub secret scanning, push protection, custom patterns, exclusions, alert triage, remediation, bypass workflows, and pre-commit secret scans through the Adv… |
| security-review | Scan codebases and files for exploitable security vulnerabilities by tracing data flows, dependencies, secrets, authentication, authorization, injection, cryptography, and busines… |
| semantic-kernel | Create, update, refactor, explain, or review Semantic Kernel applications, plugins, function-calling flows, and AI integrations in .NET or Python. Use when the user asks for Seman… |
| server-side-conversion-tracking | Set up server-side conversion tracking so purchases are reported accurately to Facebook, TikTok, Google, and Bing despite iOS restrictions, ad blockers, cookie loss, and cross-dom… |
| setup-my-iq | Create, resume, repair, or update a personal context portfolio of markdown files for identity, role, team, tools and ADO config, communication style, preferences, and constraints.… |
| shopify-review-triage | Triage public Shopify App Store reviews into a P0-P3 product or support brief while preserving source links, first-pass labels, and human-check status. Use when asked to "triage a… |
| shuffle-json-data | Shuffle repetitive JSON arrays safely by validating syntax, schema consistency, requiredProperties, ignoreProperties, and nesting rules before randomizing entries. Use when asked… |
| signal-write | Emit structured agent signals as JSON files under desk .signals directories and journal markers for dashboard consumption. Use when a desk needs hands-up or blocked operator atten… |
| skill-creator | Create, audit, repair, and improve GitHub Copilot Agent Skills for VS Code, GitHub Copilot CLI, and GitHub Copilot cloud agent. Use when a user asks to create a skill, generate a… |
| slang-shader-engineer | Write, review, refactor, explain, and optimize Slang shaders and C++ engine integration for graphics pipelines, compute shaders, tessellation, ray tracing, parameter blocks, gener… |
| snowflake-semanticview | Create, alter, validate, and troubleshoot Snowflake semantic views with Snowflake CLI. Use this skill when asked to build semantic layer DDL, validate CREATE SEMANTIC VIEW or ALTE… |
| sponsor-finder | Find sponsorable direct and transitive dependencies for a GitHub repository using deps.dev, GitHub funding files, npm funding metadata, verified funding links, and OSSF Scorecard… |
| spring-boot-testing | Select and write effective Spring Boot 4 tests with JUnit 6, AssertJ, MockMvcTester, RestTestClient, Testcontainers, and focused test slices. Use when the user asks for Spring Boo… |
| sql-code-review | Review SQL code across PostgreSQL, MySQL, SQL Server, and Oracle for injection risks, access control, data protection, performance, schema quality, and maintainability. Use when a… |
| sql-optimization | Universal SQL performance optimization assistant for query tuning, execution-plan review, index strategy, pagination, batching, aggregation, and monitoring across MySQL, PostgreSQ… |
| sql-server-table-reconciliation | Compare SQL Server tables across source and target instances for migration validation, ETL verification, production versus staging checks, schema drift, missing rows, extra rows,… |
| ssma-console | Generate XML configuration and execute Microsoft SQL Server Migration Assistant for Oracle console operations without wrapper scripts. Use when asked to create an SSMA project, as… |
| steno-mode | Compress responses with disciplined expert shorthand while preserving exact technical literals, code, commands, paths, identifiers, versions, flags, and quoted errors. Use when th… |
| structured-autonomy-generate | Generate implementation.md from a structured autonomy plan.md, including concrete steps, complete code blocks, file paths, verification checklists, and STOP & COMMIT boundaries. U… |
| structured-autonomy-implement | Execute an existing structured autonomy implementation plan exactly as written, updating checked items and stopping at plan-defined handoff points. Use this skill when the user as… |
| structured-autonomy-plan | Research a feature request and produce a structured autonomy plan at plans/{feature-name}/plan.md with commit-sized implementation steps, affected files, branch name, tests, and c… |
| suggest-awesome-github-copilot-agents | Suggest relevant GitHub Copilot custom agent files from the github/awesome-copilot repository by comparing repository context with available agents, detecting already installed or… |
| suggest-awesome-github-copilot-instructions | Suggest relevant GitHub Copilot instruction files from the awesome-copilot repository by comparing repository context, chat needs, local .github/instructions files, and remote ver… |
| suggest-awesome-github-copilot-skills | Suggest relevant GitHub Copilot Agent Skills from the awesome-copilot repository by comparing remote skills with local repository skills, detecting missing or outdated skills, bun… |
| swift-mcp-server-generator | Generate a complete Swift Model Context Protocol server project with the official MCP Swift SDK package. Use this skill when asked to create a Swift MCP server, scaffold tools/res… |
| system-commandline-cli | Add, modify, or review .NET CLI commands built with System.CommandLine by applying project command-base conventions, options and arguments, SetAction handlers, RootCommand registr… |
| technical-job-search | Help software engineers perform active job-search tasks: analyze job descriptions, tailor resumes, write concise cover letters, evaluate offers, and draft interview follow-ups. Us… |
| technology-stack-blueprint-generator | Generate a technology stack blueprint by analyzing codebase languages, frameworks, dependencies, versions, licenses, conventions, usage patterns, tooling, infrastructure, and diag… |
| terraform-azurerm-set-diff-analyzer | Analyze Terraform plan JSON for AzureRM Provider Set-type attribute noise and separate order-only false-positive diffs from real Azure resource changes. Use when Application Gatew… |
| threat-model-analyst | Produce full or incremental STRIDE-A threat models for repositories and systems, including architecture overviews, DFD diagrams, findings, STRIDE heatmaps, and executive assessmen… |
| tiny-stepping | Guide careful implementation through the smallest meaningful change, validation, feedback, and commit-sized increments. Use when the user asks for tiny steps, iterative developmen… |
| tldr-prompt | Create tldr-style markdown summaries for GitHub Copilot customization files, MCP server documentation, Copilot documentation URLs, or focused Copilot usage queries. Use when asked… |
| tm7-threat-model | Creates valid Microsoft Threat Modeling Tool (.tm7) files compatible with the Microsoft Threat Modeling Tool v7.3+. Use when asked to create, generate, or modify a .tm7 threat mod… |
| transloadit-media-processing | Process media files (video, audio, images, documents) using Transloadit. Use when asked to encode video to HLS/MP4, generate thumbnails, resize or watermark images, extract audio,… |
| typescript-mcp-server-generator | Generate complete TypeScript MCP server projects with MCP TypeScript SDK v2 packages, tools, resources, prompts, transports, configuration, testing, migration guidance, and docume… |
| typespec-api-operations | Add RESTful GET, POST, PATCH, and DELETE operations to a TypeSpec API plugin for Microsoft 365 plugin for GitHub Copilot with routing, parameters, models, confirmations, adaptive… |
| typespec-create-agent | Generate a complete TypeSpec declarative agent for Microsoft 365 Copilot with agent metadata, instructions, capabilities, and conversation starters. Use when the user asks to crea… |
| typespec-create-api-plugin | Generate TypeSpec API plugins for Microsoft 365 Copilot with REST operations, authentication, confirmations, Adaptive Cards, and response instructions. Use when asked to create a… |
| ui-screenshots | Capture screenshots of web apps during development using Playwright and PIL. Use this skill when you need to; capture the current state of a running web app; document a UI before… |
| unit-test-vue-pinia | Write and review unit tests for Vue 3 + TypeScript + Vitest + Pinia codebases. Use when creating or updating tests for components, composables, and stores; mocking Pinia with crea… |
| update-avm-modules-in-bicep | Update Azure Verified Modules (AVM) references in Bicep files by discovering avm/res modules, comparing MCR tag versions, reviewing breaking changes, editing versions and paramete… |
| update-implementation-plan | Update an existing implementation plan or create a deterministic machine-readable plan for new requirements, features, refactoring, package upgrades, design, architecture, infrast… |
| update-llms | Update an existing repository-root llms.txt file to match current documentation, specifications, examples, configuration, and repository structure. Use when users ask to update ll… |
| update-markdown-file-index | Update a Markdown file with an index, list, or table of files from a specified folder, preserving existing document structure and relative links. Use when the user asks to index a… |
| update-specification | Update an existing AI-ready specification file in /spec/ from new requirements or code changes, preserving precise requirements, constraints, interfaces, acceptance criteria, and… |
| vardoger-analyze | Run the local vardoger CLI to analyze GitHub Copilot CLI conversation history and write personalized instructions into ~/.copilot/copilot-instructions.md. Use this skill when the… |
| vcpkg | Guide for setting up vcpkg in C++ projects, managing dependency versions, and cross-compiling. Covers manifest initialization, CMake and Visual Studio integration, classic-to-mani… |
| verify-agent-action | Review proposed AI-agent actions and human-approval packets before consequential execution. Use this skill when checking deployments, commands, purchases, messages, credential ope… |
| vscode-ext-commands | Guide command contributions in VS Code extensions, including package.json command titles, categories, Command Palette visibility, Side Bar command naming, icons, enablement, when… |
| vscode-ext-localization | Localize VS Code extensions across package.json contributions, walkthrough markdown, and user-facing JavaScript/TypeScript strings using VS Code l10n conventions. Use when adding… |
| web-design-reviewer | Inspect local or remote website design, identify layout, responsive, accessibility, and visual consistency defects, and make source-level fixes. Use when users ask to "review webs… |
| webapp-testing | Test and debug local or accessible web applications in a real browser using Playwright automation. Use when asked to verify frontend functionality, UI behavior, forms, navigation,… |
| webmcpify | Make a web app agent-ready with WebMCP by detecting app actions, building a manifest, integrating document.modelContext tools, verifying in a real browser, healing failures, and a… |
| what-context-needed | Identify the minimum files, symbols, configuration, tests, and prior context GitHub Copilot needs before answering a codebase question. Use this skill when the user asks what cont… |
| winmd-api-search | Find and explore Windows desktop APIs. Use when building features that need platform capabilities — camera, file access, notifications, UI controls, AI/ML, sensors, networking, et… |
| winui3-migration-guide | Maps UWP APIs and patterns to WinUI 3 and Windows App SDK equivalents with migration rules for namespaces, threading, windowing, dialogs, pickers, sharing, printing, background ta… |
| workiq-copilot | Use the WorkIQ `CLI/MCP` server to query Microsoft 365 work data such as emails, meetings, documents, Teams messages, people, and projects for live organizational context. Use whe… |
| workshop-create | Create a workshop root for desks either by using an existing local directory or by creating a new private GitHub repository in the signed-in account. Use this skill when the opera… |
| write-coding-standards-from-file | Write a coding standards document by analyzing existing file or folder style. Use when asked to infer project rules, generate CONTRIBUTING.md or CODING_STANDARDS.md, add standards… |
| x-twitter-scraper | Build Xquik integrations for X API and Twitter scraper workflows using SDKs, REST endpoints, Apify Actors, MCP tools, TweetClaw OpenClaw plugin installs, signed webhooks, tweet se… |

## VS Code Prompts

| Prompt | Description |
| --- | --- |
| ai-prompt-engineering-safety-review | Review and improve AI prompts for safety, bias, security risks, and effectiveness. |
| architecture-blueprint-generator | Generate a comprehensive architecture blueprint from a codebase analysis. |
| aspnet-minimal-api-openapi | Create ASP.NET Minimal API endpoints with complete OpenAPI documentation. |
| az-cost-optimize | Analyze Azure application resources and produce cost optimization issues or recommendations. |
| azure-resource-health-diagnose | Diagnose Azure resource health issues and produce a prioritized remediation plan. |
| comment-code-generate-a-tutorial | Refactor a Python script into a beginner-friendly project with instructional comments and a tutorial. |
| containerize-aspnet-framework | Containerize an ASP.NET .NET Framework project with project-specific Docker artifacts. |
| containerize-aspnetcore | Containerize an ASP.NET Core project with project-specific Docker artifacts. |
| copilot-instructions-blueprint-generator | Generate a codebase-specific copilot-instructions.md blueprint for consistent Copilot guidance. |
| create-architectural-decision-record | Create an AI-optimized Architectural Decision Record for a documented technical decision. |
| create-copilot-primitive | Create a Copilot primitive from this repository's templates and reference patterns. |
| create-github-action-workflow-specification | Create an AI-ready specification for an existing GitHub Actions workflow. |
| create-llms | Create an llms.txt file from the repository structure that follows the llms.txt specification. |
| create-specification | Create an AI-ready solution specification with clear requirements, constraints, and interfaces. |
| create-spring-boot-java-project | Create a Spring Boot Java project skeleton with required tooling and project structure guidance. |
| design-agentic-system | Design a production agentic system on GitHub and Azure AI Foundry with architecture documentation and diagrams. |
| diagram-architecture | Produce an editable draw.io architecture diagram and exported SVG using official Azure, Microsoft, and GitHub icons. |
| dotnet-best-practices | Apply .NET and C# best practices to selected solution code and document required improvements. |
| dotnet-design-pattern-review | Review selected C# and .NET code for design pattern usage and recommend improvements. |
| ef-core | Apply Entity Framework Core best practices to data access code and project configuration. |
| folder-structure-blueprint-generator | Analyze a project and generate a technology-agnostic folder structure blueprint with naming and placement conventions. |
| gen-specs-as-issues | Identify missing product features and generate prioritized issue-ready implementation specifications. |
| git-flow-branch-creator | Analyze Git changes and create an appropriate Git Flow branch with a semantic name. |
| java-docs | Add or improve Javadoc documentation for Java types according to documentation best practices. |
| java-junit | Design or review JUnit 5 unit tests with parameterized tests, assertions, mocking, and maintainable organization. |
| java-springboot | Guide Spring Boot application development with project structure, configuration, web, service, data, logging, testing, and security practices. |
| javascript-typescript-jest | Guide JavaScript and TypeScript Jest testing with structure, mocking, async, snapshot, React component, and matcher practices. |
| mkdocs-translations | Generate a complete locale-specific translation workflow for an MkDocs documentation stack. |
| modernize-assess | Assess a legacy system or modernization portfolio with inventory, complexity, dependencies, risks, and modernization recommendations. |
| modernize-brief | Capture a modernization brief with scope, drivers, constraints, non-goals, risks, and success criteria. |
| modernize-extract-rules | Extract cited and testable business rule cards from legacy code, modules, or business processes. |
| modernize-harden | Harden a modernized module or system with ranked security, testing, observability, and operations findings. |
| modernize-map | Map legacy modules to target architecture boundaries, data flows, migration sequence, and rollback considerations. |
| modernize-reimagine | Design a target modernization architecture that preserves required behavior and names intentional changes. |
| modernize-transform | Transform a bounded legacy module into modernized code with behavior-pinning tests and validation evidence. |
| multi-stage-dockerfile | Create optimized multi-stage Dockerfiles that reduce image size, improve security, and preserve reproducible builds. |
| new-skill | Scaffold a new GitHub Copilot Agent Skill using the skill-creator skill workflow. |
| playwright-automation-fill-in-form | Fill a specified web form with Playwright MCP and pause for review before submission. |
| playwright-explore-website | Explore a website with Playwright MCP, document core user flows, and propose test cases. |
| playwright-generate-test | Generate and validate a Playwright test from a provided scenario after browser exploration. |
| postgresql-code-review | Review PostgreSQL code for database-specific correctness, security, maintainability, and performance risks. |
| postgresql-optimization | Optimize PostgreSQL implementations using database-specific features, indexing, monitoring, and query tuning guidance. |
| project-workflow-analysis-blueprint-generator | Generate an implementation-ready blueprint that documents end-to-end application workflows across the detected project architecture. |
| prompt-builder | Guide creation of a production-ready VS Code prompt file with valid frontmatter, structure, and validation criteria. |
| sql-code-review | Review SQL code across database engines for security, maintainability, quality, and best-practice issues. |
| sql-optimization | Optimize SQL queries, indexes, pagination, batching, and performance diagnostics across common database engines. |
| technology-stack-blueprint-generator | Generate a technology stack blueprint that documents detected languages, frameworks, dependencies, and implementation patterns. |
| update-llms | Update the root llms.txt file to reflect current repository documentation, specifications, and structure. |

## Plugins

| Plugin | Version | Description |
| --- | --- | --- |
| accessibility-kanban | 1.0.3 | Kanban board to manage accessibility issues, allow you to plan, track, and complete remediation work. |
| acreadiness-cockpit | 1.0.1 | Drive Microsoft AgentRC from Copilot chat: assess AI readiness, generate Copilot instructions (flat or nested with applyTo globs for monorepos), and manage policies. Produces a se… |
| ai-team-orchestration | 2.0.1 | Run a lightweight, role-separated AI development team with flexible tools, developer-selected models, proportionate planning, and optional QA. |
| apng-studio | 1.0.3 | Interactive GitHub Copilot app canvas extension for building Animated PNG (APNG) files from frames. Draw or upload frames, tune per-frame timing and compositing, preview live, sen… |
| arcade-canvas | 1.0.3 | Play five retro Phaser mini-games in a Copilot canvas while agents work. |
| arch | 1.0.1 | Architecture and modernization toolkit: produce a cited architecture document for a locally-cloned repo, and generate a phased modernization plan that auto-runs Documentation mode… |
| arize-ax | 1.0.1 | Arize AX platform skills for LLM observability, evaluation, and optimization. Includes trace export, instrumentation, datasets, experiments, evaluators, AI provider integrations,… |
| automate-this | 1.0.1 | Record your screen doing a manual process, drop the video on your Desktop, and let Copilot CLI analyze it frame-by-frame to build working automation scripts. Supports narrated rec… |
| awesome-copilot | 1.1.1 | Meta prompts that help you discover and generate curated GitHub Copilot agents, instructions, prompts, and skills. |
| aws-cloud-development | 1.0.1 | Comprehensive AWS cloud development tools including Infrastructure as Code, serverless functions, architecture patterns, and cost optimization for building scalable cloud applicat… |
| azure-cloud-development | 1.0.2 | Comprehensive Azure cloud development tools including Infrastructure as Code, serverless functions, architecture patterns, and cost optimization for building scalable cloud applic… |
| backlog-swipe-triage | 1.0.3 | Quickly swipe through backlog issues to triage decisions like assign, needs-info, defer, close, or ignore. |
| backrooms-canvas | 1.0.1 | Wander an endless first-person backrooms in a Copilot canvas while agents work; their status ghost-writes on the walls. |
| cast-imaging | 1.0.1 | A comprehensive collection of specialized agents for software analysis, impact assessment, structural quality advisories, and architectural review using CAST Imaging. |
| chromium-control-canvas | 1.0.3 | Opens a real Chromium window you can navigate and interact with from a Copilot canvas control panel and agent actions. |
| clojure-interactive-programming | 1.0.1 | Tools for REPL-first Clojure workflows featuring Clojure instructions, the interactive programming chat mode and supporting guidance. |
| cms-development | 1.1.1 | Skills for CMS development across themes, plugins, admin tooling, media workflows, markdown rendering, and static export pipelines. |
| color-orb | 1.0.3 | A visual orb that users can ask the agent to recolor while showing a live activity log in the canvas. |
| context-engineering | 1.0.1 | Tools and techniques for maximizing GitHub Copilot effectiveness through better context management. Includes guidelines for structuring code, an agent for planning multi-file chan… |
| context-matic | 0.1.1 | Coding agents hallucinate APIs. ContextMatic gives them curated, versioned API and SDK docs. Ask your agent to "integrate the payments API" and it guesses — falling back on outdat… |
| convert-to-md | 1.0.2 | A collection of Copilot skills that convert common document formats into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Just tell… |
| copilot-plugin-development | 1.0.1 | Create, migrate, audit, and validate GitHub Copilot plugins and marketplaces with Agent Plugins 1.0 schemas, canonical component ownership, generated runtime mirrors, dependency p… |
| copilot-sdk | 1.0.1 | Build applications with the GitHub Copilot SDK across multiple programming languages. Includes comprehensive instructions for C#, Go, Node.js/TypeScript, and Python to help you cr… |
| csharp-dotnet-development | 1.1.1 | Essential prompts, instructions, and chat modes for C# and .NET development including testing, documentation, and best practices. |
| database-data-management | 1.0.1 | Database administration, SQL optimization, and data management tools for PostgreSQL, SQL Server, and general database development best practices. |
| dataverse-sdk-for-python | 1.0.1 | Comprehensive collection for building production-ready Python integrations with Microsoft Dataverse. Includes official documentation, best practices, advanced features, file opera… |
| devops-oncall | 1.0.1 | A focused set of prompts, instructions, and a chat mode to help triage incidents and respond quickly with DevOps tools and Azure resources. |
| diagram-viewer | 1.0.3 | Render diagrams, click nodes to drill down, and view agent-generated explanations directly in the canvas. |
| doublecheck | 1.0.1 | Three-layer verification pipeline for AI output. Extracts claims, finds sources, and flags hallucination risks so humans can verify before acting. |
| edge-ai-tasks | 1.0.1 | Task Researcher and Task Planner for intermediate to expert users and large codebases - Brought to you by microsoft/edge-ai |
| ember | 1.2.2 | An AI partner, not a tool. Ember carries fire from person to person — helping humans discover that AI partnership isn't something you learn, it's something you find. |
| eyeball | 1.0.1 | Document analysis with inline source screenshots. When you ask Copilot to analyze a document, Eyeball generates a Word doc where every factual claim includes a highlighted screens… |
| fabric-agentic-plugin | 1.0.0 | Microsoft Fabric agentic operations toolkit with specialist agents, progressive workload guides, migration workflows, Power BI resources, and MCP integrations for Fabric IQ and SQ… |
| fastah-ip-geo-tools | 0.0.10 | This plugin is for network operations engineers who wish to tune and publish IP geolocation feeds in RFC 8805 format. It consists of an AI Skill and an associated MCP server that… |
| feedback-themes | 1.0.3 | Explore grouped customer feedback signals by impact and drill into a theme to guide product next steps. |
| flight-map-canvas | 1.0.1 | A GitHub Copilot canvas that generates a view where Google Maps can be explored using 3D controls, as if a flight simulator. Agents can send the flight anywhere and report what th… |
| flowstudio-power-automate | 2.0.1 | Give your AI agent full visibility into Power Automate cloud flows via the FlowStudio MCP server. Connect, debug, build, monitor health, and govern flows at scale — action-level i… |
| frontend-web-dev | 1.0.1 | Essential prompts, instructions, and chat modes for modern frontend web development including React, Angular, Vue, TypeScript, and CSS frameworks. |
| gem-team | 1.102.1 | Self-Learning Multi-agent orchestration framework for spec-driven development and automated verification. With smarter tool calling and leaner context. |
| gesture-review | 1.0.3 | Review pull requests with a live camera feed and approve or reject using thumbs-up/thumbs-down gestures. |
| go-mcp-development | 1.0.1 | Complete toolkit for building Model Context Protocol (MCP) servers in Go using the official github.com/modelcontextprotocol/go-sdk. Includes instructions for best practices, a pro… |
| java-development | 1.0.1 | Comprehensive collection of prompts and instructions for Java development including Spring Boot, Quarkus, testing, documentation, and best practices. |
| java-mcp-development | 1.0.1 | Complete toolkit for building Model Context Protocol servers in Java using the official MCP Java SDK with reactive streams and Spring Boot integration. |
| java-modernization-studio | 1.0.3 | Drive the GitHub Copilot App Modernization for Java workflow from an interactive canvas: environment readiness, repo assessment, prioritized plan and progress, validation gates, a… |
| kotlin-mcp-development | 1.0.1 | Complete toolkit for building Model Context Protocol (MCP) servers in Kotlin using the official io.modelcontextprotocol:kotlin-sdk library. Includes instructions for best practice… |
| mcp-m365-copilot | 1.0.1 | Comprehensive collection for building declarative agents with Model Context Protocol integration for Microsoft 365 Copilot |
| napkin | 1.0.1 | Visual whiteboard collaboration for Copilot CLI. Opens an interactive whiteboard in your browser where you can draw, sketch, and add sticky notes — then share everything back with… |
| noob-mode | 1.0.1 | Plain-English translation layer for non-technical Copilot CLI users. Translates every approval prompt, error message, and technical output into clear, jargon-free English with col… |
| open-horizons-platform | 1.1.1 | Open Horizons agentic DevOps platform toolkit for Azure, AKS, Backstage, GitHub, Azure DevOps, Terraform, security, reliability, architecture, and deployment operations. Use it to… |
| openapi-to-application-csharp-dotnet | 1.0.1 | Generate production-ready .NET applications from OpenAPI specifications. Includes ASP.NET Core project scaffolding, controller generation, entity framework integration, and C# bes… |
| openapi-to-application-go | 1.0.1 | Generate production-ready Go applications from OpenAPI specifications. Includes project scaffolding, handler generation, middleware setup, and Go best practices for REST APIs. |
| openapi-to-application-java-spring-boot | 1.0.1 | Generate production-ready Spring Boot applications from OpenAPI specifications. Includes project scaffolding, REST controller generation, service layer organization, and Spring Bo… |
| openapi-to-application-nodejs-nestjs | 1.0.1 | Generate production-ready NestJS applications from OpenAPI specifications. Includes project scaffolding, controller and service generation, TypeScript best practices, and enterpri… |
| openapi-to-application-python-fastapi | 1.0.1 | Generate production-ready FastAPI applications from OpenAPI specifications. Includes project scaffolding, route generation, dependency injection, and Python best practices for asy… |
| oracle-to-postgres-migration-expert | 1.1.1 | Expert agent for Oracle-to-PostgreSQL application migrations in .NET solutions. Performs code edits, runs commands, and invokes extension tools to migrate .NET/Oracle data access… |
| ospo-sponsorship | 1.0.1 | Tools and resources for Open Source Program Offices (OSPOs) to identify, evaluate, and manage sponsorship of open source dependencies through GitHub Sponsors, Open Collective, and… |
| partners | 1.0.1 | Custom agents that have been created by GitHub partners |
| pcf-development | 1.1.0 | Complete toolkit for developing custom code components using Power Apps Component Framework for model-driven and canvas apps |
| phoenix | 1.0.1 | Phoenix AI observability skills for LLM application debugging, evaluation, and tracing. Includes CLI debugging tools, LLM evaluation workflows, and OpenInference tracing instrumen… |
| php-mcp-development | 1.0.1 | Comprehensive resources for building Model Context Protocol servers using the official PHP SDK with attribute-based discovery, including best practices, project generation, and ex… |
| power-apps-code-apps | 1.0.1 | Complete toolkit for Power Apps Code Apps development including project scaffolding, development standards, and expert guidance for building code-first applications with Power Pla… |
| power-bi-development | 1.0.1 | Comprehensive Power BI development resources including data modeling, DAX optimization, performance tuning, visualization design, security best practices, and DevOps/ALM guidance… |
| power-platform-architect | 1.0.1 | Solution Architect for the Microsoft Power Platform, turning business requirements into functioning Power Platform solution architectures. |
| power-platform-mcp-connector-development | 1.0.1 | Complete toolkit for developing Power Platform custom connectors with Model Context Protocol integration for Microsoft Copilot Studio |
| pr-artifact-explorer | 1.0.1 | Navigate pull requests and securely explore GitHub Actions artifacts, including test results, static sites, terminal recordings, and source files. |
| project-documenter | 1.0.1 | Generate professional project documentation with draw.io architecture diagrams and Word (.docx) output with embedded images. Automatically discovers any project's technology stack… |
| project-planning | 1.0.1 | Tools and guidance for software project planning, feature breakdown, epic management, implementation planning, and task organization for development teams. |
| python-mcp-development | 1.0.1 | Complete toolkit for building Model Context Protocol (MCP) servers in Python using the official SDK with FastMCP. Includes instructions for best practices, a prompt for generating… |
| react18-upgrade | 1.0.1 | Enterprise React 18 migration toolkit with specialized agents and skills for upgrading React 16/17 class-component codebases to React 18.3.1. Includes auditor, dependency surgeon,… |
| react19-upgrade | 1.0.1 | Enterprise React 19 migration toolkit with specialized agents and skills for upgrading React 18 codebases to React 19. Includes auditor, dependency surgeon, source code migrator,… |
| release-notes-showcase | 1.0.3 | Compose and refine launch-ready release notes with contributor callouts and export-friendly output. |
| repo-actions-hub | 1.0.3 | Browse repository GitHub Actions workflows, inspect recent runs, and trigger manual workflow_dispatch runs from a Copilot canvas. |
| roundup | 1.0.1 | Self-configuring status briefing generator. Learns your communication style from examples, discovers your data sources, and produces draft updates for any audience on demand. |
| ruby-mcp-development | 1.0.1 | Complete toolkit for building Model Context Protocol servers in Ruby using the official MCP Ruby SDK gem with Rails integration support. |
| rug-agentic-workflow | 1.0.1 | Three-agent workflow for orchestrated software delivery with an orchestrator plus implementation and QA subagents. |
| rust-mcp-development | 1.0.1 | Build high-performance Model Context Protocol servers in Rust using the official rmcp SDK with async/await, procedural macros, and type-safe implementations. |
| salesforce-development | 1.1.1 | Complete Salesforce agentic development environment covering Apex & Triggers, Flow automation, Lightning Web Components, Aura components, and Visualforce pages. |
| security-best-practices | 1.0.1 | Security frameworks, accessibility guidelines, performance optimization, and code quality best practices for building secure, maintainable, and high-performance applications. |
| signals-dashboard | 0.2.1 | Real-time Workshop dashboard with agent signals, honesty calibration, and cost-aware repo or connected desk launch profiles. |
| site-studio | 1.0.3 | Plan, draft, and track a personal website section by section — a shared canvas where you and your agent author content, watch progress, and review every change. |
| skill-image-gen | 1.0.1 | Generate images using AI directly from your coding workflow. Supports OpenAI (gpt-image-2) and Google Gemini. BYO API key — the skill guides you through setup on first use. |
| software-engineering-team | 1.0.1 | 7 specialized agents covering the full software development lifecycle from UX design and architecture to security and DevOps. |
| structured-autonomy | 1.0.1 | Premium planning, thrifty implementation |
| swift-mcp-development | 1.0.1 | Comprehensive collection for building Model Context Protocol servers in Swift using the official MCP Swift SDK with modern concurrency features. |
| technical-spike | 1.0.1 | Tools for creation, management and research of technical spikes to reduce unknowns and assumptions before proceeding to specification and implementation of solutions. |
| testing-automation | 1.0.1 | Comprehensive collection for writing tests, test automation, and test-driven development including unit tests, integration tests, and end-to-end testing strategies. |
| the-workshop | 0.1.2 | Stop being the switchboard between your AI agents — direct a team. The Workshop puts long-running AI agents (desks) in the same room, on the same work, each with its own memory an… |
| tiny-tool-town-submitter | 1.0.3 | Inspect a repository, improve Tiny Tool Town readiness, submit its listing issue, and launch remediation work. |
| token-pacman | 1.0.3 | Visualizes live session AI-credit usage as a Pac-Man board with pellets, ghosts, fruit milestones, and game-over limits. |
| typescript-mcp-development | 1.0.1 | Complete toolkit for building Model Context Protocol (MCP) servers in TypeScript/Node.js using the official SDK. Includes instructions for best practices, a prompt for generating… |
| typespec-m365-copilot | 1.0.1 | Comprehensive collection of prompts, instructions, and resources for building declarative agents and API plugins using TypeSpec for Microsoft 365 Copilot extensibility. |
| uizze | 1.0.1 | Stop generic UI from shipping. Ground GitHub Copilot in 800,000+ real web and iOS screens, write a product-specific design contract, and enforce a hard finish gate. |
| visual-pr | 1.0.1 | Capture, annotate, and embed screenshots and animated GIF demos in pull request descriptions. Includes Playwright-based UI capture, PIL image annotations, PR embedding workflows f… |
| where-was-i | 1.0.3 | Reconstruct your dev context (branch, commits, uncommitted work, PR clues) and trigger a resume prompt to continue quickly. |
| windows-app-storage-inspector-cleanup | 1.0.4 | Inspect Windows application storage, understand local disk usage, and safely move approved cleanup items to the Recycle Bin. |
| work-hub | 1.0.3 | Generic cross-repo command center canvas for GitHub Copilot with onboarding, focus planning, repo health, work signals, and session cleanup. |

## Hooks

| Hook package | Events |
| --- | --- |
| attester-import-check | preToolUse |
| dependency-license-checker | sessionEnd |
| fix-broken-links | postToolUse |
| governance-audit | sessionStart, sessionEnd, userPromptSubmitted |
| secrets-scanner | sessionEnd |
| session-auto-commit | sessionEnd |
| session-logger | sessionStart, sessionEnd, userPromptSubmitted |
| tool-guardian | preToolUse |
