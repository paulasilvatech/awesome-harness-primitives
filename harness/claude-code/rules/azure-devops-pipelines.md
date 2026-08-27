---
paths:
  - "**/azure-pipelines.yml"
  - "**/azure-pipelines*.yml"
  - "**/*.pipeline.yml"
---

<!-- Generated from harness/github-copilot/instructions/azure-devops-pipelines.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Azure DevOps Pipeline YAML conventions for structure, triggers, variables, security, testing, deployments, templates, caching, and observability.

# Azure DevOps Pipeline YAML Conventions — Reliable CI/CD

These instructions apply to Azure DevOps YAML pipeline definitions, templates, and related pipeline YAML files. They are authoritative for pipeline structure, naming, triggers, variables, security, build/test/deploy flow, templates, performance, and observability; organization-wide Azure DevOps governance, service connection policy, and repository build/test instructions win where they are stricter.

## General Pipeline Design

- Use YAML syntax consistently with 2-space indentation.
- Include meaningful names and display names for pipelines, stages, jobs, and steps.
- Implement error handling and conditional execution deliberately.
- Use variables and parameters for reusable, maintainable pipelines.
- Follow least privilege for service connections and permissions.
- Include comprehensive logging and diagnostics for troubleshooting.
- Organize complex pipelines with stages for visualization and control.
- Use jobs to group related steps and enable parallel execution where appropriate.
- Declare dependencies between stages and jobs explicitly.
- Keep pipeline files focused and modular; split large pipelines into templates or multiple files.

## Build, Test, and Artifacts

| Concern | Convention |
| --- | --- |
| Agent consistency | Use specific agent pool versions and VM images. |
| Caching | Cache dependencies such as npm, NuGet, and Maven to improve performance. |
| Artifacts | Publish artifacts with meaningful names and retention policies. |
| Versioning | Use build variables for version numbers and build metadata. |
| Quality gates | Include linting, testing, and security scans. |
| Reproducibility | Keep builds environment-independent and repeatable. |
| Unit tests | Run unit tests as part of the build process. |
| Test results | Publish standard formats such as JUnit and VSTest. |
| Coverage | Include code coverage reporting and quality gates. |
| Integration/E2E | Run integration and end-to-end tests in appropriate stages. |
| Fail-fast | Fail fast on test failures for quick feedback. |
| Test optimization | Use test impact analysis when available. |

## Security, Variables, and Parameters

- Use Azure Key Vault for sensitive configuration and secrets.
- Manage secrets with variable groups and mark sensitive variables as secrets.
- Use service connections with minimal required permissions.
- Enable dependency vulnerability and static analysis scans.
- Add approval gates for production deployments.
- Use managed identities when possible instead of service principals.
- Use variable groups for shared configuration across pipelines.
- Use runtime parameters for flexible execution.
- Use conditional variables based on branches or environments.
- Document variable purposes and expected values.
- Use variable templates for complex variable logic.
- Never hardcode sensitive values directly in YAML files.

## Deployment Strategy and Environments

Implement environment promotion such as dev → staging → production. Use deployment jobs with environment targeting, blue-green or canary strategies where appropriate, rollback mechanisms, health checks, and infrastructure as code with ARM, Bicep, or Terraform for consistent deployments. Keep configuration management explicit per environment, and protect production with approval gates and health validation.

## Templates, Triggers, and Performance

- Use templates for reusable pipeline components.
- Create pipeline templates for common patterns.
- Use `extends` templates for complete pipeline inheritance.
- Use step templates for reusable task sequences.
- Use variable templates for complex variable logic.
- Version templates appropriately for stability.
- Document template parameters and usage examples.
- Implement appropriate triggers for different branch types.
- Use path filters to trigger builds only when relevant files change.
- Configure CI/CD triggers for main or master branches.
- Use pull request triggers for code validation.
- Use scheduled triggers for maintenance tasks.
- Consider resource triggers for multi-repository scenarios.
- Use parallel jobs and matrix strategies when appropriate.
- Use shallow clone for Git operations when full history is unnecessary.
- Optimize Docker image builds with multi-stage builds and layer caching.
- Monitor pipeline performance and optimize bottlenecks.
- Use pipeline resource triggers efficiently.

## Monitoring and Observability

Include comprehensive logging throughout the pipeline, use Azure Monitor and Application Insights for deployment tracking, implement notifications for failures and successes, include deployment health checks and automated rollback triggers, use pipeline analytics to identify improvement opportunities, and document pipeline behavior and troubleshooting steps.

## Example Structure

```yaml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - docs/*
      - README.md

variables:
  - group: shared-variables
  - name: buildConfiguration
    value: 'Release'

stages:
  - stage: Build
    displayName: 'Build and Test'
    jobs:
      - job: Build
        displayName: 'Build Application'
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: UseDotNet@2
            displayName: 'Use .NET SDK'
            inputs:
              version: '8.x'

          - task: DotNetCoreCLI@2
            displayName: 'Restore dependencies'
            inputs:
              command: 'restore'
              projects: '**/*.csproj'

          - task: DotNetCoreCLI@2
            displayName: 'Build application'
            inputs:
              command: 'build'
              projects: '**/*.csproj'
              arguments: '--configuration $(buildConfiguration) --no-restore'

  - stage: Deploy
    displayName: 'Deploy to Staging'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployToStaging
        displayName: 'Deploy to Staging Environment'
        environment: 'staging'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  displayName: 'Download drop artifact'
                  artifact: drop
                - task: AzureWebApp@1
                  displayName: 'Deploy to Azure Web App'
                  inputs:
                    azureSubscription: 'staging-service-connection'
                    appType: 'webApp'
                    appName: 'myapp-staging'
                    package: '$(Pipeline.Workspace)/drop/**/*.zip'
```

## Anti-Patterns

Avoid hardcoding sensitive values in YAML, overly broad triggers, mixing build and deployment logic in a single stage, missing error handling or cleanup, deprecated task versions without upgrade plans, monolithic pipelines that are difficult to maintain, unclear naming conventions, and ignored pipeline security practices.

## Good / Bad Examples

The examples below illustrate secure variable handling.

**Good:**

```yaml
variables:
  - group: shared-variables
```

Why: Shared and secret values can be managed centrally and protected.

**Bad:**

```yaml
variables:
  sqlPassword: 'P@ssw0rd!'
```

Why: Hardcoded secrets in YAML leak through source control and logs.

## Branch Vocabulary

Treat `main/master` as the legacy branch shorthand for trigger guidance; prefer the repository's actual default branch when configuring CI/CD.


## Conventions

| Rule | Rationale |
| --- | --- |
| Use stages, jobs, dependencies, and display names consistently | Pipeline runs are readable and diagnosable |
| Put shared logic in templates and parameters | Pipelines stay reusable without monolithic YAML |
| Use specific VM images and cache dependencies | Builds remain reproducible and fast |
| Publish tests, coverage, and artifacts in standard formats | Quality signals and release outputs remain visible |
| Store secrets in Key Vault or secret variable groups | Sensitive data stays outside source control |
| Use deployment jobs, environments, approvals, health checks, and rollback | Production releases are controlled and recoverable |
| Use branch, path, PR, scheduled, and resource triggers intentionally | Pipelines run when useful without wasting capacity |
| Add logging, notifications, Azure Monitor, Application Insights, and analytics | Failures and regressions become observable |

## Do / Do Not

| Do | Do not |
| --- | --- |
| Use 2-space YAML indentation | Mix indentation styles |
| Name stages, jobs, and steps clearly | Leave generated or ambiguous labels |
| Use variable groups, runtime parameters, and templates | Hardcode environment-specific values repeatedly |
| Cache npm, NuGet, Maven, and Docker layers where appropriate | Reinstall every dependency from scratch unnecessarily |
| Use service connections with least privilege | Reuse broad production permissions everywhere |
| Split build, test, and deployment concerns | Hide deployment logic inside a generic build stage |
| Version reusable templates | Change shared templates without stability control |

## Checklist Before Opening a PR

- [ ] YAML uses 2-space indentation and meaningful display names.
- [ ] Stages, jobs, dependencies, and conditions model the intended build/test/deploy flow.
- [ ] Variables, runtime parameters, variable groups, and templates avoid duplication and document expected values.
- [ ] Secrets use Azure Key Vault, secret variables, or protected variable groups; no secrets are hardcoded.
- [ ] Build steps use pinned agent images, caching, artifacts, version metadata, and quality gates.
- [ ] Unit, integration, E2E, test results, and coverage publication are included where applicable.
- [ ] Deployment jobs target environments with approvals, health checks, rollback, and IaC where needed.
- [ ] Triggers, path filters, PR validation, schedules, and resource triggers are scoped deliberately.
- [ ] Logging, notifications, Azure Monitor, Application Insights, and troubleshooting documentation are present where needed.
