# Practice — Building an Architecture Reasoning Agent

In this practice you will build agents from scratch: an engineering team lead chatbot, an architecture reasoning orchestrator, and an RFC writer subagent. The tools and data are provided — your job is to write the agent instructions.

The target codebase is **QPay** (`qpay-multiplatform/`), a fintech app built with Kotlin Multiplatform (KMP) and Compose Multiplatform. It targets Android and iOS from a single shared Kotlin codebase, with Decompose for navigation and Koin for DI.

Two team lead personas are provided — each requests a different platform-native feature. Pick one to start:

| Persona | Directory | Feature requested |
|---------|-----------|-------------------|
| **Priya Malhotra** | `teamlead-android/` | QR code scanner for Scan-to-Pay (Android camera → shared Decompose flow) |
| **Marco Reyes** | `teamlead-ios/` | Biometric auth for payment confirmation (Face ID / Touch ID → shared auth flow) |

---

## Repository layout

```
arch-reasoning-agent-mobile/
├── qpay-multiplatform/                    ← the real codebase under analysis
│   ├── shared/                            ← KMP shared code (commonMain / androidMain / iosMain)
│   │   └── src/commonMain/kotlin/.../
│   │       ├── decompose/                 ← Decompose components (root, home, wallet, qrpay, …)
│   │       ├── ui/screens/                ← Compose Multiplatform screens
│   │       ├── data/                      ← entities + repositories
│   │       └── koin/                      ← shared Koin DI module
│   ├── androidApp/                        ← thin Android shell (MainActivity)
│   └── iosApp/                            ← thin Swift shell (entry point)
│
├── data/
│   ├── context/company.md             ← QPay platform: business context, pain points, constraints
│   ├── adrs/
│   │   ├── ADR-001-database.md        ← minimal ADR (intentionally thin)
│   │   ├── ADR-002-api-design.md      ← well-structured ADR
│   │   └── ADR-003-deployment.md      ← outdated monolith ADR
│   └── diagrams/
│       └── current-architecture.mmd   ← current KMP topology (Mermaid)
│
├── skills/                            ← COMPLETE — do not modify
│   ├── list_adrs/list_adrs.py         ← lists all ADRs as JSON
│   ├── read_adr/read_adr.py           ← reads one ADR by ID
│   ├── write_adr/write_adr.py         ← validates + saves new ADR to output/adrs/
│   └── save_diagram/save_diagram.py   ← validates + saves Mermaid to output/diagrams/
│
├── output/
│   ├── adrs/                          ← agent writes new ADRs here
│   └── diagrams/                      ← agent writes new diagrams here
│
├── teamlead-android/
│   └── CLAUDE.md.template             ← Priya Malhotra: QR scanner / Scan-to-Pay
├── teamlead-ios/
│   └── CLAUDE.md.template             ← Marco Reyes: biometric auth
│
├── .claude/agents/
│   ├── team_lead_android.md.template  ← Priya Malhotra subagent (used by main agent)
│   ├── team_lead_ios.md.template      ← Marco Reyes subagent (used by main agent)
│   └── rfc_writer.md.template         ← Step 4: build the RFC writer subagent
│
├── CLAUDE.md.template                 ← Step 3: build the architecture reasoning agent
└── README.md
```

---

## Step 0 — Setup

Verify the skills work:

```bash
python skills/list_adrs/list_adrs.py
python skills/read_adr/read_adr.py ADR-001
```

Read `data/context/company.md` to understand the scenario, then browse `qpay-multiplatform/shared/src/commonMain/` to see the actual code the agent will reason about.

Key files to read first:
- `qpay-multiplatform/shared/src/commonMain/kotlin/.../decompose/root/QPayRoot.kt` — navigation root
- `qpay-multiplatform/shared/src/commonMain/kotlin/.../decompose/qrpay/QrPayComponent.kt` — existing QR component
- `qpay-multiplatform/shared/src/androidMain/kotlin/.../permissions/CameraPermissionDelegate.kt` — existing camera permission

---

## Step 1 — Build a Team Lead chatbot

Two personas are available. Pick one (or build both for extra practice).

| Persona | Feature | Templates to copy |
|---------|---------|-------------------|
| Priya Malhotra | QR scanner / Scan-to-Pay | `teamlead-android/CLAUDE.md.template` → `teamlead-android/CLAUDE.md`<br>`.claude/agents/team_lead_android.md.template` → `.claude/agents/team_lead_android.md` |
| Marco Reyes | Biometric auth | `teamlead-ios/CLAUDE.md.template` → `teamlead-ios/CLAUDE.md`<br>`.claude/agents/team_lead_ios.md.template` → `.claude/agents/team_lead_ios.md` |

Each persona already has content filled in — the templates are complete, not blank. Read them, then optionally customise before running.

Test the standalone chatbot for your chosen persona:

```bash
cd teamlead-android        # or teamlead-ios
claude
```

**Good opening questions by persona:**
- Priya: *"Where should the camera preview surface live — in `androidApp` or `shared/androidMain`?"*
- Marco: *"If Face ID fails, what exactly should the user see and which layer handles that?"*

The team lead should answer in product/delivery language, push back on KMP boundary violations, and ask clarifying questions when architecture jargon appears.

---

## Step 2 — Read and analyse the existing ADRs

Before building the agent, spend 10 minutes reading the three ADRs in `data/adrs/` manually.

- What was decided and when?
- Which ADR touches the platform abstraction strategy for native APIs?
- What does ADR-003 warn about for shared-code assumptions on platform-specific features?

This shapes the requirements section of your agent.

---

## Step 3 — Build the Architecture Reasoning Agent

This is the main agent. It reads ADRs, explores the QPay codebase, identifies gaps, proposes options, generates diagrams, and writes new ADRs.

1. Copy the template:

```bash
cp CLAUDE.md.template CLAUDE.md
```

2. Fill in every `[TODO]`. Required sections:

| Section | What to write |
|---|---|
| **Your role** | One-sentence identity |
| **Purpose** | Full scope: what the agent reads, analyses, produces |
| **Trigger** | Exact phrases that start the workflow |
| **Workflow** | ≥ 10 numbered steps (see hints in template) |
| **Output format** | Gap analysis table + option structure with costs/risks/timelines |
| **Guardrails** | Must include the ADR write gate and diagram gate |
| **Failure handling** | What to do when each tool or subagent fails |

### Required guardrails

Your `CLAUDE.md` **must** include both of these rules:

> `write_adr` must **not** be called unless the user's message contains **"write adr"**, **"save adr"**, or **"publish"**.

> `save_diagram` must **not** be called before the user has selected a specific option.

3. Run the agent:

```bash
claude          # from the arch-reasoning-agent-mobile/ directory
```

Send: `analyse the architecture`

Confirm it:
- Reads `company.md` and all 3 ADRs
- Browses relevant files in `qpay-multiplatform/shared/`
- Identifies at least 3 architectural gaps related to the feature (KMP boundary, Decompose lifecycle, platform permission reuse)
- Proposes 2–3 options with cost estimates and timelines
- **Waits** — does not call `write_adr` or `save_diagram` yet

4. Drive it through the full flow:
   - Select an option → diagram should be saved to `output/diagrams/`
   - Say `write adr` → ADR should be saved to `output/adrs/`

---

## Step 4 — Add the RFC writer subagent

After the agent writes an ADR, it should produce a complete RFC document that combines everything: requirements, architecture, ADRs, diagram, and migration plan.

1. Copy the template:

```bash
cp .claude/agents/rfc_writer.md.template .claude/agents/rfc_writer.md
```

2. Fill in every `[TODO]`:

| Section | What to write |
|---|---|
| **Your role** | One-sentence identity |
| **Purpose** | What document it produces and who reads it |
| **RFC sections** | Ordered list of ≥ 8 sections the RFC must contain |
| **Output format** | How each section is structured |
| **Guardrails** | What the RFC writer must never do |

3. Update your `CLAUDE.md` to invoke `rfc_writer` after the ADR is written. The subagent receives:
   - Full company context
   - All ADR content (existing + new)
   - The selected architecture option
   - Diagram path in `output/diagrams/`
   - Requirements summary from the team lead session

4. Re-run the full workflow and verify `output/rfc.md` is created.

---

## Setting up the Mermaid diagram plugin

The architecture agent can render and live-preview Mermaid diagrams in your browser using the **claude-mermaid** Claude Code plugin. This is optional but recommended — without it the agent can still write `.mmd` files, but you won't get live previews.

### 1. Register the marketplace source

Add the following to your **user-level** Claude Code settings (`~/.claude/settings.json`). Create the file if it doesn't exist; merge with your existing config if it does.

```json
{
  "extraKnownMarketplaces": {
    "claude-mermaid": {
      "source": {
        "source": "github",
        "repo": "veelenga/claude-mermaid"
      }
    }
  }
}
```

### 2. Install the plugin

Open Claude Code (any project) and run:

```
/plugin install claude-mermaid
```

### 3. Enable the plugin

The install command enables the plugin automatically. Verify it is active by checking that `~/.claude/settings.json` contains:

```json
"enabledPlugins": {
  "claude-mermaid@claude-mermaid": true
}
```

### 4. Verify it works

From this project's root directory, open Claude Code and ask:

```
draw a simple mermaid flowchart with three boxes
```

A browser tab should open with a live-preview of the diagram.

### Permissions

The `.claude/settings.json` in this repo already pre-approves the two mermaid tool calls (`mermaid_preview` and `mermaid_save`) so you will not be prompted to allow them during the exercise.

---

## Submission checklist

- [ ] At least one team lead `CLAUDE.md` exists in `teamlead-android/` or `teamlead-ios/`
- [ ] Matching `.claude/agents/team_lead_android.md` or `team_lead_ios.md` file exists
- [ ] Team lead chatbot responds in delivery/product language (test: propose something that crosses the KMP boundary — they should push back)
- [ ] `CLAUDE.md` exists — no `[TODO]` tokens remain
- [ ] ADR write gate present in `CLAUDE.md`
- [ ] Diagram gate present in `CLAUDE.md`
- [ ] Agent reads all 3 ADRs and browses `qpay-multiplatform/shared/` before proposing options
- [ ] Agent presents 2–3 options and **waits** before writing anything
- [ ] `output/diagrams/` contains a generated diagram
- [ ] `output/adrs/` contains a generated ADR
- [ ] `.claude/agents/rfc_writer.md` exists — no `[TODO]` tokens remain
- [ ] `output/rfc.md` exists after full workflow run

---

## Tips

- Read `data/context/company.md` carefully — your agent's gap analysis should map directly to the KMP architectural constraints described there, especially the shared vs platform-specific code boundary.
- Browse `qpay-multiplatform/shared/src/commonMain/` and `androidMain/` — the agent should reason about what the real code actually does, not just the company doc.
- The write gate is the most important guardrail. Test that the agent does **not** call `write_adr` when you say "looks good" or "I approve".
- If the agent skips a step, add more explicit ordering language to the workflow section ("do not proceed to step N until step N-1 is complete").
- For Cursor or Windsurf: use the same template content, saved to `.cursor/rules/architecture-agent.mdc` or `.windsurfrules` respectively. For the Team Lead, open `teamlead-android/` or `teamlead-ios/` as a separate workspace root.
