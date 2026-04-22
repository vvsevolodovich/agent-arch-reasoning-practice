# Practice — Building an Architecture Reasoning Agent

In this practice you will build agents from scratch: an engineering team lead chatbot, an architecture reasoning orchestrator, and an RFC writer subagent. The tools and data are provided — your job is to write the agent instructions.

The target codebase is the **Conduit RealWorld** app (`conduit-realworld-example-app/`), a Medium-clone with a Node.js/Express backend, Sequelize + PostgreSQL, and a React/Vite frontend.

Three team lead personas are provided — each requests a different feature. Pick one to start:

| Persona | Directory | Feature requested |
|---------|-----------|-------------------|
| **Alex Chen** | `team-lead/` | Real-time collaborative article editing (WebSockets + OT) |
| **Marcus Webb** | `team-lead-2/` | AI-powered personalized article feed (recommendation engine) |
| **Priya Sharma** | `team-lead-3/` | Premium subscription paywall + writer revenue share (Stripe) |

---

## Repository layout

```
arch-reasoning-agent-practice/
├── conduit-realworld-example-app/         ← the real codebase under analysis
│   ├── backend/                           ← Express + Sequelize + PostgreSQL
│   └── frontend/                          ← React + Vite SPA
│
├── data/
│   ├── context/company.md             ← Conduit platform: business context, pain points, constraints
│   ├── adrs/
│   │   ├── ADR-001-database.md        ← minimal ADR (intentionally thin)
│   │   ├── ADR-002-api-design.md      ← well-structured ADR
│   │   └── ADR-003-deployment.md      ← outdated monolith ADR
│   └── diagrams/
│       └── current-architecture.mmd   ← current single-VPS topology (Mermaid)
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
├── team-lead/
│   └── CLAUDE.md.template             ← Alex Chen: real-time collaboration
├── team-lead-2/
│   └── CLAUDE.md.template             ← Marcus Webb: AI personalized feed
├── team-lead-3/
│   └── CLAUDE.md.template             ← Priya Sharma: premium subscriptions
│
├── .claude/agents/
│   ├── team_lead.md.template          ← Alex Chen subagent (used by main agent)
│   ├── team_lead_2.md.template        ← Marcus Webb subagent (used by main agent)
│   ├── team_lead_3.md.template        ← Priya Sharma subagent (used by main agent)
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

Read `data/context/company.md` to understand the scenario, then browse `conduit-realworld-example-app/backend/` to see the actual code the agent will reason about.

---

## Step 1 — Build a Team Lead chatbot

Three personas are available. Pick one (or build all three for extra practice).

| Persona | Feature | Templates to copy |
|---------|---------|-------------------|
| Alex Chen | Real-time collab editing | `team-lead/CLAUDE.md.template` → `team-lead/CLAUDE.md`<br>`.claude/agents/team_lead.md.template` → `.claude/agents/team_lead.md` |
| Marcus Webb | AI personalized feed | `team-lead-2/CLAUDE.md.template` → `team-lead-2/CLAUDE.md`<br>`.claude/agents/team_lead_2.md.template` → `.claude/agents/team_lead_2.md` |
| Priya Sharma | Premium subscriptions | `team-lead-3/CLAUDE.md.template` → `team-lead-3/CLAUDE.md`<br>`.claude/agents/team_lead_3.md.template` → `.claude/agents/team_lead_3.md` |

Each persona already has content filled in — the templates are complete, not blank. Read them, then optionally customise before running.

Test the standalone chatbot for your chosen persona:

```bash
cd team-lead        # or team-lead-2 / team-lead-3
claude
```

**Good opening questions by persona:**
- Alex: *"What exactly should two writers be able to do at the same time?"*
- Marcus: *"What data do you have today that a recommendation engine could use?"*
- Priya: *"What happens if we charge a reader and the server crashes before we record it?"*

The team lead should answer in product/delivery language and push back when proposals sound complex or slow to ship.

---

## Step 2 — Read and analyse the existing ADRs

Before building the agent, spend 10 minutes reading the three ADRs in `data/adrs/` manually.

- What was decided and when?
- Which ADR explicitly flags that real-time features need a different transport layer?
- What does ADR-003 warn about for multi-process WebSocket deployments?

This shapes the requirements section of your agent.

---

## Step 3 — Build the Architecture Reasoning Agent

This is the main agent. It reads ADRs, identifies gaps, proposes options, generates diagrams, and writes new ADRs.

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
claude          # from the arch-reasoning-agent-practice/ directory
```

Send: `analyse the architecture`

Confirm it:
- Reads `company.md` and all 3 ADRs
- Identifies at least 3 architectural gaps related to the real-time collaboration feature
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

## Submission checklist

- [ ] At least one team lead `CLAUDE.md` exists in `team-lead/`, `team-lead-2/`, or `team-lead-3/`
- [ ] Matching `.claude/agents/team_lead*.md` file exists for your chosen persona
- [ ] Team lead chatbot responds in delivery/product language (test: propose something complex — they should push back on scope or timeline)
- [ ] `CLAUDE.md` exists — no `[TODO]` tokens remain
- [ ] ADR write gate present in `CLAUDE.md`
- [ ] Diagram gate present in `CLAUDE.md`
- [ ] Agent reads all 3 ADRs before proposing options
- [ ] Agent presents 2–3 options and **waits** before writing anything
- [ ] `output/diagrams/` contains a generated diagram
- [ ] `output/adrs/` contains a generated ADR
- [ ] `.claude/agents/rfc_writer.md` exists — no `[TODO]` tokens remain
- [ ] `output/rfc.md` exists after full workflow run

---

## Tips

- Read `data/context/company.md` carefully — your agent's gap analysis should map directly to the pain points described there, especially the single-VPS constraint that affects WebSocket scaling.
- Browse `conduit-realworld-example-app/backend/` — the agent should be able to reason about what the real code actually does, not just the company doc.
- The write gate is the most important guardrail. Test that the agent does **not** call `write_adr` when you say "looks good" or "I approve".
- If the agent skips a step, add more explicit ordering language to the workflow section ("do not proceed to step N until step N-1 is complete").
- For Cursor or Windsurf: use the same template content, saved to `.cursor/rules/architecture-agent.mdc` or `.windsurfrules` respectively. For the Team Lead, open `team-lead/` as a separate workspace root.
