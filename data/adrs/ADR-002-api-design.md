# ADR-002: API Design Style

Date: 2022-05-03
Status: Accepted
Author: Backend Lead

## Context
The Conduit frontend (React SPA) needs to communicate with the backend.
The project follows the RealWorld spec, which prescribes a REST API.
The team considered deviating to GraphQL before the first release.

## Options Considered

1. **REST over HTTPS (RealWorld spec)** — well-understood, broad tooling, cacheable GET responses.
2. **GraphQL** — flexible queries, reduces over-fetching for complex screens; higher server complexity and harder CDN caching.
3. **tRPC** — end-to-end type safety with TypeScript; requires full TypeScript migration on both sides.

## Decision
REST API with JSON payloads over HTTPS, following the RealWorld OpenAPI specification.
Endpoints live under `/api/` with no explicit version prefix (spec-defined paths).

## Rationale
- RealWorld spec compliance enables community tooling, test suites, and frontend interoperability.
- Every team member has REST experience; no learning curve.
- The SPA's data needs (articles list, single article, profile) map cleanly to individual REST resources.
- Current traffic does not justify GraphQL operational overhead.

## Consequences

**Positive**
- Spec-compliant API is well-documented; easy to test with the RealWorld Postman collection.
- New developers onboard without API design discussions.

**Negative**
- Feed screen requires 2–3 sequential requests (articles + tags + user profile).
- Real-time features (e.g., collaborative editing) cannot use REST alone — WebSocket or SSE needed.

**To watch**
- When real-time collaboration lands, define a clear boundary: REST for CRUD, WebSocket for presence and live deltas.
