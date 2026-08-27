---
name: aws-cdk-python-setup
description: >-
  Set up and initialize AWS CDK applications in Python, including prerequisites, credentials,
  project creation, virtual environments, dependencies, synthesis, bootstrap, diff, deploy, and
  troubleshooting. Use this skill when the user asks for AWS CDK Python setup instructions, a new
  CDK Python project, or first deployment guidance.
---

<!-- Generated from harness/github-copilot/skills/aws-cdk-python-setup/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# AWS CDK Python setup

Set up a Python AWS CDK project from prerequisites through first deployment, preserving the expected CDK project layout and validating the local environment before touching AWS resources.

## When to invoke

- "Set up AWS CDK with Python."
- "Create a new CDK Python app."
- "What commands do I run before cdk deploy?"
- "Bootstrap my AWS account for a Python CDK project."
- "Fix AWS CDK Python setup errors."

## Prerequisites and context

| Tool | Minimum or purpose | Check |
| --- | --- | --- |
| Node.js | `>= 14.15.0`; required for the AWS CDK CLI. | `node --version` |
| Python | `>= 3.7`; used for CDK application code. | `python3 --version` |
| AWS CLI | Manages AWS credentials and account/region defaults. | `aws --version` |
| Git | Version control and project management. | `git --version` |
| AWS credentials | Required before `cdk bootstrap`, `cdk diff`, or `cdk deploy`. | `aws sts get-caller-identity` |

## Setup workflow

1. Install and verify the CDK CLI:

   ```bash
   npm install -g aws-cdk
   cdk --version
   ```

2. Configure AWS credentials if `aws sts get-caller-identity` fails:

   ```bash
   brew install awscli
   aws configure
   ```

   Enter the AWS Access Key, Secret Access Key, default region, and output format when prompted. Prefer existing organization credential flows when the project already uses SSO or environment-based credentials.

3. Create the project:

   ```bash
   mkdir my-cdk-project
   cd my-cdk-project
   cdk init app --language python
   ```

4. Activate the generated virtual environment:

   ```bash
   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

5. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Synthesize before deploying:

   ```bash
   cdk synth
   ```

7. Bootstrap once per account/region before first deployment:

   ```bash
   cdk bootstrap
   ```

8. Preview and deploy:

   ```bash
   cdk diff
   cdk deploy
   ```

## Project anatomy

| Path | Purpose |
| --- | --- |
| `app.py` | Main CDK application entry point; instantiates stacks. |
| `my_cdk_project/` | Python package containing stack definitions and constructs. |
| `requirements.txt` | Python dependencies; keep it pinned for consistent builds. |
| `cdk.json` | CDK app command and context configuration. |
| `cdk.out/` | Generated CloudFormation templates from `cdk synth`; do not hand-edit. |

Primary dependencies are `aws-cdk-lib` for core CDK constructs and `constructs` for the base construct library.

## Development rules

| Rule | Why |
| --- | --- |
| Activate `.venv` before working | Ensures `aws-cdk-lib` and project dependencies resolve consistently. |
| Run `cdk synth` before `cdk deploy` | Catches syntax, construct, and context errors without changing AWS. |
| Run `cdk diff` before deployment | Shows IAM, replacement, and destructive changes before confirmation. |
| Use development accounts for testing | Keeps experiments away from production resources. |
| Follow Pythonic naming and directory conventions | Keeps stacks and constructs discoverable. |
| Pin `requirements.txt` | Prevents unreviewed dependency drift. |

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `cdk: command not found` | AWS CDK CLI not installed or global npm bin not on `PATH`. | Run `npm install -g aws-cdk`, then `cdk --version`. |
| `Unable to resolve AWS account` | Credentials or region missing. | Run `aws configure` or the project's SSO flow, then `aws sts get-caller-identity`. |
| `This stack uses assets, so the toolkit stack must be deployed` | Account/region not bootstrapped. | Run `cdk bootstrap` for the target account and region. |
| Python import errors | Virtual environment inactive or dependencies missing. | Run `source .venv/bin/activate` or `.venv\Scripts\activate`, then `pip install -r requirements.txt`. |
| Unexpected deployment changes | Context or construct changes changed synthesized output. | Run `cdk diff` and inspect `cdk.out/` before `cdk deploy`. |
| Environment diagnostics needed | Mixed tool versions or missing configuration. | Run `cdk doctor`. |

## Output template

```markdown
## AWS CDK Python setup result

**Status:** ready | needs credentials | blocked
**Project path:** `<path>`
**Account/region:** `<account or unknown>` / `<region or unknown>`

| Step | Command | Result |
| --- | --- | --- |
| Prerequisites | `<command>` | `<pass/fail>` |
| Project init | `cdk init app --language python` | `<pass/fail/not run>` |
| Dependencies | `pip install -r requirements.txt` | `<pass/fail/not run>` |
| Synthesis | `cdk synth` | `<pass/fail/not run>` |
| Deployment readiness | `cdk diff` / `cdk bootstrap` / `cdk deploy` | `<result>` |

**Next action:** <specific command or blocker>
```

## Quality gate

- [ ] Node.js, Python, AWS CLI, Git, and credentials were checked before deployment commands.
- [ ] The CDK CLI was installed or verified with `cdk --version`.
- [ ] The project uses `cdk init app --language python` and preserves `app.py`, `my_cdk_project/`, `requirements.txt`, and `cdk.json`.
- [ ] The Python virtual environment was activated before installing dependencies.
- [ ] `cdk synth` ran before `cdk diff` or `cdk deploy`.
- [ ] `cdk bootstrap` was run or confirmed for first deployment to the account/region.
- [ ] Troubleshooting guidance names the failing command and the next corrective command.
