# SBS-Centric Medical Coding Platform Blueprint

This blueprint realigns GIVC Core Academy with the updated **SBS-Centric Medical Coding Training Platform** specification. It captures the required Saudi-focused architecture, compliance, and delivery milestones so engineering, product, and compliance teams can execute against a single source of truth.

## Architecture & Platform Alignment

### Backend (FastAPI async)
- **Data**: PostgreSQL 15 + PostGIS for spatial/region-aware rules; keep SQLite only for local development. Connection URLs must support read replicas to receive traffic in KSA regions.
- **Caching/Queue**: Redis Cluster for low-latency Arabic search caching; Celery workers for batch SBS migration, audits, and notifications.
- **Identity & Auth**: JWT + OAuth2 + SCFHS ID federation; enforce MFA for admins/auditors. Include CHI audit governance hooks on auth events.
- **Compliance Modules**:
  - SBSCS/ICD-10-AM integration services with version pinning and diff/migration tools (v2.0/v3.0).
  - Corporate billing with VAT, LTC insurance, and regional pricing; auditable invoice/receipt payloads.
  - Audit/compliance APIs exposing CHI/MOH/SCFHS evidence (immutable log stream).
  - Coding simulation engine for SBS, ICD-10-AM, AR-DRG aligned to Success Criteria latency budgets.

### Frontend (Next.js 14, App Router)
- Bilingual (Arabic/English) with RTL/LTR switching; BrainSAIT design tokens for typography, spacing, and components.
- Compliance-ready UI: consent capture, PHI masking, access logs surfacing, and audit trails per screen.
- Advanced dashboards: Prometheus/Grafana data surfaces for performance, audit heatmaps, corporate KPIs; Storybook-powered UI catalog kept in sync with BrainSAIT tokens.

### Mobile / Multi-Channel (React Native + Expo)
- Bilingual learning flows with offline-first caches for KSA connectivity constraints.
- Regional KPI views for corporate clients; push notifications routed through compliance-approved channels.
- Same role-based access and audit logging as web (SCFHS/CHI identifiers propagated end-to-end).

### Infrastructure
- Docker/K8s baselines with Saudi data residency; NCSS-aligned security hardening (TLS 1.3, AES-256 at rest, RBAC, secrets in K8s/Vault).
- Observability: Prometheus scraping, Grafana dashboards, SIEM-forwarded audit logs, and SLO dashboards measured against the Success Criteria latency budgets.
- Encryption, audit logging, and role enforcement are mandatory middleware; workloads isolated per environment with least-privilege service accounts.

## Modules & Deliverables
- **SBS Libraries**: v2.0/v3.0 code sets, migration impact analysis, rehab services (Chapter 26).
- **Audit Governance**: CHI/NPHIES evidence API, immutable audit store, alerting on policy drift.
- **Compliance Workflows**: Regional/B2B flows, corporate billing/VAT, LTC insurance, SCFHS ID capture.
- **Coding Simulation Engine**: Timed SBS/ICD-10-AM/AR-DRG scenarios with scoring and remediation hints.
- **Analytics**: Regional KPIs, corporate dashboards, learner progress, billing performance, and SLA monitoring.

## Roadmap (Phased)
Timelines assume parallel workstreams with buffer for compliance reviews, security sign-off, and UAT feedback loops.
1. **Foundations (Week 1-2)**: PostGIS-ready DB layer, Redis Cluster config, JWT+OAuth2+SCFHS ID plumbing, baseline audit logger + CHI hooks.
2. **Compliance & Data Residency (Week 3-4)**: NCSS hardening, encryption everywhere, immutable audit stream, PHI masking, consent & access logs in UI.
3. **Feature Completion (Week 5-7)**: SBS v2/v3 migration tools, rehab (Chapter 26) library, corporate billing/LTC, coding simulator with latency budgets.
4. **Observability & Launch (Week 8)**: Prometheus/Grafana dashboards, Storybook alignment to BrainSAIT tokens, performance tuning to hit the Success Criteria SLOs, UAT with 50 KSA clients.

## Success Criteria
- Performance SLOs (p99): Arabic code search endpoints (e.g., `/api/v1/codes/search`) <500ms; learner/corporate APIs <2s across regions.
- 99.9% SBS mapping accuracy.
- Full CHI/MOH/SCFHS/NPHIES compliance evidence available via audit APIs.
- Bilingual UX with RTL/LTR parity and accessibility conforming to BrainSAIT standards.
- Launch-ready with at least 50 Saudi corporate clients onboarded in phased rollout.
