from __future__ import annotations

import asyncio
import logging
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import StrEnum
from functools import total_ordering
from pathlib import Path
from typing import ClassVar

from ask_shell.rich_progress import new_task
from model_lib import Entity
from pydantic import Field, model_validator
from zero_3rdparty import datetime_utils, file_utils
from zero_3rdparty.iter_utils import group_by_once

from atlas_init.cli_tf.github_logs import summary_dir
from atlas_init.cli_tf.go_test_run import GoTestRun, GoTestStatus
from atlas_init.cli_tf.go_test_tf_error import GoTestError, GoTestErrorClass, GoTestErrorClassification
from atlas_init.crud.mongo_dao import init_mongo_dao
from atlas_init.settings.env_vars import AtlasInitSettings

logger = logging.getLogger(__name__)
_COMPLETE_STATUSES = {GoTestStatus.PASS, GoTestStatus.FAIL}


@total_ordering
class GoTestSummary(Entity):
    name: str
    results: list[GoTestRun] = Field(default_factory=list)

    @model_validator(mode="after")
    def sort_results(self):
        self.results.sort()
        return self

    @property
    def total_completed(self) -> int:
        return sum((r.status in _COMPLETE_STATUSES for r in self.results), 0)

    @property
    def success_rate(self) -> float:
        total = self.total_completed
        if total == 0:
            logger.warning(f"No results to calculate success rate for {self.name}")
            return 0
        return sum(r.status == "PASS" for r in self.results) / total

    @property
    def is_skipped(self) -> bool:
        return all(r.status == GoTestStatus.SKIP for r in self.results)

    @property
    def success_rate_human(self) -> str:
        return f"{self.success_rate:.2%}"

    @property
    def group_name(self) -> str:
        return next((r.group_name for r in self.results if r.group_name), "unknown-group")

    def last_pass_human(self) -> str:
        return next(
            (f"Passed {test.when}" for test in reversed(self.results) if test.status == GoTestStatus.PASS),
            "never passed",
        )

    def __lt__(self, other) -> bool:
        if not isinstance(other, GoTestSummary):
            raise TypeError
        return (self.success_rate, self.name) < (other.success_rate, other.name)

    def select_tests(self, date: date) -> list[GoTestRun]:
        return [r for r in self.results if r.ts.date() == date]


def summary_str(summary: GoTestSummary, start_date: datetime, end_date: datetime) -> str:
    return "\n".join(
        [
            f"## {summary.name}",
            f"Success rate: {summary.success_rate_human}",
            "",
            "### Timeline",
            *timeline_lines(summary, start_date, end_date),
            "",
            *failure_details(summary),
        ]
    )


def timeline_lines(summary: GoTestSummary, start_date: datetime, end_date: datetime) -> list[str]:
    lines = []
    one_day = timedelta(days=1)
    for active_date in datetime_utils.day_range(start_date.date(), (end_date + one_day).date(), one_day):
        active_tests = summary.select_tests(active_date)
        if not active_tests:
            lines.append(f"{active_date:%Y-%m-%d}: MISSING")
            continue

        tests_str = ", ".join(format_test_oneline(t) for t in active_tests)
        lines.append(f"{active_date:%Y-%m-%d}: {tests_str}")
    return lines


def failure_details(summary: GoTestSummary) -> list[str]:
    lines = ["## Failures"]
    for test in summary.results:
        if test.status == GoTestStatus.FAIL:
            lines.extend(
                (
                    f"### {test.when} {format_test_oneline(test)}",
                    test.finish_summary(),  # type: ignore
                    "",
                )
            )
    return lines


def format_test_oneline(test: GoTestRun) -> str:
    return f"[{test.status} {test.runtime_human}]({test.url})"  # type: ignore


def create_detailed_summary(
    summary_name: str,
    end_test_date: datetime,
    start_test_date: datetime,
    test_results: dict[str, list[GoTestRun]],
    expected_names: set[str] | None = None,
) -> list[str]:
    summary_dir_path = summary_dir(summary_name)
    if summary_dir_path.exists():
        file_utils.clean_dir(summary_dir_path)
    summaries = [GoTestSummary(name=name, results=runs) for name, runs in test_results.items()]
    top_level_summary = ["# SUMMARY OF ALL TESTS name (success rate)"]
    summaries = [summary for summary in summaries if summary.results and not summary.is_skipped]
    if expected_names and (skipped_names := expected_names - {summary.name for summary in summaries}):
        logger.warning(f"skipped test names: {'\n'.join(skipped_names)}")
        top_level_summary.append(f"Skipped tests: {', '.join(skipped_names)}")
    for summary in sorted(summaries):
        test_summary_path = summary_dir_path / f"{summary.success_rate_human}_{summary.name}.md"
        test_summary_md = summary_str(summary, start_test_date, end_test_date)
        file_utils.ensure_parents_write_text(test_summary_path, test_summary_md)
        top_level_summary.append(
            f"- {summary.name} - {summary.group_name} ({summary.success_rate_human}) ({summary.last_pass_human()}) ('{test_summary_path}')"
        )
    return top_level_summary


def create_short_summary(test_results: dict[str, list[GoTestRun]], failing_names: list[str]) -> list[str]:
    summary = ["# SUMMARY OF FAILING TESTS"]
    summary_fail_details: list[str] = ["# FAIL DETAILS"]

    for fail_name in failing_names:
        fail_tests = test_results[fail_name]
        summary.append(f"- {fail_name} has {len(fail_tests)} failures:")
        summary.extend(
            f"  - [{fail_run.when} failed in {fail_run.runtime_human}]({fail_run.url})"  # type: ignore
            for fail_run in fail_tests
        )
        summary_fail_details.append(f"\n\n ## {fail_name} details:")
        summary_fail_details.extend(f"```\n{fail_run.finish_summary()}\n```" for fail_run in fail_tests)  # type: ignore
    logger.info("\n".join(summary_fail_details))
    return summary


@dataclass
class GoRunTestReport:
    summary: str
    error_details: str


def create_test_report(
    runs: list[GoTestRun],
    errors: list[GoTestError],
    *,
    indent_size=2,
    max_runs=20,
    env_name: str = "",
) -> GoRunTestReport:
    if env_name:
        runs = [run for run in runs if run.env == env_name]
        errors = [error for error in errors if error.run.env == env_name]
    single_indent = " " * indent_size
    if not runs:
        return GoRunTestReport(
            summary="No test runs found",
            error_details="",
        )
    envs = {run.env for run in runs if run.env}
    lines = [summary_line(runs, errors)]
    if errors:
        env_name_str = f" in {env_name}" if env_name else ""
        lines.append(f"\n\n## Errors Overview{env_name_str}")
        lines.extend(error_overview_lines(errors, single_indent))
    for env in envs:
        env_runs = [run for run in runs if run.env == env]
        lines.append(f"\n\n## {env.upper()} Had {len(env_runs)} Runs")
        lines.extend(env_summary_lines(env_runs, max_runs, single_indent))
    if len(envs) > 1:
        lines.append(f"\n\n## All Environments Had {len(runs)} Runs")
        lines.extend(env_summary_lines(runs, max_runs, single_indent))
    error_detail_lines = []
    if errors:
        error_detail_lines.append("# Errors Details")
        error_detail_lines.extend(error_details(errors, include_env=len(envs) > 1))
    return GoRunTestReport(
        summary="\n".join(lines),
        error_details="\n".join(error_detail_lines),
    )


def summary_line(runs: list[GoTestRun], errors: list[GoTestError]):
    run_delta = GoTestRun.run_delta(runs)
    envs = {run.env for run in runs if run.env}
    pkg_test_names = {run.name_with_package for run in runs}
    skipped = sum(run.status == GoTestStatus.SKIP for run in runs)
    passed = sum(run.status == GoTestStatus.PASS for run in runs)
    envs_str = ", ".join(sorted(envs))
    branches = {run.branch for run in runs if run.branch}
    branches_str = (
        "from " + ", ".join(sorted(branches)) + " branches" if len(branches) > 1 else f"from {branches.pop()} branch"
    )
    return f"# Found {len(runs)} TestRuns in {envs_str} {run_delta} {branches_str}: {len(pkg_test_names)} unique tests, {len(errors)} Errors, {skipped} Skipped, {passed} Passed"


def error_overview_lines(errors: list[GoTestError], single_indent: str) -> list[str]:
    lines = []
    grouped_errors = GoTestError.group_by_classification(errors)
    if errors_unclassified := grouped_errors.unclassified:
        lines.append(f"- Found {len(grouped_errors.unclassified)} unclassified errors:")
        lines.extend(count_errors_by_test(single_indent, errors_unclassified))
    if errors_by_class := grouped_errors.classified:
        for classification, errors in errors_by_class.items():
            lines.append(f"- Error Type `{classification}`:")
            lines.extend(count_errors_by_test(single_indent, errors))
    return lines


def count_errors_by_test(indent: str, errors: list[GoTestError]) -> list[str]:
    lines: list[str] = []
    counter = Counter()
    for error in errors:
        counter[error.header(use_ticks=True)] += 1
    for error_header, count in counter.most_common():
        if count > 1:
            lines.append(f"{indent}- {count} x {error_header}")
        else:
            lines.append(f"{indent}- {error_header}")
    return sorted(lines)


def env_summary_lines(env_runs: list[GoTestRun], max_runs: int, single_indent: str) -> list[str]:
    lines: list[str] = []
    if pass_rates := GoTestRun.lowest_pass_rate(env_runs, max_tests=max_runs, include_single_run=False):
        lines.append(f"- Lowest pass rate: {GoTestRun.run_delta(env_runs)}")
        for pass_rate, name, name_tests in pass_rates:
            ran_count_str = f"ran {len(name_tests)} times" if len(name_tests) > 1 else "ran 1 time"
            if last_pass := GoTestRun.last_pass(name_tests):
                lines.append(f"{single_indent}- {pass_rate:.2%} {name} ({ran_count_str}) last PASS {last_pass}")
            else:
                lines.append(f"{single_indent}- {pass_rate:.2%} {name} ({ran_count_str}) never passed")
    if pass_stats := GoTestRun.last_pass_stats(env_runs, max_tests=max_runs):
        lines.append(f"- Longest time since `{GoTestStatus.PASS}`: {GoTestRun.run_delta(env_runs)}")
        lines.extend(
            f"{single_indent}- {pass_stat.pass_when} {pass_stat.name_with_package}" for pass_stat in pass_stats
        )
    lines.append(f"- Slowest tests: {GoTestRun.run_delta(env_runs)}")
    for time_stat in GoTestRun.slowest_tests(env_runs):
        avg_time_str = (
            f"(avg = {time_stat.average_duration} across {len(time_stat.runs)} runs)"
            if time_stat.average_seconds
            else ""
        )
        lines.append(
            f"{single_indent}- {time_stat.slowest_duration} {time_stat.name_with_package} {avg_time_str}".rstrip()
        )
    return lines


def error_details(errors: list[GoTestError], include_env: bool) -> list[str]:
    lines: list[str] = []
    for name, name_errors in GoTestError.group_by_name_with_package(errors).items():
        lines.append(
            f"## {name} had {len(name_errors)} errors {GoTestRun.run_delta([error.run for error in name_errors])}",
        )
        for error in sorted(name_errors, reverse=True):  # newest first
            env_str = f" in {error.run.env} " if include_env and error.run.env else ""
            lines.extend(
                [
                    f"### Started @ {error.run.ts} {env_str}ran for ({error.run.runtime_human})",
                    f"- error classes: bot={error.bot_error_class}, human={error.human_error_class}",
                    f"- details summary: {error.short_description}",
                    f"- test output:\n```log\n{error.run.output_lines_str}\n```\n",
                ]
            )
    return lines


class TFCITestOutput(Entity):
    """Represent the CI Test Output for a day"""

    log_paths: list[Path] = Field(
        default_factory=list, description="Paths to the log files of the test runs analyzed by the run history."
    )
    found_tests: list[GoTestRun] = Field(default_factory=list, description="All tests for report day.")
    found_errors: list[GoTestError] = Field(default_factory=list, description="All errors for the report day.")
    classified_errors: list[GoTestErrorClassification] = Field(
        default_factory=list, description="Classified errors for the report day."
    )


class DailyReportIn(Entity):
    report_date: datetime
    run_history_start: datetime
    run_history_end: datetime
    env_filter: list[str] = field(default_factory=list)
    skip_branch_filter: bool = False
    skip_columns: set[ErrorRowColumns] = field(default_factory=set)


class DailyReportOut(Entity):
    summary_md: str
    details_md: str


def create_daily_report(output: TFCITestOutput, settings: AtlasInitSettings, event: DailyReportIn) -> DailyReportOut:
    errors = output.found_errors
    error_classes = {cls.run_id: cls.error_class for cls in output.classified_errors}
    one_line_summary = summary_line(output.found_tests, errors)

    with new_task("Daily Report"):
        with new_task("Collecting error rows") as task:
            failure_rows = asyncio.run(_collect_error_rows(errors, error_classes, settings, event, task))
        if not failure_rows:
            return DailyReportOut(summary_md=f"🎉All tests passed\n{one_line_summary}", details_md="")
    columns = ErrorRowColumns.column_names(failure_rows, event.skip_columns)
    summary_md = [
        "# Daily Report",
        one_line_summary,
        "",
        "## Errors Table",
        " | ".join(columns),
        " | ".join("---" for _ in columns),
        *(" | ".join(row.as_row(columns)) for row in failure_rows),
    ]
    return DailyReportOut(summary_md="\n".join(summary_md), details_md="TODO")


class ErrorRowColumns(StrEnum):
    GROUP_NAME = "Group or Package"
    TEST = "Test"
    ERROR_CLASS = "Error Class"
    DETAILS_SUMMARY = "Details Summary"
    PASS_RATE = "Pass Rate"  # nosec B105 # This is not a security issue, just a column name
    TIME_SINCE_PASS = "Time Since PASS"  # nosec B105 # This is not a security issue, just a column name

    __ENV_BASED__: ClassVar[list[str]] = [PASS_RATE, TIME_SINCE_PASS]

    @classmethod
    def column_names(cls, rows: list[ErrorRow], skip_columns: set[ErrorRowColumns]) -> list[str]:
        if not rows:
            return []
        envs = set()
        for row in rows:
            envs.update(row.last_env_runs.keys())
        columns: list[str] = [cls.GROUP_NAME, cls.TEST, cls.ERROR_CLASS, cls.DETAILS_SUMMARY]
        for env in sorted(envs):
            columns.extend(f"{env_col} ({env})" for env_col in cls.__ENV_BASED__ if env_col not in skip_columns)
        return [col for col in columns if col not in skip_columns]


@total_ordering
class ErrorRow(Entity):
    group_name: str
    package_url: str
    test_name: str
    error_class: GoTestErrorClass
    details_summary: str
    last_env_runs: dict[str, list[GoTestRun]] = field(default_factory=dict)

    def __lt__(self, other) -> bool:
        if not isinstance(other, ErrorRow):
            raise TypeError
        return (self.group_name, self.test_name) < (other.group_name, other.test_name)

    @property
    def pass_rates(self) -> dict[str, float]:
        rates = {}
        for env, runs in self.last_env_runs.items():
            if not runs:
                continue
            total = len(runs)
            passed = sum(run.status == GoTestStatus.PASS for run in runs)
            rates[env] = passed / total if total > 0 else 0.0
        return rates

    @property
    def time_since_pass(self) -> dict[str, str]:
        time_since = {}
        for env, runs in self.last_env_runs.items():
            if not runs:
                time_since[env] = "never run"
                continue
            time_since[env] = next(
                (run.when for run in sorted(runs, reverse=True) if run.status == GoTestStatus.PASS), "never pass"
            )
        return time_since

    def as_row(self, columns: list[str]) -> list[str]:
        values = []
        pass_rates = self.pass_rates
        time_since_pass = self.time_since_pass
        for col in columns:
            match col:
                case ErrorRowColumns.GROUP_NAME:
                    values.append(self.group_name or self.package_url or "Unknown Group")
                case ErrorRowColumns.TEST:
                    values.append(self.test_name)
                case ErrorRowColumns.ERROR_CLASS:
                    values.append(self.error_class)
                case ErrorRowColumns.DETAILS_SUMMARY:
                    values.append(self.details_summary)
                case s if s.startswith(ErrorRowColumns.PASS_RATE):
                    env = s.split(" (")[-1].rstrip(")")
                    env_pass_rate = pass_rates.get(env, 0.0)
                    env_run_count = len(self.last_env_runs.get(env, []))
                    values.append(f"{env_pass_rate:.2%} ({env_run_count} runs)" if env in pass_rates else "N/A")
                case s if s.startswith(ErrorRowColumns.TIME_SINCE_PASS):
                    env = s.split(" (")[-1].rstrip(")")
                    values.append(time_since_pass.get(env, "never passed"))
                case _:
                    logger.warning(f"Unknown column: {col}, skipping")
                    values.append("N/A")
        return values


async def _collect_error_rows(
    errors: list[GoTestError],
    error_classes: dict[str, GoTestErrorClass],
    settings: AtlasInitSettings,
    event: DailyReportIn,
    task: new_task,
) -> list[ErrorRow]:
    error_rows: list[ErrorRow] = []
    dao = await init_mongo_dao(settings)
    for error in errors:
        package_url = error.run.package_url
        group_name = error.run.group_name
        package_url = error.run.package_url or ""
        error_class = error_classes[error.run_id]
        branch = error.run.branch
        branch_filter = []
        if branch and not event.skip_branch_filter:
            branch_filter.append(branch)
        run_history = await dao.read_run_history(
            test_name=error.run_name,
            package_url=package_url,
            group_name=group_name,
            start_date=event.run_history_start,
            end_date=event.run_history_end,
            envs=event.env_filter,
            branches=branch_filter,
        )
        last_env_runs = group_by_once(run_history, key=lambda run: run.env or "unknown-env")
        error_rows.append(
            ErrorRow(
                group_name=group_name,
                package_url=package_url,
                test_name=error.run_name,
                error_class=error_class,
                details_summary=error.short_description,
                last_env_runs=last_env_runs,
            )
        )
        task.update(advance=1)
    return sorted(error_rows)
