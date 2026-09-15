# AgentForge AI

### Autonomous Software Engineering Platform

**One-line product:**

> Describe an application. AgentForge plans it, designs it, codes it, tests it, deploys it, monitors it, analyses it and repairs it using autonomous specialised AI agents.

---

# 1. The final product

A user enters:

> Build a multi-tenant inventory management platform for Australian retailers with authentication, products, warehouses, suppliers, purchase orders, inventory forecasting, analytics, Stripe billing and admin dashboards.

AgentForge responds with something like:

```text
PROJECT CREATED

InventoryOS

Architecture
✓ Next.js frontend
✓ FastAPI backend
✓ PostgreSQL
✓ Redis
✓ S3
✓ Stripe
✓ Docker
✓ AWS

Users
✓ Platform Admin
✓ Business Owner
✓ Manager
✓ Employee

Features
✓ Authentication
✓ Inventory
✓ Warehouses
✓ Suppliers
✓ Orders
✓ Forecasting
✓ Analytics
✓ Billing
✓ Notifications

AI agents assigned
12

Estimated build tasks
143

Status
READY TO BUILD
```

Then the user presses:

**Build Application**

Everything else happens through agents.

---

# 2. System architecture

```text
                         USER
                          │
                          ▼
                ┌───────────────────┐
                │  AgentForge UI    │
                │ Next.js / React   │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │ API Gateway       │
                │ FastAPI           │
                └─────────┬─────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ AGENT ORCHESTRATOR     │
              │ LangGraph / Python     │
              └────────────┬───────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
       Planner         Architect        Project Memory
       Agent             Agent          RAG / pgvector
          │                │
          └───────┬────────┘
                  ▼
        ┌─────────────────────┐
        │ Task Graph / Queue  │
        └──────────┬──────────┘
                   │
      ┌────────────┼────────────────────────┐
      │            │            │           │
      ▼            ▼            ▼           ▼
 Frontend       Backend      Database      AI/ML
 Agent          Agent        Agent         Agent
      │            │            │           │
      └────────────┴────────────┴───────────┘
                        │
                        ▼
                 Git Repository
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Tester        Security       Reviewer
       Agent          Agent          Agent
          └─────────────┬─────────────┘
                        ▼
                   CI/CD Engine
                        │
                        ▼
                    STAGING
                        │
                Automated Testing
                        │
                        ▼
                   PRODUCTION
                        │
        ┌───────────────┼─────────────────┐
        ▼               ▼                 ▼
    Monitoring      Analytics        Logs/Tracing
        │
        ▼
     Bug Agent
        │
        ▼
      Fix → Test → Review → Deploy
```

---

# 3. The agent organisation

Don't create twenty independent ChatGPT prompts.

Every agent should follow a common contract.

```python
class Agent:
    id
    role
    objective
    tools
    permissions
    context
    memory
    model
    inputs
    outputs
    validation_rules
    escalation_policy
```

The initial architecture eventually supports these agents:

| Agent               | Responsibility                     |
| ------------------- | ---------------------------------- |
| Product Agent       | Converts ideas into requirements   |
| Requirements Agent  | User stories + acceptance criteria |
| Architect Agent     | Technical architecture             |
| UI/UX Agent         | Screens and design system          |
| Frontend Agent      | React/Next.js                      |
| Backend Agent       | FastAPI/business logic             |
| Database Agent      | Schema/migrations/SQL              |
| AI Engineer         | RAG/ML/AI functionality            |
| Data Engineer       | Pipelines/events/transformation    |
| Analytics Agent     | Business metrics                   |
| Security Agent      | Security validation                |
| QA Agent            | Tests                              |
| Browser Agent       | End-to-end testing                 |
| Visual QA Agent     | Detect UI defects                  |
| Code Reviewer       | Reviews pull requests              |
| Bug Hunter          | Finds root causes                  |
| Performance Agent   | Performance optimisation           |
| DevOps Agent        | Docker/cloud/deployment            |
| Monitoring Agent    | Watches production                 |
| Documentation Agent | Documentation                      |
| FinOps Agent        | Infrastructure cost analysis       |

But **you should not build all of these initially**.

---

# 4. Your MVP agents

Start with seven.

```text
1. Planner
2. Architect
3. Developer
4. Database
5. Tester
6. Bug Fixer
7. Deployment
```

Your developer agent can initially handle both frontend and backend.

Later split it.

---

# 5. Planner Agent

Input:

```text
Build a gym management SaaS.
```

Output:

```json
{
  "application": "GymFlow",
  "users": [
    "owner",
    "trainer",
    "member"
  ],
  "features": [
    "authentication",
    "membership",
    "payments",
    "class_booking",
    "attendance",
    "analytics"
  ]
}
```

It generates:

```text
Product specification
Functional requirements
Non-functional requirements
User roles
User stories
Acceptance criteria
Required integrations
Security requirements
Analytics requirements
```

Example:

```text
USER STORY

As a member
I want to book a fitness class
so that I can reserve a place.

Acceptance criteria

Given a class has capacity
When a member books
Then their booking should be confirmed.

Given the class is full
When another member attempts booking
Then they should be added to the waitlist.
```

---

# 6. Architect Agent

The Architect receives the specification.

It generates:

```text
architecture.json

Frontend:
Next.js

Backend:
FastAPI

Database:
PostgreSQL

Authentication:
Supabase Auth

Storage:
S3

Payments:
Stripe

Cache:
Redis

Deployment:
Docker + AWS

Monitoring:
OpenTelemetry

Testing:
pytest
Vitest
Playwright
```

It also determines service boundaries.

```text
/auth
/users
/billing
/products
/orders
/analytics
/notifications
```

---

# 7. Task graph

This is critical.

Don't simply ask agents to start coding.

Generate dependencies.

```text
TASK-001
Create database schema

TASK-002
Create authentication
depends_on: TASK-001

TASK-003
Create user API
depends_on: TASK-001
depends_on: TASK-002

TASK-004
Create dashboard
depends_on: TASK-003

TASK-005
Create tests
depends_on: TASK-003
depends_on: TASK-004
```

Represent this internally as a DAG.

You can use:

```text
LangGraph
+
PostgreSQL
+
Redis
```

---

# 8. Project memory

This will become one of AgentForge's strongest features.

Every project gets a persistent knowledge base.

```text
PROJECT MEMORY

/product
requirements.md
user-stories.md

/architecture
architecture.md
services.md

/database
schema.sql
relationships.md

/api
contracts.json

/design
design-system.md

/security
permissions.md

/decisions
ADR-001.md
ADR-002.md

/issues
bugs.json

/deployment
history.json

/analytics
metrics.json
```

Embeddings go into:

```text
PostgreSQL
+
pgvector
```

When an agent needs information:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant project knowledge
   ↓
Agent
```

This uses your RAG/vector database experience directly. 

---

# 9. Generated code repository

Every generated application should follow a predictable structure.

```text
generated-app/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── tests/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── tests/
│
├── database/
│   ├── migrations/
│   └── seeds/
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   └── terraform/
│
├── tests/
│   └── e2e/
│
├── docs/
│
├── docker-compose.yml
│
└── README.md
```

---

# 10. Frontend

Use:

```text
Next.js
React
TypeScript
Tailwind
TanStack Query
Zod
```

Generated frontend components should be modular.

```text
components/

Button
Input
Modal
Table
Charts
Sidebar
Navbar
Forms
Notifications
```

Each generated page should have:

```text
Loading state
Error state
Empty state
Success state
Responsive version
Accessibility support
```

---

# 11. Backend

Use your strongest backend combination:

```text
Python
FastAPI
Pydantic
SQLAlchemy
Alembic
PostgreSQL
```

Architecture:

```text
Route
   ↓
Controller
   ↓
Service
   ↓
Repository
   ↓
Database
```

Example:

```text
POST /api/orders
        ↓
OrderService
        ↓
InventoryService
        ↓
OrderRepository
        ↓
PostgreSQL
```

---

# 12. Database Agent

The Database Agent generates schemas automatically.

Input:

```text
Users purchase products from stores.
Each store contains warehouses.
Warehouses contain inventory.
```

Output:

```text
users
stores
warehouses
products
inventory
orders
order_items
```

It should generate:

```text
Primary keys
Foreign keys
Indexes
Constraints
Audit columns
Soft deletion
Migration scripts
```

It should also detect:

```text
Missing indexes
N+1 queries
Poor schema design
Duplicate data
Foreign-key problems
Slow queries
```

This directly uses your SQL, data modelling, schema design and data-quality background. 

---

# 13. AI Agent

Applications generated by AgentForge can optionally request AI.

Example:

> Add customer support AI.

AgentForge generates:

```text
Document ingestion
       ↓
Chunking
       ↓
Embeddings
       ↓
Vector database
       ↓
Retriever
       ↓
LLM
       ↓
Response
```

Support:

```text
OpenAI
Hugging Face
Ollama
```

Eventually allow:

```text
Cloud AI
Private AI
Local AI
```

---

# 14. ML Agent

Don't restrict AgentForge to LLMs.

Your platform should support actual ML.

For example:

> Predict customer churn.

The ML Agent generates:

```text
Data pipeline
Feature engineering
Training dataset
Train/test split
Model
Evaluation
Inference endpoint
Monitoring
```

Example endpoint:

```text
POST /ml/churn/predict
```

Response:

```json
{
  "customer_id": 8451,
  "churn_probability": 0.82
}
```

---

# 15. Computer Vision Agent

This differentiates your platform.

Applications could request:

> Detect damaged products from uploaded images.

AgentForge provisions:

```text
Upload service
       ↓
Image preprocessing
       ↓
Vision model
       ↓
Inference
       ↓
Result
       ↓
Storage
       ↓
Dashboard
```

---

# 16. Visual QA system

You can use OpenCV in AgentForge itself.

Playwright captures screenshots.

```text
Expected Screenshot
        ↓
      compare
        ↑
Actual Screenshot
```

Detect:

```text
Broken layouts
Missing elements
Text overflow
Unexpected colour changes
Image failures
Buttons outside viewport
Responsive problems
```

Example:

```text
VISUAL QA

Page
/dashboard

Device
iPhone

Problem
Revenue chart overlaps menu.

Confidence
96%

Severity
Medium

Assigned
Frontend Agent
```

---

# 17. Automated testing

You have three testing layers.

```text
Backend
pytest

Frontend
Vitest

Browser
Playwright
```

Every feature requires:

```text
Feature
↓
Code
↓
Unit test
↓
Integration test
↓
E2E test
↓
Security test
↓
Build
```

If anything fails:

```text
DEPLOYMENT BLOCKED
```

---

# 18. The Bug Hunter

This is probably the most commercially valuable feature.

Production produces:

```text
500

POST /api/orders
```

Monitoring creates:

```text
INCIDENT-128
```

Bug Agent receives:

```text
Stack trace
Logs
Recent commits
Relevant source files
DB metadata
Previous similar bugs
```

It creates hypotheses.

```text
H1 database constraint
H2 race condition
H3 missing environment variable
```

It attempts reproduction.

```text
FAILED TEST CREATED
```

Then asks Developer Agent for a patch.

```text
fix/incident-128
```

QA runs.

```text
242 tests
242 passed
```

Reviewer checks the diff.

Then staging.

Then production.

---

# 19. Self-healing workflow

This is the loop you should showcase publicly.

```text
ERROR
 ↓
Detect
 ↓
Capture context
 ↓
Classify
 ↓
Find affected code
 ↓
Retrieve project memory
 ↓
Generate hypothesis
 ↓
Create reproduction test
 ↓
Create branch
 ↓
Patch
 ↓
Run unit tests
 ↓
Run integration tests
 ↓
Run Playwright
 ↓
Security review
 ↓
Deploy staging
 ↓
Smoke test
 ↓
Approval
 ↓
Production
 ↓
Monitor
```

Production deployment should initially require human approval.

Do **not** let V1 autonomously push arbitrary code directly to production.

---

# 20. Permission system

Agents need explicit permissions.

Example:

```text
Frontend Agent

READ
frontend/**

WRITE
frontend/**

DENIED
infrastructure/**
database/**

--------------------------------

Database Agent

READ
database/**
backend/models/**

WRITE
database/migrations/**

DENIED
production credentials
```

This creates proper isolation.

---

# 21. Execution sandbox

Generated code must run inside isolated environments.

```text
AgentForge
     ↓
Job Queue
     ↓
Docker Sandbox
     ↓
Clone repository
     ↓
Install dependencies
     ↓
Build
     ↓
Run tests
     ↓
Destroy container
```

Never run generated code directly on your core AgentForge server.

---

# 22. Git workflow

Every task creates:

```text
Branch
↓
Commit
↓
Pull Request
↓
AI Review
↓
Tests
↓
Merge
```

Example:

```text
feature/inventory-forecasting

bugfix/order-race-condition

feature/customer-dashboard
```

---

# 23. Code Reviewer Agent

Reviewer receives the diff.

Checks:

```text
Correctness
Architecture
Security
Performance
Testing
Code duplication
Error handling
Maintainability
```

Output:

```text
REVIEW

Architecture       PASS
Security           PASS
Tests              PASS
Performance        WARNING

Issue

Repeated query executed once per
customer.

Recommendation

Use batch query.

Decision

CHANGES REQUESTED
```

---

# 24. Security Agent

At minimum check:

```text
SQL injection
XSS
CSRF
Broken authentication
Broken authorisation
Exposed API keys
Secrets committed to Git
Unsafe file uploads
Dependency vulnerabilities
Rate limiting
Input validation
CORS
```

Later integrate:

```text
Semgrep
Trivy
OWASP ZAP
Dependabot
```

---

# 25. Observability

Every application needs:

```text
Logs
Metrics
Traces
Errors
Business events
```

Use:

```text
OpenTelemetry
Prometheus
Grafana
Sentry
```

Eventually AgentForge itself understands:

```text
POST /checkout

p50 180ms
p95 710ms
p99 1.8s

error rate 3.2%
```

---

# 26. Analytics Agent

This is where your data-analytics background becomes a major differentiator.

Capture events:

```text
user_registered
login_completed
product_created
checkout_started
checkout_completed
subscription_cancelled
```

Pipeline:

```text
Application
   ↓
Event API
   ↓
Queue
   ↓
ETL
   ↓
Warehouse
   ↓
Analytics
```

The dashboard can show:

```text
DAU
MAU
Retention
Conversion
MRR
Churn
Feature adoption
Error rate
Revenue/customer
```

Then users can ask:

> Why did conversions fall last week?

The Analytics Agent performs SQL analysis and explains the result.

---

# 27. Automatic optimisation

Eventually:

> Improve conversion.

AgentForge investigates.

```text
Landing visits       18,240
Signup started        4,820
Signup complete       2,410
Email verification    1,670
Paid                    310
```

AI finds:

```text
31% abandonment during verification.
```

It can recommend:

```text
Google OAuth
Magic links
Improved email delivery
Resend verification button
```

Later it can implement approved changes.

---

# 28. Control Room UI

The dashboard should look like an engineering command centre.

```text
AGENTFORGE

InventoryOS                     PRODUCTION 🟢

------------------------------------------

Agents

Planner               Idle
Architect             Idle
Frontend              Working
Backend               Working
Database              Idle
QA                    Testing
Security              Scanning
Bug Hunter            Investigating
DevOps                Monitoring

------------------------------------------

Current Deployment

v1.19.4

Tests
244 / 244 passed

Security
0 critical
1 warning

Production uptime
99.96%

API errors
0.18%

------------------------------------------

Active Issues

#182 Checkout latency
#184 Mobile navbar
#186 Inventory race condition
```

---

# 29. Build timeline display

Users should be able to watch AgentForge building their software.

```text
09:42 Requirements generated
09:45 Architecture completed
09:47 Database generated
09:51 Authentication complete
10:02 Backend endpoints created
10:13 Frontend generated
10:21 Tests generated
10:29 4 tests failed
10:31 Bug Agent assigned
10:36 Bug resolved
10:41 86/86 tests passed
10:44 Staging deployed
```

This makes the agents understandable and gives the platform credibility.

---

# 30. Core AgentForge database

You will need approximately these entities:

```text
users
organisations
projects
applications

agents
agent_runs
agent_tools
agent_permissions

tasks
task_dependencies

repositories
branches
commits

builds
deployments
environments

tests
test_runs

bugs
incidents

logs
metrics

requirements
architecture_decisions

project_documents
embeddings

conversations
messages

integrations
secrets

usage
subscriptions
billing
```

---

# 31. Core AgentForge API

Your own platform API could look like:

```text
POST   /projects
GET    /projects/{id}

POST   /projects/{id}/prompt

POST   /projects/{id}/build

GET    /projects/{id}/tasks

GET    /projects/{id}/agents

POST   /agents/{id}/run

GET    /builds/{id}

POST   /builds/{id}/cancel

GET    /deployments

POST   /deployments/staging

POST   /deployments/production

GET    /incidents

POST   /incidents/{id}/investigate

GET    /analytics/{project}

GET    /logs/{project}
```

---

# 32. Agent event architecture

Do not have agents call each other directly everywhere.

Use events.

```text
CODE_GENERATED
      ↓
Event Bus
      ↓
TESTER

TEST_FAILED
      ↓
Event Bus
      ↓
BUG_AGENT

TEST_PASSED
      ↓
Event Bus
      ↓
SECURITY_AGENT

SECURITY_PASSED
      ↓
Event Bus
      ↓
DEPLOYMENT_AGENT
```

Initially:

```text
Redis
```

Later:

```text
Kafka
```

---

# 33. Technology stack

### Core platform

```text
Frontend
Next.js
React
TypeScript
Tailwind

Backend
Python
FastAPI
Pydantic
SQLAlchemy

Agents
LangGraph
LangChain

Database
PostgreSQL
pgvector

Cache / queue
Redis

Files
AWS S3

Containers
Docker

Cloud
AWS

CI/CD
GitHub Actions

Reverse proxy
Nginx

Testing
pytest
Vitest
Playwright
```

This lines up extremely well with the technologies already demonstrated across your professional experience and projects. 

---

# 34. LLM architecture

Don't hard-code AgentForge to one model.

Create:

```python
class ModelProvider:
    generate()
    stream()
    embeddings()
    tools()
```

Then adapters:

```text
OpenAIProvider
AnthropicProvider
GeminiProvider
HuggingFaceProvider
OllamaProvider
```

Your agents request capabilities rather than models.

```text
task:
code_review

requirements:
reasoning = high
context = large
cost = medium
```

The router selects the model.

---

# 35. Cost control

Agent systems can become extremely expensive.

Create a model router:

```text
Simple task
→ cheaper model

Complex architecture
→ stronger model

Code formatting
→ local model

Embedding
→ embedding model

Image inspection
→ vision model
```

Track:

```text
Tokens
API cost
GPU time
Build time
Storage
Infrastructure
```

per project.

---

# 36. Human approval gates

Three operating modes:

```text
ASSISTED

Agent proposes everything.
Human approves everything.

SEMI-AUTONOMOUS

Agent can code/test automatically.
Human approves deployments.

AUTONOMOUS

Approved categories of fixes
can deploy automatically.
```

For V1:

**Semi-autonomous.**

---

# 37. Your MVP

Do not start by trying to generate every kind of application.

Make V1 capable of generating one category extremely well:

### CRUD SaaS applications.

For example:

```text
Admin dashboards
Inventory systems
CRM
Booking systems
Project management systems
Employee management
Customer portals
Analytics platforms
```

Support:

```text
Authentication
RBAC
CRUD
Forms
Tables
Search
Dashboards
REST APIs
PostgreSQL
Basic analytics
Docker
Automated testing
Deployment
```

That's enough for a seriously impressive MVP.

---

# 38. Twelve-week development roadmap

| Week | Build                                |
| ---- | ------------------------------------ |
| 1    | AgentForge frontend + authentication |
| 2    | Projects + prompts + database        |
| 3    | Planner Agent                        |
| 4    | Architecture Agent                   |
| 5    | Code generation engine               |
| 6    | Docker sandbox                       |
| 7    | GitHub integration                   |
| 8    | Testing Agent                        |
| 9    | Bug Fixer                            |
| 10   | Deployment Agent                     |
| 11   | Monitoring + analytics               |
| 12   | Full autonomous demo                 |

At week 12:

```text
PROMPT
↓
SPEC
↓
ARCHITECTURE
↓
CODE
↓
DATABASE
↓
TEST
↓
BUG FIX
↓
DOCKER
↓
DEPLOY
↓
MONITOR
```

That is your first major milestone.

---

# 39. Phase 2

Then introduce:

```text
Separate frontend/backend agents
Security Agent
Analytics Agent
RAG project memory
Visual QA
Stripe
Email integrations
Performance analysis
Infrastructure optimisation
```

---

# 40. Phase 3

Add serious AI capabilities.

```text
AI model deployment
RAG applications
Predictive ML
Computer vision
Fine-tuning
Agent-generated datasets
Model monitoring
GPU deployment
```

This lets you use your ML background instead of remaining purely an LLM application.

---

# 41. Phase 4

AgentForge becomes an operating system for software teams.

```text
Developer Agent
Data Engineer Agent
ML Engineer Agent
Business Analyst Agent
Security Engineer Agent
DevOps Engineer Agent
QA Engineer Agent
Product Manager Agent
UI Designer Agent
Database Engineer Agent
```

A founder can effectively launch a virtual development team.

---

# 42. Business model

Eventually:

```text
FREE

1 project
limited builds

PRO
$49–99/month

More builds
GitHub
Deployment
AI debugging

STARTUP
$199–499/month

Multiple apps
Monitoring
Analytics
More agents

BUSINESS
$1,000+/month

Private infrastructure
Teams
Approval workflows
Security
Audit logs

ENTERPRISE

Private cloud
Local models
SSO
Custom agents
Compliance
Dedicated infrastructure
```

But do not optimise the MVP around subscriptions initially.

Build the engineering loop first.

---

# 43. Your public demo

The demo should deliberately create a failure.

User says:

> Build an inventory management SaaS.

AgentForge builds it.

Then simulate:

```text
Two customers buy the final product
at exactly the same moment.
```

Inventory becomes:

```text
-1
```

Monitoring detects it.

Bug Agent discovers a race condition.

Database Agent proposes row-level locking.

Developer patches it.

QA creates a concurrency test.

```text
Before

Expected stock: 0
Actual stock: -1
FAIL

After patch

Expected stock: 0
Actual stock: 0
PASS
```

AgentForge deploys.

Then display:

```text
INCIDENT RESOLVED

Detection        14:01:03
Diagnosis        14:01:26
Fix generated    14:02:02
Tests passed     14:02:41
Staging passed   14:03:18
Production       14:03:52

MTTR
2m 49s
```

That one demo communicates:

**AI + backend + SQL + distributed systems + testing + DevOps + cloud + analytics + autonomous agents.**

---

# 44. What you personally demonstrate through this project

This matters because AgentForge isn't only a startup idea.

It becomes a demonstration that you understand:

```text
Artificial intelligence
Machine learning
LLMs
Agents
RAG
Data engineering
SQL
Data modelling
Backend development
Frontend development
APIs
Distributed architecture
Microservices
Cloud
Docker
CI/CD
Testing
Security
Analytics
Computer vision
Observability
System design
Product thinking
Business strategy
Technical leadership
```

**AgentForge connects all of those pieces into one story.**

---

# The end vision

The final interaction should eventually be this simple:

> **You:** Build an Australian construction management system for contractors. Include projects, workers, timesheets, invoices, safety reporting, AI document analysis and management analytics.

AgentForge:

```text
Requirements created.
Architecture designed.
Database created.
71 backend endpoints generated.
38 UI components created.
126 tests generated.
3 defects detected.
3 defects repaired.
Security scan passed.
Docker images created.
Staging deployed.

Application ready.

Build time: 38 minutes.
```

Two weeks later:

> **You:** Our users aren't using safety reports. Find out why and improve it.

AgentForge:

```text
Analysis complete.

62% of users abandon the workflow
after the third form screen.

Mobile abandonment: 74%.

Proposed improvement:

Convert 5-step workflow into
2-step mobile form.

Estimated completion improvement:
+28–37%.

Create implementation?
```

Then:

> **Approve.**

And the engineering team of agents handles the rest.

That is the company I would build around your skill set:

## **AgentForge — Build. Test. Deploy. Observe. Understand. Repair. Improve.**

The next practical step is **not more ideation**. It is turning this blueprint into the actual **V1 engineering specification: database schema, API contracts, exact seven-agent prompts, LangGraph workflow, repo structure, UI screens and Week-1 code architecture**.

