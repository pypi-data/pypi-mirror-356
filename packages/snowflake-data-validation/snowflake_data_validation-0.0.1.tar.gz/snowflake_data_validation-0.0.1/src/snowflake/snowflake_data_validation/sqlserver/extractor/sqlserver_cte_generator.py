# Copyright 2025 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from snowflake.snowflake_data_validation.utils.constants import (
    METRIC_COLUMN_KEY,
    NORMALIZATION_COLUMN_KEY,
    TEMPLATE_COLUMN_KEY,
    TYPE_COLUMN_KEY,
)
from snowflake.snowflake_data_validation.utils.context import Context


def generate_cte_query(
    metrics_templates,
    col_name,
    col_type,
    table_name,
    where_clause: str,
    has_where_clause: bool,
    context: Context,
):
    """Generate a Common Table Expression (CTE) SQL query based on the provided data.

    Args:
        metrics_templates (pd.DataFrame): DataFrame containing metrics templates to be applied.
        col_name (str): The name of the column for which the CTE query is being generated.
        col_type (str): The type of the column (e.g., "int", "varchar") used to filter templates.
        table_name (str): The name of the table to be referenced in the CTE query.
        where_clause (str): A WHERE clause to filter the data in the CTE query.
        has_where_clause (bool): A boolean indicating whether the WHERE clause is present.
        context (Context): A context object containing the SQL generator and template environment.

    Returns:
        tuple: A tuple containing:
            - cte_query (str or None): The rendered CTE SQL query as a string, or None if no templates
                                       are found for the given column type.
            - type_category (str or None): A string representing the type category for the CTE, or None
                                           if no templates are found.
            - metrics (list or None): A list of metric names used in the CTE, or None if no templates
                                      are found.

    """
    cte_template = context.sql_generator.env.get_template(
        "sqlserver_columns_cte_template.sql.j2"
    )

    type_category = f"{col_name}"
    metrics_templates_df = metrics_templates[
        (metrics_templates[TYPE_COLUMN_KEY] == col_type.upper())
    ]
    metrics = {}
    for _, row in metrics_templates_df.iterrows():
        metric_name = row[METRIC_COLUMN_KEY]
        metric_query = row[TEMPLATE_COLUMN_KEY].replace("{{ col_name }}", col_name)
        metric_query_normalized = row[NORMALIZATION_COLUMN_KEY].replace(
            "{{ metric_query }}", metric_query
        )
        metrics[metric_name] = metric_query_normalized

    if not metrics:
        # add some logging warning "No templates found for column type: {col_type}"
        return None, None, None

    cte_query = cte_template.render(
        type_category=type_category,
        metrics=metrics,
        table_name=table_name,
        where_clause=where_clause,
        has_where_clause=has_where_clause,
    )

    return cte_query.strip(), type_category, list(metrics.keys())


def generate_outer_query(cte_names, metrics):
    """Generate the outer query that combines the results from all CTEs.

    Args:
        cte_names (list): List of CTE names
        metrics (list): List of available metrics for each CTE

    Returns:
        str: The outer query string

    """
    # Collect all unique metrics across all types
    all_metrics = set()
    for metric_list in metrics:
        all_metrics.update(metric_list)

    union_queries = []

    for cte_name, available_metrics in zip(cte_names, metrics):
        # Determine which metrics to include
        metric_clauses = []
        for metric in all_metrics:
            if metric in available_metrics:
                # We need to have all values with the same type for the UNION ALL to work
                metric_clauses.append(f"CAST({metric} AS VARCHAR(25)) AS {metric}")
            else:
                metric_clauses.append(f"NULL AS {metric}")

        # Build individual SELECT statement for this CTE
        select_query = f"""SELECT
    '{cte_name}' AS COLUMN_VALIDATED,
    {', '.join(metric_clauses)}
FROM {cte_name}"""

        union_queries.append(select_query)

    # Join all queries with UNION ALL
    outer_query = "\n\nUNION ALL\n\n".join(union_queries)
    return outer_query
