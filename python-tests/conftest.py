import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "extra: tests that currently fail and require the --run-extra flag to run"
    )


def pytest_addoption(parser):
    parser.addoption(
        "--run-extra",
        action="store_true",
        default=False,
        help="Run tests marked 'extra' (currently failing / require extra setup)",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-extra"):
        return
    skip_extra = pytest.mark.skip(reason="needs --run-extra option to run")
    for item in items:
        if "extra" in item.keywords:
            item.add_marker(skip_extra)
