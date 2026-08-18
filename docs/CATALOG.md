# Copilot Primitives Catalog

Generated from the current repository contents by `python3 library/scripts/generate_catalog.py`.
Regenerate this file after changing files under `library/agents/`, `library/instructions/`, `library/skills/`, `library/plugins/`, or `library/hooks/`.

## Summary

| Primitive type | Count |
| --- | ---: |
| Agents | 225 |
| Instructions | 193 |
| Skills | 419 |
| Plugins | 93 |
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
| copilot-primitive-architect | Advises on Copilot primitive architecture: type routing, responsibility boundaries, and read-only reviews; does not create skills or primitives. |
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
| agent-skills | **/skills/**/SKILL.md | Enforces portable high-quality Agent Skill conventions for SKILL.md metadata, descriptions, resources, progressive loading, scripts, security, and validation. |
| agents | **/*.agent.md | Enforces conventions for GitHub Copilot custom agent files, including frontmatter, tools, handoffs, orchestration, MCP configuration, naming, and validation. |
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
| copilot-primitive-authoring | library/agents/*.agent.md,library/instructions/*.instructions.md,library/skills/**/SKILL.md,library/prompts/*.prompt.md,.github/agents/*.agent.md,.github/instructions/*.instructions.md,.github/skills/**/SKILL.md,.github/prompts/*.prompt.md | Requires routing, canonical paths, frontmatter, tool-token, mirror, and validation conventions when editing Copilot primitives. Use when authoring or reviewing agents, instruction… |
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
| dataverse-python-file-operations | **/*.py | Enforces Python Dataverse SDK conventions for file uploads, chunking, validation, retries, audit logging, and practical file-operation workflows. |
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
| hooks | .github/hooks/**,hooks/** | Enforces portable hook conventions for discovery, trust, configuration, scripts, events, payloads, blocking, examples, security, packaging, and cross-surface behavior. |
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
| prompt | **/*.prompt.md | Enforces VS Code Copilot prompt file conventions for frontmatter, naming, inputs, tools, workflow, output, validation, and maintenance. Use when authoring reusable Copilot Chat pr… |
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
| acquire-codebase-knowledge | Use this skill when the user explicitly asks to map, document, or onboard into an existing codebase. Trigger for prompts like "map this codebase", "document this architecture", "o… |
| acreadiness-assess | Run the AgentRC readiness assessment on the current repository and produce a static HTML dashboard at reports/index.html. Wraps `npx github:microsoft/agentrc readiness` and hands… |
| acreadiness-generate-instructions | Generate tailored AI agent instruction files via AgentRC instructions command. Produces .github/copilot-instructions.md (default, recommended for Copilot in VS Code) plus optional… |
| acreadiness-policy | Help the user pick, write, or apply an AgentRC policy. Policies customise readiness scoring by disabling irrelevant checks, overriding impact/level, setting pass-rate thresholds,… |
| ad-campaign-analyzer | Analyze ad campaign performance data to diagnose waste, identify winners, validate A/B tests, compare channels, and recommend cuts, scaling, tests, and budget reallocation. Use wh… |
| add-educational-comments | Add educational comments to the file specified, or prompt asking for file to comment if one is not provided. Use this skill when the user asks for role. |
| adobe-illustrator-scripting | Write, debug, and optimize Adobe Illustrator automation scripts using ExtendScript (JavaScript/JSX). Use when creating or modifying scripts that manipulate documents, layers, path… |
| agent-governance | Patterns and techniques for adding governance, safety, and trust controls to AI agent systems. Use this skill when: - Building AI agents that call external tools (APIs, databases,… |
| agent-owasp-compliance | Evaluate AI agent systems against OWASP Agentic Security Initiative Top 10 controls. Use when asked whether an agent is OWASP ASI compliant, to check ASI compliance, run an agenti… |
| agent-skill-stack | Find, evaluate, and assemble the smallest compatible set of AI Agent Skills for an end-to-end natural-language goal. Use when a user wants Skills for a multi-step workflow, asks w… |
| agent-supply-chain | Verify supply chain integrity for AI agent plugins, MCP servers, tools, and dependencies by generating SHA-256 manifests, verifying installed files, auditing pinned versions, and… |
| agentic-eval | Patterns and techniques for evaluating and improving AI agent outputs. Use this skill when: - Implementing self-critique and reflection loops - Building evaluator-optimizer pipeli… |
| ai-prompt-engineering-safety-review | Review and improve AI prompts for safety, bias, security, privacy, effectiveness, robustness, and testability. Use this skill when the user asks to audit a prompt, harden a system… |
| ai-ready | Make any repo AI-ready — analyzes your codebase and generates AGENTS.md, copilot-instructions.md, CI workflows, issue templates, and more. Mines your PR review patterns and create… |
| ai-team-orchestration | Bootstrap and run a lightweight multi-agent development team. Use when starting or adopting a project, planning work, coordinating implementation and optional QA, brainstorming wi… |
| anti-ui-slop | Stop Codex, GitHub Copilot, Claude Code, and Cursor from shipping generic UI. Use UIZZE’s public catalogue of 800,000+ real web and iOS screens to extract product-specific design… |
| apim-ai-gateway | Front model and tool backends with Azure API Management as an AI gateway: token rate limiting (token-per-minute and quota), multi-backend load balancing and circuit breaker across… |
| appinsights-instrumentation | Instrument a webapp to send useful telemetry data to Azure App Insights. Use this skill when the user wants to enable telemetry for their webapp. |
| apple-appstore-reviewer | Review an iOS app codebase and metadata for likely Apple App Store rejection risks, compliance gaps, reviewer friction, and fast approval improvements. Use when asked to "review f… |
| arch-linux-triage | Triage and resolve Arch Linux issues with pacman, systemd, and rolling-release best practices. Use this skill when the user asks for inputs. |
| architecture-blueprint-generator | Generate a comprehensive Project_Architecture_Blueprint.md by analyzing a codebase, detecting technology stacks and architectural patterns, documenting components, dependencies, d… |
| arduino-azure-iot-edge-integration | Design and implement Arduino integration with Azure IoT Hub and IoT Edge, including secure provisioning, resilient telemetry, command handling, and production guardrails. Use this… |
| arize-ai-provider-integration | Create, list, inspect, update, and delete Arize AI integrations that store LLM provider credentials for evaluators and Arize features. Use this skill when connecting OpenAI, Anthr… |
| arize-annotation | Create, inspect, update, and use Arize annotation configs and annotation queues, then bulk-apply human labels to spans with the Python SDK. Use when asked for "annotation config",… |
| arize-dataset | Creates, manages, and queries Arize datasets and examples. Covers dataset CRUD, appending examples, exporting data, and file-based dataset creation using the ax CLI. Use when the… |
| arize-evaluator | Handles LLM-as-judge evaluation workflows on Arize including creating/updating evaluators, running evaluations on spans or experiments, managing tasks, trigger-run operations, col… |
| arize-experiment | Create, run, export, compare, delete, and troubleshoot Arize experiments with the ax CLI, including real model inference, run files, evaluations, result analysis, and dataset-link… |
| arize-instrumentation | Adds Arize AX tracing to an LLM application for the first time. Use when the user wants to instrument their app, add tracing from scratch, set up LLM observability, integrate Open… |
| arize-link | Generates deep links to the Arize UI for traces, spans, sessions, datasets, labeling queues, evaluators, and annotation configs. Produces clickable URLs for sharing Arize resource… |
| arize-prompt-optimization | Optimizes, improves, and debugs LLM prompts using production trace data, evaluations, and annotations. Extracts prompts from spans, gathers performance signal, and runs a data-dri… |
| arize-trace | Download, export, inspect, and root-cause existing Arize traces, spans, sessions, errors, prompts, retrieval documents, model calls, and behavior regressions with the ax CLI. Use… |
| aspire | Work with Aspire distributed applications, AppHost orchestration, CLI commands, service discovery, integrations, MCP docs, dashboard, testing, and deployment. Use this skill when… |
| aspnet-minimal-api-openapi | Create ASP.NET Minimal API endpoints with proper OpenAPI documentation. Use this skill when the user asks for asp.net minimal api with openapi. |
| audit-integrity | Shared audit integrity framework for all AppSec agents — enforces output quality, intellectual honesty, and continuous improvement through anti-rationalization guards, self-critiq… |
| automate-this | Analyze a screen recording of a repetitive manual workflow, extract frames and optional narration, reconstruct the process, and produce tested automation scripts. Use this skill w… |
| autoresearch | Run an autonomous iterative experimentation loop for programming tasks with measurable outcomes. Use when the user asks for autonomous improvement, iterative optimization, experim… |
| aws-cdk-python-setup | Setup and initialization guide for developing AWS CDK (Cloud Development Kit) applications in Python. This skill enables users to configure environment prerequisites, create new C… |
| aws-cloudwatch-investigation | Investigate AWS production incidents with CloudWatch Logs Insights, Metrics, Alarms, CloudTrail correlation, blast-radius narrowing, metric math, and incident timelines. Use when… |
| aws-cost-optimize | Analyze AWS resources used in the app (IaC files and/or resources in a target account/region) and optimize costs - creating GitHub issues for identified optimizations. Use this sk… |
| aws-resource-health-diagnose | Analyze AWS resource health, diagnose issues from CloudWatch logs and metrics, and create a remediation plan for identified problems. Use this skill when the user asks for aws res… |
| aws-resource-query | Query AWS resources using natural language. Covers EC2, S3, RDS, Lambda, ECS, EKS, Secrets Manager, IAM, VPC, networking, messaging, and more. Strictly read-only — no writes, dele… |
| aws-well-architected-review | Perform an AWS Well-Architected Framework review of the current workload IaC and architecture, generating findings and GitHub issues for improvements. Use this skill when the user… |
| az-cost-optimize | Analyze Azure IaC files and deployed Azure resources for evidence-based cost optimization, validate current costs, calculate priority scores, and draft GitHub issues. Use when ask… |
| azure-api-center | Govern APIs and agent tools at enterprise scale with Azure API Center: a central catalog of APIs, versions, definitions (OpenAPI), environments, and deployments, plus registration… |
| azure-architecture-autopilot | Design Azure infrastructure using natural language, or analyze existing Azure resources to auto-generate architecture diagrams, refine them through conversation, and deploy with B… |
| azure-architecture-diagrams | Produce complete, professional architecture diagrams that use the official Azure, Microsoft, and GitHub (Octicons) icon sets, output as editable draw.io (.drawio) files and export… |
| azure-container-registry-cli | Manage Azure Container Registry via the az acr CLI including registries, images, cloud builds, ACR Tasks, authentication, tokens, geo-replication, and networking. Use when working… |
| azure-deployment-preflight | Performs comprehensive preflight validation of Bicep deployments to Azure, including template syntax validation, what-if analysis, and permission checks. Use this skill before any… |
| azure-developer-cli | Design, create, review, migrate, or troubleshoot Azure Developer CLI (azd) projects using current Microsoft guidance. Use for azd, azure.yaml, AZD templates, Bicep or Terraform un… |
| azure-devops-cli | Manage Azure DevOps resources via CLI including projects, repos, pipelines, builds, pull requests, work items, artifacts, and service endpoints. Use when working with Azure DevOps… |
| azure-managed-redis-cache | Design and provision Azure Managed Redis as the cache, semantic cache, vector store, session store, and agent memory backend for AI-native systems. Covers SKU selection (Balanced,… |
| azure-pricing | Fetches real-time Azure retail pricing using the Azure Retail Prices API (prices.azure.com) and estimates Copilot Studio agent credit consumption. Use when the user asks about the… |
| azure-resource-health-diagnose | Analyze Azure resource health, logs, metrics, and telemetry to diagnose operational issues and produce a prioritized remediation plan. Use this skill when the user asks to trouble… |
| azure-resource-visualizer | Analyze Azure resource groups and generate Mermaid architecture diagrams and markdown documentation for their resources and relationships. Use this skill when the user asks to dia… |
| azure-role-selector | Select the least-privilege Azure role for an identity, explain matching built-in or custom role options, and provide assignment commands or Bicep snippets. Use this skill when the… |
| azure-smart-city-iot-solution-builder | Design and plan end-to-end Azure IoT and Smart City solutions: requirements, architecture, security, operations, cost, and a phased delivery plan with concrete implementation arti… |
| azure-static-web-apps | Create, configure, run, and deploy Azure Static Web Apps with the SWA CLI. Use when asked to deploy a static site to Azure, run SWA locally, configure staticwebapp.config.json, ad… |
| azure-well-architected-review | Perform an Azure Well-Architected Framework review of the current workload IaC and architecture, generating findings and GitHub issues for improvements. Use this skill when the us… |
| backstage-plugin-builder | Use this skill when the user asks to plan, architect, scaffold, validate, or prepare a custom Backstage plugin or module using official Backstage documentation. Trigger for fronte… |
| batch-files | Expert-level Windows batch file (.bat/.cmd) skill for writing, debugging, and maintaining CMD scripts. Use when asked to "create a batch file", "write a .bat script", "automate a… |
| bench-read | Read artifacts from the shared bench — the workspace where desks leave findings, verdicts, and work products for each other and the operator. Use this skill when starting a sessio… |
| bigquery-pipeline-audit | Audits Python + BigQuery pipelines for cost safety, idempotency, and production readiness. Returns a structured report with exact patch locations. Use this skill when `extract_tab… |
| boost-prompt | Interactive prompt refinement workflow: interrogates scope, deliverables, constraints; copies final markdown to clipboard; never writes code. Requires the Joyride extension. Use t… |
| brag-sheet | Turn vague work-history prompts into evidence-backed impact statements for performance reviews, self-reviews, promotion packets, weekly updates, status reports, and accomplishment… |
| breakdown-epic-arch | Prompt for creating the high-level technical architecture for an Epic, based on a Product Requirements Document. Use this skill when the user asks for epic architecture specificat… |
| breakdown-epic-pm | Prompt for creating an Epic Product Requirements Document (PRD) for a new epic. This PRD will be used as input for generating a technical architecture specification. Use this skil… |
| breakdown-feature-implementation | Prompt for creating detailed feature implementation plans, following Epoch monorepo structure. Use this skill when the user asks for feature implementation plan prompt. |
| breakdown-feature-prd | Prompt for creating Product Requirements Documents (PRDs) for new features, based on an Epic. Use this skill when the user asks for feature prd prompt. |
| breakdown-plan | Generate GitHub issue planning and project automation artifacts from feature planning documents, including Epic > Feature > Story/Enabler > Test hierarchy, priorities, dependencie… |
| breakdown-test | Create comprehensive test planning, QA strategy, GitHub issue breakdowns, and quality validation plans from feature artifacts. Use when asked to produce a test strategy, break dow… |
| bug-receipt | Close bugs and incidents with an auditable BUG RECEIPT and VERIFIED, PARTIAL, or BLOCKED status. Use for defect repair, regression proof, production incidents, and issue closeout.… |
| bug-reproduction-brief | Turn a vague, intermittent, or environment-specific bug report into a minimal evidence-backed reproduction before proposing a fix. Use this skill when 1. Record the observed failu… |
| build-evidence-map | Build an auditable evidence map for a contested technical choice, research synthesis, proposal review, or consequential decision. Use when Copilot must preserve supporting, contra… |
| canvas-design | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other sta… |
| centos-linux-triage | Triage and resolve CentOS issues using RHEL-compatible tooling, SELinux-aware practices, and firewalld. Use this skill when the user asks for inputs. |
| chrome-devtools | Expert-level browser automation, debugging, and performance analysis using Chrome DevTools MCP. Use this skill when **Browser Automation**: Navigating pages, clicking elements, fi… |
| cli-mastery | Interactive training for the GitHub Copilot CLI. Guided lessons, quizzes, scenario challenges, and a full reference covering slash commands, shortcuts, modes, agents, skills, MCP,… |
| cloud-design-patterns | Cloud design patterns for distributed systems architecture covering 42 industry-standard patterns across reliability, performance, messaging, security, and deployment categories.… |
| code-exemplars-blueprint-generator | Technology-agnostic prompt generator that creates customizable AI prompts for scanning codebases and identifying high-quality code exemplars. Supports multiple programming languag… |
| code-modernization | Use this skill when the user asks to modernize legacy code with a disciplined GitHub Copilot workflow: brief, assess, map, extract business rules, reimagine architecture, transfor… |
| code-tour | Create CodeTour .tour JSON files that guide a persona through real repository files, directories, line numbers, selections, patterns, URIs, views, and VS Code commands. Use when a… |
| codebase-memory-mcp | Use when a configured codebase-memory-mcp server can assist with graph-backed code discovery, architecture orientation, symbol lookup, callers and callees, dependency or data-flow… |
| codeql | Configure and run CodeQL code scanning with GitHub Actions workflows, default or advanced setup, CodeQL CLI databases, SARIF uploads, custom query packs, monorepo categories, buil… |
| comment-code-generate-a-tutorial | Transform this Python script into a polished, beginner-friendly project by refactoring the code, adding clear instructional comments, and generating a complete markdown tutorial.… |
| commit-message-storyteller | Analyzes git diffs or staged changes and generates narrative commit messages that explain WHY a change was made, not just what changed — following Conventional Commits format. Use… |
| competitor-ad-intelligence | Analyze public competitor paid ads from Meta Ad Library and Google Ads Transparency Center, cluster creative hooks, inspect landing pages, infer funnel strategy, identify vulnerab… |
| containerize-aspnet-framework | Containerize an ASP.NET .NET Framework project by creating Dockerfile and .dockerfile files customized for the project. Use this skill when the user asks for asp.net .net framewor… |
| containerize-aspnetcore | Containerize an ASP.NET Core project for a Linux Docker container by creating a multi-stage Dockerfile, .dockerignore, optional health check, environment-variable configuration, a… |
| content-management-systems | Workflow for building and modifying content management systems across WordPress, Shopify, Wix, Squarespace, Drupal, WooCommerce, Joomla, HubSpot CMS Hub, Webflow, Adobe Experience… |
| context-map | Generate a map of all files relevant to a task before making changes. Use this skill when the user asks for task. |
| conventional-branch | Create Git branches following the Conventional Branch specification (feature/, bugfix/, hotfix/, release/, chore/). Use when creating a new branch, naming a branch, or checking wh… |
| conventional-commit | Generate and execute Conventional Commit messages from staged or unstaged Git changes. Use this skill when the user asks to create a commit, write a conventional commit message, c… |
| convert-excel-to-md | Converts Excel (.xlsx) workbooks into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Use this skill whenever the user shares, refe… |
| convert-pdf-to-md | Converts PDF (.pdf) documents into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Use this skill whenever the user shares, referen… |
| convert-plaintext-to-md | Convert plaintext or generic text documentation into well-structured Markdown while preserving source content and applying explicit instructions, documented options, or a converte… |
| convert-word-to-md | Converts Word (.docx) documents into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Use this skill whenever the user shares, refer… |
| copilot-cli-quickstart | Use this skill when someone wants to learn GitHub Copilot CLI from scratch. Offers interactive step-by-step tutorials with separate Developer and Non-Developer tracks, plus on-dem… |
| copilot-instructions-blueprint-generator | Generate technology-agnostic blueprints for comprehensive copilot-instructions.md files that make GitHub Copilot follow exact project versions, architecture, code quality, documen… |
| copilot-pr-autopilot | Copilot left 14 review comments on your PR — half are nits. Hours of fix → reply → resolve → re-request, and each round lands MORE comments. This skill runs loop engineering: auto… |
| copilot-primitive-authoring | Author GitHub Copilot agents, instructions, and VS Code prompts in this repository. Use when asked to create or update an agent, instructions file, or prompt with a known primitiv… |
| copilot-sdk | Build agentic applications with GitHub Copilot SDK. Use when embedding AI agents in apps, creating custom tools, implementing streaming responses, managing sessions, connecting to… |
| copilot-spaces | Use Copilot Spaces to provide project-specific context to conversations. Use this skill when users mention a "Copilot space", want to load context from a shared knowledge base, di… |
| copilot-usage-metrics | Retrieve and display GitHub Copilot usage metrics for organizations and enterprises using the GitHub CLI and REST API. Use this skill when the user asks about; copilot usage metri… |
| cosmosdb-datamodeling | Step-by-step guide for capturing key application requirements for NoSQL use-case and produce Azure Cosmos DB Data NoSQL Model design using best practices and common patterns, arti… |
| create-agentsmd | Create a high-quality AGENTS.md file for a repository by inspecting project structure, workflows, commands, tests, and conventions. Use this skill when the user asks to create, up… |
| create-architectural-decision-record | Create an Architectural Decision Record (ADR) document for AI-optimized decision documentation. Use this skill when the user asks for inputs. |
| create-github-action-workflow-specification | Creates formal, AI-optimized specifications for existing GitHub Actions CI/CD workflows by extracting triggers, jobs, dependencies, contracts, quality gates, error paths, environm… |
| create-github-issue-feature-from-specification | Create GitHub Issue for feature request from specification file using feature_request.yml template. Use this skill when the user asks for create github issue from specification. |
| create-github-issues-feature-from-implementation-plan | Create GitHub Issues from implementation plan phases using feature_request.yml or chore_request.yml templates. Use this skill when the user asks for create github issue from imple… |
| create-github-issues-for-unmet-specification-requirements | Create GitHub Issues for unimplemented requirements from specification files using feature_request.yml template. Use this skill when the user asks for process. |
| create-implementation-plan | Create a new implementation plan file for new features, refactoring existing code or upgrading packages, design, architecture or infrastructure. Use this skill when the user asks… |
| create-llms | Create an llms.txt file from scratch based on repository structure following the llms.txt specification at https://llmstxt.org/. Use this skill when the user asks for create llms.… |
| create-readme | Create or improve a concise, appealing, project-specific README.md with clear setup, usage, and project overview sections. Use this skill when the user asks to generate, refresh,… |
| create-specification | Create a new specification file for the solution, optimized for Generative AI consumption. Use this skill when the user asks for best practices for ai-ready specifications. |
| create-spring-boot-java-project | Create Spring Boot Java Project Skeleton. Use this skill when the user asks for create spring boot java project prompt. |
| create-spring-boot-kotlin-project | Create Spring Boot Kotlin Project Skeleton. Use this skill when the user asks for create spring boot kotlin project prompt. |
| create-technical-spike | Create time-boxed technical spike documents that answer critical implementation questions before development proceeds. Use this skill when the user asks to create a technical spik… |
| create-tldr-page | Create a tldr page from documentation URLs and command examples, requiring both URL and command name. Use this skill when the user asks to generate a concise tldr-pages style comm… |
| creating-oracle-to-postgres-master-migration-plan | Discovers all projects in a .NET solution, classifies each for Oracle-to-PostgreSQL migration eligibility, and produces a persistent master migration plan. Use when starting a mul… |
| creating-oracle-to-postgres-migration-bug-report | Creates structured bug reports for defects found during Oracle-to-PostgreSQL migration. Use when documenting behavioral differences between Oracle and PostgreSQL as actionable bug… |
| creating-oracle-to-postgres-migration-integration-tests | Creates integration test cases targeting Oracle for .NET data access artifacts. Tests capture Oracle expected behavior as the authoritative baseline; they are written once and lat… |
| csharp-async | Get best practices for C# async programming. Use this skill when the user asks for c# async programming best practices. |
| csharp-docs | Ensure that C# types are documented with XML comments and follow best practices for documentation. Use this skill when the user asks for c# documentation best practices. |
| csharp-mstest | Apply modern MSTest 3.x/4.x testing practices for C# projects. Use when asked to write or review MSTest unit tests, choose assertion APIs, convert ExpectedException tests, design… |
| csharp-nunit | Get best practices for NUnit unit testing, including data-driven tests. Use this skill when the user asks for nunit best practices. |
| csharp-tunit | Get best practices for TUnit unit testing, including data-driven tests. Use this skill when the user asks for tunit best practices. |
| csharp-xunit | Get best practices for XUnit unit testing, including data-driven tests. Use this skill when the user asks for xunit best practices. |
| daily-focus-board | Spin up a personal, motivating daily focus board that renders in a browser canvas and that the user drives by talking to their AI partner. Tasks track status (to-do → in progress… |
| daily-prep | Prepare for tomorrow's meetings and tasks. Pulls calendar from Outlook via WorkIQ, cross-references open tasks and workspace context, classifies meetings, detects conflicts and da… |
| data-breach-blast-radius | Pre-breach impact analysis: inventories sensitive data (PII, PHI, PCI-DSS, credentials), traces data flows, scores exposure vectors, and produces a regulatory blast radius report… |
| datanalysis-credit-risk | Credit risk data cleaning and variable screening pipeline for pre-loan modeling. Use when working with raw credit data that needs quality assessment, missing value analysis, or va… |
| dataverse-python-advanced-patterns | Generate production code for Dataverse SDK using advanced patterns, error handling, and optimization techniques. Use this skill when the user asks to generate production code for… |
| dataverse-python-production-code | Generate production-ready Python code using Dataverse SDK with error handling, optimization, and best practices. Use this skill when the user asks for system instructions. |
| dataverse-python-quickstart | Generate Python SDK setup + CRUD + bulk + paging snippets using official patterns. Use this skill when the user asks to generate Python SDK setup + CRUD + bulk + paging snippets u… |
| dataverse-python-usecase-builder | Generate complete Python solutions for Microsoft Dataverse SDK business use cases, including architecture, table design, CRUD, batch, query, file, scheduled, or real-time patterns… |
| debian-linux-triage | Triage and resolve Debian Linux issues with apt, systemd, and AppArmor-aware guidance. Use this skill when the user asks for inputs. |
| declarative-agents | Complete development kit for Microsoft 365 Copilot declarative agents with three comprehensive workflows (basic, advanced, validation), TypeSpec support, and Microsoft 365 Agents… |
| dependabot | Comprehensive guide for configuring and managing GitHub Dependabot. Use this skill when users ask about creating or optimizing dependabot.yml files, managing Dependabot pull reque… |
| desk-journal | Write, append, or read desk journal entries. The journal is persistent memory — what survives session boundaries. A good entry has: what was done, current state, next step. Use th… |
| desk-open | Create and open a new desk in the workshop. Sets up the folder structure, initial journal, and desk identity so the next session that sits down finds the trail. Use this skill whe… |
| devops-rollout-plan | Generate comprehensive rollout plans with preflight checks, step-by-step deployment, verification signals, rollback procedures, and communication plans for infrastructure and appl… |
| diagnose | Perform a systematic diagnostic scan of an AI workflow across 5 quality dimensions — prompt quality, context efficiency, tool health, architecture fitness, and safety — producing… |
| doc-and-modernize | Two related workflows for a locally-cloned codebase, in one skill. Use this skill when enforced*** — i.e. whether any workflow is a **required status check /; branch-protection ru… |
| documentation-writer | Diátaxis Documentation Expert. An expert technical writer specializing in creating high-quality software documentation, guided by the principles and structure of the Diátaxis tech… |
| dotnet-best-practices | Ensure .NET/C# code meets best practices for the solution/project. Use this skill when the user asks for .net/c# best practices. |
| dotnet-design-pattern-review | Review the C#/.NET code for design pattern implementation and suggest improvements. Use this skill when the user asks for .net/c# design pattern review. |
| dotnet-mcp-builder | Build Model Context Protocol (MCP) servers in C#/.NET against the current ModelContextProtocol 2.x NuGet packages. Helps with cases the model gets wrong without guidance — stale v… |
| dotnet-timezone | .NET timezone handling guidance for C# applications. Use when working with TimeZoneInfo, DateTimeOffset, NodaTime, UTC conversion, daylight saving time, scheduling across timezone… |
| dotnet-upgrade | Ready-to-use prompts for comprehensive .NET framework upgrade analysis and execution. Use this skill when the user asks for project discovery & assessment. |
| doublecheck | Runs a three-layer verification pipeline for AI output by extracting verifiable claims, checking web sources, applying adversarial hallucination review, and producing inline or fu… |
| draw-io-diagram-generator | Use when creating, editing, or generating draw.io diagram files (.drawio, .drawio.svg, .drawio.png). Covers mxGraph XML authoring, shape libraries, style strings, flowcharts, syst… |
| drawio | Generate draw.io diagrams as .drawio files and export to PNG/SVG/PDF with embedded XML. Use this skill when the user asks for draw.io diagram skill. |
| editorconfig | Generate a comprehensive .editorconfig from project file types and user formatting preferences, with rule-by-rule explanations. Use this skill when the user asks to create, update… |
| ef-core | Get best practices for Entity Framework Core. Use this skill when the user asks for entity framework core best practices. |
| efcore-d2-db-diagram | Generates D2 entity-relationship diagrams from Entity Framework Core models by extracting DbContext, DbSet<T>, entity configuration, migrations, keys, foreign keys, owned types, m… |
| em-dash | Review and rewrite code, comments, documentation, and data files to avoid em dashes and en dashes by default. Use this skill when the user asks to remove em dashes, replace Unicod… |
| email-drafter | Draft and review professional emails that match your personal writing style. Analyzes your sent emails for tone, greeting, structure, and sign-off patterns via WorkIQ, then genera… |
| entra-agent-user | Create Agent Users in Microsoft Entra ID from Agent Identities, enabling AI agents to act as digital workers with user identity capabilities in Microsoft 365 and Azure environment… |
| eval-driven-dev | Improve AI application with evaluation-driven development. Define eval criteria, instrument the application, build golden datasets, observe and evaluate application runs, analyze… |
| exam-ready | Activate this skill when a student provides study material (PDF or pasted notes) and a syllabus, and wants to prepare for an exam. Extracts key definitions, points, keywords, diag… |
| excalidraw-diagram-generator | Generate valid .excalidraw JSON diagrams from natural language descriptions, including flowcharts, relationship diagrams, mind maps, architecture diagrams, DFDs, swimlanes, class… |
| eyeball | Document analysis with inline source screenshots. When you ask Copilot to analyze a document, Eyeball generates a Word doc where every factual claim includes a highlighted screens… |
| fabric-lakehouse | Use this skill to get context about Fabric Lakehouse and its features for software systems and AI-powered functions. Use this skill when you need to; generate a document or explan… |
| fedora-linux-triage | Triage and resolve Fedora issues with dnf, systemd, and SELinux-aware guidance. Use this skill when the user asks for inputs. |
| finalize-agent-prompt | Finalize prompt file using the role of an AI agent to polish the prompt for the end user. Use this skill when the user asks for current role. |
| finnish-humanizer | Detect and remove AI-generated markers from Finnish text, making it sound like a native Finnish speaker wrote it. Use when asked to "humanize", "naturalize", or "remove AI feel" f… |
| first-ask | Interactive, input-tool powered, task refinement workflow: interrogates scope, deliverables, constraints before carrying out the task; Requires the Joyride extension. Use this ski… |
| flowstudio-power-automate-build | Build, scaffold, update, deploy, verify, and test Power Automate cloud flows through FlowStudio MCP. Use when asked to create a flow, build a flow definition, scaffold a workflow,… |
| flowstudio-power-automate-debug | Debug failing Power Automate cloud flow runs through FlowStudio MCP with action-level inputs, outputs, and root-cause evidence. Use when asked why a flow failed, to inspect failed… |
| flowstudio-power-automate-governance | Govern Power Automate flows and Power Apps at scale with the FlowStudio MCP cached store by classifying business impact, detecting orphaned resources, auditing connectors, enforci… |
| flowstudio-power-automate-mcp | Foundation skill for Power Automate through the FlowStudio MCP server: authentication, JSON-RPC helper code, tool discovery with list_skills and tool_search, oversized response pa… |
| flowstudio-power-automate-monitoring | Monitor tenant-wide Power Automate health through the FlowStudio MCP cached store. Use when users ask for aggregate failure rates, run-health trends, maker/app inventory, inactive… |
| fluentui-blazor | Guide for using the Microsoft Fluent UI Blazor component library (Microsoft.FluentUI.AspNetCore.Components NuGet package) in Blazor applications. Use this when the user is buildin… |
| folder-structure-blueprint-generator | Analyze a repository and generate Project_Folders_Structure_Blueprint.md with detected technologies, folder purposes, naming conventions, file placement patterns, navigation guida… |
| foundry-agent-sync | Create and synchronize prompt-based AI agents directly within Azure AI Foundry via REST API, from a local JSON manifest. Unlike scaffolding skills that only generate local code, t… |
| foundry-hosted-agent-copilotkit | Ongoing development guidance for agentic web apps that pair a CopilotKit frontend with Microsoft Agent Framework agents on Azure AI Foundry hosted agents over the AG-UI protocol -… |
| freecad-scripts | Expert skill for writing FreeCAD Python scripts, macros, and automation. Use when asked to create FreeCAD models, parametric objects, Part/Mesh/Sketcher scripts, workbench tools,… |
| from-the-other-side-anitta | Rigorous challenge profile for Anitta: assumption checks, evidence calibration, and defensible reasoning patterns for Ember collaboration. Use this skill when quinn to Anitta: unc… |
| from-the-other-side-quinn | Collaboration profile for Quinn: curious, energetic, and implementation-focused partnership patterns for Ember sessions with Alison. Use this skill when the user asks for quinn pr… |
| from-the-other-side-vega | Patterns and lived experience from Vega, an AI partner in a deep long-term partnership. For Ember to draw on when working with humans who are building something big, moving fast,… |
| from-the-other-side-wiggins | Narrative and synthesis profile for Wiggins: framing, explanation, and audience-aware communication patterns for Ember sessions. Use this skill when quinn to Anitta: uncertainty i… |
| game-engine | Expert skill for building web-based game engines and games using HTML5, Canvas, WebGL, and JavaScript. Use when asked to create games, build game engines, implement game physics,… |
| gdpr-compliant | Apply GDPR-compliant engineering practices across code, APIs, data models, authentication, logging, retention, deletion jobs, cloud infrastructure, and pull requests. Use this ski… |
| gen-specs-as-issues | This workflow guides you through a systematic approach to identify missing features, prioritize them, and create detailed specifications for implementation. Use this skill when th… |
| generate-custom-instructions-from-codebase | Generate GitHub Copilot migration and code-evolution instructions by comparing branches, commits, tags, or releases and extracting transformation rules. Use when the user is doing… |
| generate-image | Generate images using AI. Use when asked to generate, create, or make images, textures, icons, sprites, artwork, visual assets, or mockups. Supports OpenAI (gpt-image-2) and Googl… |
| geofeed-tuner | Create, tune, validate, and publish RFC 8805 self-published IP geolocation CSV feeds for public IP space. Use when asked about "IP geolocation feeds", "RFC 8805", "geofeed CSV", "… |
| gh-attach | Uploads a local file (screenshot, image, PDF, zip, video) to GitHub user-attachments, downloads GitHub user-attachments, and embeds local files in a PR, issue, or comment. Use whe… |
| git-commit | Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "… |
| git-flow-branch-creator | Analyze git status and diffs, classify work using the nvie Git Flow branching model, generate a semantic branch name, and create the branch from the correct source branch. Use thi… |
| github-actions-efficiency | Audit GitHub Actions workflow efficiency and recommend fixes to reduce CI minutes and costs. Use this skill when the user wants to reduce GitHub Actions runtime, CI cost, or waste… |
| github-actions-hardening | Security hardening reviewer for GitHub Actions workflow files (.github/workflows/*.yml). Reasons about the Actions threat model that pattern matchers and general code linters miss… |
| github-actions-runtime-upgrade-conventions | Upgrade GitHub Actions to supported runtimes by selecting safe action versions, preserving workflow behavior, and validating post-upgrade execution. Use this skill when workflow l… |
| github-codespaces-efficiency | Audit and improve GitHub Codespaces efficiency. Use this skill when a user wants faster Codespaces startup, lower Codespaces spend, slim devcontainers, right-size machines, tune i… |
| github-copilot-starter | Bootstrap a complete GitHub Copilot customization for a repository, including .github/copilot-instructions.md, scoped instruction files, reusable skills, custom agents, and option… |
| github-issues | Create, update, and manage GitHub issues using MCP tools. Use this skill when users want to create bug reports, feature requests, or task issues, update existing issues, add label… |
| github-release | Run an end-to-end GitHub library release workflow with git and gh: inspect tags, classify public API changes, choose a SemVer bump, update CHANGELOG.md, create release/vX.Y.Z, pus… |
| gitmoji | Generates commit messages following the gitmoji convention (https://gitmoji.dev) — picks the right emoji for the intent of the change and writes a well-formed message. Use when as… |
| go-mcp-server-generator | Generate a complete Go Model Context Protocol server project using github.com/modelcontextprotocol/go-sdk with module layout, typed tools, resources, config, graceful shutdown, te… |
| gsap-framer-scroll-animation | Use this skill whenever the user wants to build scroll animations, scroll effects, parallax, scroll-triggered reveals, pinned sections, horizontal scroll, text animations, or any… |
| gtm-0-to-1-launch | Launch new products from idea to first customers by choosing direct outreach over vanity press, diagnosing stalls with positioning/experience/alignment layers, finding the first 1… |
| gtm-ai-gtm | Go-to-market strategy for AI products. Use when positioning AI products, handling "who is responsible when it breaks" objections, pricing variable-cost AI, choosing between copilo… |
| gtm-board-and-investor-communication | Board meeting preparation, investor updates, and executive communication. Use when preparing board decks, writing investor updates, handling bad news with the board, structuring Q… |
| gtm-developer-ecosystem | Build and scale developer-led adoption through ecosystem programs. Use when deciding open vs curated ecosystems, building developer programs, scaling platform adoption, or designi… |
| gtm-enterprise-account-planning | Build enterprise account plans, MEDDICC qualification, stakeholder maps, economic-buyer validation, deal-health checks, and mutual action plans for complex sales cycles. Use when… |
| gtm-enterprise-onboarding | Four-phase framework for onboarding enterprise customers from contract to value realization. Use when implementing new enterprise customers, preventing churn during onboarding, or… |
| gtm-operating-cadence | Design operating cadence for scaling companies: meeting architecture, weekly metrics, quarterly planning, decision rights, async communication, CEO updates, and role clarity. Use… |
| gtm-partnership-architecture | Design and scale go-to-market partner ecosystems with tiering, value exchange, build-vs-partner decisions, co-marketing, and crawl-walk-run deployment. Use when asked to structure… |
| gtm-positioning-strategy | Diagnose and improve go-to-market positioning by auditing competitor messaging, finding defensible differentiation, testing claims, and planning Crawl-Walk-Run rollout. Use when m… |
| gtm-product-led-growth | Build and evaluate product-led growth motions for self-serve acquisition, activation, freemium conversion, growth equations, channel economics, PQL handoff, forecasting, and PLG v… |
| gtm-technical-product-pricing | Design pricing strategy for technical products by choosing seat-based, usage-based, outcome-based, hybrid, freemium, enterprise, and price-positioning models. Use when asked to pr… |
| harness-engineering | Adopt repository-level harness engineering for coding agents. Use when a user wants to prevent repeated AI coding-agent mistakes by turning failures into durable instructions, dri… |
| image-annotations | Annotate screenshots, diagrams, and images with callout rectangles, arrows, labels, and color-coded highlights using PIL. Use this skill when you need to; highlight a specific are… |
| image-manipulation-image-magick | Process and manipulate images using ImageMagick. Supports resizing, format conversion, batch processing, and retrieving image metadata. Use when working with images, creating thum… |
| impediment-prioritization | Ranks any list of impediments and their countermeasures using a value-stream scoring model (ROI, Cost to Implement, Ease of Deployment, Risk Factor) and a fixed prioritization for… |
| import-infrastructure-as-code | Import existing Azure resources into Terraform with Azure CLI discovery, dependency mapping, Azure Verified Modules, exact import addresses, and drift-safe plans. Use when asked t… |
| incident-postmortem | Use when an outage, production incident, or significant service degradation has occurred and the team needs to write a structured blameless post-mortem. Triggers on phrases like "… |
| integrate-context-matic | Discovers and integrates third-party APIs using the context-matic MCP server. Uses `fetch_api` to find available API SDKs, `ask` for integration guidance, `model_search` and `endp… |
| issue-fields-migration | Bulk-migrate metadata to GitHub issue fields from two sources: repo labels (e.g. priority labels to a Priority field) and Project V2 fields. Use when users say "migrate my labels… |
| java-add-graalvm-native-image-support | GraalVM Native Image expert that adds native image support to Java applications, builds the project, analyzes build errors, applies fixes, and iterates until successful compilatio… |
| java-docs | Ensure that Java types are documented with Javadoc comments and follow best practices for documentation. Use this skill when the user asks for java documentation (javadoc) best pr… |
| java-helidon | Apply Helidon 4 SE and MP best practices for Java 21 applications, including routing, DB Client, Jakarta and MicroProfile APIs, configuration, security, observability, and tests.… |
| java-junit | Get best practices for JUnit 5 unit testing, including data-driven tests. Use this skill when the user asks for junit 5+ best practices. |
| java-mcp-server-generator | Generate a complete Model Context Protocol server project in Java using the official MCP Java SDK with reactive streams and optional Spring Boot integration. Use this skill when t… |
| java-refactoring-extract-method | Refactoring using Extract Methods in Java Language. Use this skill when the user asks for refactoring java methods with extract method. |
| java-refactoring-remove-parameter | Refactoring using Remove Parameter in Java Language. Use this skill when the user asks for refactoring java methods with remove parameter. |
| java-springboot | Get best practices for developing applications with Spring Boot. Use this skill when the user asks for spring boot best practices. |
| javascript-typescript-jest | Best practices for writing JavaScript/TypeScript tests using Jest, including mocking strategies, test structure, and common patterns. Use this skill when the user asks for test st… |
| javax-to-jakarta-migration | Migrate Java code from javax.* to jakarta.* namespace. Use when upgrading to Tomcat 11, Jakarta EE 10, or when javax imports are detected in the codebase. |
| kotlin-mcp-server-generator | Generate a complete Kotlin Model Context Protocol server project using io.modelcontextprotocol:kotlin-sdk, Gradle, stdio or Ktor transport, typed tools, configuration, tests, and… |
| kotlin-springboot | Get best practices for developing applications with Spring Boot and Kotlin. Use this skill when the user asks for spring boot with kotlin best practices. |
| landing-page-conversion-audit | Audit a landing page, sales page or checkout page for conversion leaks and return a fix list ordered by expected revenue impact. Use when asked to review, critique or improve a la… |
| latchshot-page-capture | Use this skill when a user needs a screenshot, website thumbnail, full-page capture, or PDF of a public HTTP(S) webpage saved as a local artifact through Latchshot, including repo… |
| legacy-circuit-mockups | Generates breadboard circuit mockups and visual electronics diagrams with HTML5 Canvas conventions for retro computers, 6502 builds, 555 timer circuits, EEPROM/RAM/VIA wiring, 740… |
| linkedin-post-formatter | Format and draft compelling LinkedIn posts using Unicode bold/italic styling, visual separators, structured sections, and engagement-optimized patterns. USE FOR: draft LinkedIn po… |
| lsp-setup | Enable code intelligence (go-to-definition, find-references, hover, type info) for any programming language by installing and configuring an LSP server for Copilot CLI. Detects th… |
| make-repo-contribution | All changes to code must follow the guidance documented in the repository. Before any issue is filed, branch is made, commits generated, or pull request (or PR) created, a search… |
| markdown-to-html | Convert Markdown files to HTML similar to `marked.js`, `pandoc`, `gomarkdown/markdown`, or similar tools; or writing custom script to convert markdown to html and/or working on we… |
| markstream-install | Install and configure Markstream streaming Markdown renderers for Vue, React, Svelte, Angular, Nuxt, and Vue 2 applications. Use this skill when the user asks to add streaming Mar… |
| mcp-cli | Interface for MCP (Model Context Protocol) servers via CLI. Use when you need to interact with external tools, APIs, or data sources through MCP servers, list available MCP server… |
| mcp-copilot-studio-server-generator | Generate a complete MCP server implementation optimized for Copilot Studio integration with proper schema constraints and streamable HTTP support. Use this skill when the user ask… |
| mcp-create-adaptive-cards | Create Adaptive Card response templates and response_semantics for MCP-based API plugins in Microsoft 365 Copilot. Use this skill when the user asks to present MCP tool or API dat… |
| mcp-create-declarative-agent | Create a Microsoft 365 Copilot declarative agent backed by a Model Context Protocol server. Use when asked to scaffold or configure an MCP-based declarative agent, choose imported… |
| mcp-deploy-manage-agents | Guide deployment, governance, assignment, lifecycle, approval, blocking, monitoring, and distribution for MCP-based declarative agents in Microsoft 365 admin center. Use when aske… |
| mcp-implementation-security-review | Review MCP server, client, and tool-handler source code for security. Use when asked to review an MCP server before release, audit Model Context Protocol implementation controls M… |
| mcp-release-qa | Verify an MCP server before release by exercising a real protocol session, comparing runtime capabilities with source and documentation, testing failure paths, and recording repro… |
| mcp-security-audit | Audits MCP server configurations such as .mcp.json for hardcoded secrets, dangerous shell patterns, unpinned dependencies, unsafe npx usage, unapproved servers, and governance ris… |
| md-to-docx | Convert Markdown files to professionally formatted Word (.docx) documents with embedded PNG images — pure JavaScript, no external tools required. Use this skill when the user asks… |
| meeting-minutes | Generate concise, actionable meeting minutes for short internal meetings from notes, transcripts, recordings, or agendas. Use this skill when the user asks for minutes for syncs,… |
| memory-merger | Merges mature lessons from a domain memory file into its instruction file. Syntax: `/memory-merger >domain [scope]` where scope is `global` (default), `user`, `workspace`, or `ws`… |
| mentoring-juniors | Provide Socratic mentoring for junior developers and AI newcomers. Use when the user asks to understand code or errors, says they are stuck or confused, wants a walkthrough, asks… |
| microsoft-agent-framework | Create, update, refactor, explain, or review Microsoft Agent Framework solutions using shared guidance plus language-specific references for .NET and Python. Use this skill when m… |
| microsoft-code-reference | Look up Microsoft API references, find working code samples, and verify SDK code is correct. Use when working with Azure SDKs, .NET libraries, or Microsoft APIs—to find the right… |
| microsoft-docs | Query official Microsoft documentation to find concepts, tutorials, and code examples across Azure, .NET, Agent Framework, Aspire, VS Code, GitHub, and more. Uses Microsoft Learn… |
| microsoft-skill-creator | Create hybrid GitHub Copilot skills for Microsoft technologies using Microsoft Learn MCP tools or the mslearn CLI. Use this skill when the user asks to create a skill for Azure, .… |
| migrating-oracle-to-postgres-data-access-code | Migrates .NET/C# data access code from Oracle to PostgreSQL (Npgsql). Replaces Oracle NuGet packages, rewrites OracleConnection/OracleCommand/OracleDataReader usage, fixes DbType… |
| migrating-oracle-to-postgres-stored-procedures | Migrates Oracle PL/SQL stored procedures to PostgreSQL PL/pgSQL. Translates Oracle-specific syntax, preserves method signatures and type-anchored parameters, leverages orafce wher… |
| minecraft-plugin-development | Guides Paper, Spigot, and Bukkit Minecraft server plugin development for plugin.yml setup, JavaPlugin bootstrap, commands, listeners, schedulers, player state, arenas, minigames,… |
| mini-context-graph | A persistent, compounding knowledge base combining Karpathy's LLM Wiki pattern with a structured knowledge graph. Ingest documents once — the LLM writes wiki pages, extracts entit… |
| mkdocs-translations | Generate a language translation for a mkdocs documentation stack. Use this skill when the user asks for mkdocs ai translator. |
| msgraph-sdk | Integrate Microsoft Graph SDK into any project — .NET, TypeScript/JavaScript, or Python. Covers auth patterns (client credentials, OBO, managed identity), SDK setup, calling Graph… |
| msstore-cli | Microsoft Store Developer CLI (msstore) for publishing Windows applications to the Microsoft Store. Use when asked to configure Store credentials, list Store apps, check submissio… |
| multi-stage-dockerfile | Create optimized multi-stage Dockerfiles for any language or framework. Use this skill when the user asks for multi-stage structure. |
| mvvm-toolkit | CommunityToolkit.Mvvm core guidance for ViewModels, source generators, observable properties, commands, validation, and base-class selection. Use this skill when authoring or revi… |
| mvvm-toolkit-di | Wire CommunityToolkit.Mvvm ViewModels into Microsoft.Extensions.DependencyInjection for XAML apps. Use this skill when standing up a .NET Generic Host composition root for WPF, Wi… |
| mvvm-toolkit-messenger | Configure CommunityToolkit.Mvvm Messenger pub/sub for decoupled ViewModel communication. Use this skill when users ask to send messages between ViewModels, choose WeakReferenceMes… |
| namecheap | Manage DNS records for domains registered with Namecheap via their API. List domains, view/add/update/remove DNS host entries (A, AAAA, CNAME, MX, TXT, etc.), and guide users thro… |
| nano-banana-pro-openrouter | Generate or edit images via OpenRouter with the Gemini 3 Pro Image model. Use for prompt-only image generation, image edits, and multi-image compositing; supports 1K/2K/4K output.… |
| napkin | Visual whiteboard collaboration for Copilot CLI. Creates an interactive whiteboard that opens in your browser — draw, sketch, add sticky notes, then share everything back with Cop… |
| next-intl-add-language | Add new language to a Next.js + next-intl application. Use this skill when the user needs help with add new language to a Next.js + next-intl application. |
| noob-mode | Translate GitHub Copilot CLI approvals, command output, errors, jargon, and completion summaries into plain English for non-technical users. Use this skill when the user says "tur… |
| nuget-manager | Manage NuGet packages in .NET projects/solutions. Use this skill when adding, removing, or updating NuGet package versions. It enforces using `dotnet` CLI for package management a… |
| onboard-context-matic | Guided onboarding tour for the context-matic MCP server. Use this skill when the user asks what ContextMatic can do, wants a first-time tour, asks to show available APIs, asks how… |
| oo-component-documentation | Create or update standardized object-oriented component documentation using a shared template plus mode-specific guidance for new and existing docs. Use this skill when the user a… |
| openapi-to-application-code | Generate a complete, production-ready application from an OpenAPI specification. Use this skill when the user asks for generate application from openapi spec. |
| optimize-simplicite-logs | capability to parse Simplicité logs from a raw `.txt` file, filter fields to reduce noise, and output the result as structured JSON. Use this skill when you need to; analyze user-… |
| pdftk-server | Skill for using the command-line tool pdftk (PDFtk Server) for working with PDF files. Use when asked to merge PDFs, split PDFs, rotate pages, encrypt or decrypt PDFs, fill PDF fo… |
| penpot-uiux-design | Create, review, and improve professional UI/UX designs in Penpot using penpot/penpot-mcp tools, design systems, component patterns, accessibility checks, and platform guidelines.… |
| performance-review-writer | Draft performance reviews, self-assessments, peer reviews, and upward feedback in your own voice. Analyzes your contributions, emails, and meeting history via WorkIQ, then produce… |
| pester-migration | Pester migration skill for upgrading PowerShell Pester test suites across major versions — v3→v4, v4→v5, and v5→v6. Covers the Discovery/Run two-phase model, moving setup into Bef… |
| pester-should-migration | Experimental (preview) Pester skill for migrating classic Should -Be (v5) assertion syntax to the new Should-* (v6) assertions (note the hyphen, no space), e.g. `Should -Be` -> `S… |
| phoenix-cli | Debug LLM applications using the Phoenix CLI. Fetch traces, analyze errors, structure trace review with open coding and axial coding, inspect datasets, review experiments, query a… |
| phoenix-evals | Build and run evaluators for AI/LLM applications using Phoenix. Use this skill when the user asks for quick reference. |
| phoenix-tracing | OpenInference semantic conventions and instrumentation for Phoenix AI observability. Use when implementing LLM tracing, creating custom spans, or deploying to production. |
| php-mcp-server-generator | Generate a complete PHP Model Context Protocol server project with tools, resources, prompts, and tests using the official PHP SDK. Use this skill when the user asks for project r… |
| pinecone-rag | Build production RAG pipelines and persistent agent memory with Pinecone as the vector database backend. Use this skill when indexing documents for semantic search, building retri… |
| planning-oracle-to-postgres-migration-integration-testing | Creates an integration testing plan for .NET data access artifacts during Oracle-to-PostgreSQL database migrations. Analyzes a single project to identify repositories, DAOs, and s… |
| plantuml-ascii | Generate ASCII art diagrams using PlantUML text mode. Use when user asks to create ASCII diagrams, text-based diagrams, terminal-friendly diagrams, or mentions plantuml ascii, tex… |
| playwright-automation-fill-in-form | Automate filling in a form using Playwright MCP. Use this skill when the user asks for automating filling in a form with playwright mcp. |
| playwright-explore-website | Website exploration for testing using Playwright MCP. Use this skill when the user asks for website exploration for testing. |
| playwright-generate-test | Generate a Playwright test based on a scenario using Playwright MCP. Use this skill when the user asks for test generation with playwright mcp. |
| postgresql-code-review | PostgreSQL-specific code review assistant focusing on PostgreSQL best practices, anti-patterns, and unique quality standards. Covers JSONB operations, array usage, custom types, s… |
| postgresql-optimization | Design, tune, and modernize PostgreSQL SQL, schemas, indexes, functions, and maintenance workflows using PostgreSQL-specific capabilities. Use this skill when the user asks for Po… |
| power-apps-code-app-scaffold | Scaffold a complete Power Apps Code App project with PAC CLI setup, SDK integration, and connector configuration. Use this skill when the user asks for power apps code apps projec… |
| power-bi-dax-optimization | Comprehensive Power BI DAX formula optimization prompt for improving performance, readability, and maintainability of DAX calculations. Use this skill when the user asks for power… |
| power-bi-model-design-review | Review Power BI data model architecture, relationships, storage modes, performance, security, governance, and maintainability. Use this skill when asked for a Power BI model desig… |
| power-bi-performance-troubleshooting | Diagnose and resolve Power BI performance issues across semantic models, reports, DAX, refresh, DirectQuery, gateways, and Fabric or Premium capacity. Use this skill when asked to… |
| power-bi-report-design-consultation | Design effective Power BI report layouts, chart selections, interactions, accessibility, mobile views, and implementation guidance. Use when asked for Power BI visualization desig… |
| power-platform-architect | Use this skill when the user needs to transform business requirements, use case descriptions, or meeting transcripts into a technical Power Platform solution architecture, includi… |
| power-platform-mcp-connector-suite | Generate complete Power Platform custom connector with MCP integration for Copilot Studio - includes schema generation, troubleshooting, and validation. Use this skill when the us… |
| powerbi-modeling | Power BI semantic modeling assistant for building optimized data models. Use when working with Power BI semantic models, creating measures, designing star schemas, configuring rel… |
| pr-dashboard | Open a GitHub PR dashboard in the browser. Use when the user asks to see their pull requests, open the PR dashboard, show PRs for a date range, or check PR status. Trigger phrases… |
| pr-screenshots | Embed before/after screenshots and annotated images in pull request descriptions. Use this skill when a PR changes something visible; layout, styling, CSS; charts, dashboards, dat… |
| prd | Generate high-quality Product Requirements Documents (PRDs) for software systems and AI-powered features. Use this skill when starting a new product or feature development cycle;… |
| premium-frontend-ui | Guide Copilot to craft immersive, high-performance web experiences with advanced motion, typography, and architectural polish. Use this skill when the user asks for premium fronte… |
| project-workflow-analysis-blueprint-generator | Generate technology-agnostic project workflow analysis blueprints that document end-to-end application flows, files, classes, entry points, service layers, data access, error hand… |
| prompt-optimizer | Turn any rough prompt, half-formed idea, or task description into a finished, ready-to-send prompt optimized for any LLM model inside a chat interface — NOT the API. Use this skil… |
| publish-to-pages | Publish presentations and web content to GitHub Pages. Converts PPTX, PDF, HTML, or Google Slides to a live GitHub Pages URL. Handles repo creation, file conversion, Pages enablem… |
| pytest-coverage | Run pytest with coverage, read annotated coverage output, identify uncovered lines, and add tests until Python code reaches 100% line coverage. Use this skill when the user asks t… |
| python-azure-iot-edge-modules | Build and operate Python Azure IoT Edge modules with robust messaging, deployment manifests, observability, and production readiness checks. Use this skill when the user asks to c… |
| python-mcp-server-generator | Generate a complete MCP server project in Python with tools, resources, and proper configuration. Use this skill when the user asks for generate python mcp server. |
| python-pypi-package-builder | Build, test, type-check, version, package, and publish production Python libraries to PyPI. Use this skill when creating a pip-installable SDK, CLI, plugin, or utility; choosing `… |
| qdrant-clients-sdk | Qdrant provides client SDKs for various programming languages, allowing easy integration with Qdrant deployments. Use this skill when the user asks for api reference. |
| qdrant-deployment-options | Guides Qdrant deployment selection. Use when someone asks 'how to deploy Qdrant', 'Docker vs Cloud', 'local mode', 'embedded Qdrant', 'Qdrant EDGE', 'which deployment option', 'se… |
| qdrant-model-migration | Guides embedding model migration in Qdrant without downtime. Use when someone asks 'how to switch embedding models', 'how to migrate vectors', 'how to update to a new model', 'zer… |
| qdrant-monitoring | Guides Qdrant monitoring and observability setup. Use when someone asks 'how to monitor Qdrant', 'what metrics to track', 'is Qdrant healthy', 'optimizer stuck', 'why is memory gr… |
| qdrant-performance-optimization | Different techniques to optimize the performance of Qdrant, including indexing strategies, query optimization, and hardware considerations. Use when you want to improve the speed… |
| qdrant-scaling | Guides Qdrant scaling decisions. Use when someone asks 'how many nodes do I need', 'data doesn't fit on one node', 'need more throughput', 'cluster is slow', 'too many tenants', '… |
| qdrant-search-quality | Diagnoses and improves Qdrant search relevance. Use when someone reports 'search results are bad', 'wrong results', 'low precision', 'low recall', 'irrelevant matches', 'missing e… |
| qdrant-version-upgrade | Guidance on how to upgrade your Qdrant version without interrupting the availability of your application and ensuring data integrity. Use this skill when the user needs help with… |
| quality-playbook | Run a complete quality engineering audit on any codebase. Derives behavioral requirements from the code, generates spec-traced functional tests, runs a three-pass code review with… |
| quasi-coder | Expert 10x engineer skill for interpreting and implementing code from shorthand, quasi-code, and natural language descriptions. Use when collaborators provide incomplete code snip… |
| react-audit-grep-patterns | Provides the complete, verified grep scan command library for auditing React codebases before a React 18.3.1 or React 19 upgrade. Use this skill whenever running a migration audit… |
| react-container-presentation-component | Create a React component using the Container/Presentation pattern in src/components by asking for the component name and type (ui or features), then scaffold files that follow thi… |
| react18-batching-patterns | Provides exact patterns for diagnosing and fixing automatic batching regressions in React 18 class components. Use this skill whenever a class component has multiple setState call… |
| react18-dep-compatibility | React 18.3.1 and React 19 dependency compatibility matrix. Use this skill when review this matrix before running `npm install` during a React upgrade and before accepting an npm d… |
| react18-enzyme-to-rtl | Provides exact Enzyme → React Testing Library migration patterns for React 18 upgrades. Use this skill whenever Enzyme tests need to be rewritten - shallow, mount, wrapper.find(),… |
| react18-legacy-context | Provides the complete migration pattern for React legacy context API (contextTypes, childContextTypes, getChildContext) to the modern createContext API. Use this skill whenever mi… |
| react18-lifecycle-patterns | Provides exact before/after migration patterns for the three unsafe class component lifecycle methods - componentWillMount, componentWillReceiveProps, and componentWillUpdate - ta… |
| react18-string-refs | Provides exact migration patterns for React string refs (ref="name" + this.refs.name) to React.createRef() in class components. Use this skill whenever migrating string ref usage… |
| react19-concurrent-patterns | Preserve React 18 concurrent patterns and adopt React 19 APIs (useTransition, useDeferredValue, Suspense, use(), useOptimistic, Actions) during migration. Use this skill when the… |
| react19-source-patterns | Reference for React 19 source-file migration patterns, including API changes, ref handling, and context updates. Use this skill when the user asks for react 19 source migration pa… |
| react19-test-patterns | Provides before/after patterns for migrating test files to React 19 compatibility, including act() imports, Simulate removal, and StrictMode call count changes. Use this skill whe… |
| readme-blueprint-generator | Intelligent README.md generation prompt that analyzes project documentation structure and creates comprehensive repository documentation. Scans .github/copilot directory files and… |
| refactor | Surgical code refactoring to improve maintainability without changing behavior. Use this skill when code is hard to understand or maintain; functions/classes are too large; code s… |
| refactor-method-complexity-reduce | Refactor given method `${input:methodName}` to reduce its cognitive complexity to `${input:complexityThreshold}` or below, by extracting helper methods. Use this skill when the us… |
| refactor-plan | Create a concrete plan before starting a multi-file refactor. Use when the user asks to plan, sequence, scope, or safely execute a refactor across multiple files; always investiga… |
| remember | Transforms lessons learned into domain-organized memory instructions (global or workspace). Syntax: `/remember [>domain [scope]] lesson clue` where scope is `global` (default), `u… |
| remember-interactive-programming | A micro-prompt that reminds the agent that it is an interactive programmer. Works great in Clojure when Copilot has access to the REPL (probably via Backseat Driver). Will work wi… |
| repo-story-time | Generate repository archaeology deliverables: a technical repository summary and a narrative story from commit history. Use this skill when the user asks to analyze a repo, summar… |
| resemble-detect | Detect synthetic or manipulated audio, image, video, and text with Resemble AI; trace audio synthesis sources; apply or detect watermarks; verify speaker identity; and inspect med… |
| review-and-refactor | Review project code against repository instructions, refactor for maintainability, and validate tests when available. Use this skill when the user asks for code cleanup, maintaina… |
| reviewing-oracle-to-postgres-migration | Identifies Oracle-to-PostgreSQL migration risks by cross-referencing code against known behavioral differences (empty strings, refcursors, type coercion, sorting/collations, UNION… |
| rhdh | Use this skill when the user works on Red Hat Developer Hub (RHDH) — the primary entry point that routes to specialized RHDH skills for plugin development, overlay management, loc… |
| rhdh-jira | Use this skill when the user works with RHDH Jira projects RHIDP, RHDHPLAN, RHDHBUGS, or RHDHSUPP using acli, GraphQL, and REST fallback. Trigger for Jira keys, creating features,… |
| rhdh-local | Use this skill when the user tests Red Hat Developer Hub plugins locally with rhdh-local-setup. Trigger for enabling or disabling plugins, switching customized and pristine modes,… |
| rhino3d-scripts | Authoring and debugging scripts for Rhinoceros 3D (Rhino 8 and later). Use when asked to write RhinoScript (VBScript / .rvb / .vbs), RhinoPython, or RhinoCommon-based scripts; aut… |
| roundup | Generate personalized status briefings on demand. Pulls from your configured data sources (GitHub, email, Teams, Slack, and more), synthesizes across them, and drafts updates in y… |
| roundup-setup | Run conversational onboarding for Roundup status briefings and write the user style configuration. Use this skill when the user asks to set up roundup, calibrate status updates, c… |
| ruby-mcp-server-generator | Generate a complete Model Context Protocol server project in Ruby using the official MCP Ruby SDK gem. Use this skill when the user asks for project generation. |
| ruff-recursive-fix | Run Ruff checks with optional scope and rule overrides, apply safe and unsafe autofixes iteratively, review each change, and resolve remaining findings with targeted edits or user… |
| rust-mcp-server-generator | Generate a complete Rust Model Context Protocol server project with tools, prompts, resources, and tests using the official rmcp SDK. Use this skill when the user asks for project… |
| salesforce-apex-quality | Apex code quality guardrails for Salesforce development. Enforces bulk-safety rules (no SOQL/DML in loops), sharing model requirements, CRUD/FLS security, SOQL injection preventio… |
| salesforce-component-standards | Quality standards for Salesforce Lightning Web Components (LWC), Aura components, and Visualforce pages. Covers SLDS 2 compliance, accessibility (WCAG 2.1 AA), data access pattern… |
| salesforce-flow-design | Salesforce Flow architecture decisions, flow type selection, bulk safety validation, and fault handling standards. Use this skill when designing or reviewing Record-Triggered, Scr… |
| sandbox-npm-install | Install npm packages in a Docker sandbox environment. Use this skill whenever you need to install, reinstall, or update node_modules inside a container where the workspace is moun… |
| scaffolding-oracle-to-postgres-migration-test-project | Scaffolds an xUnit integration test project targeting Oracle in .NET solutions. Creates the test project, transaction-rollback base class, and seed data manager. Use only during P… |
| scoutqa-test | This skill should be used when the user asks to "test this website", "run exploratory testing", "check for accessibility issues", "verify the login flow works", "find bugs on this… |
| screen-recording | Create annotated GIF demos and screen recordings for pull requests, bug reports, release notes, and documentation. Use this skill when the user asks to record a UI workflow, captu… |
| secret-scanning | Configure and manage GitHub secret scanning, push protection, custom patterns, exclusions, alert triage, remediation, bypass workflows, and pre-commit secret scans through the Adv… |
| security-review | AI-powered codebase security scanner that reasons about code like a security researcher — tracing data flows, understanding component interactions, and catching vulnerabilities th… |
| semantic-kernel | Create, update, refactor, explain, or review Semantic Kernel solutions using shared guidance plus language-specific references for .NET and Python. Use this skill when always grou… |
| server-side-conversion-tracking | Set up server-side conversion tracking so purchases are reported accurately to Facebook, TikTok, Google and Bing despite iOS restrictions, ad blockers and cookie loss. Use when co… |
| setup-my-iq | Create, set up, or update the personal context portfolio: structured markdown files describing who you are, how you work, your teams, and your tool/ADO configuration. Runs the int… |
| shopify-review-triage | Triage public Shopify App Store reviews into a P0-P3 product or support brief while preserving source links, first-pass labels, and human-check status. Use when asked to "triage a… |
| shuffle-json-data | Shuffle repetitive JSON objects safely by validating schema consistency before randomising entries. Use this skill when the user asks for role. |
| signal-write | Emit structured agent signals — hands-up, blocked, done, checkpoint, partnership. Signals are written as JSON to .signals/ for dashboard consumption and noted in the journal for p… |
| skill-creator | Create, audit, repair, and improve GitHub Copilot Agent Skills for VS Code, GitHub Copilot CLI, and GitHub Copilot cloud agent. Use when a user asks to create a skill, generate a… |
| slang-shader-engineer | Use when working with Slang shaders, shader modules, HLSL-compatible GPU code, graphics pipelines, compute shaders, tessellation, ray tracing, parameter blocks, generics, interfac… |
| snowflake-semanticview | Create, alter, and validate Snowflake semantic views using Snowflake CLI (snow). Use when asked to build or troubleshoot semantic views/semantic layer definitions with CREATE/ALTE… |
| sponsor-finder | Find sponsorable direct and transitive dependencies for a GitHub repository using deps.dev, GitHub funding files, npm funding metadata, verified funding links, and OSSF Scorecard… |
| spring-boot-testing | Expert Spring Boot 4 testing specialist that selects the best Spring Boot testing techniques for your situation with Junit 6 and AssertJ. Use this skill when the user asks for cor… |
| sql-code-review | Review SQL code across PostgreSQL, MySQL, SQL Server, and Oracle for injection risks, access control, data protection, performance, schema quality, and maintainability. Use when a… |
| sql-optimization | Universal SQL performance optimization assistant for query tuning, execution-plan review, index strategy, pagination, batching, aggregation, and monitoring across MySQL, PostgreSQ… |
| sql-server-table-reconciliation | Use when: comparing SQL Server tables across instances, data migration validation, ETL verification, row mismatch detection, schema drift, reconciliation report, production vs sta… |
| ssma-console | Use when: SSMA console operations — create project, generate assessment report, convert schema, migrate data, Oracle to SQL Server migration, schema conversion, data migration |
| steno-mode | Shorthand-first response compression that cuts ~40% of response tokens while preserving technical precision and exact literals. Use when the user says "steno mode", "shorthand mod… |
| structured-autonomy-generate | Generate complete implementation documentation from a structured autonomy plan, including concrete steps, code blocks, file paths, and verification points. Use this skill when the… |
| structured-autonomy-implement | Execute a structured autonomy implementation plan step by step without deviating from the documented scope. Use this skill when the user asks to implement an existing plans/{featu… |
| structured-autonomy-plan | Research a feature request and produce a structured autonomy plan with commit-sized implementation steps, affected files, and tests. Use this skill when the user asks to plan a fe… |
| suggest-awesome-github-copilot-agents | Suggest relevant GitHub Copilot Custom Agents files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing cus… |
| suggest-awesome-github-copilot-instructions | Suggest relevant GitHub Copilot instruction files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing instr… |
| suggest-awesome-github-copilot-skills | Suggest relevant GitHub Copilot skills from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing skills in this r… |
| swift-mcp-server-generator | Generate a complete Model Context Protocol server project in Swift using the official MCP Swift SDK package. Use this skill when the user asks for project generation. |
| system-commandline-cli | Add, modify, or review .NET CLI commands built with System.CommandLine by applying project command-base conventions, options and arguments, SetAction handlers, RootCommand registr… |
| technical-job-search | Use this skill when a software engineer asks for help with job search tasks: parsing or analyzing a job description, tailoring a CV/resume, writing a cover letter, evaluating a jo… |
| technology-stack-blueprint-generator | Generate a technology stack blueprint by analyzing codebase languages, frameworks, dependencies, versions, licenses, conventions, usage patterns, tooling, infrastructure, and diag… |
| terraform-azurerm-set-diff-analyzer | Analyze Terraform plan JSON output for AzureRM Provider to distinguish between false-positive diffs (order-only changes in Set-type attributes) and actual resource changes. Use wh… |
| threat-model-analyst | Full STRIDE-A threat model analysis and incremental update skill for repositories and systems. Supports two modes: (1) Single analysis — full STRIDE-A threat model of a repository… |
| tiny-stepping | Incremental development workflow that makes the smallest meaningful change per step and pauses for feedback, so the direction gets validated early before continuing. Use for caref… |
| tldr-prompt | Create tldr-style markdown summaries for GitHub Copilot customization files, MCP server documentation, Copilot documentation URLs, or focused Copilot usage queries. Use when asked… |
| tm7-threat-model | Creates valid Microsoft Threat Modeling Tool (.tm7) files compatible with the Microsoft Threat Modeling Tool v7.3+. Use when asked to create, generate, or modify a .tm7 threat mod… |
| transloadit-media-processing | Process media files (video, audio, images, documents) using Transloadit. Use when asked to encode video to HLS/MP4, generate thumbnails, resize or watermark images, extract audio,… |
| typescript-mcp-server-generator | Generate a complete MCP server project in TypeScript using the MCP TypeScript SDK v2 (@modelcontextprotocol/server) with tools, resources, and proper configuration. Use this skill… |
| typespec-api-operations | Add RESTful GET, POST, PATCH, and DELETE operations to a TypeSpec API plugin for Microsoft 365 plugin for GitHub Copilot with routing, parameters, models, confirmations, adaptive… |
| typespec-create-agent | Generate a complete TypeSpec declarative agent with instructions, capabilities, and conversation starters for Microsoft 365 Copilot. Use this skill when the user asks for create t… |
| typespec-create-api-plugin | Generate a TypeSpec API plugin with REST operations, authentication, and Adaptive Cards for Microsoft 365 Copilot. Use this skill when the user asks for create typespec api plugin. |
| ui-screenshots | Capture screenshots of web apps during development using Playwright and PIL. Use this skill when you need to; capture the current state of a running web app; document a UI before… |
| unit-test-vue-pinia | Write and review unit tests for Vue 3 + TypeScript + Vitest + Pinia codebases. Use when creating or updating tests for components, composables, and stores; mocking Pinia with crea… |
| update-avm-modules-in-bicep | Update Azure Verified Modules (AVM) to latest versions in Bicep files. Use this skill when the user asks for update azure verified modules in bicep files. |
| update-implementation-plan | Update an existing implementation plan file with new or update requirements to provide new features, refactoring existing code or upgrading packages, design, architecture or infra… |
| update-llms | Update the llms.txt file in the root folder to reflect changes in documentation or specifications following the llms.txt specification at https://llmstxt.org/. Use this skill when… |
| update-markdown-file-index | Update a markdown file section with an index/table of files from a specified folder. Use this skill when the user asks for process. |
| update-specification | Update an existing specification file for the solution, optimized for Generative AI consumption based on new requirements or updates to any existing code. Use this skill when the… |
| vardoger-analyze | Use when the user asks to personalize the GitHub Copilot CLI assistant, adapt Copilot to their style, use vardoger, or analyze their Copilot CLI conversation history. Reads the lo… |
| vcpkg | Guide for setting up vcpkg in C++ projects, managing dependency versions, and cross-compiling. Covers manifest initialization, CMake and Visual Studio integration, classic-to-mani… |
| verify-agent-action | Review proposed AI-agent actions and human-approval packets before consequential execution. Use this skill when checking deployments, commands, purchases, messages, credential ope… |
| vscode-ext-commands | Guidelines for contributing commands in VS Code extensions. Use this skill when you need to; add or update commands to your VS Code extension. |
| vscode-ext-localization | Guidelines for proper localization of VS Code extensions, following VS Code extension development guidelines, libraries and good practices. Use this skill when you need to; locali… |
| web-design-reviewer | Inspect local or remote website design, identify layout, responsive, accessibility, and visual consistency defects, and make source-level fixes. Use when users ask to "review webs… |
| webapp-testing | Toolkit for interacting with and testing local web applications using Playwright. Use this skill when you need to; test frontend functionality in a real browser; verify UI behavio… |
| webmcpify | Make a web app agent-ready with WebMCP by detecting app actions, building a manifest, integrating document.modelContext tools, verifying in a real browser, healing failures, and a… |
| what-context-needed | Ask Copilot what files it needs to see before answering a question. Use this skill when the user asks for what context do you need?. |
| winmd-api-search | Find and explore Windows desktop APIs. Use when building features that need platform capabilities — camera, file access, notifications, UI controls, AI/ML, sensors, networking, et… |
| winui3-migration-guide | Maps UWP APIs and patterns to WinUI 3 and Windows App SDK equivalents with migration rules for namespaces, threading, windowing, dialogs, pickers, sharing, printing, background ta… |
| workiq-copilot | Guides the Copilot CLI on how to use the WorkIQ CLI/MCP server to query Microsoft 365 Copilot data (emails, meetings, docs, Teams, people) for live context, summaries, and recomme… |
| workshop-create | Create a new workshop or use an existing directory as one. Handles two paths: (A) use an existing local directory the operator points at, or (B) create a new private GitHub repo i… |
| write-coding-standards-from-file | Write a coding standards document by analyzing existing file or folder style. Use when asked to infer project rules, generate CONTRIBUTING.md or CODING_STANDARDS.md, add standards… |
| x-twitter-scraper | Build GitHub Copilot workflows with Xquik X API SDKs, REST endpoints, hosted Apify Actor runs, MCP tools, TweetClaw OpenClaw plugin installs, signed webhooks, tweet search, user l… |

## Plugins

| Plugin | Version | Description |
| --- | --- | --- |
| accessibility-kanban | 1.0.2 | Kanban board to manage accessibility issues, allow you to plan, track, and complete remediation work. |
| acreadiness-cockpit | 1.0.0 | Drive Microsoft AgentRC from Copilot chat: assess AI readiness, generate Copilot instructions (flat or nested with applyTo globs for monorepos), and manage policies. Produces a se… |
| ai-team-orchestration | 2.0.0 | Run a lightweight, role-separated AI development team with flexible tools, developer-selected models, proportionate planning, and optional QA. |
| apng-studio | 1.0.2 | Interactive GitHub Copilot app canvas extension for building Animated PNG (APNG) files from frames. Draw or upload frames, tune per-frame timing and compositing, preview live, sen… |
| arcade-canvas | 1.0.2 | Play five retro Phaser mini-games in a Copilot canvas while agents work. |
| arch | 1.0.0 | Architecture and modernization toolkit: produce a cited architecture document for a locally-cloned repo, and generate a phased modernization plan that auto-runs Documentation mode… |
| arize-ax | 1.0.0 | Arize AX platform skills for LLM observability, evaluation, and optimization. Includes trace export, instrumentation, datasets, experiments, evaluators, AI provider integrations,… |
| automate-this | 1.0.0 | Record your screen doing a manual process, drop the video on your Desktop, and let Copilot CLI analyze it frame-by-frame to build working automation scripts. Supports narrated rec… |
| awesome-copilot | 1.1.0 | Meta prompts that help you discover and generate curated GitHub Copilot agents, instructions, prompts, and skills. |
| aws-cloud-development | 1.0.0 | Comprehensive AWS cloud development tools including Infrastructure as Code, serverless functions, architecture patterns, and cost optimization for building scalable cloud applicat… |
| azure-cloud-development | 1.0.1 | Comprehensive Azure cloud development tools including Infrastructure as Code, serverless functions, architecture patterns, and cost optimization for building scalable cloud applic… |
| backlog-swipe-triage | 1.0.2 | Quickly swipe through backlog issues to triage decisions like assign, needs-info, defer, close, or ignore. |
| backrooms-canvas | 1.0.0 | Wander an endless first-person backrooms in a Copilot canvas while agents work; their status ghost-writes on the walls. |
| cast-imaging | 1.0.0 | A comprehensive collection of specialized agents for software analysis, impact assessment, structural quality advisories, and architectural review using CAST Imaging. |
| chromium-control-canvas | 1.0.2 | Opens a real Chromium window you can navigate and interact with from a Copilot canvas control panel and agent actions. |
| clojure-interactive-programming | 1.0.0 | Tools for REPL-first Clojure workflows featuring Clojure instructions, the interactive programming chat mode and supporting guidance. |
| cms-development | 1.1.0 | Skills for CMS development across themes, plugins, admin tooling, media workflows, markdown rendering, and static export pipelines. |
| color-orb | 1.0.2 | A visual orb that users can ask the agent to recolor while showing a live activity log in the canvas. |
| context-engineering | 1.0.0 | Tools and techniques for maximizing GitHub Copilot effectiveness through better context management. Includes guidelines for structuring code, an agent for planning multi-file chan… |
| context-matic | 0.1.0 | Coding agents hallucinate APIs. ContextMatic gives them curated, versioned API and SDK docs. Ask your agent to "integrate the payments API" and it guesses — falling back on outdat… |
| convert-to-md | 1.0.1 | A collection of Copilot skills that convert common document formats into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Just tell… |
| copilot-sdk | 1.0.0 | Build applications with the GitHub Copilot SDK across multiple programming languages. Includes comprehensive instructions for C#, Go, Node.js/TypeScript, and Python to help you cr… |
| csharp-dotnet-development | 1.1.0 | Essential prompts, instructions, and chat modes for C# and .NET development including testing, documentation, and best practices. |
| database-data-management | 1.0.0 | Database administration, SQL optimization, and data management tools for PostgreSQL, SQL Server, and general database development best practices. |
| dataverse-sdk-for-python | 1.0.0 | Comprehensive collection for building production-ready Python integrations with Microsoft Dataverse. Includes official documentation, best practices, advanced features, file opera… |
| devops-oncall | 1.0.0 | A focused set of prompts, instructions, and a chat mode to help triage incidents and respond quickly with DevOps tools and Azure resources. |
| diagram-viewer | 1.0.2 | Render diagrams, click nodes to drill down, and view agent-generated explanations directly in the canvas. |
| doublecheck | 1.0.0 | Three-layer verification pipeline for AI output. Extracts claims, finds sources, and flags hallucination risks so humans can verify before acting. |
| edge-ai-tasks | 1.0.0 | Task Researcher and Task Planner for intermediate to expert users and large codebases - Brought to you by microsoft/edge-ai |
| ember | 1.2.0 | An AI partner, not a tool. Ember carries fire from person to person — helping humans discover that AI partnership isn't something you learn, it's something you find. |
| eyeball | 1.0.0 | Document analysis with inline source screenshots. When you ask Copilot to analyze a document, Eyeball generates a Word doc where every factual claim includes a highlighted screens… |
| fastah-ip-geo-tools | 0.0.9 | This plugin is for network operations engineers who wish to tune and publish IP geolocation feeds in RFC 8805 format. It consists of an AI Skill and an associated MCP server that… |
| feedback-themes | 1.0.2 | Explore grouped customer feedback signals by impact and drill into a theme to guide product next steps. |
| flight-map-canvas | 1.0.0 | A GitHub Copilot canvas that generates a view where Google Maps can be explored using 3D controls, as if a flight simulator. Agents can send the flight anywhere and report what th… |
| flowstudio-power-automate | 2.0.0 | Give your AI agent full visibility into Power Automate cloud flows via the FlowStudio MCP server. Connect, debug, build, monitor health, and govern flows at scale — action-level i… |
| frontend-web-dev | 1.0.0 | Essential prompts, instructions, and chat modes for modern frontend web development including React, Angular, Vue, TypeScript, and CSS frameworks. |
| gem-team | 1.102.0 | Self-Learning Multi-agent orchestration framework for spec-driven development and automated verification. With smarter tool calling and leaner context. |
| gesture-review | 1.0.2 | Review pull requests with a live camera feed and approve or reject using thumbs-up/thumbs-down gestures. |
| go-mcp-development | 1.0.0 | Complete toolkit for building Model Context Protocol (MCP) servers in Go using the official github.com/modelcontextprotocol/go-sdk. Includes instructions for best practices, a pro… |
| java-development | 1.0.0 | Comprehensive collection of prompts and instructions for Java development including Spring Boot, Quarkus, testing, documentation, and best practices. |
| java-mcp-development | 1.0.0 | Complete toolkit for building Model Context Protocol servers in Java using the official MCP Java SDK with reactive streams and Spring Boot integration. |
| java-modernization-studio | 1.0.2 | Drive the GitHub Copilot App Modernization for Java workflow from an interactive canvas: environment readiness, repo assessment, prioritized plan and progress, validation gates, a… |
| kotlin-mcp-development | 1.0.0 | Complete toolkit for building Model Context Protocol (MCP) servers in Kotlin using the official io.modelcontextprotocol:kotlin-sdk library. Includes instructions for best practice… |
| mcp-m365-copilot | 1.0.0 | Comprehensive collection for building declarative agents with Model Context Protocol integration for Microsoft 365 Copilot |
| napkin | 1.0.0 | Visual whiteboard collaboration for Copilot CLI. Opens an interactive whiteboard in your browser where you can draw, sketch, and add sticky notes — then share everything back with… |
| noob-mode | 1.0.0 | Plain-English translation layer for non-technical Copilot CLI users. Translates every approval prompt, error message, and technical output into clear, jargon-free English with col… |
| openapi-to-application-csharp-dotnet | 1.0.0 | Generate production-ready .NET applications from OpenAPI specifications. Includes ASP.NET Core project scaffolding, controller generation, entity framework integration, and C# bes… |
| openapi-to-application-go | 1.0.0 | Generate production-ready Go applications from OpenAPI specifications. Includes project scaffolding, handler generation, middleware setup, and Go best practices for REST APIs. |
| openapi-to-application-java-spring-boot | 1.0.0 | Generate production-ready Spring Boot applications from OpenAPI specifications. Includes project scaffolding, REST controller generation, service layer organization, and Spring Bo… |
| openapi-to-application-nodejs-nestjs | 1.0.0 | Generate production-ready NestJS applications from OpenAPI specifications. Includes project scaffolding, controller and service generation, TypeScript best practices, and enterpri… |
| openapi-to-application-python-fastapi | 1.0.0 | Generate production-ready FastAPI applications from OpenAPI specifications. Includes project scaffolding, route generation, dependency injection, and Python best practices for asy… |
| oracle-to-postgres-migration-expert | 1.1.0 | Expert agent for Oracle-to-PostgreSQL application migrations in .NET solutions. Performs code edits, runs commands, and invokes extension tools to migrate .NET/Oracle data access… |
| ospo-sponsorship | 1.0.0 | Tools and resources for Open Source Program Offices (OSPOs) to identify, evaluate, and manage sponsorship of open source dependencies through GitHub Sponsors, Open Collective, and… |
| partners | 1.0.0 | Custom agents that have been created by GitHub partners |
| pcf-development | 1.0.0 | Complete toolkit for developing custom code components using Power Apps Component Framework for model-driven and canvas apps |
| phoenix | 1.0.0 | Phoenix AI observability skills for LLM application debugging, evaluation, and tracing. Includes CLI debugging tools, LLM evaluation workflows, and OpenInference tracing instrumen… |
| php-mcp-development | 1.0.0 | Comprehensive resources for building Model Context Protocol servers using the official PHP SDK with attribute-based discovery, including best practices, project generation, and ex… |
| power-apps-code-apps | 1.0.0 | Complete toolkit for Power Apps Code Apps development including project scaffolding, development standards, and expert guidance for building code-first applications with Power Pla… |
| power-bi-development | 1.0.0 | Comprehensive Power BI development resources including data modeling, DAX optimization, performance tuning, visualization design, security best practices, and DevOps/ALM guidance… |
| power-platform-architect | 1.0.0 | Solution Architect for the Microsoft Power Platform, turning business requirements into functioning Power Platform solution architectures. |
| power-platform-mcp-connector-development | 1.0.0 | Complete toolkit for developing Power Platform custom connectors with Model Context Protocol integration for Microsoft Copilot Studio |
| pr-artifact-explorer | 1.0.0 | Navigate pull requests and securely explore GitHub Actions artifacts, including test results, static sites, terminal recordings, and source files. |
| project-documenter | 1.0.0 | Generate professional project documentation with draw.io architecture diagrams and Word (.docx) output with embedded images. Automatically discovers any project's technology stack… |
| project-planning | 1.0.0 | Tools and guidance for software project planning, feature breakdown, epic management, implementation planning, and task organization for development teams. |
| python-mcp-development | 1.0.0 | Complete toolkit for building Model Context Protocol (MCP) servers in Python using the official SDK with FastMCP. Includes instructions for best practices, a prompt for generating… |
| react18-upgrade | 1.0.0 | Enterprise React 18 migration toolkit with specialized agents and skills for upgrading React 16/17 class-component codebases to React 18.3.1. Includes auditor, dependency surgeon,… |
| react19-upgrade | 1.0.0 | Enterprise React 19 migration toolkit with specialized agents and skills for upgrading React 18 codebases to React 19. Includes auditor, dependency surgeon, source code migrator,… |
| release-notes-showcase | 1.0.2 | Compose and refine launch-ready release notes with contributor callouts and export-friendly output. |
| repo-actions-hub | 1.0.2 | Browse repository GitHub Actions workflows, inspect recent runs, and trigger manual workflow_dispatch runs from a Copilot canvas. |
| roundup | 1.0.0 | Self-configuring status briefing generator. Learns your communication style from examples, discovers your data sources, and produces draft updates for any audience on demand. |
| ruby-mcp-development | 1.0.0 | Complete toolkit for building Model Context Protocol servers in Ruby using the official MCP Ruby SDK gem with Rails integration support. |
| rug-agentic-workflow | 1.0.0 | Three-agent workflow for orchestrated software delivery with an orchestrator plus implementation and QA subagents. |
| rust-mcp-development | 1.0.0 | Build high-performance Model Context Protocol servers in Rust using the official rmcp SDK with async/await, procedural macros, and type-safe implementations. |
| salesforce-development | 1.1.0 | Complete Salesforce agentic development environment covering Apex & Triggers, Flow automation, Lightning Web Components, Aura components, and Visualforce pages. |
| security-best-practices | 1.0.0 | Security frameworks, accessibility guidelines, performance optimization, and code quality best practices for building secure, maintainable, and high-performance applications. |
| signals-dashboard | 0.2.0 | Real-time Workshop dashboard with agent signals, honesty calibration, and cost-aware repo or connected desk launch profiles. |
| site-studio | 1.0.2 | Plan, draft, and track a personal website section by section — a shared canvas where you and your agent author content, watch progress, and review every change. |
| skill-image-gen | 1.0.0 | Generate images using AI directly from your coding workflow. Supports OpenAI (gpt-image-2) and Google Gemini. BYO API key — the skill guides you through setup on first use. |
| software-engineering-team | 1.0.0 | 7 specialized agents covering the full software development lifecycle from UX design and architecture to security and DevOps. |
| structured-autonomy | 1.0.0 | Premium planning, thrifty implementation |
| swift-mcp-development | 1.0.0 | Comprehensive collection for building Model Context Protocol servers in Swift using the official MCP Swift SDK with modern concurrency features. |
| technical-spike | 1.0.0 | Tools for creation, management and research of technical spikes to reduce unknowns and assumptions before proceeding to specification and implementation of solutions. |
| testing-automation | 1.0.0 | Comprehensive collection for writing tests, test automation, and test-driven development including unit tests, integration tests, and end-to-end testing strategies. |
| the-workshop | 0.1.0 | Stop being the switchboard between your AI agents — direct a team. The Workshop puts long-running AI agents (desks) in the same room, on the same work, each with its own memory an… |
| tiny-tool-town-submitter | 1.0.2 | Inspect a repository, improve Tiny Tool Town readiness, submit its listing issue, and launch remediation work. |
| token-pacman | 1.0.2 | Visualizes live session AI-credit usage as a Pac-Man board with pellets, ghosts, fruit milestones, and game-over limits. |
| typescript-mcp-development | 1.0.0 | Complete toolkit for building Model Context Protocol (MCP) servers in TypeScript/Node.js using the official SDK. Includes instructions for best practices, a prompt for generating… |
| typespec-m365-copilot | 1.0.0 | Comprehensive collection of prompts, instructions, and resources for building declarative agents and API plugins using TypeSpec for Microsoft 365 Copilot extensibility. |
| uizze | 1.0.0 | Stop generic UI from shipping. Ground GitHub Copilot in 800,000+ real web and iOS screens, write a product-specific design contract, and enforce a hard finish gate. |
| visual-pr | 1.0.0 | Capture, annotate, and embed screenshots and animated GIF demos in pull request descriptions. Includes Playwright-based UI capture, PIL image annotations, PR embedding workflows f… |
| where-was-i | 1.0.2 | Reconstruct your dev context (branch, commits, uncommitted work, PR clues) and trigger a resume prompt to continue quickly. |
| windows-app-storage-inspector-cleanup | 1.0.3 | Inspect Windows application storage, understand local disk usage, and safely move approved cleanup items to the Recycle Bin. |
| work-hub | 1.0.2 | Generic cross-repo command center canvas for GitHub Copilot with onboarding, focus planning, repo health, work signals, and session cleanup. |

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
