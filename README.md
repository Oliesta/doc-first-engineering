# Doc-First Engineering

**Documentation is the source of truth. LLMs write the code. Humans own the decisions.**

A standard, and a Claude skill that applies it, for building software when large language models write most of the code.

Every layer of software has moved humans further from the machine: binary, assembly, programming languages, and now LLMs. Each layer below the LLM is deterministic. The LLM is not. So the durable human work moves up a layer, into documentation that defines intent, records decisions and makes correctness checkable.

> We cannot see the future, but we can prepare for it.

## What is in this repository

| Path | What it is |
|---|---|
| [`plugins/doc-first-engineering/skills/doc-first-engineering/SKILL.md`](plugins/doc-first-engineering/skills/doc-first-engineering/SKILL.md) | The skill: how Claude applies the standard |
| [`plugins/doc-first-engineering/skills/doc-first-engineering/references/standard.md`](plugins/doc-first-engineering/skills/doc-first-engineering/references/standard.md) | The full standard, Version 1.1 |
| [`docs/Doc_First_Engineering_Standard_v1.1.pdf`](docs/Doc_First_Engineering_Standard_v1.1.pdf) | The standard as a phone-friendly PDF |
| [`dist/doc-first-engineering.zip`](dist/doc-first-engineering.zip) | The skill packaged for upload to the Claude app |
| [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | Lets Claude Code install the skill as a plugin |

## What the skill does

Once installed, Claude follows the standard whenever you:

- **Change code or infrastructure.** Claude reads the relevant docs first and follows Define, Decide, Generate, Verify, Reconcile. Every change comes with a doc update or an explicit `No doc impact, because...`.
- **Debug an environment.** Claude treats the runbook and environment guide as the source of truth and turns them into exact, read-only commands with explicit profile, region and context. It labels anything that changes state, asks rather than guessing resource names, and never runs commands against shared environments.
- **Prepare for failure.** For a new component or decision, Claude offers a pre-mortem and drafts runbook failure mode entries before go-live.
- **Write or review docs.** ADRs with review triggers, Rule IDs, repository-relative hyperlinks, a review checklist, and six templates: ADR, domain rules, change description, bug record, failure mode entry and environment guide.

## Install

### Claude Code (as a plugin)

In a Claude Code session:

```text
/plugin marketplace add Oliesta/doc-first-engineering
/plugin install doc-first-engineering@doc-first-engineering
```

Or from your shell:

```bash
claude plugin install doc-first-engineering --marketplace Oliesta/doc-first-engineering
```

### Claude Code (as a plain skill)

Copy the skill folder into your personal or project skills directory:

```bash
# Personal, all projects
cp -r plugins/doc-first-engineering/skills/doc-first-engineering ~/.claude/skills/

# One project, shared with your team
cp -r plugins/doc-first-engineering/skills/doc-first-engineering .claude/skills/
```

### Claude app (claude.ai, desktop, mobile)

Download [`dist/doc-first-engineering.zip`](dist/doc-first-engineering.zip), then upload it in the Claude app's skills settings.

## The standard in one page

**Core thesis.** Code becomes a derived artifact. Documentation becomes the source.

**The mapping is layered, not line by line.** Decision or rule, to implementation, to test or validation. Detail below that level belongs to the LLM and is judged by behaviour.

**Principles**

1. Documentation is the source of truth.
2. Change starts in documentation.
3. Record decisions, not just descriptions.
4. Every rule is verifiable.
5. Structure is consistent.
6. Every bug is classified: Decision Wrong, Doc Missing, Code Diverged or Environment.
7. Archive, do not delete.
8. Humans stay accountable.
9. One fact, one place.
10. Documentation has two readers: humans and LLMs.
11. Prepare before it breaks.

**Adoption levels:** Documented, Decided, Doc-Led, Traceable, Source of Truth. Most teams reach Doc-Led quickly.

Read the [full standard](plugins/doc-first-engineering/skills/doc-first-engineering/references/standard.md) or the [PDF](docs/Doc_First_Engineering_Standard_v1.1.pdf).

## Contributing

Issues and pull requests are welcome. This repository follows its own standard:

- Change the standard first, then the skill.
- Describe each change with the Change Description template (Appendix C of the standard).
- After changing the skill, run `scripts/build-skill-zip.sh` and update [`CHANGELOG.md`](CHANGELOG.md).

## License

- **The standard** (the full standard in Markdown and the PDF): [CC BY 4.0](LICENSE-DOCS). Share and adapt it freely with attribution.
- **Everything else** (the skill, plugin manifests and scripts): [MIT](LICENSE).
