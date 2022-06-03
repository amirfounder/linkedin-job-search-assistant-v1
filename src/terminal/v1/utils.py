import json
from typing import Callable, Any


def pprint(obj: dict):
    print(json.dumps(obj, indent=4))


def try_convert_value_base(value: str, to: type, validation_fn: Callable[[str], Any], conversion_fn: Callable[[str], Any]):
    if not validation_fn(value):
        return value

    if value.endswith(' -y') or value.endswith(' --yes'):
        value.removesuffix(' -y')
        value.removesuffix(' --yes')
        should_convert = 'y'
    else:
        print(f'Convert value, "{value}", to {to.__name__}? y/n')
        should_convert = input()

    if should_convert == 'y':
        value = conversion_fn(value)

    return value


def try_convert_input_to_bool(value: str) -> bool:
    return try_convert_value_base(
        value=value,
        to=bool,
        validation_fn=lambda v: v.lower() in ['true', 'false'],
        conversion_fn=lambda v: True if v.lower() == 'true' else False
    )

def try_convert_input_to_float(value: str) -> float:
    return try_convert_value_base(
        value=value,
        to=float,
        validation_fn=lambda v: v.isdecimal(),
        conversion_fn=lambda v: float(v)
    )

def try_convert_input_to_int(value) -> int:
    return try_convert_value_base(
        value=value,
        to=int,
        validation_fn=lambda v: v.isdecimal(),
        conversion_fn=lambda v: int(v)
    )


def try_convert_input(value):
    fns = [
        try_convert_input_to_int,
        try_convert_input_to_float,
        try_convert_input_to_bool
    ]
    for fn in fns:
        if not isinstance(value, str):
            break
        value = fn(value)
    return value
