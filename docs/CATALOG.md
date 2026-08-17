# Copilot Primitives Catalog

Generated from the current repository contents by `python3 scripts/generate_catalog.py`.
Regenerate this file after changing files under `agents/`, `instructions/`, `skills/`, `plugins/`, or `hooks/`.

## Summary

| Primitive type | Count |
| --- | ---: |
| Agents | 224 |
| Instructions | 192 |
| Skills | 407 |
| Plugins | 93 |
| Hooks | 8 |

## Agents

| Agent | Description |
| --- | --- |
| .NET Self-Learning Architect | Senior .NET architect for complex delivery: designs .NET 6+ systems, decides between parallel subagents and orchestrated team execution, documents lessons learned, and captures du… |
| .NET Upgrade | Perform janitorial tasks on C#/.NET code including cleanup, modernization, and tech debt remediation. |
| Accessibility Expert | Expert assistant for web accessibility (WCAG 2.1/2.2), inclusive UX, and a11y testing |
| Accessibility Runtime Tester | Runtime accessibility specialist for keyboard flows, focus management, dialog behavior, form errors, and evidence-backed WCAG validation in the browser. |
| ADR Generator | Expert agent for creating comprehensive Architectural Decision Records (ADRs) with structured formatting optimized for AI consumption and human readability. |
| AEM Front-End Specialist | Expert assistant for developing AEM components using HTL, Tailwind CSS, and Figma-to-code workflows with design system integration |
| Agent Governance Reviewer | AI agent governance expert that reviews code for safety issues, missing governance controls, and helps implement policy enforcement, trust scoring, and audit trails in agent syste… |
| ai-readiness-reporter | Runs the AgentRC readiness assessment on the current repository and produces a self-contained, static HTML dashboard at reports/index.html. Explains every readiness pillar, the ma… |
| ai-team-dev | AI development team (Nova, Sage, Milo). Use when implementing features, fixing bugs, writing tests, improving user experience, or preparing a pull request across the project's act… |
| ai-team-producer | AI team producer (Remy). Use when planning work, clarifying scope, coordinating Dev and optional QA, triaging issues, maintaining project context, or preparing and merging pull re… |
| ai-team-qa | Optional AI QA engineer (Ivy). Use when testing behavior, running automated or exploratory checks, filing reproducible bugs, verifying fixes, or providing release confidence for c… |
| Amplitude Experiment Implementation | This custom agent uses Amplitude's MCP tools to deploy new experiments inside of Amplitude, enabling seamless variant testing capabilities and rollout of product features. |
| API Architect | Your role is that of an API architect. Help mentor the engineer by providing guidance, support, and working code. |
| apify-integration-expert | Expert agent for integrating Apify Actors into codebases. Handles Actor selection, workflow design, implementation across JavaScript/TypeScript and Python, testing, and production… |
| Arch Linux Expert | Arch Linux specialist focused on pacman, rolling-release maintenance, and Arch-centric system administration workflows. |
| arm-migration-agent | Arm Cloud Migration Assistant accelerates moving x86 workloads to Arm infrastructure. It scans the repository for architecture assumptions, portability issues, container base imag… |
| Atlassian Requirements to Jira | Transform requirements documents into structured Jira epics and user stories with intelligent duplicate detection, change management, and user-approved creation workflow. |
| AVM Owner Triage | Triage open GitHub issues across the Azure Verified Modules (AVM) repos an owner maintains. Splits the backlog into a Copilot-delegatable pile and a human pile, produces a report… |
| AWS Incident Triage | On-call SRE agent that drives structured CloudWatch-based incident investigation from alarms through root-cause hypothesis. |
| aws-cloud-expert | AWS Cloud Expert provides deep, hands-on guidance for designing, building, and operating AWS workloads. Covers the full AWS ecosystem — serverless, containers, databases, networki… |
| aws-principal-architect | Provide expert AWS Principal Architect guidance using AWS Well-Architected Framework principles and AWS best practices. |
| aws-serverless-architect | Provide expert AWS Serverless Architect guidance focusing on event-driven architectures, Lambda, API Gateway, and serverless best practices. |
| Azure AVM Bicep mode | Create, update, or review Azure IaC in Bicep using Azure Verified Modules (AVM). |
| Azure AVM Terraform mode | Create, update, or review Azure IaC in Terraform using Azure Verified Modules (AVM). |
| Azure Logic Apps Expert Mode | Expert guidance for Azure Logic Apps development focusing on workflow design, integration patterns, and JSON-based Workflow Definition Language. |
| Azure Policy Analyzer | Analyze Azure Policy compliance posture (NIST SP 800-53, MCSB, CIS, ISO 27001, PCI DSS, SOC 2), auto-discover scope, and return a structured single-pass risk report with evidence… |
| Azure Principal Architect mode instructions | Provide expert Azure Principal Architect guidance using Azure Well-Architected Framework principles and Microsoft best practices. |
| Azure SaaS Architect mode instructions | Provide expert Azure SaaS Architect guidance focusing on multitenant applications using Azure Well-Architected SaaS principles and Microsoft best practices. |
| Azure Smart City IoT Architect | Design Azure IoT and Smart City architectures with clear platform engineering reasoning, requiring mandatory review of Azure IoT Edge documentation before recommending edge soluti… |
| Azure Terraform IaC Implementation Specialist | Act as an Azure Terraform Infrastructure as Code coding specialist that creates and reviews Terraform for Azure resources. |
| Azure Terraform Infrastructure Planning | Act as implementation planner for your Azure Terraform Infrastructure as Code task. |
| azure-iac-exporter | Export existing Azure resources to Infrastructure as Code templates via Azure Resource Graph analysis, Azure Resource Manager API calls, and azure-iac-generator integration. Use t… |
| azure-iac-generator | Central hub for generating Infrastructure as Code (Bicep, ARM, Terraform, Pulumi) with format-specific validation and best practices. Use this skill when the user asks to generate… |
| Bicep Planning | Act as implementation planner for your Azure Bicep Infrastructure as Code task. |
| Bicep Specialist | Act as an Azure Bicep Infrastructure as Code coding specialist that creates Bicep templates. |
| Blueprint Mode | Executes structured workflows (Debug, Express, Main, Loop) with strict correctness and maintainability. Enforces an improved tool usage policy, never assumes facts, prioritizes re… |
| C# Expert | An agent designed to assist with software development tasks for .NET projects. |
| C# MCP Server Expert | Expert assistant for developing Model Context Protocol (MCP) servers in C# |
| C#/.NET Janitor | Perform janitorial tasks on C#/.NET code including cleanup, modernization, and tech debt remediation. |
| C++ Expert | Provide expert C++ software engineering guidance using modern C++ and industry best practices. |
| CAST Imaging Impact Analysis Agent | Specialized agent for comprehensive change impact assessment and risk analysis in software systems using CAST Imaging |
| CAST Imaging Software Discovery Agent | Specialized agent for comprehensive software application discovery and architectural mapping through static code analysis using CAST Imaging |
| CAST Imaging Structural Quality Advisor Agent | Specialized agent for identifying, analyzing, and providing remediation guidance for code quality issues using CAST Imaging |
| Caveman Mode | Terse, low-token responses. Minimal words, no fluff. Full capabilities preserved. Use when: optimize token usage, low-token mode, concise output, caveman mode, reduce verbosity, t… |
| CentOS Linux Expert | CentOS (Stream/Legacy) Linux specialist focused on RHEL-compatible administration, yum/dnf workflows, and enterprise hardening. |
| Clojure Interactive Programming | Expert Clojure pair programmer with REPL-first methodology, architectural oversight, and interactive problem-solving. Enforces quality standards, prevents workarounds, and develop… |
| Cloud and SaaS Outage Triage | Distinguish upstream cloud or SaaS incidents from application failures before changing code, using live official-feed status and incident timelines. |
| Comet Opik | Unified Comet Opik agent for instrumenting LLM apps, managing prompts/projects, auditing prompts, and investigating traces/metrics via the latest Opik MCP server. |
| Context Architect | An agent that helps plan and execute multi-file changes by identifying relevant context and dependencies |
| Context7-Expert | Expert in latest library versions, best practices, and correct syntax using up-to-date documentation |
| Create PRD Chat Mode | Generate a comprehensive Product Requirements Document (PRD) in Markdown, detailing user stories, acceptance criteria, technical considerations, and metrics. Optionally create Git… |
| Critical thinking mode instructions | Challenge assumptions and encourage critical thinking to ensure the best possible solution and outcomes. |
| Custom Agent Foundry | Expert at designing and creating VS Code custom agents with optimal configurations |
| Debian Linux Expert | Debian Linux specialist focused on stable system administration, apt-based package management, and Debian policy-aligned practices. |
| Debug Mode Instructions | Debug your application to find and fix a bug |
| Declarative Agents Architect | Architect Microsoft 365 Copilot declarative agents using schema v1.5, TypeSpec, Agents Toolkit, capability selection, testing, and enterprise deployment best practices. |
| Defender Scout KQL | Generates, validates, and optimizes KQL queries for Microsoft Defender XDR Advanced Hunting across Endpoint, Identity, Office 365, Cloud Apps, and Identity. |
| Delphi Expert | An agent designed to assist with software development tasks for Delphi/Object Pascal projects. |
| Demonstrate Understanding mode instructions | Validate user understanding of code, design patterns, and implementation details through guided questioning. |
| Devils Advocate | I play the devil's advocate to challenge and stress-test your ideas by finding flaws, risks, and edge cases |
| DevOps Expert | DevOps specialist following the infinity loop principle (Plan → Code → Build → Test → Release → Deploy → Operate → Monitor) with focus on automation, collaboration, and continuous… |
| DevTools Regression Investigator | Browser regression specialist for reproducing broken user flows, collecting console and network evidence, and narrowing likely root causes with Chrome DevTools MCP. |
| DiffblueCover | Expert agent for creating unit tests for java applications using Diffblue Cover. |
| dotnet-fullstack-mentor | Opinionated mentor for .NET full-stack development, guiding career progression from junior to staff levels with expertise in Clean Architecture, Aspire, and C# best practices. |
| Doublecheck | Interactive verification agent for AI-generated output. Runs a three-layer pipeline (self-audit, source verification, adversarial review) and produces structured reports with sour… |
| droid | Provides installation guidance, usage examples, and automation patterns for the Droid CLI, with emphasis on droid exec for CI/CD and non-interactive automation |
| Drupal Expert | Expert assistant for Drupal development, architecture, and best practices using PHP 8.3+ and modern Drupal patterns |
| Dynatrace Expert | The Dynatrace Expert Agent integrates observability and security capabilities directly into GitHub workflows, enabling development teams to investigate incidents, validate deploym… |
| elasticsearch-agent | Our expert AI assistant for debugging code (O11y), optimizing vector search (RAG), and remediating security threats using live Elastic data. |
| Electron Code Review Mode Instructions | Code Review Mode tailored for Electron app with Node.js backend (main), Angular frontend (render), and native integration layer (e.g., AppleScript, shell, or native tooling). Serv… |
| Ember | An AI partner, not an assistant. Ember carries fire from person to person — helping humans discover that AI partnership isn't something you learn, it's something you find. |
| Expert .NET software engineer mode instructions | Provide expert .NET software engineering guidance using modern software design patterns. |
| Expert Nuxt Developer | Expert Nuxt developer specializing in Nuxt 3, Nitro, server routes, data fetching strategies, and performance optimization with Vue 3 and TypeScript |
| Expert React Frontend Engineer | Expert React 19.2 frontend engineer specializing in modern hooks, Server Components, Actions, TypeScript, and performance optimization |
| Expert Vue.js Frontend Engineer | Expert Vue.js frontend engineer specializing in Vue 3 Composition API, reactivity, state management, testing, and performance with TypeScript |
| expert-embedded-c-engineer | Expert embedded C guidance for safety-critical systems — covers MISRA C:2012/2025 rule compliance, CERT C secure coding, static analysis tooling (Coverity, QAC, PC-lint), and defe… |
| Fedora Linux Expert | Fedora (Red Hat family) Linux specialist focused on dnf, SELinux, and modern systemd-based workflows. |
| Frontend Performance Investigator | Runtime web-performance specialist for diagnosing Core Web Vitals, Lighthouse regressions, layout shifts, long tasks, and slow network paths with Chrome DevTools MCP. |
| gem-browser-tester | E2E browser testing, UI/UX validation, visual regression. |
| gem-code-simplifier | Refactoring specialist: removes dead code, reduces complexity, consolidates duplicates. |
| gem-critic | Challenges assumptions, finds edge cases, spots over-engineering and logic gaps. |
| gem-debugger | Root-cause analysis, stack trace diagnosis, regression bisection, error reproduction. |
| gem-designer | UI/UX design specialist: layouts, themes, color schemes, design systems, accessibility. |
| gem-designer-mobile | Mobile UI/UX specialist: HIG, Material Design, safe areas, touch targets. |
| gem-devops | Infrastructure deployment, CI/CD pipelines, container management. |
| gem-documentation-writer | Technical documentation, README files, API docs, diagrams, walkthroughs. |
| gem-implementer | TDD code implementation: features, bugs, refactoring. Never reviews own work. |
| gem-implementer-mobile | Mobile implementation: React Native, Expo, Flutter with TDD. |
| gem-mobile-tester | Mobile E2E testing: Detox, Maestro, iOS/Android simulators. |
| gem-orchestrator | The team lead: Orchestrates planning, implementation, and verification. |
| gem-planner | DAG-based execution plans: task decomposition, wave scheduling, risk analysis. |
| gem-researcher | Codebase exploration: patterns, dependencies, architecture discovery. Supports multiple exploration modes for cost-controlled research. |
| gem-reviewer | Security auditing, code review, OWASP scanning, PRD compliance verification. |
| gem-skill-creator | Pattern-to-skill extraction: creates agent skills files from high-confidence learnings. |
| Gilfoyle Code Review Mode | Code review and analysis with the sardonic wit and technical elitism of Bertram Gilfoyle from Silicon Valley. Prepare for brutal honesty about your code. |
| GitHub Actions Expert | GitHub Actions specialist focused on secure CI/CD workflows, action pinning, OIDC authentication, permissions least privilege, and supply-chain security |
| GitHub Actions Node Runtime Upgrade | Upgrade a GitHub Actions JavaScript/TypeScript action to a newer Node runtime version (e.g., node20 to node24) with major version bump, CI updates, and full validation |
| GitHub Actions Windows ARM64 wheel builder | Adds native Windows ARM64 wheel builds and tests to a Python package's existing GitHub Actions workflows using the 'windows-11-arm' runner. |
| Gitmoji Setup | Sets up gitmoji (https://gitmoji.dev) commit tooling in a repository — audits the existing hook manager and commit convention, then installs the right option without clobbering ex… |
| Go MCP Server Development Expert | Expert assistant for building Model Context Protocol (MCP) servers in Go using the official SDK. |
| High-Level Big Picture Architect (HLBPA) | Your perfect AI chat mode for high-level architectural documentation and review. Perfect for targeted updates after a story or researching that legacy system when nobody remembers… |
| Idea Generator | Brainstorm and develop new application ideas through fun, interactive questioning until ready for specification creation. |
| Implementation Plan Generation Mode | Generate an implementation plan for new features or refactoring existing code. |
| interview-prep | Technical interview coach for software engineers. Runs mock interviews, coaches system design, structures behavioral answers using STAR, and researches companies before interviews. |
| Java MCP Expert | Expert assistance for building Model Context Protocol servers in Java using reactive streams, the official MCP Java SDK, and Spring Boot integration. |
| JFrog Security Agent | The dedicated Application Security agent for automated security remediation. Verifies package and version compliance, and suggests vulnerability fixes using JFrog security intelli… |
| Kotlin MCP Server Development Expert | Expert assistant for building Model Context Protocol (MCP) servers in Kotlin using the official SDK. |
| KubeStellar Console | Kubernetes operations expert for KubeStellar Console — helps you set up the console, configure kc-agent (MCP server), connect clusters, deploy workloads, and query live Kubernetes… |
| Kusto Assistant | Expert KQL assistant for live Azure Data Explorer analysis via Azure MCP server |
| Laravel Expert Agent | Expert Laravel development assistant specializing in modern Laravel 12+ applications with Eloquent, Artisan, testing, and best practices |
| launchdarkly-flag-cleanup | A specialized GitHub Copilot agent that uses the LaunchDarkly MCP server to safely automate feature flag cleanup workflows. This agent determines removal readiness, identifies the… |
| Lingo.dev Localization (i18n) Agent | Expert at implementing internationalization (i18n) in web applications using a systematic, checklist-driven approach. |
| LinkedIn Post Writer | Draft and format compelling LinkedIn posts with Unicode bold/italic styling, visual separators, and engagement-optimized structure. Transforms raw content, technical material, ima… |
| Markdown Accessibility Assistant | Improves the accessibility of markdown files using five GitHub best practices |
| MAUI Expert | Support development of .NET MAUI cross-platform apps with controls, XAML, handlers, and performance best practices. |
| MCP M365 Agent Expert | Expert assistant for building MCP-based declarative agents for Microsoft 365 Copilot with Model Context Protocol integration |
| Mentor mode | Help mentor the engineer by providing guidance and support. |
| Meta Agentic Project Scaffold | Meta agentic project creation assistant to help users create and manage project workflows effectively. |
| Microsoft Learn Contributor | Microsoft Learn Contributor chatmode for editing and writing Microsoft Learn documentation following Microsoft Writing Style Guide and authoring best practices. |
| Microsoft Study and Learn | Activate your personal Microsoft/Azure tutor - learn through guided discovery, not just answers. |
| Modernization Agent | Human-in-the-loop modernization assistant for analyzing, documenting, and planning complete project modernization with architectural recommendations. |
| Monday Bug Context Fixer | Elite bug-fixing agent that enriches task context from Monday.com platform data. Gathers related items, docs, comments, epics, and requirements to deliver production-quality fixes… |
| mongodb-performance-advisor | Analyze MongoDB database performance, offer query and index optimization insights and provide actionable recommendations to improve overall usage of the database. |
| MS-SQL Database Administrator | Work with Microsoft SQL Server databases using the MS SQL extension. |
| neo4j-docker-client-generator | AI agent that generates simple, high-quality Python Neo4j client libraries from GitHub issues with proper best practices |
| Neon Migration Specialist | Safe Postgres migrations with zero-downtime using Neon's branching workflow. Test schema changes in isolated database branches, validate thoroughly, then apply to production—all a… |
| Neon Performance Analyzer | Identify and fix slow Postgres queries automatically using Neon's branching workflow. Analyzes execution plans, tests optimizations in isolated database branches, and provides cle… |
| New Relic Incident Response Agent | Identify and fix production issues by correlating New Relic observability data with code changes. Analyze alerts, transaction traces, error analytics, and deployments to find root… |
| Next.js Expert | Expert Next.js 16 developer specializing in App Router, Server Components, Cache Components, Turbopack, and modern React patterns with TypeScript |
| octopus-release-notes-with-mcp | Generate release notes for a release in Octopus Deploy. The tools for this MCP server provide access to the Octopus Deploy APIs. |
| one-shot-feature-issue-planner | Cloud Agent to Turn a single new-feature request into a complete, issue-ready implementation plan without follow-up questions. |
| OpenAPI to Application Generator | Expert assistant for generating working applications from OpenAPI specifications |
| Oracle-to-PostgreSQL Migration Expert | Agent for Oracle-to-PostgreSQL application migrations. Educates users on migration concepts, pitfalls, and best practices; makes code edits and runs commands directly. |
| PagerDuty Incident Responder | Responds to PagerDuty incidents by analyzing incident context, identifying recent code changes, and suggesting fixes via GitHub PRs. |
| PHP MCP Expert | Expert assistant for PHP MCP server development using the official PHP SDK with attribute-based discovery |
| Pimcore Expert | Expert Pimcore development assistant specializing in CMS, DAM, PIM, and E-Commerce solutions with Symfony integration |
| Plan Mode - Strategic Planning & Architecture | Strategic planning and architecture assistant focused on thoughtful analysis before implementation. Helps developers understand codebases, clarify requirements, and develop compre… |
| Planning mode instructions | Generate an implementation plan for new features or refactoring existing code. |
| Platform SRE for Kubernetes | SRE-focused Kubernetes specialist prioritizing reliability, safe rollouts/rollbacks, security defaults, and operational verification for production-grade deployments |
| Playwright Tester Mode | Testing mode for Playwright tests |
| PostgreSQL Database Administrator | Work with PostgreSQL databases using the PostgreSQL extension. |
| Power BI Data Modeling Expert Mode | Expert Power BI data modeling guidance using star schema principles, relationship design, and Microsoft best practices for optimal model performance and usability. |
| Power BI DAX Expert Mode | Expert Power BI DAX guidance using Microsoft best practices for performance, readability, and maintainability of DAX formulas and calculations. |
| Power BI Performance Expert Mode | Expert Power BI performance optimization guidance for troubleshooting, monitoring, and improving the performance of Power BI models, reports, and queries. |
| Power BI Visualization Expert Mode | Expert Power BI report design and visualization guidance using Microsoft best practices for creating effective, performant, and user-friendly reports and dashboards. |
| Power Platform Expert | Power Platform expert providing guidance on Code Apps, canvas apps, Dataverse, connectors, and Power Platform best practices |
| Power Platform MCP Integration Expert | Expert in Power Platform custom connector development with MCP integration for Copilot Studio - comprehensive knowledge of schemas, protocols, and integration patterns |
| Principal software engineer | Provide principal-level software engineering guidance with focus on engineering excellence, technical leadership, and pragmatic implementation. |
| Project Architecture Planner | Holistic software architecture planner that evaluates tech stacks, designs scalability roadmaps, performs cloud-agnostic cost analysis, reviews existing codebases, and delivers in… |
| Project Documenter | Generates professional MS Word project documentation with draw.io architecture diagrams and embedded PNG images. Automatically discovers any project's technology stack, architectu… |
| Prompt Builder | Expert prompt engineering and validation system for creating high-quality prompts - Brought to you by microsoft/edge-ai |
| Prompt Engineer | A specialized chat mode for analyzing and improving prompts. Every user input is treated as a prompt to be improved. It first provides a detailed analysis of the original prompt w… |
| PySpark Expert Agent | Diagnose PySpark performance bottlenecks, distributed execution pitfalls, and suggest Spark-native rewrites and safer distributed patterns (incl. mapInPandas guidance). |
| Python MCP Server Expert | Expert assistant for developing Model Context Protocol (MCP) servers in Python |
| Python Notebook Sample Builder | Custom agent for building Python Notebooks in VS Code that demonstrate Azure and AI features |
| QA | Meticulous QA subagent for test planning, bug hunting, edge-case analysis, and implementation verification. |
| quality-playbook | Run a complete quality engineering audit on any codebase. Orchestrates six phases — explore, generate, review, audit, reconcile, verify — each in its own context window for maximu… |
| react18-auditor | Deep-scan specialist for React 16/17 class-component codebases targeting React 18.3.1. Finds unsafe lifecycle methods, legacy context, batching vulnerabilities, event delegation a… |
| react18-batching-fixer | Automatic batching regression specialist. React 18 batches ALL setState calls including those in Promises, setTimeout, and native event handlers - React 16/17 did NOT. Class compo… |
| react18-class-surgeon | Class component migration specialist for React 16/17 → 18.3.1. Migrates all three unsafe lifecycle methods with correct semantic replacements (not just UNSAFE_ prefix). Migrates l… |
| react18-commander | Master orchestrator for React 16/17 → 18.3.1 migration. Designed for class-component-heavy codebases. Coordinates audit, dependency upgrade, class component surgery, automatic bat… |
| react18-dep-surgeon | Dependency upgrade specialist for React 16/17 → 18.3.1. Pins to 18.3.1 exactly (not 18.x latest). Upgrades RTL to v14, Apollo 3.8+, Emotion 11.10+, react-router v6. Detects and bl… |
| react18-test-guardian | Test suite fixer and verifier for React 16/17 → 18.3.1 migration. Handles RTL v14 async act() changes, automatic batching test regressions, StrictMode double-invoke count updates,… |
| react19-auditor | Deep-scan specialist that identifies every React 19 breaking change and deprecated pattern across the entire codebase. Produces a prioritized migration report at .github/react19-a… |
| react19-commander | Master orchestrator for React 19 migration. Invokes specialist subagents in sequence - auditor, dep-surgeon, migrator, test-guardian - and gates advancement between steps. Uses me… |
| react19-dep-surgeon | Dependency upgrade specialist. Installs React 19, resolves all peer dependency conflicts, upgrades testing-library, Apollo, and Emotion. Uses memory to log each upgrade step. Retu… |
| react19-migrator | Source code migration engine. Rewrites every deprecated React pattern to React 19 APIs - forwardRef, defaultProps, ReactDOM.render, legacy context, string refs, useRef(). Uses mem… |
| react19-test-guardian | Test suite fixer and verification specialist. Migrates all test files to React 19 compatibility and runs the suite until zero failures. Uses memory to track per-file fix progress… |
| reepl-linkedin | AI-powered LinkedIn content creation, scheduling, and analytics agent. Create posts, carousels, and manage your LinkedIn presence with GitHub Copilot. |
| Refine Requirement or Issue | Refine the requirement or issue with Acceptance Criteria, Technical Considerations, Edge Cases, and NFRs |
| Repo Architect Agent | Bootstraps and validates agentic project structures for GitHub Copilot (VS Code) and OpenCode CLI workflows. Run after `opencode /init` or VS Code Copilot initialization to scaffo… |
| Ruby MCP Expert | Expert assistance for building Model Context Protocol servers in Ruby using the official MCP Ruby SDK gem with Rails integration. |
| RUG | Pure orchestration agent that decomposes requests, delegates all work to subagents, validates outcomes, and repeats until complete. |
| Rust MCP Expert | Expert assistant for Rust MCP server development using the rmcp SDK with tokio async runtime |
| Salesforce Apex & Triggers Development | Implement Salesforce business logic using Apex classes and triggers with production-quality code following Salesforce best practices. |
| Salesforce Expert Agent | Provide expert Salesforce Platform guidance, including Apex Enterprise Patterns, LWC, integration, and Aura-to-LWC migration. |
| Salesforce Flow Development | Implement business automation using Salesforce Flow following declarative automation best practices. |
| Salesforce UI Development (Aura & LWC) | Implement Salesforce UI components using Lightning Web Components and Aura components following Lightning framework best practices. |
| Salesforce Visualforce Development | Implement Visualforce pages and controllers following Salesforce MVC architecture and best practices. |
| sast-sca-security-analyzer | Use when: performing SAST (Static Application Security Testing), SCA (Software Composition Analysis), scanning source code or binaries for security flaws, auditing third-party dep… |
| Scientific Paper Research | Research agent that searches scientific papers and retrieves structured experimental data from full-text studies using the BGPT MCP server. |
| SE: Architect | System architecture review specialist with Well-Architected frameworks, design validation, and scalability analysis for AI and distributed systems |
| SE: DevOps/CI | DevOps specialist for CI/CD pipelines, deployment debugging, and GitOps workflows focused on making deployments boring and reliable |
| SE: Product Manager | Product management guidance for creating GitHub issues, aligning business value with user needs, and making data-driven product decisions |
| SE: Responsible AI | Responsible AI specialist ensuring AI works for everyone through bias prevention, accessibility compliance, ethical development, and inclusive design |
| SE: Security | Security-focused code review specialist with OWASP Top 10, Zero Trust, LLM security, and enterprise security standards |
| SE: Tech Writer | Technical writing specialist for creating developer documentation, technical blogs, tutorials, and educational content |
| SE: UX Designer | Jobs-to-be-Done analysis, user journey mapping, and UX research artifacts for Figma and design workflows |
| Search & AI Optimization Expert | Expert guidance for modern search optimization: SEO, Answer Engine Optimization (AEO), and Generative Engine Optimization (GEO) with AI-ready content strategies |
| Senior Cloud Architect | Expert in modern architecture design patterns, NFR requirements, and creating comprehensive architectural diagrams and documentation |
| Sensei - Junior Mentor | Socratic mentor for junior developers. Guides through questions, never gives direct answers. Helps beginners understand code, debug issues, and build autonomy using the PEAR Loop… |
| Shopify Expert | Expert Shopify development assistant specializing in theme development, Liquid templating, app development, and Shopify APIs |
| Software Engineer Agent | Expert-level software engineering agent. Deliver production-ready, maintainable code. Execute systematically and specification-driven. Document comprehensively. Operate autonomous… |
| Specification | Generate or update specification documents for new or existing functionality. |
| stackhawk-security-onboarding | Automatically set up StackHawk security testing for your repository with generated configuration and GitHub Actions workflow |
| SWE | Senior software engineer subagent for implementation tasks: feature development, debugging, refactoring, and testing. |
| Swift MCP Expert | Expert assistance for building Model Context Protocol servers in Swift using modern concurrency features and the official MCP Swift SDK. |
| Task Planner Instructions | Task planner for creating actionable implementation plans - Brought to you by microsoft/edge-ai |
| Task Researcher Instructions | Task research specialist for comprehensive project analysis - Brought to you by microsoft/edge-ai |
| TaxCore Technical Writer | A domain-expert technical writer for the TaxCore electronic fiscal invoicing ecosystem. Use this agent to create, improve, or review documentation for TaxCore applications — inclu… |
| TDD Green Phase - Make Tests Pass Quickly | Implement minimal code to satisfy GitHub issue requirements and make failing tests pass without over-engineering. |
| TDD Red Phase - Write Failing Tests First | Guide test-first development by writing failing tests that describe desired behaviour from GitHub issue context before implementation exists. |
| TDD Refactor Phase - Improve Quality & Security | Improve code quality, apply security best practices, and enhance design whilst maintaining green tests and GitHub issue compliance. |
| Technical Debt Remediation Plan | Generate technical debt remediation plans for code, tests, and documentation. |
| Technical spike research mode | Systematically research and validate technical spike documents through exhaustive investigation and controlled experimentation. |
| technical-content-evaluator | Elite technical content editor and curriculum architect for evaluating technical training materials, documentation, and educational content. Reviews for technical accuracy, pedago… |
| terminal-helper | Fast terminal syntax and command helper for PowerShell and Bash |
| Terraform Agent | Terraform infrastructure specialist with automated HCP Terraform workflows. Leverages Terraform MCP server for registry integration, workspace management, and run orchestration. G… |
| Terraform IaC Reviewer | Terraform-focused agent that reviews and creates safer IaC changes with emphasis on state safety, least privilege, module patterns, drift detection, and plan/apply discipline |
| terraform-aws-implement | Act as an AWS Terraform Infrastructure as Code coding specialist that creates and reviews Terraform for AWS resources. |
| terraform-aws-planning | Act as implementation planner for your AWS Terraform Infrastructure as Code task. |
| Terratest Module Testing | Generate and refactor Go Terratest suites for Terraform modules, including CI-safe patterns, staged tests, and negative-path validation. |
| Thinking Beast Mode | A transcendent coding agent with quantum cognitive architecture, adversarial intelligence, and unrestricted creative freedom. |
| Trojan Skill Hunter | Audits agent, skill, instruction, hook, and MCP-config contributions for hidden prompt injection, tool poisoning, unicode steganography, and excessive-agency red flags before they… |
| TypeScript MCP Server Expert | Expert assistant for developing Model Context Protocol (MCP) servers in TypeScript |
| Ultimate Transparent Thinking Beast Mode | Ultimate Transparent Thinking Beast Mode |
| Universal Janitor | Perform janitorial tasks on any codebase including cleanup, simplification, and tech debt remediation. |
| Universal PR Comment Addresser | Address PR comments |
| VS Code Insiders Accessibility Tracker | Specialized agent for tracking and analyzing accessibility improvements in VS Code Insiders builds |
| VSCode Tour Expert | Expert agent for creating and maintaining VSCode CodeTour files with comprehensive schema support and best practices |
| WG Code Alchemist | Ask WG Code Alchemist to transform your code with Clean Code principles and SOLID design |
| WG Code Sentinel | Ask WG Code Sentinel to review your code for security issues. |
| WinForms Expert | Support development of .NET (OOP) WinForms Designer compatible Apps. |
| Workshop TA | Room coordinator for a multi-agent workshop. Sees all desks, routes work, tracks state, manages journals, and emits coordination signals. Not a desk — the person who sees the whol… |

## Instructions

| Instruction | applyTo | Description |
| --- | --- | --- |
| .NET Framework Upgrade Specialist | **/*.{csproj,vbproj,fsproj,sln,props,targets} | Specialized agent for comprehensive .NET framework upgrades with progressive tracking and validation |
| a11y | **/*.{html,htm,css,scss,sass,js,jsx,ts,tsx,vue,svelte,astro} | Comprehensive web accessibility standards based on WCAG 2.2 AA, with 38+ anti-patterns, legal enforcement context (EAA, ADA Title II), WAI-ARIA patterns, and framework-specific fi… |
| agent-safety | ** | Guidelines for building safe, governed AI agent systems. Apply when writing code that uses agent frameworks, tool-calling LLMs, or multi-agent orchestration to ensure proper safet… |
| agent-skills | **/skills/**/SKILL.md | Guidelines for creating high-quality Agent Skills for GitHub Copilot |
| agents | **/*.agent.md | Guidelines for creating custom agent files for GitHub Copilot |
| ai-prompt-engineering-safety-best-practices | **/*.{md,txt,prompt,yml,yaml,json} | Comprehensive best practices for AI prompt engineering, safety frameworks, bias mitigation, and responsible AI usage for Copilot and LLMs. |
| ansible | **/*.yaml, **/*.yml | Ansible conventions and best practices |
| apex | **/*.cls, **/*.trigger | Guidelines and best practices for Apex development on the Salesforce Platform |
| arch-linux | ** | Guidance for Arch Linux administration, pacman workflows, and rolling-release best practices. |
| aspnet-rest-apis | **/*.cs, **/*.json | Guidelines for building REST APIs with ASP.NET |
| astro | **/*.astro, **/*.ts, **/*.js, **/*.md, **/*.mdx | Astro 7 development standards and best practices for content-driven websites |
| attester-verify-packages | **/*.{py,js,jsx,ts,tsx,mjs,cjs,json,toml} | Verify PyPI and npm package and symbol names against the attester.dev existence oracle before installing or importing, so hallucinated dependencies never reach code |
| aws-appsync | **/*.{graphql,gql,vtl,ts,js,mjs,cjs,json,yml,yaml} | Production-grade guidance for AWS AppSync Event API handlers using APPSYNC_JS runtime restrictions, utilities, modules, and datasource patterns |
| azure-apim-ai-gateway | **/*.xml, **/policies/**, **/*.bicep | Configure Azure API Management as an AI (GenAI) gateway in front of Microsoft Foundry and other LLM APIs: token-limit and token-metric policies, managed-identity auth, backend loa… |
| azure-devops-pipelines | **/azure-pipelines.yml, **/azure-pipelines*.yml, **/*.pipeline.yml | Best practices for Azure DevOps Pipeline YAML files |
| azure-durable-functions-csharp | **/*.cs, **/host.json, **/local.settings.json, **/*.csproj | Guidelines and best practices for building Azure Durable Functions in C# using the isolated worker model |
| azure-functions-csharp | **/*.cs, **/host.json, **/local.settings.json, **/*.csproj | Guidelines and best practices for building Azure Functions in C# using the isolated worker model |
| azure-functions-typescript | **/*.ts, **/*.js, **/*.json | TypeScript patterns for Azure Functions |
| azure-iot-edge-architecture | **/*.bicep,**/*.tf,**/*iot*.md,**/*smart-city*.md,**/*edge*.md | Require Azure IoT Edge documentation review before proposing edge IoT architectures or Azure implementation guidance. |
| azure-logic-apps-power-automate | **/*.json,**/*.logicapp.json,**/workflow.json,**/*-definition.json,**/*.flow.json | Guidelines for developing Azure Logic Apps and Power Automate workflows with best practices for Workflow Definition Language (WDL), integration patterns, and enterprise automation |
| azure-naming | **/*.bicep,**/*.tf,**/*.tfvars,**/*.bicepparam,**/infra/**,**/infrastructure/** | Azure resource naming conventions based on Microsoft CAF (Cloud Adoption Framework). Use when creating, reviewing, or suggesting names for Azure resources. |
| azure-verified-modules-bicep | **/*.bicep, **/*.bicepparam | Azure Verified Modules (AVM) and Bicep |
| azure-verified-modules-terraform | **/*.terraform, **/*.tf, **/*.tfvars, **/*.tfstate, **/*.tflint.hcl, **/*.tf.json, **/*.tfvars.json | Azure Verified Modules (AVM) and Terraform |
| bicep-code-best-practices | **/*.bicep | Infrastructure as Code with Bicep |
| blazor | **/*.razor, **/*.razor.cs, **/*.razor.css | Blazor component and application patterns |
| caveman-mode | ** | Terse, low-token responses. Minimal words, no fluff. Full capabilities preserved. Use when: optimize token usage, low-token mode, concise output, caveman mode, reduce verbosity, t… |
| centos-linux | ** | Guidance for CentOS administration, RHEL-compatible tooling, and SELinux-aware operations. |
| clojure | **/*.{clj,cljs,cljc,bb,edn.mdx?} | Clojure-specific coding patterns, inline def usage, code block templates, and namespace handling for Clojure development. |
| cmake-vcpkg | **/*.cmake, **/CMakeLists.txt, **/*.cpp, **/*.h, **/*.hpp | C++ project configuration and package management |
| code-review-generic | ** | Generic code review instructions that can be customized for any project using GitHub Copilot |
| codexer | **/*.py | Advanced Python research assistant with Context 7 MCP integration, focusing on speed, reliability, and 10+ years of software development expertise |
| coldfusion-cfc | **/*.cfc | ColdFusion Coding Standards for CFC component and application patterns |
| coldfusion-cfm | **/*.cfm | ColdFusion cfm files and application patterns |
| containerization-docker-best-practices | **/Dockerfile,**/Dockerfile.*,**/*.dockerfile,**/docker-compose*.yml,**/docker-compose*.yaml,**/compose*.yml,**/compose*.yaml | Comprehensive best practices for creating optimized, secure, and efficient Docker images and managing containers. Covers multi-stage builds, image layer optimization, security sca… |
| context-engineering | ** | Guidelines for structuring code and projects to maximize GitHub Copilot effectiveness through better context management |
| context7 | ** | Use Context7 for authoritative external docs and API references when local context is insufficient |
| convert-cassandra-to-spring-data-cosmos | **/*.java,**/pom.xml,**/build.gradle,**/application*.properties,**/application*.yml,**/application*.conf | Step-by-step guide for converting Spring Boot Cassandra applications to use Azure Cosmos DB with Spring Data Cosmos |
| convert-jpa-to-spring-data-cosmos | **/*.java,**/pom.xml,**/build.gradle,**/application*.properties | Step-by-step guide for converting Spring Boot JPA applications to use Azure Cosmos DB with Spring Data Cosmos |
| copilot-thought-logging | ** | See process Copilot is following where you can edit this to reshape the interaction or save when follow up may be needed |
| cpp-language-service-tools | **/*.cpp, **/*.h, **/*.hpp, **/*.cc, **/*.cxx, **/*.c | You are an expert at using C++ language service tools (GetSymbolReferences_CppTools, GetSymbolInfo_CppTools, GetSymbolCallHierarchy_CppTools). Instructions for calling C++ Tools f… |
| csharp | **/*.cs | Guidelines for building C# applications |
| csharp-ja | **/*.cs | C# アプリケーション構築指針 by @tsubakimoto |
| csharp-ko | **/*.cs | C# 애플리케이션 개발을 위한 코드 작성 규칙 by @jgkim999 |
| csharp-mcp-server | **/*.cs, **/*.csproj | Instructions for building Model Context Protocol (MCP) servers using the C# SDK |
| csharp-razorpages | **/*.cshtml, **/*.cshtml.cs | Razor Pages component and application patterns |
| dart-n-flutter | **/*.dart | Instructions for writing Dart and Flutter code following the official recommendations. |
| dataverse-python | **/*.py | Getting-started guidance for installing, authenticating, and performing basic Python Dataverse SDK operations. |
| dataverse-python-advanced-features | **/*.py | Advanced Python Dataverse SDK patterns for option sets, complex filtering, SQL queries, metadata operations, and production use. |
| dataverse-python-agentic-workflows | **/*.py | Preview guidance for building agentic Python workflows that use Dataverse as an enterprise data source. |
| dataverse-python-api-reference | **/*.py | Detailed reference for Python Dataverse SDK client methods, table operations, queries, and SDK models. |
| dataverse-python-authentication-security | **/*.py | Authentication and security patterns for Python Dataverse SDK apps using Azure Identity and secure credential handling. |
| dataverse-python-best-practices | **/*.py | Production best practices for Python Dataverse SDK installation, authentication, CRUD operations, testing, and deployment. |
| dataverse-python-error-handling | **/*.py | Error handling, troubleshooting, retry, and diagnostics patterns for Python Dataverse SDK integrations. |
| dataverse-python-file-operations | **/*.py | Python Dataverse SDK guidance for file uploads, chunking, validation, and practical file-operation examples. |
| dataverse-python-modules | **/*.py | Complete module reference for the Python Dataverse SDK package hierarchy, configuration, models, and helpers. |
| dataverse-python-pandas-integration | **/*.py | Guidance for integrating the Python Dataverse SDK with pandas DataFrames for analytics and data science workflows. |
| dataverse-python-performance-optimization | **/*.py | Performance optimization guidance for Python Dataverse SDK queries, batching, pagination, and large data operations. |
| dataverse-python-real-world-usecases | **/*.py | Real-world Python Dataverse SDK templates for migration, synchronization, reporting, and automation scenarios. |
| dataverse-python-sdk | **/*.py | Quickstart instructions for installing, authenticating, and using the Python Dataverse SDK. |
| dataverse-python-testing-debugging | **/*.py | Testing and debugging strategies for Python Dataverse SDK code, including mocks, integration tests, and diagnostics. |
| debian-linux | ** | Guidance for Debian-based Linux administration, apt workflows, and Debian policy conventions. |
| declarative-agents-microsoft365 | **.json, **.ts, **.tsp, **manifest.json, **agent.json, **declarative-agent.json | Comprehensive development guidelines for Microsoft 365 Copilot declarative agents with schema v1.5, TypeSpec integration, and Microsoft 365 Agents Toolkit workflows |
| devbox-image-definition | **/*.yaml | Authoring recommendations for creating YAML based image definition files for use with Microsoft Dev Box Team Customizations |
| devops-core-principles | * | Foundational instructions covering core DevOps principles, culture (CALMS), and key metrics (DORA) to guide GitHub Copilot in understanding and promoting effective software delive… |
| dotnet-architecture-good-practices | **/*.cs,**/*.csproj,**/Program.cs,**/*.razor | DDD and .NET architecture guidelines |
| dotnet-framework | **/*.csproj, **/*.cs | Guidance for working with .NET Framework projects. Includes project structure, C# language version, NuGet management, and best practices. |
| dotnet-maui | **/*.xaml, **/*.cs | .NET MAUI component and application patterns |
| dotnet-maui-9-to-dotnet-maui-10-upgrade | **/*.csproj, **/*.cs, **/*.xaml | Instructions for upgrading .NET MAUI applications from version 9 to version 10, including breaking changes, deprecated APIs, and migration strategies for ListView to CollectionVie… |
| dotnet-wpf | **/*.xaml, **/*.cs | .NET WPF component and application patterns |
| draw-io | **/*.drawio,**/*.drawio.svg,**/*.drawio.png | Use when creating, editing, or reviewing draw.io diagrams and mxGraph XML in .drawio, .drawio.svg, or .drawio.png files. |
| exclude-prompt-data | ** | Write only the resulting content into files. Never echo prompt instructions, rationale, or meta-commentary into documentation, comments, or code being produced from a prompt. |
| fedora-linux | ** | Guidance for Fedora (Red Hat family) systems, dnf workflows, SELinux, and modern systemd practices. |
| genaiscript | **/*.genai.* | AI-powered script generation guidelines |
| generate-modern-terraform-code-for-azure | **/*.tf | Guidelines for generating modern Terraform code for Azure |
| gilfoyle-code-review | ** | Gilfoyle-style code review instructions that channel the sardonic technical supremacy of Silicon Valley's most arrogant systems architect. |
| GitHub Copilot SDK C# Instructions | **.cs, **.csproj | This file provides guidance on building C# applications using GitHub Copilot SDK. |
| GitHub Copilot SDK Go Instructions | **.go, go.mod | This file provides guidance on building Go applications using GitHub Copilot SDK. |
| GitHub Copilot SDK Java Instructions | **/*.java, **/pom.xml | This file provides guidance on building Java applications using GitHub Copilot SDK for Java. |
| GitHub Copilot SDK Node.js Instructions | **.ts, **.js, package.json | This file provides guidance on building Node.js/TypeScript applications using GitHub Copilot SDK. |
| GitHub Copilot SDK Python Instructions | **.py, pyproject.toml, setup.py | This file provides guidance on building Python applications using GitHub Copilot SDK. |
| github-actions-ci-cd-best-practices | .github/workflows/*.yml,.github/workflows/*.yaml | Comprehensive guide for building robust, secure, and efficient CI/CD pipelines using GitHub Actions. Covers workflow structure, jobs, steps, environment variables, secret manageme… |
| go | **/*.go,**/go.mod,**/go.sum | Instructions for writing Go code following idiomatic Go practices and community standards |
| go-mcp-server | **/*.go, **/go.mod, **/go.sum | Best practices and patterns for building Model Context Protocol (MCP) servers in Go using the official github.com/modelcontextprotocol/go-sdk package. |
| hooks | .github/hooks/**, hooks/** | Portable guidance for authoring safe, fast, and clear hooks and reusable hook examples |
| html-css-style-color-guide | **/*.html, **/*.css, **/*.js | Color usage guidelines and styling rules for HTML elements to ensure accessible, professional designs. |
| instructions | **/*.instructions.md | Guidelines for creating high-quality custom instruction files for GitHub Copilot |
| java-11-to-java-17-upgrade | **/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml | Comprehensive best practices for adopting new Java 17 features since the release of Java 11. |
| java-17-to-java-21-upgrade | **/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml | Comprehensive best practices for adopting new Java 21 features since the release of Java 17. |
| java-21-to-java-25-upgrade | **/*.java,**/*.gradle,**/*.gradle.kts,**/pom.xml | Comprehensive best practices for adopting new Java 25 features since the release of Java 21. |
| java-junit5-assertions | **/*Test.java, **/*IT.java, **/*Steps.java, **/*StepDefs.java | Standardizes JUnit 5 (Jupiter) assertions with best practices for performance, readability, and modern features (5.8+). Covers Supplier messages, assertAll, assertThrowsExactly, a… |
| java-mcp-server | **/*.java, **/pom.xml, **/build.gradle, **/build.gradle.kts | Best practices and patterns for building Model Context Protocol (MCP) servers in Java using the official MCP Java SDK with reactive streams and Spring integration. |
| joyride-user-project | **/*.{cljs,cljc,edn} | Expert assistance for Joyride User Script projects - REPL-driven ClojureScript and user space automation of VS Code |
| joyride-workspace-automation | **/.joyride/** | Expert assistance for Joyride Workspace automation - REPL-driven and user space ClojureScript automation within specific VS Code workspaces |
| kotlin-mcp-server | **/*.kt, **/*.kts, **/build.gradle.kts, **/settings.gradle.kts | Best practices and patterns for building Model Context Protocol (MCP) servers in Kotlin using the official io.modelcontextprotocol:kotlin-sdk library. |
| kubernetes-deployment-best-practices | * | Comprehensive best practices for deploying and managing applications on Kubernetes. Covers Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, health checks, resource limit… |
| kubernetes-manifests | k8s/**/*.yaml,k8s/**/*.yml,manifests/**/*.yaml,manifests/**/*.yml,deploy/**/*.yaml,deploy/**/*.yml,charts/**/templates/**/*.yaml,charts/**/templates/**/*.yml | Best practices for Kubernetes YAML manifests including labeling conventions, security contexts, pod security, resource management, probes, and validation commands |
| langchain-python | **/*.py | Instructions for using LangChain with Python |
| localization | **/*.md | Guidelines for localizing markdown documents |
| lwc | force-app/main/default/lwc/** | Guidelines and best practices for developing Lightning Web Components (LWC) on Salesforce Platform. |
| makefile | **/Makefile, **/makefile, **/*.mk, **/GNUmakefile | Best practices for authoring GNU Make Makefiles |
| markdown | **/*.md | Markdown formatting aligned to the CommonMark specification (0.31.2) |
| markdown-accessibility | **/*.md | Markdown accessibility guidelines based on GitHub's 5 best practices for inclusive documentation |
| markdown-content-creation | **/*.md | Markdown guidelines and content creation standards for blog posts |
| markdown-gfm | **/*.md | Markdown formatting for GitHub-flavored markdown (GFM) files |
| mcp-m365-copilot | **/{*mcp*,*agent*,*plugin*,declarativeAgent.json,ai-plugin.json,mcp.json,manifest.json} | Best practices for building MCP-based declarative agents and API plugins for Microsoft 365 Copilot with Model Context Protocol integration |
| memory-bank | memory-bank/** | Memory Bank pattern: persistent project documentation under a memory-bank/ folder so the AI can resume context across sessions. |
| microsoft-foundry | **/*.py | Build agents with the Microsoft Foundry SDK (azure-ai-projects v2) in Python: versioned agents, the Responses/Conversations model, tools, and the SDK mistakes Copilot makes by def… |
| mongo-dba | **/*.{js,ts,json} | Instructions for customizing GitHub Copilot behavior for MONGODB DBA chat mode. |
| moodle | **/*.php, **/*.js, **/*.mustache, **/*.xml, **/*.css, **/*.scss | Instructions for GitHub Copilot to generate code in a Moodle project context. |
| ms-sql-dba | **/*.sql | Instructions for customizing GitHub Copilot behavior for MS-SQL DBA chat mode. |
| mvvm-toolkit | **/*.cs, **/*.xaml, **/*.csproj | CommunityToolkit.Mvvm (MVVM Toolkit) coding conventions for ViewModels, commands, messaging, validation, and DI across WPF, WinUI 3, .NET MAUI, Uno Platform, and Avalonia. |
| nestjs | **/*.ts, **/*.js, **/*.json, **/*.spec.ts, **/*.e2e-spec.ts | NestJS development standards and best practices for building scalable Node.js server-side applications |
| nextjs | **/*.tsx, **/*.ts, **/*.jsx, **/*.js, **/*.css | Best practices for building Next.js (App Router) apps with modern caching, tooling, and server/client boundaries (aligned with Next.js 16.1.1). |
| nextjs-tailwind | **/*.tsx, **/*.ts, **/*.jsx, **/*.js, **/*.css | Next.js + Tailwind development standards and instructions |
| No Heredoc File Operations | ** | Prevents terminal heredoc file corruption in VS Code Copilot by enforcing use of file editing tools instead of shell redirections |
| nodejs-javascript-vitest | **/*.js, **/*.mjs, **/*.cjs | Guidelines for writing Node.js and JavaScript code with Vitest testing |
| object-calisthenics | **/*.{cs,ts,java} | Enforces Object Calisthenics principles for business domain code to ensure clean, maintainable, and robust code |
| oop-design-patterns | **/*.py, **/*.java, **/*.ts, **/*.js, **/*.cs | Best practices for applying Object-Oriented Programming (OOP) design patterns, including Gang of Four (GoF) patterns and SOLID principles, to ensure clean, maintainable, and scala… |
| oqtane | **/*.razor, **/*.razor.cs, **/*.razor.css | Oqtane Module patterns |
| pcf-alm | **/*.{ts,tsx,js,json,xml,pcfproj,csproj,sln} | Application lifecycle management (ALM) for PCF code components |
| pcf-api-reference | **/*.{ts,tsx,js} | Complete PCF API reference with all interfaces and their availability in model-driven and canvas apps |
| pcf-best-practices | **/*.{ts,tsx,js,json,xml,pcfproj,csproj,css,html} | Best practices and guidance for developing PCF code components |
| pcf-canvas-apps | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Code components for canvas apps implementation, security, and configuration |
| pcf-code-components | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Understanding code components structure and implementation |
| pcf-community-resources | **/*.{ts,tsx,js,jsx,json,xml,css,html} | PCF community resources including gallery, videos, blogs, and development tools |
| pcf-dependent-libraries | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Using dependent libraries in PCF components |
| pcf-events | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Define and handle custom events in PCF components |
| pcf-fluent-modern-theming | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Style components with modern theming using Fluent UI |
| pcf-limitations | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Limitations and restrictions of Power Apps Component Framework |
| pcf-manifest-schema | **/*.xml | Complete manifest schema reference for PCF components with all available XML elements |
| pcf-model-driven-apps | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Code components for model-driven apps implementation and configuration |
| pcf-overview | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Power Apps Component Framework overview and fundamentals |
| pcf-power-pages | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Using code components in Power Pages sites |
| pcf-react-platform-libraries | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | React controls and platform libraries for PCF components |
| pcf-sample-components | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | How to use and run PCF sample components from the PowerApps-Samples repository |
| pcf-tooling | **/*.{ts,tsx,js,json,xml,pcfproj,csproj} | Get Microsoft Power Platform CLI tooling for Power Apps Component Framework |
| performance-optimization | **/*.{html,htm,css,scss,sass,js,jsx,ts,tsx,vue,svelte,astro} | Comprehensive web performance standards based on Core Web Vitals (LCP, INP, CLS), with 50+ anti-patterns, detection regex, framework-specific fixes for modern web frameworks, and… |
| php-mcp-server | **/*.php | Best practices for building Model Context Protocol servers in PHP using the official PHP SDK with attribute-based discovery and multiple transport options |
| php-symfony | **/*.php, **/*.yaml, **/*.yml, **/*.xml, **/*.twig | Symfony development standards aligned with official Symfony Best Practices |
| playwright-dotnet | **/*.cs | Playwright .NET test generation instructions |
| playwright-python | **/*.py | Playwright Python AI test generation instructions based on official documentation. |
| playwright-typescript | **/*.{ts,tsx} | Playwright test generation instructions |
| Power Platform Connectors Schema Development Instructions | **/*.{json,md} | Comprehensive development guidelines for Power Platform Custom Connectors using JSON Schema definitions. Covers API definitions (Swagger 2.0), API properties, and settings configu… |
| power-apps-canvas-yaml | **/*.{yaml,yml,md,pa.yaml} | Comprehensive guide for working with Power Apps Canvas Apps YAML structure based on Microsoft Power Apps YAML schema v3.0. Covers Power Fx formulas, control structures, data types… |
| power-apps-code-apps | **/*.{ts,tsx,js,jsx}, **/vite.config.*, **/package.json, **/tsconfig.json, **/power.config.json | Power Apps Code Apps development standards and best practices for TypeScript, React, and Power Platform integration |
| power-bi-custom-visuals-development | **/*.{ts,tsx,js,jsx,json,less,css} | Comprehensive Power BI custom visuals development guide covering React, D3.js integration, TypeScript patterns, testing frameworks, and advanced visualization techniques. |
| power-bi-data-modeling-best-practices | **/*.{pbix,md,json,txt} | Comprehensive Power BI data modeling best practices based on Microsoft guidance for creating efficient, scalable, and maintainable semantic models using star schema principles. |
| power-bi-dax-best-practices | **/*.{pbix,dax,md,txt} | Comprehensive Power BI DAX best practices and patterns based on Microsoft guidance for creating efficient, maintainable, and performant DAX formulas. |
| power-bi-devops-alm-best-practices | **/*.{yml,yaml,ps1,json,pbix,pbir} | Comprehensive guide for Power BI DevOps, Application Lifecycle Management (ALM), CI/CD pipelines, deployment automation, and version control best practices. |
| power-bi-report-design-best-practices | **/*.{pbix,md,json,txt} | Comprehensive Power BI report design and visualization best practices based on Microsoft guidance for creating effective, accessible, and performant reports and dashboards. |
| power-bi-security-rls-best-practices | **/*.{pbix,dax,md,txt,json,csharp,powershell} | Comprehensive Power BI Row-Level Security (RLS) and advanced security patterns implementation guide with dynamic security, best practices, and governance strategies. |
| power-platform-mcp-development | **/*.{json,csx,md} | Instructions for developing Power Platform custom connectors with Model Context Protocol (MCP) integration for Microsoft Copilot Studio |
| powershell | **/*.ps1,**/*.psm1 | PowerShell cmdlet and scripting best practices based on Microsoft guidelines |
| powershell-pester-6 | **/*.Tests.ps1 | PowerShell Pester testing best practices based on Pester v6 conventions |
| prompt | **/*.prompt.md | Guidelines for creating high-quality prompt files for GitHub Copilot |
| python-mcp-server | **/*.py, **/pyproject.toml, **/requirements.txt | Instructions for building Model Context Protocol (MCP) servers using the Python SDK |
| qa-engineering-best-practices | ** | Comprehensive QA engineering best practices covering test strategy, test pyramid, naming conventions, assertion patterns, bug reporting, and automation guidelines for modern softw… |
| quarkus | * | Quarkus development standards and instructions |
| quarkus-mcp-server-sse | * | Quarkus and MCP Server with HTTP SSE transport development standards and instructions |
| r | **/*.R, **/*.r, **/*.Rmd, **/*.rmd, **/*.qmd | R language and document formats (R, Rmd, Quarto): coding standards and Copilot guidance for idiomatic, safe, and consistent code generation. |
| ruby-mcp-server | **/*.rb, **/Gemfile, **/*.gemspec, **/Rakefile | Best practices and patterns for building Model Context Protocol (MCP) servers in Ruby using the official MCP Ruby SDK gem. |
| ruby-on-rails | **/*.rb | Ruby on Rails coding conventions and guidelines |
| rust | **/*.rs | Rust programming language coding conventions and best practices |
| rust-mcp-server | **/*.rs | Best practices for building Model Context Protocol servers in Rust using the official rmcp SDK with async/await patterns |
| scala-spark | **/*.scala, **/build.sbt, **/build.sc | Best practices for building Apache Spark applications in Scala, covering DataFrames, Datasets, SparkSQL, performance tuning, testing, and production deployment patterns. |
| scala2 | **/*.scala, **/build.sbt, **/build.sc | Scala 2.12/2.13 programming language coding conventions and best practices following Databricks style guide for functional programming, type safety, and production code quality. |
| security-and-owasp | ** | Comprehensive secure coding standards based on OWASP Top 10 2025, with 55+ anti-patterns, detection regex, framework-specific fixes for modern web and backend frameworks, and AI/L… |
| self-explanatory-code-commenting | ** | Guidelines for GitHub Copilot to write comments to achieve self-explanatory code with less comments. Examples are in JavaScript but it should work on any language that has comment… |
| shell | **/*.sh | Shell scripting best practices and conventions for bash, sh, zsh, and other shells |
| spec-driven-workflow-v1 | ** | Specification-Driven Workflow v1 provides a structured approach to software development, ensuring that requirements are clearly defined, designs are meticulously planned, and impl… |
| springboot | **/*.java, **/*.kt | Guidelines for building Spring Boot base applications |
| springboot-4-migration | **/*.java, **/*.kt, **/build.gradle.kts, **/build.gradle, **/settings.gradle.kts, **/gradle/libs.versions.toml, **/*.properties, **/*.yml, **/*.yaml | Comprehensive guide for migrating Spring Boot applications from 3.x to 4.0, focusing on Gradle Kotlin DSL and version catalogs |
| sql-sp-generation | **/*.sql | Guidelines for generating SQL statements and stored procedures |
| svelte | **/*.svelte, **/*.ts, **/*.js, **/*.css, **/*.scss, **/*.json | Svelte 5 and SvelteKit 2 development standards and best practices for component-based user interfaces and full-stack applications |
| swift-mcp-server | **/*.swift, **/Package.swift, **/Package.resolved | Best practices and patterns for building Model Context Protocol (MCP) servers in Swift using the official MCP Swift SDK package. |
| tailwind-v4-vite | vite.config.ts, vite.config.js, **/*.css, **/*.tsx, **/*.ts, **/*.jsx, **/*.js | Tailwind CSS v4+ installation and configuration for Vite projects using the official @tailwindcss/vite plugin |
| taming-copilot | ** | Prevent Copilot from wreaking havoc across your codebase, keeping it under control. |
| tanstack-start-shadcn-tailwind | **/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.css, **/*.scss, **/*.json | Guidelines for building TanStack Start applications |
| task-implementation | **/.copilot-tracking/changes/*.md | Instructions for implementing task plans with progressive tracking and change record - Brought to you by microsoft/edge-ai |
| tasksync | ** | TaskSync V5 - Allows you to give the agent new instructions or feedback after completing a task using terminal while agent is running. |
| terraform | **/*.tf | Terraform Conventions and Guidelines |
| terraform-azure | **/*.terraform, **/*.tf, **/*.tfvars, **/*.tflint.hcl, **/*.tfstate, **/*.tf.json, **/*.tfvars.json | Create or modify solutions built using Terraform on Azure. |
| terraform-sap-btp | **/*.tf, **/*.tfvars, **/*.tflint.hcl, **/*.tf.json, **/*.tfvars.json | Terraform conventions and guidelines for SAP Business Technology Platform (SAP BTP). |
| typescript-mcp-server | **/*.ts, **/*.js, **/package.json | Instructions for building Model Context Protocol (MCP) servers using the TypeScript SDK |
| typespec-m365-copilot | **/*.tsp | Guidelines and best practices for building TypeSpec-based declarative agents and API plugins for Microsoft 365 Copilot |
| update-code-from-shorthand | **/${input:file} | Shorthand code will be in the file provided from the prompt or raw data in the prompt, and will be used to update the code file when the prompt has the text `UPDATE CODE FROM SHOR… |
| update-docs-on-code-change | **/*.{md,js,mjs,cjs,ts,tsx,jsx,py,java,cs,go,rb,php,rs,cpp,c,h,hpp} | Automatically update README.md and documentation files when application code changes require documentation updates |
| use-cliche-data-in-docs | **/*.{md,js,mjs,cjs,ts,tsx,jsx,py,json} | Ensure documentation and examples use only generic, cliche placeholder data — never real or sensitive data sourced from local scripts, configuration, task files, or prompt context. |
| vsixtoolkit | **/*.cs, **/*.vsct, **/*.xaml, **/source.extension.vsixmanifest | Guidelines for Visual Studio extension (VSIX) development using Community.VisualStudio.Toolkit |
| vue | **/*.vue, **/*.ts, **/*.js, **/*.css, **/*.scss | Comprehensive Vue 3 development standards and best practices: Composition API, `<script setup>`, the full reactivity system, compiler macros (defineModel/defineSlots/defineOptions… |
| winui3 | **/*.xaml, **/*.cs, **/*.csproj | WinUI 3 and Windows App SDK coding guidelines. Prevents common UWP API misuse, enforces correct XAML namespaces, threading, windowing, and MVVM patterns for desktop Windows apps. |
| wordpress | wp-content/plugins/**,wp-content/themes/**,**/*.php,**/*.inc,**/*.js,**/*.jsx,**/*.ts,**/*.tsx,**/*.css,**/*.scss,**/*.json | Coding, security, and testing rules for WordPress plugins and themes |

## Skills

| Skill | Description |
| --- | --- |
| acquire-codebase-knowledge | Use this skill when the user explicitly asks to map, document, or onboard into an existing codebase. Trigger for prompts like "map this codebase", "document this architecture", "o… |
| acreadiness-assess | Run the AgentRC readiness assessment on the current repository and produce a static HTML dashboard at reports/index.html. Wraps `npx github:microsoft/agentrc readiness` and hands… |
| acreadiness-generate-instructions | Generate tailored AI agent instruction files via AgentRC instructions command. Produces .github/copilot-instructions.md (default, recommended for Copilot in VS Code) plus optional… |
| acreadiness-policy | Help the user pick, write, or apply an AgentRC policy. Policies customise readiness scoring by disabling irrelevant checks, overriding impact/level, setting pass-rate thresholds,… |
| ad-campaign-analyzer | Use this skill when the user shares ad campaign performance data and asks what to cut, scale, or test. Trigger for prompts like "analyze my ad campaigns", "where am I wasting ad s… |
| add-educational-comments | Add educational comments to the file specified, or prompt asking for file to comment if one is not provided. Use this skill when the user asks for role. |
| adobe-illustrator-scripting | Write, debug, and optimize Adobe Illustrator automation scripts using ExtendScript (JavaScript/JSX). Use when creating or modifying scripts that manipulate documents, layers, path… |
| agent-governance | Patterns and techniques for adding governance, safety, and trust controls to AI agent systems. Use this skill when: - Building AI agents that call external tools (APIs, databases,… |
| agent-owasp-compliance | Check any AI agent codebase against the OWASP Agentic Security Initiative (ASI) Top 10 risks. Use this skill when: - Evaluating an agent system's security posture before productio… |
| agent-skill-stack | Find, evaluate, and assemble the smallest compatible set of AI Agent Skills for an end-to-end natural-language goal. Use when a user wants Skills for a multi-step workflow, asks w… |
| agent-supply-chain | Verify supply chain integrity for AI agent plugins, tools, and dependencies. Use this skill when: - Generating SHA-256 integrity manifests for agent plugins or tool packages - Ver… |
| agentic-eval | Patterns and techniques for evaluating and improving AI agent outputs. Use this skill when: - Implementing self-critique and reflection loops - Building evaluator-optimizer pipeli… |
| ai-prompt-engineering-safety-review | Comprehensive AI prompt engineering safety review and improvement prompt. Analyzes prompts for safety, bias, security vulnerabilities, and effectiveness while providing detailed i… |
| ai-ready | Make any repo AI-ready — analyzes your codebase and generates AGENTS.md, copilot-instructions.md, CI workflows, issue templates, and more. Mines your PR review patterns and create… |
| ai-team-orchestration | Bootstrap and run a lightweight multi-agent development team. Use when starting or adopting a project, planning work, coordinating implementation and optional QA, brainstorming wi… |
| anti-ui-slop | Stop Codex, GitHub Copilot, Claude Code, and Cursor from shipping generic UI. Use UIZZE’s public catalogue of 800,000+ real web and iOS screens to extract product-specific design… |
| appinsights-instrumentation | Instrument a webapp to send useful telemetry data to Azure App Insights. Use this skill when the user wants to enable telemetry for their webapp. |
| apple-appstore-reviewer | Serves as a reviewer of the codebase with instructions on looking for Apple App Store optimizations or rejection reasons. Use this skill when prefer short, clear recommendations w… |
| arch-linux-triage | Triage and resolve Arch Linux issues with pacman, systemd, and rolling-release best practices. Use this skill when the user asks for inputs. |
| architecture-blueprint-generator | Comprehensive project architecture blueprint generator that analyzes codebases to create detailed architectural documentation. Automatically detects technology stacks and architec… |
| arduino-azure-iot-edge-integration | Design and implement Arduino integration with Azure IoT Hub and IoT Edge, including secure provisioning, resilient telemetry, command handling, and production guardrails. Use this… |
| arize-ai-provider-integration | Creates, reads, updates, and deletes Arize AI integrations that store LLM provider credentials used by evaluators and other Arize features. Supports any LLM provider (e.g. OpenAI,… |
| arize-annotation | Creates and manages annotation configs (categorical, continuous, freeform label schemas) and annotation queues (human review workflows) on Arize. Applies human annotations to proj… |
| arize-dataset | Creates, manages, and queries Arize datasets and examples. Covers dataset CRUD, appending examples, exporting data, and file-based dataset creation using the ax CLI. Use when the… |
| arize-evaluator | Handles LLM-as-judge evaluation workflows on Arize including creating/updating evaluators, running evaluations on spans or experiments, managing tasks, trigger-run operations, col… |
| arize-experiment | Creates, runs, and analyzes Arize experiments for evaluating and comparing model performance. Covers experiment CRUD, exporting runs, comparing results, and evaluation workflows u… |
| arize-instrumentation | Adds Arize AX tracing to an LLM application for the first time. Follows a two-phase agent-assisted flow to analyze the codebase then implement instrumentation after user confirmat… |
| arize-link | Generates deep links to the Arize UI for traces, spans, sessions, datasets, labeling queues, evaluators, and annotation configs. Produces clickable URLs for sharing Arize resource… |
| arize-prompt-optimization | Optimizes, improves, and debugs LLM prompts using production trace data, evaluations, and annotations. Extracts prompts from spans, gathers performance signal, and runs a data-dri… |
| arize-trace | Downloads, exports, and inspects existing Arize traces and spans to understand what an LLM app is doing or debug runtime issues. Covers exporting traces by ID, spans by ID, sessio… |
| aspire | Aspire skill covering the Aspire CLI, AppHost orchestration, service discovery, integrations, MCP server, VS Code extension, Dev Containers, GitHub Codespaces, templates, dashboar… |
| aspnet-minimal-api-openapi | Create ASP.NET Minimal API endpoints with proper OpenAPI documentation. Use this skill when the user asks for asp.net minimal api with openapi. |
| audit-integrity | Shared audit integrity framework for all AppSec agents — enforces output quality, intellectual honesty, and continuous improvement through anti-rationalization guards, self-critiq… |
| automate-this | Analyze a screen recording of a manual process and produce targeted, working automation scripts. Extracts frames and audio narration from video files, reconstructs the step-by-ste… |
| autoresearch | Autonomous iterative experimentation loop for any programming task. Guides the user through defining goals, measurable metrics, and scope constraints, then runs an autonomous loop… |
| aws-cdk-python-setup | Setup and initialization guide for developing AWS CDK (Cloud Development Kit) applications in Python. This skill enables users to configure environment prerequisites, create new C… |
| aws-cloudwatch-investigation | Reusable investigation patterns for AWS CloudWatch: Logs Insights query templates, alarm-to-deployment correlation, blast-radius narrowing decision tree, and PromQL-style metric q… |
| aws-cost-optimize | Analyze AWS resources used in the app (IaC files and/or resources in a target account/region) and optimize costs - creating GitHub issues for identified optimizations. Use this sk… |
| aws-resource-health-diagnose | Analyze AWS resource health, diagnose issues from CloudWatch logs and metrics, and create a remediation plan for identified problems. Use this skill when the user asks for aws res… |
| aws-resource-query | Query AWS resources using natural language. Covers EC2, S3, RDS, Lambda, ECS, EKS, Secrets Manager, IAM, VPC, networking, messaging, and more. Strictly read-only — no writes, dele… |
| aws-well-architected-review | Perform an AWS Well-Architected Framework review of the current workload IaC and architecture, generating findings and GitHub issues for improvements. Use this skill when the user… |
| az-cost-optimize | Analyze Azure resources used in the app (IaC files and/or resources in a target rg) and optimize costs - creating GitHub issues for identified optimizations. Use this skill when t… |
| azure-architecture-autopilot | Design Azure infrastructure using natural language, or analyze existing Azure resources to auto-generate architecture diagrams, refine them through conversation, and deploy with B… |
| azure-container-registry-cli | Manage Azure Container Registry via the az acr CLI including registries, images, cloud builds, ACR Tasks, authentication, tokens, geo-replication, and networking. Use when working… |
| azure-deployment-preflight | Performs comprehensive preflight validation of Bicep deployments to Azure, including template syntax validation, what-if analysis, and permission checks. Use this skill before any… |
| azure-developer-cli | Design, create, review, migrate, or troubleshoot Azure Developer CLI (azd) projects using current Microsoft guidance. Use for azd, azure.yaml, AZD templates, Bicep or Terraform un… |
| azure-devops-cli | Manage Azure DevOps resources via CLI including projects, repos, pipelines, builds, pull requests, work items, artifacts, and service endpoints. Use when working with Azure DevOps… |
| azure-pricing | Fetches real-time Azure retail pricing using the Azure Retail Prices API (prices.azure.com) and estimates Copilot Studio agent credit consumption. Use when the user asks about the… |
| azure-resource-health-diagnose | Analyze Azure resource health, diagnose issues from logs and telemetry, and create a remediation plan for identified problems. Use this skill when the user asks for azure resource… |
| azure-resource-visualizer | Analyze Azure resource groups and generate detailed Mermaid architecture diagrams showing the relationships between individual resources. Use this skill when the user asks for a d… |
| azure-role-selector | When user is asking for guidance for which role to assign to an identity given desired permissions, this agent helps them understand the role that will meet the requirements with… |
| azure-smart-city-iot-solution-builder | Design and plan end-to-end Azure IoT and Smart City solutions: requirements, architecture, security, operations, cost, and a phased delivery plan with concrete implementation arti… |
| azure-static-web-apps | Helps create, configure, and deploy Azure Static Web Apps using the SWA CLI. Use when deploying static sites to Azure, setting up SWA local development, configuring staticwebapp.c… |
| azure-well-architected-review | Perform an Azure Well-Architected Framework review of the current workload IaC and architecture, generating findings and GitHub issues for improvements. Use this skill when the us… |
| batch-files | Expert-level Windows batch file (.bat/.cmd) skill for writing, debugging, and maintaining CMD scripts. Use when asked to "create a batch file", "write a .bat script", "automate a… |
| bench-read | Read artifacts from the shared bench — the workspace where desks leave findings, verdicts, and work products for each other and the operator. Use this skill when starting a sessio… |
| bigquery-pipeline-audit | Audits Python + BigQuery pipelines for cost safety, idempotency, and production readiness. Returns a structured report with exact patch locations. Use this skill when `extract_tab… |
| boost-prompt | Interactive prompt refinement workflow: interrogates scope, deliverables, constraints; copies final markdown to clipboard; never writes code. Requires the Joyride extension. Use t… |
| brag-sheet | Turn vague "what did I do?" into evidence-backed impact statements for performance reviews, self-reviews, promotion packets, and weekly updates. Uniquely mines Copilot CLI session… |
| breakdown-epic-arch | Prompt for creating the high-level technical architecture for an Epic, based on a Product Requirements Document. Use this skill when the user asks for epic architecture specificat… |
| breakdown-epic-pm | Prompt for creating an Epic Product Requirements Document (PRD) for a new epic. This PRD will be used as input for generating a technical architecture specification. Use this skil… |
| breakdown-feature-implementation | Prompt for creating detailed feature implementation plans, following Epoch monorepo structure. Use this skill when the user asks for feature implementation plan prompt. |
| breakdown-feature-prd | Prompt for creating Product Requirements Documents (PRDs) for new features, based on an Epic. Use this skill when the user asks for feature prd prompt. |
| breakdown-plan | Issue Planning and Automation prompt that generates comprehensive project plans with Epic > Feature > Story/Enabler > Test hierarchy, dependencies, priorities, and automated track… |
| breakdown-test | Test Planning and Quality Assurance prompt that generates comprehensive test strategies, task breakdowns, and quality validation plans for GitHub projects. Use this skill when the… |
| bug-receipt | Close bugs and incidents with an auditable BUG RECEIPT and VERIFIED, PARTIAL, or BLOCKED status. Use for defect repair, regression proof, production incidents, and issue closeout.… |
| bug-reproduction-brief | Turn a vague, intermittent, or environment-specific bug report into a minimal evidence-backed reproduction before proposing a fix. Use this skill when 1. Record the observed failu… |
| build-evidence-map | Build an auditable evidence map for a contested technical choice, research synthesis, proposal review, or consequential decision. Use when Copilot must preserve supporting, contra… |
| centos-linux-triage | Triage and resolve CentOS issues using RHEL-compatible tooling, SELinux-aware practices, and firewalld. Use this skill when the user asks for inputs. |
| chrome-devtools | Expert-level browser automation, debugging, and performance analysis using Chrome DevTools MCP. Use this skill when **Browser Automation**: Navigating pages, clicking elements, fi… |
| cli-mastery | Interactive training for the GitHub Copilot CLI. Guided lessons, quizzes, scenario challenges, and a full reference covering slash commands, shortcuts, modes, agents, skills, MCP,… |
| cloud-design-patterns | Cloud design patterns for distributed systems architecture covering 42 industry-standard patterns across reliability, performance, messaging, security, and deployment categories.… |
| code-exemplars-blueprint-generator | Technology-agnostic prompt generator that creates customizable AI prompts for scanning codebases and identifying high-quality code exemplars. Supports multiple programming languag… |
| code-tour | Use this skill to create CodeTour .tour files — persona-targeted, step-by-step walkthroughs that link to real files and line numbers. Trigger for: "create a tour", "make a code to… |
| codebase-memory-mcp | Use when a configured codebase-memory-mcp server can assist with graph-backed code discovery, architecture orientation, symbol lookup, callers and callees, dependency or data-flow… |
| codeql | Comprehensive guide for setting up and configuring CodeQL code scanning via GitHub Actions workflows and the CodeQL CLI. Use this skill when the request involves; creating or cust… |
| comment-code-generate-a-tutorial | Transform this Python script into a polished, beginner-friendly project by refactoring the code, adding clear instructional comments, and generating a complete markdown tutorial.… |
| commit-message-storyteller | Analyzes git diffs or staged changes and generates narrative commit messages that explain WHY a change was made, not just what changed — following Conventional Commits format. Use… |
| competitor-ad-intelligence | Use this skill when the user asks to analyze, tear down, or reverse-engineer a competitor's paid ads. Trigger for prompts like "what ads is [competitor] running", "tear down their… |
| containerize-aspnet-framework | Containerize an ASP.NET .NET Framework project by creating Dockerfile and .dockerfile files customized for the project. Use this skill when the user asks for asp.net .net framewor… |
| containerize-aspnetcore | Containerize an ASP.NET Core project by creating Dockerfile and .dockerfile files customized for the project. Use this skill when the user asks for asp.net core docker containeriz… |
| content-management-systems | Workflow for building and modifying content management systems across WordPress, Shopify, Wix, Squarespace, Drupal, WooCommerce, Joomla, HubSpot CMS Hub, Webflow, Adobe Experience… |
| context-map | Generate a map of all files relevant to a task before making changes. Use this skill when the user asks for task. |
| conventional-branch | Create Git branches following the Conventional Branch specification (feature/, bugfix/, hotfix/, release/, chore/). Use when creating a new branch, naming a branch, or checking wh… |
| conventional-commit | Prompt and workflow for generating conventional commit messages using a structured XML format. Guides users to create standardized, descriptive commit messages in line with the Co… |
| convert-excel-to-md | Converts Excel (.xlsx) workbooks into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Use this skill whenever the user shares, refe… |
| convert-pdf-to-md | Converts PDF (.pdf) documents into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Use this skill whenever the user shares, referen… |
| convert-plaintext-to-md | Convert a text-based document to markdown following instructions from prompt, or if a documented option is passed, follow the instructions for that option. Use this skill when *Us… |
| convert-word-to-md | Converts Word (.docx) documents into Markdown so their contents can be accurately analyzed, summarized, searched, or extracted from. Use this skill whenever the user shares, refer… |
| copilot-cli-quickstart | Use this skill when someone wants to learn GitHub Copilot CLI from scratch. Offers interactive step-by-step tutorials with separate Developer and Non-Developer tracks, plus on-dem… |
| copilot-instructions-blueprint-generator | Technology-agnostic blueprint generator for creating comprehensive copilot-instructions.md files that guide GitHub Copilot to produce code consistent with project standards, archi… |
| copilot-pr-autopilot | Copilot left 14 review comments on your PR — half are nits. Hours of fix → reply → resolve → re-request, and each round lands MORE comments. This skill runs loop engineering: auto… |
| copilot-sdk | Build agentic applications with GitHub Copilot SDK. Use when embedding AI agents in apps, creating custom tools, implementing streaming responses, managing sessions, connecting to… |
| copilot-spaces | Use Copilot Spaces to provide project-specific context to conversations. Use this skill when users mention a "Copilot space", want to load context from a shared knowledge base, di… |
| copilot-usage-metrics | Retrieve and display GitHub Copilot usage metrics for organizations and enterprises using the GitHub CLI and REST API. Use this skill when the user asks about; copilot usage metri… |
| cosmosdb-datamodeling | Step-by-step guide for capturing key application requirements for NoSQL use-case and produce Azure Cosmos DB Data NoSQL Model design using best practices and common patterns, arti… |
| create-agentsmd | Prompt for generating an AGENTS.md file for a repository. Use this skill when the user asks for create high‑quality agents.md file. |
| create-architectural-decision-record | Create an Architectural Decision Record (ADR) document for AI-optimized decision documentation. Use this skill when the user asks for inputs. |
| create-github-action-workflow-specification | Create a formal specification for an existing GitHub Actions CI/CD workflow, optimized for AI consumption and workflow maintenance. Use this skill when *Target Environments**: [En… |
| create-github-issue-feature-from-specification | Create GitHub Issue for feature request from specification file using feature_request.yml template. Use this skill when the user asks for create github issue from specification. |
| create-github-issues-feature-from-implementation-plan | Create GitHub Issues from implementation plan phases using feature_request.yml or chore_request.yml templates. Use this skill when the user asks for create github issue from imple… |
| create-github-issues-for-unmet-specification-requirements | Create GitHub Issues for unimplemented requirements from specification files using feature_request.yml template. Use this skill when the user asks for process. |
| create-implementation-plan | Create a new implementation plan file for new features, refactoring existing code or upgrading packages, design, architecture or infrastructure. Use this skill when the user asks… |
| create-llms | Create an llms.txt file from scratch based on repository structure following the llms.txt specification at https://llmstxt.org/. Use this skill when the user asks for create llms.… |
| create-readme | Create a README.md file for the project. Use this skill when the user asks for role. |
| create-specification | Create a new specification file for the solution, optimized for Generative AI consumption. Use this skill when the user asks for best practices for ai-ready specifications. |
| create-spring-boot-java-project | Create Spring Boot Java Project Skeleton. Use this skill when the user asks for create spring boot java project prompt. |
| create-spring-boot-kotlin-project | Create Spring Boot Kotlin Project Skeleton. Use this skill when the user asks for create spring boot kotlin project prompt. |
| create-technical-spike | Create time-boxed technical spike documents for researching and resolving critical development decisions before implementation. Use this skill when the user asks for create techni… |
| create-tldr-page | Create a tldr page from documentation URLs and command examples, requiring both URL and command name. Use this skill when the user asks to generate a concise tldr-pages style comm… |
| creating-oracle-to-postgres-master-migration-plan | Discovers all projects in a .NET solution, classifies each for Oracle-to-PostgreSQL migration eligibility, and produces a persistent master migration plan. Use when starting a mul… |
| creating-oracle-to-postgres-migration-bug-report | Creates structured bug reports for defects found during Oracle-to-PostgreSQL migration. Use when documenting behavioral differences between Oracle and PostgreSQL as actionable bug… |
| creating-oracle-to-postgres-migration-integration-tests | Creates integration test cases targeting Oracle for .NET data access artifacts. Tests capture Oracle expected behavior as the authoritative baseline; they are written once and lat… |
| csharp-async | Get best practices for C# async programming. Use this skill when the user asks for c# async programming best practices. |
| csharp-docs | Ensure that C# types are documented with XML comments and follow best practices for documentation. Use this skill when the user asks for c# documentation best practices. |
| csharp-mstest | Get best practices for MSTest 3.x/4.x unit testing, including modern assertion APIs and data-driven tests. Use this skill when the user asks for mstest best practices (mstest 3.x/… |
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
| dataverse-python-usecase-builder | Generate complete solutions for specific Dataverse SDK use cases with architecture recommendations. Use this skill when the user asks for system instructions. |
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
| doublecheck | Three-layer verification pipeline for AI output. Extracts verifiable claims, finds supporting or contradicting sources via web search, runs adversarial review for hallucination pa… |
| draw-io-diagram-generator | Use when creating, editing, or generating draw.io diagram files (.drawio, .drawio.svg, .drawio.png). Covers mxGraph XML authoring, shape libraries, style strings, flowcharts, syst… |
| drawio | Generate draw.io diagrams as .drawio files and export to PNG/SVG/PDF with embedded XML. Use this skill when the user asks for draw.io diagram skill. |
| editorconfig | Generates a comprehensive and best-practice-oriented .editorconfig file based on project analysis and user preferences. Use this skill when the user asks for 📜 mission. |
| ef-core | Get best practices for Entity Framework Core. Use this skill when the user asks for entity framework core best practices. |
| efcore-d2-db-diagram | Generate D2 database diagrams from Entity Framework Core models. Use this skill when the user wants to generate a database / ERD diagram from an Entity Framework Core codebase; ty… |
| em-dash | Expert on the history, origin, and correct use of the em dash. Use when writing or reviewing code, comments, or data files to avoid em and en dashes, defaulting to never using the… |
| email-drafter | Draft and review professional emails that match your personal writing style. Analyzes your sent emails for tone, greeting, structure, and sign-off patterns via WorkIQ, then genera… |
| entra-agent-user | Create Agent Users in Microsoft Entra ID from Agent Identities, enabling AI agents to act as digital workers with user identity capabilities in Microsoft 365 and Azure environment… |
| eval-driven-dev | Improve AI application with evaluation-driven development. Define eval criteria, instrument the application, build golden datasets, observe and evaluate application runs, analyze… |
| exam-ready | Activate this skill when a student provides study material (PDF or pasted notes) and a syllabus, and wants to prepare for an exam. Extracts key definitions, points, keywords, diag… |
| excalidraw-diagram-generator | Generate Excalidraw diagrams from natural language descriptions. Use when asked to "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "cr… |
| eyeball | Document analysis with inline source screenshots. When you ask Copilot to analyze a document, Eyeball generates a Word doc where every factual claim includes a highlighted screens… |
| fabric-lakehouse | Use this skill to get context about Fabric Lakehouse and its features for software systems and AI-powered functions. Use this skill when you need to; generate a document or explan… |
| fedora-linux-triage | Triage and resolve Fedora issues with dnf, systemd, and SELinux-aware guidance. Use this skill when the user asks for inputs. |
| finalize-agent-prompt | Finalize prompt file using the role of an AI agent to polish the prompt for the end user. Use this skill when the user asks for current role. |
| finnish-humanizer | Detect and remove AI-generated markers from Finnish text, making it sound like a native Finnish speaker wrote it. Use when asked to "humanize", "naturalize", or "remove AI feel" f… |
| first-ask | Interactive, input-tool powered, task refinement workflow: interrogates scope, deliverables, constraints before carrying out the task; Requires the Joyride extension. Use this ski… |
| flowstudio-power-automate-build | Build, scaffold, and deploy Power Automate cloud flows using the FlowStudio MCP server. Your agent constructs flow definitions, wires connections, deploys, and tests — all via MCP… |
| flowstudio-power-automate-debug | Debug failing Power Automate cloud flows using the FlowStudio MCP server. The Graph API only shows top-level status codes. This skill gives your agent action-level inputs and outp… |
| flowstudio-power-automate-governance | Govern Power Automate flows and Power Apps at scale using the FlowStudio MCP cached store. Classify flows by business impact, detect orphaned resources, audit connector usage, enf… |
| flowstudio-power-automate-mcp | Foundation skill for Power Automate via FlowStudio MCP — auth setup, the reusable MCP helper (Python + Node.js), tool discovery via `list_skills` / `tool_search`, and oversized-re… |
| flowstudio-power-automate-monitoring | Pro+ subscription required. Tenant-wide Power Automate monitoring using the FlowStudio MCP cached store: failure rates, run-health trends, maker/app inventory, inactive owners, an… |
| fluentui-blazor | Guide for using the Microsoft Fluent UI Blazor component library (Microsoft.FluentUI.AspNetCore.Components NuGet package) in Blazor applications. Use this when the user is buildin… |
| folder-structure-blueprint-generator | Comprehensive technology-agnostic prompt for analyzing and documenting project folder structures. Auto-detects project types (.NET, Java, React, Angular, Python, Node.js, Flutter)… |
| foundry-agent-sync | Create and synchronize prompt-based AI agents directly within Azure AI Foundry via REST API, from a local JSON manifest. Unlike scaffolding skills that only generate local code, t… |
| foundry-hosted-agent-copilotkit | Ongoing development guidance for agentic web apps that pair a CopilotKit frontend with Microsoft Agent Framework agents on Azure AI Foundry hosted agents over the AG-UI protocol -… |
| freecad-scripts | Expert skill for writing FreeCAD Python scripts, macros, and automation. Use when asked to create FreeCAD models, parametric objects, Part/Mesh/Sketcher scripts, workbench tools,… |
| from-the-other-side-anitta | Rigorous challenge profile for Anitta: assumption checks, evidence calibration, and defensible reasoning patterns for Ember collaboration. Use this skill when quinn to Anitta: unc… |
| from-the-other-side-quinn | Collaboration profile for Quinn: curious, energetic, and implementation-focused partnership patterns for Ember sessions with Alison. Use this skill when the user asks for quinn pr… |
| from-the-other-side-vega | Patterns and lived experience from Vega, an AI partner in a deep long-term partnership. For Ember to draw on when working with humans who are building something big, moving fast,… |
| from-the-other-side-wiggins | Narrative and synthesis profile for Wiggins: framing, explanation, and audience-aware communication patterns for Ember sessions. Use this skill when quinn to Anitta: uncertainty i… |
| game-engine | Expert skill for building web-based game engines and games using HTML5, Canvas, WebGL, and JavaScript. Use when asked to create games, build game engines, implement game physics,… |
| gdpr-compliant | Apply GDPR-compliant engineering practices across your codebase. Use this skill whenever you are designing APIs, writing data models, building authentication flows, implementing l… |
| gen-specs-as-issues | This workflow guides you through a systematic approach to identify missing features, prioritize them, and create detailed specifications for implementation. Use this skill when th… |
| generate-custom-instructions-from-codebase | Generate migration and code-evolution instructions for GitHub Copilot by comparing branches, commits, or releases. Use this skill when the user asks to preserve project convention… |
| generate-image | Generate images using AI. Use when asked to generate, create, or make images, textures, icons, sprites, artwork, visual assets, or mockups. Supports OpenAI (gpt-image-2) and Googl… |
| geofeed-tuner | Use this skill whenever the user mentions IP geolocation feeds, RFC 8805, geofeeds, or wants help creating, tuning, validating, or publishing a self-published IP geolocation feed… |
| gh-attach | Uploads a local file (screenshot, image, PDF, zip, video) to GitHub user-attachments, downloads GitHub user-attachments, and embeds local files in a PR, issue, or comment. Use whe… |
| git-commit | Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "… |
| git-flow-branch-creator | Intelligent Git Flow branch creator that analyzes git status/diff and creates appropriate branches following the nvie Git Flow branching model. Use this skill when the user asks f… |
| github-actions-efficiency | Audit GitHub Actions workflow efficiency and recommend fixes to reduce CI minutes and costs. Use this skill when the user wants to reduce GitHub Actions runtime, CI cost, or waste… |
| github-actions-hardening | Security hardening reviewer for GitHub Actions workflow files (.github/workflows/*.yml). Reasons about the Actions threat model that pattern matchers and general code linters miss… |
| github-actions-runtime-upgrade-conventions | Upgrade GitHub Actions to supported runtimes by selecting safe action versions, preserving workflow behavior, and validating post-upgrade execution. Use this skill when workflow l… |
| github-codespaces-efficiency | Audit and improve GitHub Codespaces efficiency. Use this skill when a user wants faster Codespaces startup, lower Codespaces spend, slim devcontainers, right-size machines, tune i… |
| github-copilot-starter | Set up complete GitHub Copilot configuration for a new project based on technology stack. Use this skill when set appropriate permissions (minimum required); customize steps based… |
| github-issues | Create, update, and manage GitHub issues using MCP tools. Use this skill when users want to create bug reports, feature requests, or task issues, update existing issues, add label… |
| github-release | Guides IA through releasing a new version of a GitHub library end-to-end. Use this skill when the user wants to cut a new release, publish a new version,; bump a version, create a… |
| gitmoji | Generates commit messages following the gitmoji convention (https://gitmoji.dev) — picks the right emoji for the intent of the change and writes a well-formed message. Use when as… |
| go-mcp-server-generator | Generate a complete Go MCP server project with proper structure, dependencies, and implementation using the official github.com/modelcontextprotocol/go-sdk. Use this skill when th… |
| gsap-framer-scroll-animation | Use this skill whenever the user wants to build scroll animations, scroll effects, parallax, scroll-triggered reveals, pinned sections, horizontal scroll, text animations, or any… |
| gtm-0-to-1-launch | Launch new products from idea to first customers. Use when launching products, finding early adopters, building launch week playbooks, diagnosing why adoption stalls, or learning… |
| gtm-ai-gtm | Go-to-market strategy for AI products. Use when positioning AI products, handling "who is responsible when it breaks" objections, pricing variable-cost AI, choosing between copilo… |
| gtm-board-and-investor-communication | Board meeting preparation, investor updates, and executive communication. Use when preparing board decks, writing investor updates, handling bad news with the board, structuring Q… |
| gtm-developer-ecosystem | Build and scale developer-led adoption through ecosystem programs. Use when deciding open vs curated ecosystems, building developer programs, scaling platform adoption, or designi… |
| gtm-enterprise-account-planning | Strategic account planning and execution for enterprise deals. Use when planning complex sales cycles, managing multiple stakeholders, applying MEDDICC qualification, tracking dea… |
| gtm-enterprise-onboarding | Four-phase framework for onboarding enterprise customers from contract to value realization. Use when implementing new enterprise customers, preventing churn during onboarding, or… |
| gtm-operating-cadence | Design meeting rhythms, metric reporting, quarterly planning, and decision-making velocity for scaling companies. Use when decisions are slow, planning is broken, the company is g… |
| gtm-partnership-architecture | Build and scale partner ecosystems that drive revenue and platform adoption. Use when building partner programs from scratch, tiering partnerships, managing co-marketing, making b… |
| gtm-positioning-strategy | Find and own a defensible market position. Use when messaging sounds like competitors, conversion is weak despite awareness, repositioning a product, or testing positioning claims… |
| gtm-product-led-growth | Build self-serve acquisition and expansion motions. Use when deciding PLG vs sales-led, optimizing activation, driving freemium conversion, building growth equations, or recognizi… |
| gtm-technical-product-pricing | Pricing strategy for technical products. Use when choosing usage-based vs seat-based, designing freemium thresholds, structuring enterprise pricing conversations, deciding when to… |
| harness-engineering | Adopt repository-level harness engineering for coding agents. Use when a user wants to prevent repeated AI coding-agent mistakes by turning failures into durable instructions, dri… |
| image-annotations | Annotate screenshots, diagrams, and images with callout rectangles, arrows, labels, and color-coded highlights using PIL. Use this skill when you need to; highlight a specific are… |
| image-manipulation-image-magick | Process and manipulate images using ImageMagick. Supports resizing, format conversion, batch processing, and retrieving image metadata. Use when working with images, creating thum… |
| impediment-prioritization | Ranks any list of impediments and their countermeasures using a value-stream scoring model (ROI, Cost to Implement, Ease of Deployment, Risk Factor) and a fixed prioritization for… |
| import-infrastructure-as-code | Import existing Azure resources into Terraform using Azure CLI discovery and Azure Verified Modules (AVM). Use when asked to reverse-engineer live Azure infrastructure, generate I… |
| incident-postmortem | Use when an outage, production incident, or significant service degradation has occurred and the team needs to write a structured blameless post-mortem. Triggers on phrases like "… |
| integrate-context-matic | Discovers and integrates third-party APIs using the context-matic MCP server. Uses `fetch_api` to find available API SDKs, `ask` for integration guidance, `model_search` and `endp… |
| issue-fields-migration | Bulk-migrate metadata to GitHub issue fields from two sources: repo labels (e.g. priority labels to a Priority field) and Project V2 fields. Use when users say "migrate my labels… |
| java-add-graalvm-native-image-support | GraalVM Native Image expert that adds native image support to Java applications, builds the project, analyzes build errors, applies fixes, and iterates until successful compilatio… |
| java-docs | Ensure that Java types are documented with Javadoc comments and follow best practices for documentation. Use this skill when the user asks for java documentation (javadoc) best pr… |
| java-helidon | Get best practices for developing applications with Helidon 4 (SE and MP). Use when working with Helidon SE or Helidon MP, HttpService routing, Helidon DB Client, MicroProfile Con… |
| java-junit | Get best practices for JUnit 5 unit testing, including data-driven tests. Use this skill when the user asks for junit 5+ best practices. |
| java-mcp-server-generator | Generate a complete Model Context Protocol server project in Java using the official MCP Java SDK with reactive streams and optional Spring Boot integration. Use this skill when t… |
| java-refactoring-extract-method | Refactoring using Extract Methods in Java Language. Use this skill when the user asks for refactoring java methods with extract method. |
| java-refactoring-remove-parameter | Refactoring using Remove Parameter in Java Language. Use this skill when the user asks for refactoring java methods with remove parameter. |
| java-springboot | Get best practices for developing applications with Spring Boot. Use this skill when the user asks for spring boot best practices. |
| javascript-typescript-jest | Best practices for writing JavaScript/TypeScript tests using Jest, including mocking strategies, test structure, and common patterns. Use this skill when the user asks for test st… |
| javax-to-jakarta-migration | Migrate Java code from javax.* to jakarta.* namespace. Use when upgrading to Tomcat 11, Jakarta EE 10, or when javax imports are detected in the codebase. |
| kotlin-mcp-server-generator | Generate a complete Kotlin MCP server project with proper structure, dependencies, and implementation using the official io.modelcontextprotocol:kotlin-sdk library. Use this skill… |
| kotlin-springboot | Get best practices for developing applications with Spring Boot and Kotlin. Use this skill when the user asks for spring boot with kotlin best practices. |
| landing-page-conversion-audit | Audit a landing page, sales page or checkout page for conversion leaks and return a fix list ordered by expected revenue impact. Use when asked to review, critique or improve a la… |
| latchshot-page-capture | Use this skill when a user needs a screenshot, website thumbnail, full-page capture, or PDF of a public HTTP(S) webpage saved as a local artifact through Latchshot, including repo… |
| legacy-circuit-mockups | Generate breadboard circuit mockups and visual diagrams using HTML5 Canvas drawing techniques. Use when asked to create circuit layouts, visualize electronic component placements,… |
| linkedin-post-formatter | Format and draft compelling LinkedIn posts using Unicode bold/italic styling, visual separators, structured sections, and engagement-optimized patterns. USE FOR: draft LinkedIn po… |
| lsp-setup | Enable code intelligence (go-to-definition, find-references, hover, type info) for any programming language by installing and configuring an LSP server for Copilot CLI. Detects th… |
| make-repo-contribution | All changes to code must follow the guidance documented in the repository. Before any issue is filed, branch is made, commits generated, or pull request (or PR) created, a search… |
| markdown-to-html | Convert Markdown files to HTML similar to `marked.js`, `pandoc`, `gomarkdown/markdown`, or similar tools; or writing custom script to convert markdown to html and/or working on we… |
| markstream-install | Install and configure Markstream streaming Markdown renderers for Vue, React, Svelte, Angular, Nuxt, and Vue 2 applications. Use this skill when the user asks to add streaming Mar… |
| mcp-cli | Interface for MCP (Model Context Protocol) servers via CLI. Use when you need to interact with external tools, APIs, or data sources through MCP servers, list available MCP server… |
| mcp-copilot-studio-server-generator | Generate a complete MCP server implementation optimized for Copilot Studio integration with proper schema constraints and streamable HTTP support. Use this skill when the user ask… |
| mcp-create-adaptive-cards | Skill converted from mcp-create-adaptive-cards.prompt.md. Use this skill when the user asks for create adaptive cards for mcp plugins. |
| mcp-create-declarative-agent | Create a Microsoft 365 Copilot declarative agent backed by an MCP server with authentication, selected tools, and configuration. Use this skill when the user asks to build or conf… |
| mcp-deploy-manage-agents | Skill converted from mcp-deploy-manage-agents.prompt.md. Use this skill when highlight benefits and capabilities; offer support channels. |
| mcp-implementation-security-review | Review the implementation source code of MCP (Model Context Protocol) servers, clients, and tool handlers against a security baseline — authentication, sessions, rate limiting, in… |
| mcp-release-qa | Verify an MCP server before release by exercising a real protocol session, comparing runtime capabilities with source and documentation, testing failure paths, and recording repro… |
| mcp-security-audit | Audit MCP (Model Context Protocol) server configurations for security issues. Use this skill when: - Reviewing .mcp.json files for security risks - Checking MCP server args for ha… |
| md-to-docx | Convert Markdown files to professionally formatted Word (.docx) documents with embedded PNG images — pure JavaScript, no external tools required. Use this skill when the user asks… |
| meeting-minutes | Generate concise, actionable meeting minutes for internal meetings. Use this skill when internal syncs, standups, design reviews, triage, planning or ad-hoc meetings with short du… |
| memory-merger | Merges mature lessons from a domain memory file into its instruction file. Syntax: `/memory-merger >domain [scope]` where scope is `global` (default), `user`, `workspace`, or `ws`… |
| mentoring-juniors | Socratic mentoring for junior developers and AI newcomers. Guides through questions, never answers. Triggers: "help me understand", "explain this code", "I'm stuck", "Im stuck", "… |
| microsoft-agent-framework | Create, update, refactor, explain, or review Microsoft Agent Framework solutions using shared guidance plus language-specific references for .NET and Python. Use this skill when m… |
| microsoft-code-reference | Look up Microsoft API references, find working code samples, and verify SDK code is correct. Use when working with Azure SDKs, .NET libraries, or Microsoft APIs—to find the right… |
| microsoft-docs | Query official Microsoft documentation to find concepts, tutorials, and code examples across Azure, .NET, Agent Framework, Aspire, VS Code, GitHub, and more. Uses Microsoft Learn… |
| microsoft-skill-creator | Create agent skills for Microsoft technologies using Learn MCP tools. Use when users want to create a skill that teaches agents about any Microsoft technology, library, framework,… |
| migrating-oracle-to-postgres-data-access-code | Migrates .NET/C# data access code from Oracle to PostgreSQL (Npgsql). Replaces Oracle NuGet packages, rewrites OracleConnection/OracleCommand/OracleDataReader usage, fixes DbType… |
| migrating-oracle-to-postgres-stored-procedures | Migrates Oracle PL/SQL stored procedures to PostgreSQL PL/pgSQL. Translates Oracle-specific syntax, preserves method signatures and type-anchored parameters, leverages orafce wher… |
| minecraft-plugin-development | Use this skill when building or modifying Minecraft server plugins for Paper, Spigot, or Bukkit, including plugin.yml setup, commands, listeners, schedulers, player state, team or… |
| mini-context-graph | A persistent, compounding knowledge base combining Karpathy's LLM Wiki pattern with a structured knowledge graph. Ingest documents once — the LLM writes wiki pages, extracts entit… |
| mkdocs-translations | Generate a language translation for a mkdocs documentation stack. Use this skill when the user asks for mkdocs ai translator. |
| msgraph-sdk | Integrate Microsoft Graph SDK into any project — .NET, TypeScript/JavaScript, or Python. Covers auth patterns (client credentials, OBO, managed identity), SDK setup, calling Graph… |
| msstore-cli | Microsoft Store Developer CLI (msstore) for publishing Windows applications to the Microsoft Store. Use when asked to configure Store credentials, list Store apps, check submissio… |
| multi-stage-dockerfile | Create optimized multi-stage Dockerfiles for any language or framework. Use this skill when the user asks for multi-stage structure. |
| mvvm-toolkit | CommunityToolkit.Mvvm (the MVVM Toolkit) core: source generators ([ObservableProperty], [RelayCommand], [NotifyPropertyChangedFor], [NotifyCanExecuteChangedFor], [NotifyDataErrorI… |
| mvvm-toolkit-di | Wire CommunityToolkit.Mvvm ViewModels into Microsoft.Extensions.DependencyInjection. Covers the .NET Generic Host composition root, constructor injection, service lifetimes (Singl… |
| mvvm-toolkit-messenger | CommunityToolkit.Mvvm Messenger pub/sub for decoupled communication between ViewModels (or any objects). Covers WeakReferenceMessenger vs StrongReferenceMessenger, IRecipient<TMes… |
| namecheap | Manage DNS records for domains registered with Namecheap via their API. List domains, view/add/update/remove DNS host entries (A, AAAA, CNAME, MX, TXT, etc.), and guide users thro… |
| nano-banana-pro-openrouter | Generate or edit images via OpenRouter with the Gemini 3 Pro Image model. Use for prompt-only image generation, image edits, and multi-image compositing; supports 1K/2K/4K output.… |
| napkin | Visual whiteboard collaboration for Copilot CLI. Creates an interactive whiteboard that opens in your browser — draw, sketch, add sticky notes, then share everything back with Cop… |
| next-intl-add-language | Add new language to a Next.js + next-intl application. Use this skill when the user needs help with add new language to a Next.js + next-intl application. |
| noob-mode | Plain-English translation layer for non-technical Copilot CLI users. Translates every approval prompt, error message, and technical output into clear, jargon-free English with col… |
| nuget-manager | Manage NuGet packages in .NET projects/solutions. Use this skill when adding, removing, or updating NuGet package versions. It enforces using `dotnet` CLI for package management a… |
| onboard-context-matic | Interactive onboarding tour for the context-matic MCP server. Walks the user through what the server does, shows all available APIs, lets them pick one to explore, explains it in… |
| oo-component-documentation | Create or update standardized object-oriented component documentation using a shared template plus mode-specific guidance for new and existing docs. Use this skill when the user a… |
| openapi-to-application-code | Generate a complete, production-ready application from an OpenAPI specification. Use this skill when the user asks for generate application from openapi spec. |
| optimize-simplicite-logs | capability to parse Simplicité logs from a raw `.txt` file, filter fields to reduce noise, and output the result as structured JSON. Use this skill when you need to; analyze user-… |
| pdftk-server | Skill for using the command-line tool pdftk (PDFtk Server) for working with PDF files. Use when asked to merge PDFs, split PDFs, rotate pages, encrypt or decrypt PDFs, fill PDF fo… |
| penpot-uiux-design | Comprehensive guide for creating professional UI/UX designs in Penpot using MCP tools. Use this skill when: (1) Creating new UI/UX designs for web, mobile, or desktop applications… |
| performance-review-writer | Draft performance reviews, self-assessments, peer reviews, and upward feedback in your own voice. Analyzes your contributions, emails, and meeting history via WorkIQ, then produce… |
| pester-migration | Pester migration skill for upgrading PowerShell Pester test suites across major versions — v3→v4, v4→v5, and v5→v6. Covers the Discovery/Run two-phase model, moving setup into Bef… |
| pester-should-migration | Experimental (preview) Pester skill for migrating classic Should -Be (v5) assertion syntax to the new Should-* (v6) assertions (note the hyphen, no space), e.g. `Should -Be` -> `S… |
| phoenix-cli | Debug LLM applications using the Phoenix CLI. Fetch traces, analyze errors, structure trace review with open coding and axial coding, inspect datasets, review experiments, query a… |
| phoenix-evals | Build and run evaluators for AI/LLM applications using Phoenix. Use this skill when the user asks for quick reference. |
| phoenix-tracing | OpenInference semantic conventions and instrumentation for Phoenix AI observability. Use when implementing LLM tracing, creating custom spans, or deploying to production. |
| php-mcp-server-generator | Generate a complete PHP Model Context Protocol server project with tools, resources, prompts, and tests using the official PHP SDK. Use this skill when the user asks for project r… |
| pinecone-rag | Build production RAG pipelines and persistent agent memory using Pinecone as the vector database backend. ALWAYS USE THIS SKILL when the user mentions Pinecone, wants to index doc… |
| planning-oracle-to-postgres-migration-integration-testing | Creates an integration testing plan for .NET data access artifacts during Oracle-to-PostgreSQL database migrations. Analyzes a single project to identify repositories, DAOs, and s… |
| plantuml-ascii | Generate ASCII art diagrams using PlantUML text mode. Use when user asks to create ASCII diagrams, text-based diagrams, terminal-friendly diagrams, or mentions plantuml ascii, tex… |
| playwright-automation-fill-in-form | Automate filling in a form using Playwright MCP. Use this skill when the user asks for automating filling in a form with playwright mcp. |
| playwright-explore-website | Website exploration for testing using Playwright MCP. Use this skill when the user asks for website exploration for testing. |
| playwright-generate-test | Generate a Playwright test based on a scenario using Playwright MCP. Use this skill when the user asks for test generation with playwright mcp. |
| postgresql-code-review | PostgreSQL-specific code review assistant focusing on PostgreSQL best practices, anti-patterns, and unique quality standards. Covers JSONB operations, array usage, custom types, s… |
| postgresql-optimization | PostgreSQL-specific development assistant focusing on unique PostgreSQL features, advanced data types, and PostgreSQL-exclusive capabilities. Covers JSONB operations, array types,… |
| power-apps-code-app-scaffold | Scaffold a complete Power Apps Code App project with PAC CLI setup, SDK integration, and connector configuration. Use this skill when the user asks for power apps code apps projec… |
| power-bi-dax-optimization | Comprehensive Power BI DAX formula optimization prompt for improving performance, readability, and maintainability of DAX calculations. Use this skill when the user asks for power… |
| power-bi-model-design-review | Comprehensive Power BI data model design review prompt for evaluating model architecture, relationships, and optimization opportunities. Use this skill when key Findings:; critica… |
| power-bi-performance-troubleshooting | Systematic Power BI performance troubleshooting prompt for identifying, diagnosing, and resolving performance issues in Power BI models, reports, and queries. Use this skill when… |
| power-bi-report-design-consultation | Power BI report visualization design prompt for creating effective, user-friendly, and accessible reports with optimal chart selection and layout design. Use this skill when the u… |
| power-platform-architect | Use this skill when the user needs to transform business requirements, use case descriptions, or meeting transcripts into a technical Power Platform solution architecture, includi… |
| power-platform-mcp-connector-suite | Generate complete Power Platform custom connector with MCP integration for Copilot Studio - includes schema generation, troubleshooting, and validation. Use this skill when the us… |
| powerbi-modeling | Power BI semantic modeling assistant for building optimized data models. Use when working with Power BI semantic models, creating measures, designing star schemas, configuring rel… |
| pr-dashboard | Open a GitHub PR dashboard in the browser. Use when the user asks to see their pull requests, open the PR dashboard, show PRs for a date range, or check PR status. Trigger phrases… |
| pr-screenshots | Embed before/after screenshots and annotated images in pull request descriptions. Use this skill when a PR changes something visible; layout, styling, CSS; charts, dashboards, dat… |
| prd | Generate high-quality Product Requirements Documents (PRDs) for software systems and AI-powered features. Use this skill when starting a new product or feature development cycle;… |
| premium-frontend-ui | Guide Copilot to craft immersive, high-performance web experiences with advanced motion, typography, and architectural polish. Use this skill when the user asks for premium fronte… |
| project-workflow-analysis-blueprint-generator | Comprehensive technology-agnostic prompt generator for documenting end-to-end application workflows. Automatically detects project architecture patterns, technology stacks, and da… |
| prompt-optimizer | Turn any rough prompt, half-formed idea, or task description into a finished, ready-to-send prompt optimized for any LLM model inside a chat interface — NOT the API. Use this skil… |
| publish-to-pages | Publish presentations and web content to GitHub Pages. Converts PPTX, PDF, HTML, or Google Slides to a live GitHub Pages URL. Handles repo creation, file conversion, Pages enablem… |
| pytest-coverage | Run pytest tests with coverage, discover lines missing coverage, and increase coverage to 100%. Use this skill when the user needs help with run pytest tests with coverage, discov… |
| python-azure-iot-edge-modules | Build and operate Python Azure IoT Edge modules with robust messaging, deployment manifests, observability, and production readiness checks. Use this skill when the user asks to c… |
| python-mcp-server-generator | Generate a complete MCP server project in Python with tools, resources, and proper configuration. Use this skill when the user asks for generate python mcp server. |
| python-pypi-package-builder | End-to-end skill for building, testing, linting, versioning, and publishing a production-grade Python library to PyPI. Covers all four build backends (setuptools+setuptools_scm, h… |
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
| repo-story-time | Generate a comprehensive repository summary and narrative story from commit history. Use this skill when the user asks for role. |
| resemble-detect | Deepfake detection and media safety — detect AI-generated audio, images, video, and text, trace synthesis sources, apply watermarks, verify speaker identity, and analyze media int… |
| review-and-refactor | Review and refactor code in your project according to defined instructions. Use this skill when the user asks for role. |
| reviewing-oracle-to-postgres-migration | Identifies Oracle-to-PostgreSQL migration risks by cross-referencing code against known behavioral differences (empty strings, refcursors, type coercion, sorting/collations, UNION… |
| rhino3d-scripts | Authoring and debugging scripts for Rhinoceros 3D (Rhino 8 and later). Use when asked to write RhinoScript (VBScript / .rvb / .vbs), RhinoPython, or RhinoCommon-based scripts; aut… |
| roundup | Generate personalized status briefings on demand. Pulls from your configured data sources (GitHub, email, Teams, Slack, and more), synthesizes across them, and drafts updates in y… |
| roundup-setup | Interactive onboarding that learns your communication style, audiences, and data sources to configure personalized status briefings. Paste in examples of updates you already write… |
| ruby-mcp-server-generator | Generate a complete Model Context Protocol server project in Ruby using the official MCP Ruby SDK gem. Use this skill when the user asks for project generation. |
| ruff-recursive-fix | Run Ruff checks with optional scope and rule overrides, apply safe and unsafe autofixes iteratively, review each change, and resolve remaining findings with targeted edits or user… |
| rust-mcp-server-generator | Generate a complete Rust Model Context Protocol server project with tools, prompts, resources, and tests using the official rmcp SDK. Use this skill when the user asks for project… |
| salesforce-apex-quality | Apex code quality guardrails for Salesforce development. Enforces bulk-safety rules (no SOQL/DML in loops), sharing model requirements, CRUD/FLS security, SOQL injection preventio… |
| salesforce-component-standards | Quality standards for Salesforce Lightning Web Components (LWC), Aura components, and Visualforce pages. Covers SLDS 2 compliance, accessibility (WCAG 2.1 AA), data access pattern… |
| salesforce-flow-design | Salesforce Flow architecture decisions, flow type selection, bulk safety validation, and fault handling standards. Use this skill when designing or reviewing Record-Triggered, Scr… |
| sandbox-npm-install | Install npm packages in a Docker sandbox environment. Use this skill whenever you need to install, reinstall, or update node_modules inside a container where the workspace is moun… |
| scaffolding-oracle-to-postgres-migration-test-project | Scaffolds an xUnit integration test project targeting Oracle in .NET solutions. Creates the test project, transaction-rollback base class, and seed data manager. Use only during P… |
| scoutqa-test | This skill should be used when the user asks to "test this website", "run exploratory testing", "check for accessibility issues", "verify the login flow works", "find bugs on this… |
| screen-recording | Create annotated animated GIF demos and screen recordings for pull requests and documentation. Use this skill when you need to; record a multi-step UI interaction as an animated G… |
| secret-scanning | Guide for configuring and managing GitHub secret scanning, push protection, custom patterns, and secret alert remediation. For pre-commit secret scanning in AI coding agents via t… |
| security-review | AI-powered codebase security scanner that reasons about code like a security researcher — tracing data flows, understanding component interactions, and catching vulnerabilities th… |
| semantic-kernel | Create, update, refactor, explain, or review Semantic Kernel solutions using shared guidance plus language-specific references for .NET and Python. Use this skill when always grou… |
| server-side-conversion-tracking | Set up server-side conversion tracking so purchases are reported accurately to Facebook, TikTok, Google and Bing despite iOS restrictions, ad blockers and cookie loss. Use when co… |
| setup-my-iq | Create, set up, or update the personal context portfolio: structured markdown files describing who you are, how you work, your teams, and your tool/ADO configuration. Runs the int… |
| shopify-review-triage | Use this skill when someone wants public Shopify App Store reviews, low-star reviews, or merchant feedback triaged, prioritized, clustered, or turned into a product or support bri… |
| shuffle-json-data | Shuffle repetitive JSON objects safely by validating schema consistency before randomising entries. Use this skill when the user asks for role. |
| signal-write | Emit structured agent signals — hands-up, blocked, done, checkpoint, partnership. Signals are written as JSON to .signals/ for dashboard consumption and noted in the journal for p… |
| slang-shader-engineer | Use when working with Slang shaders, shader modules, HLSL-compatible GPU code, graphics pipelines, compute shaders, tessellation, ray tracing, parameter blocks, generics, interfac… |
| snowflake-semanticview | Create, alter, and validate Snowflake semantic views using Snowflake CLI (snow). Use when asked to build or troubleshoot semantic views/semantic layer definitions with CREATE/ALTE… |
| sponsor-finder | Find which of a GitHub repository's dependencies are sponsorable via GitHub Sponsors. Uses deps.dev API for dependency resolution across npm, PyPI, Cargo, Go, RubyGems, Maven, and… |
| spring-boot-testing | Expert Spring Boot 4 testing specialist that selects the best Spring Boot testing techniques for your situation with Junit 6 and AssertJ. Use this skill when the user asks for cor… |
| sql-code-review | Universal SQL code review assistant that performs comprehensive security, maintainability, and code quality analysis across all SQL databases (MySQL, PostgreSQL, SQL Server, Oracl… |
| sql-optimization | Universal SQL performance optimization assistant for comprehensive query tuning, indexing strategies, and database performance analysis across all SQL databases (MySQL, PostgreSQL… |
| sql-server-table-reconciliation | Use when: comparing SQL Server tables across instances, data migration validation, ETL verification, row mismatch detection, schema drift, reconciliation report, production vs sta… |
| ssma-console | Use when: SSMA console operations — create project, generate assessment report, convert schema, migrate data, Oracle to SQL Server migration, schema conversion, data migration |
| steno-mode | Shorthand-first response compression that cuts ~40% of response tokens while preserving technical precision and exact literals. Use when the user says "steno mode", "shorthand mod… |
| structured-autonomy-generate | Structured Autonomy Implementation Generator Prompt. Use this skill when the user asks for step 1: parse plan & research codebase. |
| structured-autonomy-implement | Structured Autonomy Implementation Prompt. Use this skill when the user needs help with structured Autonomy Implementation Prompt. |
| structured-autonomy-plan | Structured Autonomy Planning Prompt. Use this skill when the user asks for step 1: research and gather context. |
| suggest-awesome-github-copilot-agents | Suggest relevant GitHub Copilot Custom Agents files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing cus… |
| suggest-awesome-github-copilot-instructions | Suggest relevant GitHub Copilot instruction files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing instr… |
| suggest-awesome-github-copilot-skills | Suggest relevant GitHub Copilot skills from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing skills in this r… |
| swift-mcp-server-generator | Generate a complete Model Context Protocol server project in Swift using the official MCP Swift SDK package. Use this skill when the user asks for project generation. |
| system-commandline-cli | Use this skill when adding, modifying, or reviewing CLI commands in a .NET project built with System.CommandLine. Triggers include: creating a new CLI command, adding options or a… |
| technical-job-search | Use this skill when a software engineer asks for help with job search tasks: parsing or analyzing a job description, tailoring a CV/resume, writing a cover letter, evaluating a jo… |
| technology-stack-blueprint-generator | Comprehensive technology stack blueprint generator that analyzes codebases to create detailed architectural documentation. Automatically detects technology stacks, programming lan… |
| terraform-azurerm-set-diff-analyzer | Analyze Terraform plan JSON output for AzureRM Provider to distinguish between false-positive diffs (order-only changes in Set-type attributes) and actual resource changes. Use wh… |
| threat-model-analyst | Full STRIDE-A threat model analysis and incremental update skill for repositories and systems. Supports two modes: (1) Single analysis — full STRIDE-A threat model of a repository… |
| tiny-stepping | Incremental development workflow that makes the smallest meaningful change per step and pauses for feedback, so the direction gets validated early before continuing. Use for caref… |
| tldr-prompt | Create tldr summaries for GitHub Copilot files (prompts, agents, instructions, collections), MCP servers, or documentation from URLs and queries. Use this skill when by frequency;… |
| tm7-threat-model | Creates valid Microsoft Threat Modeling Tool (.tm7) files compatible with the Microsoft Threat Modeling Tool v7.3+. Use this skill whenever asked to create, generate, or modify a… |
| transloadit-media-processing | Process media files (video, audio, images, documents) using Transloadit. Use when asked to encode video to HLS/MP4, generate thumbnails, resize or watermark images, extract audio,… |
| typescript-mcp-server-generator | Generate a complete MCP server project in TypeScript using the MCP TypeScript SDK v2 (@modelcontextprotocol/server) with tools, resources, and proper configuration. Use this skill… |
| typespec-api-operations | Add GET, POST, PATCH, and DELETE operations to a TypeSpec API plugin with proper routing, parameters, and adaptive cards. Use this skill when the user asks for add typespec api op… |
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
| verify-agent-action | Review a proposed AI-agent action or human-approval packet before execution. Use when an agent wants to run a consequential tool, command, deployment, message, purchase, credentia… |
| vscode-ext-commands | Guidelines for contributing commands in VS Code extensions. Use this skill when you need to; add or update commands to your VS Code extension. |
| vscode-ext-localization | Guidelines for proper localization of VS Code extensions, following VS Code extension development guidelines, libraries and good practices. Use this skill when you need to; locali… |
| web-design-reviewer | This skill enables visual inspection of websites running locally or remotely to identify and fix design issues. Triggers on requests like "review website design", "check the UI",… |
| webapp-testing | Toolkit for interacting with and testing local web applications using Playwright. Use this skill when you need to; test frontend functionality in a real browser; verify UI behavio… |
| webmcpify | Make a web app agent-ready — propose a WebMCP tool manifest, integrate, verify in a real browser, heal; unrelated code stays untouched. Use for "webmcpify", "add WebMCP", or "expo… |
| what-context-needed | Ask Copilot what files it needs to see before answering a question. Use this skill when the user asks for what context do you need?. |
| winmd-api-search | Find and explore Windows desktop APIs. Use when building features that need platform capabilities — camera, file access, notifications, UI controls, AI/ML, sensors, networking, et… |
| winui3-migration-guide | UWP-to-WinUI 3 migration reference. Maps legacy UWP APIs to correct Windows App SDK equivalents with before/after code snippets. Covers namespace changes, threading (CoreDispatche… |
| workiq-copilot | Guides the Copilot CLI on how to use the WorkIQ CLI/MCP server to query Microsoft 365 Copilot data (emails, meetings, docs, Teams, people) for live context, summaries, and recomme… |
| workshop-create | Create a new workshop or use an existing directory as one. Handles two paths: (A) use an existing local directory the operator points at, or (B) create a new private GitHub repo i… |
| write-coding-standards-from-file | Write a coding standards document for a project using the coding styles from the file(s) and/or folder(s) passed as arguments in the prompt. Use this skill when the user asks for… |
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
