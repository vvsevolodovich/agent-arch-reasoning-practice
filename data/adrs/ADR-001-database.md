# ADR-001: Database Selection

Date: 2022-04-10
Status: Accepted
Author: Backend Lead

## Context
We needed a database for the Conduit MVP. The data model is relational:
Users follow Users, Users write Articles, Articles have Comments and Tags, Users favourite Articles.
The team had prior PostgreSQL experience; no dedicated DBA.

## Decision
PostgreSQL 15 on a single managed instance, accessed via Sequelize ORM.

## Rationale
- Relational model maps cleanly to PostgreSQL; foreign keys enforce referential integrity.
- Sequelize migrations give the team a version-controlled schema history.
- Sufficient for current write volume (~2,600 articles/month, ~480 comments/day).

## Consequences

**Positive**
- Familiar tooling; fast onboarding for new backend devs.
- ACID transactions prevent partial writes (e.g., article + tag creation together).

**Negative**
- Single instance is a SPOF; no read replicas, no standby.
- Full-table tag searches degrade as the tag table grows (no index on tag slugs).

**To watch**
- Add a GIN index on tag slugs when tag-search p95 exceeds 200 ms.
- Evaluate read replica if feed query latency grows with user base.
