# ADR 0001: Use Prefect for orchestration

- **Status:** Accepted
- **Date:** 2026-11-09

## Context

The pipeline must run hourly with retries, logging, run history, and backfills. Options considered:
plain cron, Apache Airflow, Dagster, Prefect.

## Decision

Use **Prefect 3**, with Prefect Cloud's free tier for the run UI.

## Reasons

- Flows and tasks are plain Python functions with decorators, so there's little boilerplate.
- Built-in retries with backoff, structured logging, and run history.
- No scheduler/webserver/metadata database to operate (unlike Airflow), and it works well on Windows
  for local development.
- Free hosted UI for observability.

## Rejected alternatives

- **Cron:** schedules only; no retries, history, task-level visibility, or backfills.
- **Airflow:** industry standard, but heavy to run for a single small pipeline.
- **Dagster:** strong asset-based model; a good future comparison, but Prefect is lighter to start.

## Consequences

- Scheduling in production is done by GitHub Actions cron (free); Prefect provides retries,
  observability, and the flow structure.
- Migrating to Airflow later would mean rewriting the flow definition, but the stage functions
  (extract/transform/validate/load) are orchestrator-agnostic and would be reused unchanged.
