# ADR 0003: DuckDB for SQL analytics

- **Status:** Accepted
- **Date:** 2026-11-09

## Context

Users need SQL over the gold catalogs (rankings, rolling averages, completeness checks).

## Decision

Use **DuckDB** to query Parquet directly on S3.

## Reasons

- No server to run or pay for; it runs in-process (scripts, dashboard).
- Reads Parquet on S3 directly and supports Hive partition pruning.
- Full analytical SQL: CTEs, window functions.

## Rejected alternatives

- **PostgreSQL:** needs hosting and a loading step that duplicates the data.
- **AWS Athena:** a good fit, but billed per data scanned; kept as an optional extension.

## Consequences

- Concurrency and access control rely on S3/IAM, which is sufficient for a read-only analytics use case.
