# ADR 0004: GitHub OIDC instead of stored AWS access keys

- **Status:** Accepted
- **Date:** 2026-11-09

## Context

The scheduled GitHub Actions job must write to S3. The traditional approach stores a long-lived
access key as a repository secret.

## Decision

Use **GitHub's OIDC provider** with an AWS IAM role. The workflow requests a short-lived token and
exchanges it for temporary credentials via STS.

## Reasons

- No long-lived credentials exist to leak or rotate.
- The role's trust policy accepts tokens only from this repository (and its production environment).
- The role's permission policy is scoped to a single bucket (least privilege).

## Consequences

- One-time setup of an IAM OIDC identity provider and role.
- The dashboard (hosted outside GitHub) still needs a key: a separate read-only user restricted to
  `gold/*`, stored only in the hosting platform's secrets.
