# Conduit — Company Context

## What We Do
Conduit is an open publishing platform where writers create and share articles,
readers follow authors and curate feeds, and community members discuss ideas through comments.
Think of it as a lean, indie version of Medium.
Founded in 2022, single-region deployment, growing steadily.

## Current Numbers
- 14,000 registered users
- 2,600 articles published per month
- 52,000 monthly active readers
- 480 comments per day
- Average session length: 6 min
- 70% of traffic is unauthenticated (SEO / read-only)

## Growth Trajectory
- Month-over-month registered-user growth: 18%
- Article output growing 22% MoM since the writer program launched
- Planning to introduce a premium tier (paid subscriptions for authors) in Q3

## Current Technology Stack
- Backend: Node.js monolith (Express.js + Sequelize ORM)
- Database: Single PostgreSQL 15 instance (models: User, Article, Comment, Tag)
- Frontend: React + Vite SPA, served via the same VPS
- Auth: JWT (stateless, no refresh tokens yet)
- Hosting: Single VPS — €120/month
- No dedicated CDN, no cache layer, no message queue

## Engineering Team
- 2 backend developers (Node.js, some Python)
- 1 frontend developer (React)
- 1 DevOps / part-time infra engineer
- No dedicated SRE or data engineering

## Infrastructure Budget
- Current spend: ~€280/month
- Approved budget for new features: up to €1,200/month additional

## Known Pain Points (Business Impact)

1. **No real-time collaboration** — Writers cannot co-author an article simultaneously.
   Co-authors must pass a Google Doc back and forth, then paste the final version.
   Several power users have complained this is the #1 missing feature.

2. **No draft auto-save** — If a writer closes the tab, their draft is lost.
   Support tickets about lost work: ~30/month.

3. **Feed latency at peak** — The personalised article feed re-queries PostgreSQL
   on every page load. p95 latency hits 1.8 s on weekday mornings.

4. **No media storage** — Articles cannot embed images hosted by Conduit.
   Writers must paste external URLs, which rot over time.

5. **Auth session length** — JWT access tokens never expire.
   Security team flagged this; any leaked token is valid forever.

6. **Tag search is a full-table scan** — No index on tags.
   As the tag table grows the search endpoint degrades linearly.

## Timeline
- Premium tier (paid subscriptions) launch: Q3 — hard deadline, marketing committed.
- Real-time collaboration MVP: Q4 goal, team lead is pushing hard.
- Image hosting: backlog, no firm date.
