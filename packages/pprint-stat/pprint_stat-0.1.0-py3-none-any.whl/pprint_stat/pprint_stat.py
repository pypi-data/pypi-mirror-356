import re

from .data import (
    INT_PATTERN, 
    VALUE_INDENT, 
    FIELD_INDENT, 
    proc_pid_stat_fields
)

def coerce_type(string):
    if re.match(INT_PATTERN, string):
        return "int", string
    else:
        return "string", string

def format_string(type, string) -> str:
    match type:
        case "int":
            return format(int(string), ",")
        case "string":
            return string


def get_values(pid):
    with open(f"/proc/{pid}/stat") as f:
        yield from f.read().split()

def generate_mapping(values):
    mapping = zip(proc_pid_stat_fields, values)
    return mapping

def print_table(field_value_mapping):
    print(format("Field", FIELD_INDENT), format("Value", VALUE_INDENT), end = "\n\n")

    for field, value in field_value_mapping:
        if field == "comm":
            value = value[1:-1]
        val_type, val = coerce_type(value)
        val = format_string(val_type, val)
        print(format(field, FIELD_INDENT), format(val, VALUE_INDENT))


