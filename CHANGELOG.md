# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-09

### Added
- Project scaffold: `src/` package layout, module skeletons for every pipeline stage
- Tooling: uv (locked dependencies), ruff (lint + format), mypy, pytest + coverage, poethepoet tasks
- Pre-commit hooks including secret scanning
- CI workflow (lint, format check, type check, tests, secret scan) on every push and PR
- Dependabot, PR template, issue templates
- Documentation: README, architecture, data dictionary, runbook, ADRs 0001–0004
