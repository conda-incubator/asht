"""Holds example syntax tree cases for tests."""
import pytest

#
# Empty example cases with no content in blocks
#
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
            "iter": {"String": {"parts": []}},
            "body": [{"Pass": {}}],
        }
    },
]
EMPTY_DICT_CASES = {
    "empty-" + next(iter(c.keys())).lower(): c for c in EMPTY_DICT_CASES
}
DICT_CASES = EMPTY_DICT_CASES


#
# Minimal cases
#
MINIMAL_DICT_CASES = [
    {"Script": {"body": [{"Pass": {}}]}},
    {"Comment": {"value": "I am a comment"}},
    {"String": {"parts": [{"RawString": {"value": "cd"}}]}},
    {"RawString": {"value": "ls"}},
    {"Var": {"name": "x"}},
    {"EnvVar": {"name": "HOME"}},
    {"And": {"lhs": {"Var": {"name": "x"}}, "rhs": {"Var": {"name": "y"}}}},
    {"Or": {"lhs": {"Var": {"name": "x"}}, "rhs": {"Var": {"name": "y"}}}},
    {"Not": {"node": {"Var": {"name": "x"}}}},
    {
        "Assign": {
            "name": "x",
            "value": {"String": {"parts": [{"RawString": {"value": "cd"}}]}},
            "scope": "global",
        }
    },
    {
        "EnvAssign": {
            "name": "HOME",
            "value": {"String": {"parts": [{"RawString": {"value": "/path/to/home"}}]}},
        }
    },
    {"Delete": {"name": "x"}},
    {"EnvDelete": {"name": "HOME"}},
    {
        "If": {
            "test": {"Var": {"name": "x"}},
            "body": [{"Pass": {}}],
            "orelse": [{"Pass": {}}],
        }
    },
    {
        "For": {
            "target": {"Var": {"name": "x"}},
            "iter": {"String": {"parts": [{"RawString": {"value": "cd"}}]}},
            "body": [{"Pass": {}}],
        }
    },
]
MINIMAL_DICT_CASES = {
    "minimal-" + next(iter(c.keys())).lower(): c for c in MINIMAL_DICT_CASES
}
DICT_CASES.update(MINIMAL_DICT_CASES)


def zip_cases(expecteds):
    """zips input and expetced values for cases"""
    rtn = []
    for key, exp in expecteds.items():
        rtn.append((key, DICT_CASES[key], exp))
    rtn.sort()
    return rtn


def mark_cases(expecteds):
    """Correctly marks all test cases."""
    rtn = zip_cases(expecteds)
    ids = []
    inp_exps = []
    for i, inp, exp in rtn:
        ids.append(i)
        inp_exps.append((inp, exp))

    def dec(f):
        return pytest.mark.parametrize("inp, exp", inp_exps, ids=ids)(f)

    return dec
