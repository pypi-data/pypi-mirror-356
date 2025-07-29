from __future__ import annotations

import pandas as pd

from dbnl.sdk.models import RunSchemaColumnSchema, RunSchemaColumnSchemaDict
from dbnl.sdk.util import get_column_schemas_from_dataframe, get_run_schema_columns_from_dataframe

from .metrics.metric import Metric


def get_column_schemas_from_metrics(metrics: list[Metric]) -> list[RunSchemaColumnSchemaDict]:
    """
    Gets the run schema column schemas from a list of metrics.

    :param metrics: list of metrics to get column schemas from
    :return: list of column schemas for metrics
    """
    return [m.column_schema() for m in metrics]


def get_column_schemas_from_dataframe_and_metrics(
    *,
    df: pd.DataFrame,
    metrics: list[Metric],
) -> list[RunSchemaColumnSchemaDict]:
    """
    Gets the run schema column schemas for a dataframe that was augmented with a list of metrics.

    :param df: Dataframe to get column schemas from
    :param metrics: list of metrics added to the dataframe
    :return: list of columns schemas for dataframe and metrics
    """
    columns: list[RunSchemaColumnSchemaDict] = []
    df_columns_by_name = {c["name"]: c for c in get_column_schemas_from_dataframe(df)}
    metrics_columns_by_name = {c["name"]: c for c in get_column_schemas_from_metrics(metrics)}
    component_strs = {
        metric["component"]
        for metric in metrics_columns_by_name.values()
        if "component" in metric and metric["component"] is not None
    }
    component_names = {c for component in component_strs for c in component.split("__")}
    # Check all provided metrics are in the dataframe.
    for name, _ in metrics_columns_by_name.items():
        if name not in df_columns_by_name:
            raise ValueError(f"Metric {name} was provided, but is missing from dataframe.")
    # Add columns from df, overwriting with metrics column if available.
    for name, df_column in df_columns_by_name.items():
        if name in metrics_columns_by_name:
            columns.append(metrics_columns_by_name[name])
        else:
            # link metric components to source columns
            if name in component_names and df_column.get("component", None) is None:
                df_column["component"] = name
            columns.append(df_column)
    return columns


def get_run_schema_columns_from_metrics(metrics: list[Metric]) -> list[RunSchemaColumnSchema]:
    """
    Gets the run schema column schemas from a list of metrics.

    :param metrics: list of metrics to get column schemas from
    :return: list of column schemas for metrics
    """
    return [m.run_schema_column() for m in metrics]


def get_run_schema_columns_from_dataframe_and_metrics(
    *,
    df: pd.DataFrame,
    metrics: list[Metric],
) -> list[RunSchemaColumnSchema]:
    """
    Gets the run schema column schemas for a dataframe that was augmented with a list of metrics.

    :param df: Dataframe to get column schemas from
    :param metrics: list of metrics added to the dataframe
    :return: list of columns schemas for dataframe and metrics
    """
    columns: list[RunSchemaColumnSchema] = []
    df_columns_by_name = {c.name: c for c in get_run_schema_columns_from_dataframe(df)}
    metrics_columns_by_name = {c.name: c for c in get_run_schema_columns_from_metrics(metrics)}
    component_strs = {
        metric_column.component
        for metric_column in metrics_columns_by_name.values()
        if metric_column.component is not None
    }
    component_names = {c for component in component_strs for c in component.split("__")}

    # Check all provided metrics are in the dataframe.
    for name in metrics_columns_by_name:
        if name not in df_columns_by_name:
            raise ValueError(f"Metric {name} was provided, but is missing from dataframe.")

    # Add columns from df, overwriting with metrics column if available.
    for name, df_column in df_columns_by_name.items():
        if name in metrics_columns_by_name:
            columns.append(metrics_columns_by_name[name])
        else:
            # link metric components to source columns
            if name in component_names and df_column.component is None:
                df_column.component = name
            columns.append(df_column)

    return columns
