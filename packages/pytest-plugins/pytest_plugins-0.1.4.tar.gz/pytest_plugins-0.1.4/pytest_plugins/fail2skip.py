import logging
from typing import Any

import pytest
from _pytest.config import Config, Parser
from _pytest.python import Function

from pytest_plugins.add_better_report import test_results
from pytest_plugins.models import ExecutionStatus
from pytest_plugins.pytest_helper import get_test_full_name, flag_is_enabled

logger = logging.getLogger("pytest_plugins.fail2skip")


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--fail2skip-enable",
        action="store_true",
        default=False,
        help="Enable converting failed tests marked with @pytest.mark.fail2skip into skipped.",
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line(
        "markers", "fail2skip: convert failed test to skip instead of fail"
    )
    config._fail2skip_enabled = config.getoption("--fail2skip-enable")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: Function, call: Any):
    outcome = yield
    report = outcome.get_result()
    if (
        item.get_closest_marker("fail2skip")
        and call.when == "call"
        and report.outcome == "failed"
        and item.config.getoption("--fail2skip-enable")
    ):
        report.outcome = "skipped"
        report.longrepr = "fail2skip: forcibly skipped after failure"
        report.wasxfail = "fail2skip"
        test_results[get_test_full_name(item=item)].test_status = ExecutionStatus.FAILED_SKIPPED
    return report
