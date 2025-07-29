from typing import Any

import mcpf_core.core.routines as routines
from mcpf_core.core.decorators import with_default_arguments
from mcpf_core.func import constants


def set_default_input_from_variable(data: dict[str, Any]) -> dict[str, Any]:
    """
    It sets the value of the label constants.DEFAULT_IO_DATA_LABEL in "data"
    Yaml args:
             'input_label': It is a label in "data", whose value will be referenced by
             the other label constants.DEFAULT_IO_DATA_LABEL as well.
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {"input_label": constants.DEFAULT_IO_DATA_LABEL}
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input_label"] = iterator

    data[constants.DEFAULT_IO_DATA_LABEL] = data[arg["input_label"]]
    routines.set_meta_in_data(data, meta)
    return data


def remove_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    It removes a label (with its referenced value) from "data"
    Yaml args:
             'input':   It is a label in "data", which will be removed from "data",
                        by default it is constants.DEFAULT_IO_DATA_LABEL.
    """
    iterator = routines.pop_loop_iterator()
    meta = routines.get_meta_data(data)
    # default_arguments_values
    arg = {"input": constants.DEFAULT_IO_DATA_LABEL}
    # merging default values with current argument values
    if meta[constants.ARGUMENTS]:
        arg = arg | meta[constants.ARGUMENTS]
    # if the function part of a loop
    if iterator:
        arg["input"] = iterator
    del data[arg["input"]]

    routines.set_meta_in_data(data, meta)
    return data


@with_default_arguments(
    {
        "separator": " ",
        "range_from": "",
        "range_to": "",
        "range_step": "1",
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "values": "",
    }
)
def set_iterator_values(data, has_iterated_value: bool, iterated_value: Any, arg: dict[str, Any]) -> dict[str, Any]:
    if has_iterated_value:
        arg["input"] = iterated_value
    if arg["range_from"]:
        start = int(arg["range_from"])
        try:
            end = int(arg["range_to"])
        except ValueError as e:
            raise ValueError("Invalid 'range_to' value: " + arg["range_to"])
        try:
            step = int(arg["range_step"])
        except ValueError as e:
            raise ValueError("Invalid 'range_step' value: " + arg["range_step"])
        list_of_iterators = range(start, end, step)
    elif arg["values"]:
        if isinstance(arg["values"], list):
            list_of_iterators = arg["values"]
        elif isinstance(arg["values"], str):
            list_of_iterators = arg["values"].split(arg["separator"])
        else:
            list_of_iterators = []
    elif isinstance(data[arg["input"]], list):
        list_of_iterators = data[arg["input"]]
    elif isinstance(data[arg["input"]], str):
        list_of_iterators = data[arg["input"]].split(arg["separator"])
    else:
        list_of_iterators = []
    routines.register_loop_iterator_list(list_of_iterators)
    return data


@with_default_arguments(
    {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "output": constants.DEFAULT_IO_DATA_LABEL,
        "operand_content": None,
        "operand_name": "x",
        "condition": "False",
        "hijacked_output": constants.DEFAULT_IO_DATA_LABEL,
    }
)
def hijack_flow(data, has_iterated_value: bool, iterated_value: Any, arg: dict[str, Any]) -> dict[str, Any]:
    if has_iterated_value:
        # TODO this does not work as expected. While the input data changes with each
        # iteraton, the operand_content remains stable, i.e. you compare every iterated
        # element with the same condition. This may be intended but it doesn't make sense
        # as the invariant portion of the condition is already specified by the lambda
        # function, and the argument (the 'operand_content') would be expected to change
        # with each iteration.
        arg["input"] = iterated_value
    # TODO consider how to harden parsing Python language constructs
    lambda_func_string = "lambda " + arg["operand_name"] + ": " + arg["condition"]
    if arg["operand_content"] in data:
        try:
            lambda_func = eval(lambda_func_string)
            if lambda_func(data[arg["operand_content"]]):
                data[arg["hijacked_output"]] = data[arg["input"]]
                if arg["hijacked_output"] != arg["output"]:
                    data[arg["output"]] = None
            else:
                data[arg["output"]] = data[arg["input"]]
                if arg["hijacked_output"] != arg["output"]:
                    data[arg["hijacked_output"]] = None
        except:
            data[arg["output"]] = data[arg["input"]]
    else:
        data[arg["output"]] = data[arg["input"]]
    return data


@with_default_arguments(
    {
        "input": constants.DEFAULT_IO_DATA_LABEL,
        "output": constants.DEFAULT_IO_DATA_LABEL,
        "new_label": "NEW",
    }
)
def duplicate_data(data, has_iterated_value: bool, iterated_value: Any, arg: dict[str, Any]) -> dict[str, Any]:
    value = data[arg["input"]]
    if has_iterated_value:
        value = iterated_value

    data[arg["output"]] = value
    data[arg["new_label"]] = value
    return data
