# AgentForge

A private engineering workspace built from the AgentForge product outline. Create projects, generate downloadable CRUD application source, inspect the seven-agent contracts, refine requirements with a configured OpenAI API, and run generated pytest suites through an isolated Docker service.

## What works

- ChatGPT identity and owner-scoped persistent projects, builds, artifacts and audit events.
- Inventory, CRM, booking and project-management CRUD templates.
- FastAPI applications with shared-key authentication, SQLite records, browser UI, search, pagination, CRUD validation, pytest suite and Docker configuration.
- Source viewer and downloadable TAR bundle; immutable build digest and idempotent source generation.
- Optional server-side OpenAI requirements generation via the Responses API.
- Optional isolated pytest runner with resource limits, path validation and digest-bound evidence.
- Four-phase platform blueprint, seven exact agent contracts, 12-week roadmap and full original outline.

## What is not yet a complete autonomous platform

The live workspace is a working foundation, not the entire four-phase vision. General-purpose LLM code generation, LangGraph orchestration, multi-tenant generated-app RBAC, application GitHub synchronization, autonomous bug repair, browser/security test execution, staging/production deployment, telemetry ingestion, ML, vision, RAG and billing are specified future work. The UI does not present these as working integrations. The generated PostgreSQL schema is a design artifact; the working template backend uses SQLite.

OpenAI planning requires an API key and model. A ChatGPT sign-in is not an API credential. Test execution requires a deployed runner. Neither service is assumed connected. Generated apps are not automatically deployed.

## Development

Node 22.13+ required. `npm run install:ci`, then `npm run dev`. If Vinext CLI startup stalls, `node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173` uses the same project configuration. The portable Sites preview supplies development-only mock identity; production identity comes from the trusted Sites dispatcher.

`npm run db:generate` generates migrations. `npm run build` produces the Worker. To preview persistent storage after building, apply each pending SQL migration with:

```
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_workable_grim_reaper.sql
```

Use `npm run start` for the built Worker preview. Do not reapply migrations already applied to a local database. Sites applies production migrations when publishing.

## Configuration

Set secrets through Sites runtime settings: `OPENAI_API_KEY`, `OPENAI_MODEL`, `RUNNER_URL`, `RUNNER_TOKEN`. Redeploy after changes. No provider keys are accepted by the browser or stored in project records. Runner setup: [services/runner/README.md](services/runner/README.md).

## Engineering documents

- [Original complete outline](docs/original-outline.md)
- [V1 specification and API contracts](docs/v1-specification.md)
- [Implementation status and remaining work](docs/implementation-status.md)
- [Seven-agent definitions](lib/blueprint.ts)
- [Schema](db/schema.ts)

## Verification

`npx tsc --noEmit`, `npm run build`, Python unit tests for runner boundaries, integration tests against the local Worker, and execution of an exported template's pytest suite. See `docs/verification.md` for the actual result of this delivery. A generated test file is not a passing test result.
