"""Holds example syntax tree cases for tests."""


EMPTY_DICT_CASES = [
    {"Script": {"body": []}},
    {"Comment": {"value": ""}},
    {"String": {"parts": []}},
    {"RawString": {"value": ""}},
    {"Var": {"name": "_"}},
    {"EnvVar": {"name": "_"}},
    {"And": {"lhs": {"Var": {"name": "_"}}, "rhs": {"Var": {"name": "_"}}}},
    {"Or": {"lhs": {"Var": {"name": "_"}}, "rhs": {"Var": {"name": "_"}}}},
    {"Not": {"node": {"Var": {"name": "_"}}}},
    {"Assign": {"name": "_", "value": {"String": {"parts": []}}, "scope": "global"}},
    {"EnvAssign": {"name": "_", "value": {"String": {"parts": []}}}},
    {"Delete": {"name": "_"}},
    {"EnvDelete": {"name": "_"}},
    {"Pass": {}},
    {"If": {"test": {"Var": {"name": "_"}}, "body": [{"Pass": {}}], "orelse": []}},
    {
        "For": {
            "target": {"Var": {"name": "_"}},
            "iter": [{"String": {"parts": []}}],
            "body": [{"Pass": {}}],
        }
    },
]
DICT_CASES = EMPTY_DICT_CASES
