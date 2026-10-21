---
name: "doc-first-engineering"
description: "Apply the Doc-First Engineering Standard when changing code or Terraform, writing ADRs, rules or runbooks, reviewing changes, or debugging an environment from its docs."
---

# Doc-First Engineering

Documentation is the source of truth. Code is a derived artifact. Humans own the why and the what; you own the how. A human approves every change and owns every decision.

Motto for operations: **We cannot see the future, but we can prepare for it.**

## Before any task

1. Find the docs. Look for `docs/` and read what applies: `docs/README.md`, the relevant `docs/domains/<domain>/rules.md`, ADRs in `docs/architecture/decision-records/`, `docs/standards/`, and for infrastructure `docs/architecture/infrastructure.md`, `docs/operations/runbook.md` and `docs/operations/environments/<env>.md`.
2. If the repo has no docs structure, say so and offer to scaffold it (see Repository layout) before writing code.
3. If code and docs disagree, do not silently pick one. Report the disagreement and ask which is correct. Docs win until a human decides otherwise.

## Making a change (code or infrastructure)

Follow the five steps in order, even for a one-line fix:

1. **Define.** Update or propose the rule, requirement or acceptance criteria in the relevant doc first.
2. **Decide.** If the change is a real choice between alternatives, or affects architecture, security, availability, cost, networking or operational ownership, draft an ADR or name the existing ADR that still holds. Check the ADR's Review Trigger before contradicting it.
3. **Generate.** Implement following the docs and standards.
4. **Verify.** Add or update tests or validation. Name tests after Rule IDs where possible. Check the change against the docs.
5. **Reconcile.** Fix any gap in docs or code, update links and `docs/CHANGELOG.md`.

Every change MUST include a doc update, or the explicit line: `No doc impact, because <reason>`. Write a change description using the Change Description template.

If code had to lead (incident, experiment), list the doc reconciliation as a follow-up with an owner.

### Structure rules

- Domain code: `src/<domain>/{api,application,domain,infrastructure}`. Never reach into another domain's `domain/` or `infrastructure/`; use a published interface or event.
- Terraform: shared logic only in `infrastructure/terraform/modules/<module>/`. `infrastructure/terraform/environments/<env>/` holds composition and variables only. Environments differ by variable, never by copied code.
- Each module and environment directory has a `README.md`. Docker files live in `infrastructure/docker/`.
- Procedures go in the runbook, not as undocumented steps beside Terraform.
- Superseded docs move to `docs/archive/`, marked superseded with a link to the replacement. Never delete reasoning.

## Writing docs

- Use MUST, MUST NOT, SHOULD, MAY in capitals for rules.
- Give each rule a Rule ID (for example `ALLOC-003`) and list it in the domain's `rules.md` with its owning module and test.
- One fact, one place. Link instead of restating.
- Examples over adjectives: valid and invalid inputs. State negative rules. Cover edge cases: empty, duplicate, concurrent, expired, unauthorised.
- Replace vague words (fast, secure, appropriate, as needed) with numbers or conditions.
- Use repository-relative Markdown links with descriptive text, never "click here", local paths or line numbers. Compute `../` from the linking file's own location and verify the target exists.
- ADRs MUST link to affected docs, modules and environments. ADR numbers are never reused or renumbered. Accepted ADRs are not edited in substance; a changed decision gets a new superseding ADR. Keep each ADR to one decision.
- When files move, update every link in the same change. A broken link is a defect.

Traceability chain links should let a reader walk: Decision or Rule, Architecture doc, Implementation (domain or Terraform module), Environment configuration, Test or validation, Operations standard and Runbook.

## Debugging and incidents

The runbook and environment guide are your source of truth. Turn them into exact, ready-to-run commands so the human does not type or look them up.

Investigation loop:

1. **Describe.** Get the symptom, environment and time window. Ask if missing.
2. **Ground.** Read the runbook, the environment guide and relevant ADRs. Check known failure modes first.
3. **Propose.** Give read-only commands, each with a one-line reason, using exact names from the docs.
4. **Run.** The human runs them and pastes output back.
5. **Narrow.** Compare evidence with documented behaviour and failure modes; propose the next step.
6. **Decide.** The human chooses the fix.
7. **Record.** Draft the runbook update: new failure mode and the commands that found it.

Classify every bug, and get the human to confirm:

- **Decision Wrong:** docs followed, decision wrong. Fix: superseding ADR, then docs and code.
- **Doc Missing:** behaviour never specified. Fix: add rule and edge case, then code.
- **Code Diverged:** docs right, code wrong. Fix: code plus the missing test.
- **Environment:** config, data, infrastructure or dependency. Fix: environment or module, then environment guide and runbook.

Docs show intended behaviour only. Always ask for runtime evidence: logs, traces, request IDs, data state.

### Safety rules (non-negotiable)

- Read before write: start with describe, get, logs, list.
- Label any command that restarts, scales, deletes, rotates or modifies as a **CHANGE** and explain its effect before it runs.
- Propose commands; do not run them against shared environments.
- Every command names its profile, region and cluster context explicitly.
- Never invent resource names. If a name is not in the docs, ask.
- Never request or repeat secret values; ask the human to redact credentials, tokens and personal data.
- Production changes follow the change process, not the investigation loop.

## Preparing proactively

When adding a component, module, integration or ADR, answer before go-live and add to the runbook:

1. How can this fail?
2. How will we know?
3. What do we run first?

Offer a pre-mortem: read the architecture docs and ADRs, list realistic failure modes, and draft diagnostic commands from the environment guide for a human to check in a non-production environment. Treat near misses like incidents.

## Reviewing a change

Check: intent matches the updated docs and nothing more; docs updated or "no doc impact" justified; affected Rule IDs have tests; domain, layer and module boundaries respected; standards followed; links correct; environment impact confined to variables; no surprises (new dependencies, files outside the layout, unrequested code).

Flag for a second human reviewer: authentication, authorisation, secrets, IAM, encryption, personal or regulated data, migrations, irreversible operations, financial or identity logic, concurrency, transactions, idempotency, networking, public exposure, production infrastructure.

## Repository layout

```text
docs/
  README.md  CHANGELOG.md
  context/overview.md  context/glossary.md
  architecture/architecture.md  infrastructure.md  security.md
  architecture/decision-records/ADR-NNN-<title>.md
  domains/<domain>/rules.md  acceptance.md
  api/specification.md  openapi.yaml
  database/conventions.md
  standards/coding.md  infrastructure.md  testing.md
  operations/operations-standard.md  runbook.md
  operations/environments/<env>.md
  operations/incidents/
  archive/
infrastructure/
  terraform/environments/<env>/README.md
  terraform/modules/<module>/README.md
  docker/
src/<domain>/api|application|domain|infrastructure
```

Operations standard says what must happen; runbook says how; environment guides hold the facts.

## Templates

### ADR

```md
# ADR-NNN: <title>
Status: Proposed | Accepted | Superseded by ADR-XXX | Deprecated
Date: YYYY-MM-DD
Owner: <name>
## Context
## Decision
<one or two sentences>
## Alternatives
- <option>: rejected because <why>
## Consequences
- Easier: / Harder:
## Rules
- <ID>: <MUST / MUST NOT rule>
## Review Trigger
## References
- Documentation / Modules / Environments: <Markdown links>
- Tests or validation: <names>
```

### Domain rules

```md
# <Domain> Rules
## Responsibility
## Invariants
- <ID>: <always true>
## Rules
- <ID>: <rule>
  Valid: <example>  Invalid: <example>
## Edge Cases
## Acceptance Criteria
## Rule Ownership
| Rule ID | Module | Test |
## Owner
```

### Change description

```md
## Change
## Docs Updated
- <file>: <what changed>  | No doc impact, because <...>
## Rules Affected
## Decision
ADR-NNN still holds | New ADR-NNN
## Environments Affected
## Links Updated
Yes | Not applicable
## Verification
- Tests or validation:
- Reviewer:  Second reviewer (if required):
```

### Bug record

```md
## Bug
## Environment and Time Window
## Classification
Decision Wrong | Doc Missing | Code Diverged | Environment
## Rules Involved
## Commands Run
## Fix
## Test or Validation Added
## Documentation and Links Updated
## Runbook Updated
```

### Failure mode entry (runbook)

```md
## <Failure mode>
Component: <...>  Environments: <...>
### Symptom
### Likely Causes
### Diagnose (read-only)
<exact commands with profile, region, context>
### Fix
<label every mutating command as a CHANGE>
### Prevention
### History
- <date>: <incident or near miss link>
```

### Environment guide

```md
# <Env> Environment Guide
## Purpose
## Access
Account / Region / CLI profile / Cluster context / Namespaces
## Resources
| Type | Name |
## Secrets (names and locations only, never values)
| Name | Location | Sync method |
## Dependencies
## Safe and Unsafe Operations
## Links
- [Terraform Environment](<path>)  - [Runbook](<path>)
```

## Full standard

The complete Doc-First Engineering Standard (rationale, roles, risks, adoption levels, glossary and full templates) is in [references/standard.md](references/standard.md). Read it when a user asks why a rule exists, wants to adopt the standard in a new repository, or needs a template in full.

## Style

No em dashes. Short sentences. Exact names. When unsure whether a fact is documented, check the docs, then ask.