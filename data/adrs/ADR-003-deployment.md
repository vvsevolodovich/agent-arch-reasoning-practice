# ADR-003: Deployment Architecture

Date: 2022-04-10
Status: Accepted
Author: DevOps Engineer

## Context
We needed to ship the Conduit MVP quickly. The team was two backend devs and one frontend dev.
We operate in a single region; latency is not a concern at current scale.

## Decision
Single VPS (Hetzner CX21, €10.90/month). Node.js app and PostgreSQL run on the same host.
Nginx handles TLS termination and serves the React build as static files.

## Rationale
- Cheapest viable option at MVP scale.
- Zero infrastructure expertise required — no orchestration, no networking complexity.
- Entire stack can be restarted with a single `systemctl restart` per service.

## Consequences

**Positive**
- Simple to operate and debug; total infra cost under €120/month.
- Deployment is a single `git pull && pm2 reload` on the VPS.

**Negative**
- Single point of failure: one hardware fault takes down the entire platform.
- No horizontal scaling — adding WebSocket connections for real-time collaboration will saturate
  a single process if many articles are edited simultaneously.
- No staging environment; all testing happens in production or locally.

**To watch**
- Revisit before real-time collaboration launch: sticky sessions or a shared presence store
  (e.g., Redis) will be required if the app runs as more than one process.
- Add a nightly PostgreSQL dump to off-site storage as a minimum DR measure.
