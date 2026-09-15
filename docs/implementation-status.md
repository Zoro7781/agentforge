# Implementation status

## Delivered
Private web control room, owner-scoped persistence, project CRUD/archive/search, four deterministic CRUD source templates, source browser/download, migration-managed schema, audit trail, source digests, seven agent contracts, full original outline, grouped blueprint and roadmap. Source includes OpenAI requirements adapter and dedicated Docker pytest runner.

## Requires external connection
OpenAI API key/model for requirements generation. HTTPS runner host and bearer secret for sandbox testing. These are reported as unavailable when unconfigured; no fake output is substituted.

## Still to implement from the full vision
General-purpose application synthesis; LangGraph/DAG orchestration; FastAPI/PostgreSQL control plane; organization roles; task dependencies and queues; GitHub App per-project branches/PRs; code review; automated security and browser/visual QA; failing-test-driven repair; staging and production deploy providers; approval records; monitoring/incidents; business analytics/warehouse; RAG and provider routing; ML/vision/GPU deployment; billing and enterprise controls.

The complete 44-section vision is a roadmap, not a claim of full autonomous production capability. The app exposes this distinction in its blueprint, agent page and release gates.

## Verification (16 September 2026)
- TypeScript check and complete production build passed.
- 71 local HTTP integration checks passed: authentication, spoofed-header rejection, input validation, origin checks, concurrent build deduplication, exports, archive/restore, and missing-service errors across all four templates.
- All four generated applications passed four pytest tests each (16 total).
- Six runner tests passed, covering authentication, digest validation, path constraints, container arguments, and unavailable Docker.
- Interrupted runner requests can be retried after a two-minute lease; source digests have a database uniqueness constraint.
- Actual Docker execution and live OpenAI requests remain unverified because those services are not connected. Browser interaction testing remains unavailable because macOS Computer Use permissions are pending.

Run local workspace checks with `python tests/check-workspace.py` after applying migrations and starting the development server. These checks create sample projects only on localhost.
