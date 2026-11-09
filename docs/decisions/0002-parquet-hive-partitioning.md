# ADR 0002: Parquet with Hive-style date/hour partitions on S3

- **Status:** Accepted
- **Date:** 2026-11-09

## Context

Hourly data must be stored cheaply, queried efficiently by time range, and safely rewritten on
re-runs.

## Decision

Store silver and gold as **Parquet**, partitioned as `.../date=YYYY-MM-DD/hour=HH/part-0.parquet`.

## Reasons

- Parquet is columnar and compressed, preserves types, and every engine reads it.
- Hive-style partition folders become queryable columns; engines skip irrelevant partitions
  (partition pruning).
- One deterministic file per partition makes each write an overwrite, so the pipeline is idempotent.

## Rejected alternatives

- **CSV:** no types, larger, slower to query.
- **Append-only files with unique names:** re-runs would create duplicates.
- **A database (Postgres):** requires a running server and a load step; unnecessary at this scale.

## Consequences

- Many small files (one per hour). Acceptable at this volume; compaction into daily files is a
  possible future optimisation.
