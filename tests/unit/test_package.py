"""Smoke tests for the package itself."""

import re

import smogwatch


def test_version_is_semver() -> None:
    """The package exposes a semantic version string (used later for data lineage)."""
    assert re.fullmatch(r"\d+\.\d+\.\d+", smogwatch.__version__)


def test_package_imports_all_stages() -> None:
    """Every pipeline stage module is importable (catches packaging mistakes early)."""
    import importlib

    for name in [
        "smogwatch.settings",
        "smogwatch.manifest",
        "smogwatch.geo.geohash",
        "smogwatch.geo.grid",
        "smogwatch.extract.open_meteo",
        "smogwatch.transform.clean",
        "smogwatch.transform.aqi",
        "smogwatch.transform.catalog",
        "smogwatch.validate.schemas",
        "smogwatch.validate.checks",
        "smogwatch.load.paths",
        "smogwatch.load.storage",
        "smogwatch.flows.hourly",
        "smogwatch.flows.backfill",
        "smogwatch.flows.freshness",
    ]:
        assert importlib.import_module(name) is not None
