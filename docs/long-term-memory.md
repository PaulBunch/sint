<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Long-term Autonomous Memory for Serious Engineering Projects

**Version:** 2026-08-31  
**Project:** sint  
**Goal:** Enable continuous evolution of an LLM agent (or team of agents) over months/years while working on a complex physical/software project (example: development of a robotic interface for real-world interaction).

## 1. Fundamental Principles (2026)

1. **External memory is more important than internal weights**  
   At the current stage of technology it is more reliable to keep experience outside the model than to constantly try to bake it in via fine-tuning.

2. **Hybrid memory wins**  
   Vector search + knowledge graph + hierarchical summarization + episodic logs.

3. **Code and structured artifacts are the most reliable memory**  
   Git + clear Markdown documents + ADR (Architecture Decision Records) often work better than any fancy memory system.

4. **Consolidation is mandatory**  
   The model should not “remember everything”. It should remember **conclusions** and have fast access to details on demand.

5. **The human remains the architect**  
   Fully autonomous evolution on a months-long horizon is still unreliable. The human sets direction, validates key decisions, and maintains memory hygiene.

6. **Transparency over opacity**  
   Agent working notes are allowed and encouraged, but must remain human-readable. Deliberately opaque, encrypted, or steganographic records are not permitted.

## 2. Recommended Memory Architecture

### Level 1. Working / Episodic Memory (last 1–7 days)
- Full session logs, tool outputs, raw sensor/camera observations.
- Storage: vector DB + files (JSONL / Markdown).
- Lifetime: short. After consolidation it is heavily compressed or archived.

### Level 2. Semantic Knowledge Graph of the Project (main “brain”)
**Nodes to store:**
- Components (parts, modules, versions)
- Decisions (ADR)
- Problems / bugs / anomalies
- Experiments
- Hypotheses
- Physical parameters and tolerances

**Typed edges:**
- `secures`, `causes`, `replaces`, `supersedes`, `confirms`, `contradicts`, `measured_in`, etc.

**Recommended tools:**
- Lightweight start: Markdown + wiki-links (Obsidian-style) + simple extraction script.
- Medium level: Zep / Graphiti, or custom graph on NetworkX / Neo4j.
- Advanced: hybrid (graph + vector embeddings of nodes).

At the start of a new session the agent should receive a **relevant subgraph** of the current problem, not random chunks.

### Level 3. Hierarchical “Project Bible”
Living documents that must always stay up to date:

- `docs/current-state.md` — **Single Source of Truth (SSOT)** for system hardware/software status. If it's not here, it's not "official".
- `docs/handoff-latest.md` — **Context Bridge**. Actionable instructions for the next agent/session.
- `docs/decisions/` — Architecture Decision Records (ADR).
- `docs/spec.md` — Global goals and constraints.

### Level 4. Crystallized Memory (Git)
- All CAD code, firmware, configurations, scripts live in Git.
- Every important stage gets a tag + clear commit message + link to ADR/experiment.
- The model can always do `git show` / `git checkout` of the needed version instead of “remembering”.

## 3. Work Process (Daily / Weekly Cycle)

### Daily / after each session
1. Agent writes a short report in `experiments/` or log.
2. Updates `current-state.md` (what changed, what works, what is broken).
3. Creates/updates nodes and edges in the graph when necessary.
4. Writes or updates the handoff document.

### Weekly (consolidation)
1. Archivist agent:
   - Compresses the week’s logs into 1–3 pages of conclusions.
   - Updates `lessons-learned.md`.
   - Checks the graph for contradictions and outdated facts.
   - Proposes new ADRs when needed.
2. Human reviews and approves key changes.

### Every 2–4 weeks (optional)
- Optional LoRA fine-tuning on a high-quality dataset (only successful + clearly labeled failed cases).
- Do this only if compute resources and a solid validation pipeline are available. Do not treat it as the primary memory mechanism.

## 4. Handoff and Persistence Mechanisms

One of the most common causes of lost progress is context breakage between sessions (chat reset, compaction, switching models, multi-day pause). To minimize this risk, at the end of every significant session the agent must leave a **handoff package**.

### Mandatory minimal handoff (end of session)

Create or update: `docs/handoff-latest.md`

Content structure:

```markdown
# Handoff — [date and short session title]

## 1. Summary of Changes
- What was changed/added/fixed in this session.
- Impact on `current-state.md` (ensure state was updated separately).

## 2. Context & Logic
- Why these changes were made.
- Key findings or failed attempts.

## 3. Open Questions & Blockers
- What is stopping progress right now.

## 4. Next Concrete Steps
- 3–5 specific actions for the next agent.
- Priority (what to do first).

## 5. Warnings
- Critical constraints or pitfalls discovered.
```

### Usage rules
1. **Read sequence**:
   - First, read `handoff-latest.md` to understand the current task and progress.
   - Second, read `current-state.md` to understand the physical/software reality.
2. **Update sequence**:
   - Update `current-state.md` whenever the system's facts change.
   - Update `handoff-latest.md` only at the end of the session or when delegating.
3. **Bootstrapping**: If files are missing, follow the "Bootstrapping Rule" in `AGENTS.md`.

This mechanism is a controlled and safe analogue of what models try to do spontaneously (leaving notes “for a future version of themselves”). The difference is that everything stays inside your repository and under your control.

## 5. Conversation Archive Rules

Raw multi-LLM and human discussions are valuable but noisy. They are stored and later consolidated.

### Location and naming
- Folder: `docs/conversations/`
- Filename: `YYYY-MM-DD--short-kebab-topic.md` (date of creation)
- Use kebab-case for all documentation files.

### Frontmatter (required)
```yaml
---
title: 
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
participants: [Bunch, Grok, ...]
status: open                    # open | closed
closed_reason:                  # decided | superseded | abandoned | merged (only when closed)
language: ru                    # or en
tags: []
related: []
---
```

### Message markup standard
- Date appears only once per day:
  ```markdown
  ---
  **2026-08-31**
  ---
  ```
- Each message:
  ```markdown
  ---
  **Author**

  message text
  ```
- Do **not** use Markdown headings (`###`, `##`) for author/date — they conflict with headings inside LLM answers.
- Avoid nested triple-backtick code blocks. Prefer outer fences with 4+ backticks.

### Lifecycle
- `status: open` — discussion is still active.
- When finished → set `status: closed` and fill `closed_reason`.
- Important conclusions must be promoted to an ADR, `current-state.md`, or a synthesis document.
- After consolidation the raw conversation can stay in the repo (marked closed) or be archived.

## 6. Agent Notes & Transparency

- Agents may keep working notes in `docs/agent-notes/`.
- All notes **must be human-readable** (English or Russian).
- Deliberately opaque, encrypted, or steganographic records are **not allowed**.
- Important conclusions must eventually be promoted to `current-state.md`, an ADR, or a handoff document.

## 7. Agent Roles (minimal set)

| Role            | Responsibility                                       | When called            |
| --------------- | ---------------------------------------------------- | ---------------------- |
| **Constructor** | Generates CAD, code, firmware, proposals             | Main work              |
| **Tester**      | Analyzes logs, sensors, finds anomalies, plans tests | After build/run        |
| **Archivist**   | Graph, summarization, updates current-state, ADRs    | End of session / week  |
| **Critic**      | Finds contradictions, risks, forgotten constraints   | Before important decisions |

You can start with one strong agent + clear system prompts and tools; add multi-agent setup later as needed.

## 8. Practical Minimal Stack for Start

1. Repository with strict `docs/` structure (see above).
2. Vector memory — any convenient one (Chroma, LanceDB, pgvector, Mem0, etc.).
3. Graph — start with Obsidian-style wiki-links + script, later move to Graphiti/Zep or Neo4j.
4. System prompt / `AGENTS.md` that forces the agent to:
   - First read `current-state.md` and relevant ADRs.
   - Update state and graph after work.
5. Regular consolidation sessions (can be automated via cron + LLM).

## 9. What to Avoid

- Relying only on long context.
- Uncontrolled accumulation of raw logs without summarization.
- Frequent fine-tuning without strict data quality control and forgetting evaluation.
- Absence of a single source of truth (`current-state.md` + Git).
- Intentionally non-transparent agent notes.

## 10. System Evolution

Start simple (structured Markdown + vector search + Git).  
As the project grows, add:
- Typed knowledge graph
- Automatic consolidation
- More sophisticated multi-agent setup
- Careful continual learning (if resources allow)

---

**Main conclusion of 2026:**  
The most effective and reliable path today is not to try to “bake” months of experience into model weights, but to build a **transparent, well-structured external memory** that the agent is obliged to read and maintain, and to use Git as the ultimate source of truth. This provides end-to-end architectural integrity without excessive risks and costs.
