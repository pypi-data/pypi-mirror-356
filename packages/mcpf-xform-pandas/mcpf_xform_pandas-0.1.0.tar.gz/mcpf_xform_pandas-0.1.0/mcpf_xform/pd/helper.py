from typing import Any

import pandas as pd


def drop_duplicates_inplace(df: pd.DataFrame, list_of_columns_position: list[int]) -> None:
    if list_of_columns_position and isinstance(list_of_columns_position, list) and len(list_of_columns_position) > 0:
        df.drop_duplicates(
            inplace=True,
            keep="first",
            subset=[x if x in df.columns else df.columns[x] for x in list_of_columns_position],
        )
    else:
        df.drop_duplicates(inplace=True, keep="first")


def vlookup(
    search_value: float, table: pd.DataFrame, index_column: int, target_column: int, preserve: bool = False
) -> Any:
    """
    Performs a vertical lookup (similar to Excel's VLOOKUP function) to find a value in a DataFrame.

    Args:
        search_value (float): The value to search for in the index column.
        table (pd.DataFrame): The DataFrame containing the data.
        index_column (int): The one-based index (column number) to search within.
        target_column (int): The one-based column number from which to retrieve the value.
        preserve (bool): If True, preserves the original DataFrame. Otherwise
                    replaces German kommas with dots and force converts any cells to float.
                    Defaults to False.

    Returns:
        float: The value found in the target column corresponding to the search value.
                If the search value is not found, returns 0.
        If preserve is True and the search value is not found, returns None.
        Otherwise, returns the value of the actual data type.
    """
    # Get column names
    columns = table.columns

    # Get the name of the index column and target column
    index_column_name = columns[index_column - 1]
    target_column_name = columns[target_column - 1]

    # Convert ',' to '.' and convert to float
    if not preserve:
        table = table.replace(",", ".", regex=True).astype(float)

    # Set index to the index column
    table.set_index(index_column_name, inplace=True)

    try:
        # Lookup the search value in the index column
        result = table.loc[search_value]
        # Retrieve the value from the target column
        value = result[target_column_name]
    except KeyError:
        # If search value not found, return 0
        if preserve:
            value = None
        else:
            value = 0

    return value
