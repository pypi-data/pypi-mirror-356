from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Optional, Union

import pandas as pd

import dbnl.sdk.core as dbnl_core
from dbnl.errors import DBNLInputValidationError
from dbnl.print_logging import dbnl_logger
from dbnl.sdk.models import Project, Run, RunQuery, RunSchema, RunSchemaMetric
from dbnl.sdk.validate import validate_column_data, validate_scalar_data

from .metrics.metric import Metric


def evaluate(*, df: pd.DataFrame, metrics: Sequence[Metric], inplace: bool = False) -> pd.DataFrame:
    """
    Evaluates a set of metrics on a dataframe, returning an augmented dataframe.

    :param df: input dataframe
    :param metrics: metrics to compute
    :param inplace: whether to modify the input dataframe in place
    :return: input dataframe augmented with metrics
    """

    items = {}
    dbnl_logger.info("Evaluating metrics:")
    for m in metrics:
        # how to make info end with space and not new line
        dbnl_logger.info(m.name())
        if m.name() in df:
            raise ValueError(f"Cannot add metric {m.name()}, column already exists in dataframe.")
        items[m.name()] = m.evaluate(df)
    dbnl_logger.info("Done evaluating metrics.")

    augmented_portion_df = pd.DataFrame(items)
    augmented_portion_df.index = df.index

    if inplace:
        df[augmented_portion_df.columns] = augmented_portion_df
        return df
    else:
        return pd.concat([df, augmented_portion_df], axis=1)


def create_run_schema_from_results(
    *,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    index: Optional[list[str]] = None,
    metrics: Optional[Sequence[Metric]] = None,
) -> RunSchema:
    """
    Create a new RunSchema from column results, scalar results, and metrics.

    This function assumes that the metrics have already been evaluated on the original, un-augmented data.
    In other words, the column data for the metrics should also be present in the `column_data`.

    :param column_data: DataFrame with the results for the columns
    :param scalar_data: Dictionary or DataFrame with the results for the scalars, defaults to None
    :param index: List of column names that are the unique identifier, defaults to None
    :param metrics: List of metrics to report with the run, defaults to None

    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: RunSchema with the desired schema for columns and scalars, if provided
    """
    run_schema = dbnl_core.create_run_schema_from_results(column_data=column_data, scalar_data=scalar_data, index=index)
    columns = run_schema.columns

    metric_mapping = {metric.name(): metric for metric in metrics} if metrics else {}
    seen_inputs = set()

    for c in columns:
        if c.name in metric_mapping:
            metric = metric_mapping[c.name]
            if metric.type() != c.type:
                raise DBNLInputValidationError(
                    f"Metric '{metric.name()}' has a different data type than column '{c.name}': {metric.type()} != {c.type}"
                )
            metric_inputs = metric.inputs()
            seen_inputs.update(metric_inputs)
            metric_dict = RunSchemaMetric(inputs=metric_inputs)
            c.metric = metric_dict
            del metric_mapping[c.name]

    if metric_mapping:
        raise DBNLInputValidationError(
            f"The following metrics were not found in the column data: {list(metric_mapping.keys())}"
        )

    non_derived_inputs = set(c.name for c in columns if c.metric is None)
    if not seen_inputs.issubset(non_derived_inputs):
        raise DBNLInputValidationError(
            f"The following inputs for the provided metrics were not found in the column data: {list(seen_inputs - set(c.name for c in columns if c.metric is not None))}"
        )

    return run_schema


@dbnl_core.validate_login
def report_run_with_results(
    *,
    project: Project,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    display_name: Optional[str] = None,
    index: Optional[list[str]] = None,
    run_schema: Optional[RunSchema] = None,
    metadata: Optional[dict[str, str]] = None,
    metrics: Optional[Sequence[Metric]] = None,
    wait_for_close: bool = True,
) -> Run:
    """
    Create a new Run, report results to it, and close it.

    If run_schema is not provided, a RunSchema will be created from the data.
    If a run_schema is provided, the results are validated against it.

    If `metrics` are provided, they are evaluated on the column data before reporting.

    :param project: DBNL Project to create the Run for
    :param column_data: DataFrame with the results for the columns
    :param scalar_data: Dictionary or DataFrame with the results for the scalars, if any. Defaults to None
    :param display_name: Display name for the Run, defaults to None.
    :param index: List of column names that are the unique identifier, defaults to None. Only used when creating a new schema.
    :param run_schema: RunSchema to use for the Run, defaults to None.
    :param metadata: Additional key:value pairs user wants to track, defaults to None
    :param metrics: List of metrics to report with the run, defaults to None
    :param wait_for_close: If True, the function will block for up to 3 minutes until the Run is closed, defaults to True

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Run, after reporting results and closing it
    """
    if metrics:
        column_data = evaluate(df=column_data, metrics=metrics)

    if run_schema is None:
        run_schema = create_run_schema_from_results(
            column_data=column_data, scalar_data=scalar_data, index=index, metrics=metrics
        )
    validate_column_data(column_data, run_schema.columns, run_schema.index)
    if scalar_data is not None:
        if isinstance(scalar_data, dict):
            scalar_data = pd.DataFrame([scalar_data])
        validate_scalar_data(scalar_data, run_schema.scalars)

    run = dbnl_core.create_run(project=project, run_schema=run_schema, display_name=display_name, metadata=metadata)
    dbnl_core.report_results(run=run, column_data=column_data, scalar_data=scalar_data)
    dbnl_core.close_run(run=run, wait_for_close=wait_for_close)
    return run


@dbnl_core.validate_login
def report_run_with_results_and_start_test_session(
    *,
    project: Project,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    display_name: Optional[str] = None,
    index: Optional[list[str]] = None,
    run_schema: Optional[RunSchema] = None,
    metadata: Optional[dict[str, str]] = None,
    baseline: Optional[Union[Run, RunQuery]] = None,
    include_tags: Optional[list[str]] = None,
    exclude_tags: Optional[list[str]] = None,
    require_tags: Optional[list[str]] = None,
    metrics: Optional[Sequence[Metric]] = None,
) -> Run:
    """
    Create a new Run, report results to it, and close it. Start a TestSession with the given inputs.
    If `metrics` are provided, they are evaluated on the column data before reporting.

    :param project: DBNL Project to create the Run for
    :param column_data: DataFrame with the results for the columns
    :param scalar_data: Dictionary or DataFrame with the scalar results to report to DBNL, defaults to None.
    :param display_name: Display name for the Run, defaults to None.
    :param index: List of column names that are the unique identifier, defaults to None. Only used when creating a new schema.
    :param run_schema: RunSchema to use for the Run, defaults to None.
    :param metadata: Additional key:value pairs user wants to track, defaults to None
    :param baseline: DBNL Run or RunQuery to use as the baseline run, defaults to None. If None, the baseline defined in the TestConfig is used.
    :param include_tags: List of Test Tag names to include in the Test Session
    :param exclude_tags: List of Test Tag names to exclude in the Test Session
    :param require_tags: List of Test Tag names to require in the Test Session
    :param metrics: List of metrics to report with the run, defaults to None

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Run, after reporting results and closing it
    """
    run = report_run_with_results(
        project=project,
        column_data=column_data,
        scalar_data=scalar_data,
        display_name=display_name,
        index=index,
        run_schema=run_schema,
        metadata=metadata,
        metrics=metrics,
        wait_for_close=True,  # we must wait for the run to close before starting the test session
    )
    dbnl_core.create_test_session(
        experiment_run=run,
        baseline=baseline,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        require_tags=require_tags,
    )
    return run
