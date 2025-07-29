from typing import Any

import mcpf_core.core.routines as routines
import mcpf_core.func.constants as constants
import pandas as pd

from mcpf_xform.pd import helper


def vertical_concatenation(data: dict[str, Any]) -> dict[str, Any]:
    """
    It appends its input pandas dataframe to another dataframe.
    Yaml args:
        'input':            it is a label in "data", which identifies the input data
                            (given in terms of pandas dataframe),
                            by default it is the value identified with the label
                            constants.DEFAULT_IO_DATA_LABEL (if it is a string)
    'left_value':           it is a label in "data", which identifies the pandas dataframe
                            in "data" to which the input dataframe will be appended.
    'reset_index': False
    'drop_duplicates': False
    'columns_to_check": None

    Returns in data:
        'output':   Not implemented yet!
                    it should be  a label in 'data' which identifies the output
                    (the content of the input pandas dataframe in pandas dataframe),
                    by default it is constants.DEFAULT_IO_DATA_LABEL
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "left_value": None,
        "reset_index": False,
        "drop_duplicates": False,
        "columns_to_check": None,
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input"] = iterator

    if "left_value" in arg and "input" in arg and data[arg["input"]] is not None:
        if arg["left_value"] not in data:
            data[arg["left_value"]] = data[arg["input"]]
            if arg["drop_duplicates"]:
                helper.drop_duplicates_inplace(data[arg["left_value"]], arg["columns_to_check"])
                if arg["reset_index"]:
                    data[arg["left_value"]].reset_index(inplace=True, drop=True)
        elif arg["reset_index"]:
            data[arg["left_value"]] = pd.concat([data[arg["left_value"]], data[arg["input"]]], ignore_index=False)
            if arg["drop_duplicates"]:
                helper.drop_duplicates_inplace(data[arg["left_value"]], arg["columns_to_check"])
                data[arg["left_value"]].reset_index(inplace=True, drop=True)
            else:
                data[arg["left_value"]].reset_index(inplace=True, drop=True)
        else:
            data[arg["left_value"]] = pd.concat([data[arg["left_value"]], data[arg["input"]]], ignore_index=True)
            if arg["drop_duplicates"]:
                helper.drop_duplicates_inplace(data[arg["left_value"]], arg["columns_to_check"])

    routines.set_meta_in_data(data, meta)
    return data


def interpolate_first_column(data: dict[str, Any]) -> dict[str, Any]:
    """
    Interpolates missing values in spectral response help table.

    Returns:
        pd.DataFrame: DataFrame with missing values interpolated.
    """
    # general code part 2/1
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "output": constants.DEFAULT_IO_DATA_LABEL,
        "step": 1,
        "preserve": False,
    }
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input"] = iterator
    if data[arg["input"]] is None:
        data[arg["output"]] = data[arg["input"]]
    else:
        preserve_commas = arg["preserve"]
        last_real_value = 0
        input_table = data[arg["input"]]
        columns = input_table.columns
        first_df_value = input_table[columns[0]].iloc[0]
        last_df_value = input_table[columns[0]].iloc[len(input_table) - 1]

        # Create new index range
        new_index = range(first_df_value, last_df_value + 1, 5)

        # Create new DataFrame with new index
        new_spectral_response_help_table = pd.DataFrame({columns[0]: new_index})

        # Sort new DataFrame by index in descending order
        new_spectral_response_help_table = new_spectral_response_help_table.sort_values(
            by=[columns[0]], ascending=False
        )

        # Initialize list to store interpolated values
        new_values = []

        # Iterate through rows of new DataFrame
        for row in new_spectral_response_help_table[columns[0]]:
            # Check if row index is greater than 840
            if row > 840:
                new_values.append(0)
                continue

            # Lookup value in original table
            value = helper.vlookup(float(row), input_table, 1, 2, preserve=preserve_commas)

            # If non-zero value found, append and update last real value
            if value != 0:
                new_values.append(value)
                last_real_value = value
                continue

            # If value is zero, interpolate
            next_real_value = 0
            i = 1
            while next_real_value == 0:
                next_real_value = helper.vlookup(float(row - i), input_table, 1, 2, preserve=preserve_commas)
                i += 1
            value = ((next_real_value + (last_real_value / 1000)) / 2) * 1000
            new_values.append(value)
            last_real_value = value

        # Assign interpolated values to new DataFrame
        new_spectral_response_help_table[columns[1]] = new_values

        # Sort new DataFrame by index in ascending order
        new_spectral_response_help_table = new_spectral_response_help_table.sort_values(by=[columns[0]], ascending=True)

        data[arg["output"]] = new_spectral_response_help_table

    routines.set_meta_in_data(data, meta)
    return data
