# AgentForge V1 engineering specification

## Scope and architecture decision
The full source brief is preserved in original-outline.md. This delivery realizes the project workspace and constrained CRUD generation slice. The hosted control plane uses the Sites-supported React/Vinext Worker runtime and D1. It is not a hosted Python/PostgreSQL/LangGraph cluster. Python execution is isolated in the separate runner; generated apps are self-contained FastAPI services. This adaptation keeps the workspace live without inventing provider access or executed jobs.

## API contracts
All routes are owner-authenticated and sensitive responses are not cached. Mutation requests reject a conflicting Origin. JSON request bodies are bounded and validated.

| Method | Path | Contract |
|---|---|---|
| GET | /api/workspace | Current user, up to 100 owned projects, configuration presence |
| POST | /api/projects | {name: 2–80 chars, prompt: 15–8000 chars, template: inventory/crm/booking/projects}; returns 201 {id} |
| GET | /api/projects/{id} | Owned project, recent builds/events/artifacts; missing or other owner's project returns 404 |
| PATCH | /api/projects/{id} | {status: draft/archived}; audit event recorded |
| POST | /api/projects/{id}/build | Deterministic template bundle; repeated unchanged source reuses existing build |
| GET | /api/projects/{id}/export | Latest source TAR; ?format=json returns files and digest |
| POST | /api/projects/{id}/plan | OpenAI structured requirements; missing configuration returns 503; bounded calls |
| POST | /api/projects/{id}/test | Digest-bound runner evidence; missing configuration returns 503; concurrent test attempts return 409 |

## Persisted contracts
projects(id, owner, name, prompt, template, status, created, updated)
builds(id, project_id, status, digest, files, report, created)
events(id, project_id, agent, message, created)
artifacts(id, project_id, kind, content, created)

UUID keys. Foreign keys with cascade on project deletion. Indexes match owner/updated and project/created queries. Schema changes are migration-owned. Project creation and source generation use database batches for atomic writes. Queries use bound parameters. No runtime schema mutation in the control plane.

## State machine
Project: draft → generated; draft/generated ↔ archived (restore returns draft).
Build: generated → testing → unit_passed | unit_failed | test_error.
No transition from unit_passed to production exists. Production requires additional independent evidence and a provider integration. Model requirements are stored separately; the template compiler does not pretend to implement arbitrary AI requirements.

## Seven-agent workflow design
Planner(requirements) → Architect(contracts/task graph) → Database(schema) → Developer(files) → Tester(evidence) → Bug Fixer(patch/reproduction) → Tester(retry) → Deployment(staging) → HumanApproval → Production.

The complete natural-language system contracts, outputs and write boundaries are stored in lib/blueprint.ts. Future LangGraph state must persist run_id, project_id, revision, task DAG, artifact digests, budget, attempt_count, evidence and approval. Conditional repair edge caps attempts at three. Interrupted jobs resume from a checkpoint; external callbacks use idempotency keys. Production approvals bind to digest and expire after source changes. The current control plane implements a direct deterministic template workflow, not a running LangGraph loop.

## Screens and UI states
Control room: prompt composer, template selection, agent pipeline and recent projects.
Projects: searchable list, archive inclusion, creation dialog.
Project: overview, source viewer/export, requirements, tests/release gates and audit trail.
Agent team: exact system contracts and permissions.
Blueprint: fourteen chapter groups covering the full outline, roadmap and stack distinction.
Connections: sign-in, OpenAI, isolated runner, repository and planned deployment integration.
Each async action has disabled/loading controls and recoverable errors. Empty states are actionable. Project creation keeps typed input on failure.

## Production hardening before broader adoption
Use job queues/checkpoints for generation and testing, atomic per-user rate limits, pagination beyond bounded history, database uniqueness for concurrent generation, stale test lease recovery, monitored runner capacity, SSO/tenant membership, generated-app security hardening, backups and restore testing, dependency audit and browser/security gates. The single-owner private workspace and bounded template scope are deliberate first-release constraints.
