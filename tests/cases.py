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
    {"Command": {"args": [{"RawString": {"value": "echo"}}]}},
    {"CapturedCommand": {"args": [{"RawString": {"value": "echo"}}]}},
    {"And": {"lhs": {"Var": {"name": "_"}}, "rhs": {"Var": {"name": "_"}}}},
    {"Or": {"lhs": {"Var": {"name": "_"}}, "rhs": {"Var": {"name": "_"}}}},
    {"Not": {"node": {"Var": {"name": "_"}}}},
    {"Assign": {"name": "_", "value": {"String": {"parts": []}}, "scope": "global"}},
    {"Delete": {"name": "_"}},
    {"EnvAssign": {"name": "_", "value": {"String": {"parts": []}}}},
    {"EnvDelete": {"name": "_"}},
    {"AliasAssign": {"name": "_", "value": {"String": {"parts": []}}}},
    {"AliasDelete": {"name": "_"}},
    {"Pass": {}},
    {"If": {"test": {"Var": {"name": "_"}}, "body": [{"Pass": {}}], "orelse": []}},
    {
        "For": {
            "target": {"Var": {"name": "_"}},
            "iter": {"String": {"parts": []}},
            "body": [{"Pass": {}}],
        }
    },
    {"Function": {"name": "f", "body": [{"Pass": {}}]}},
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
    {
        "Command": {
            "args": [
                {"RawString": {"value": "echo"}},
                {"RawString": {"value": "Wow"}},
                {"RawString": {"value": "Mom"}},
            ]
        }
    },
    {
        "CapturedCommand": {
            "args": [
                {"RawString": {"value": "echo"}},
                {"RawString": {"value": "Wow"}},
                {"RawString": {"value": "Mom"}},
            ]
        }
    },
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
    {"Delete": {"name": "x"}},
    {
        "EnvAssign": {
            "name": "HOME",
            "value": {"String": {"parts": [{"RawString": {"value": "/path/to/home"}}]}},
        }
    },
    {"EnvDelete": {"name": "HOME"}},
    {
        "AliasAssign": {
            "name": "gg",
            "value": {
                "String": {
                    "parts": [
                        {"RawString": {"value": "cd "}},
                        {"RawString": {"value": "/path/to/home"}},
                    ]
                }
            },
        }
    },
    {"AliasDelete": {"name": "gg"}},
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
    {
        "Function": {
            "name": "f",
            "body": [{"Statement": {"node": {"Var": {"name": "x"}}}}],
        }
    },
]
MINIMAL_DICT_CASES = {
    "minimal-" + next(iter(c.keys())).lower(): c for c in MINIMAL_DICT_CASES
}
DICT_CASES.update(MINIMAL_DICT_CASES)


#
# Compund cases
#
COMPOUND_DICT_CASES = [
    {
        "Script": {
            "body": [
                {"Comment": {"value": "I am a comment"}},
                {
                    "Assign": {
                        "name": "x",
                        "value": {
                            "String": {"parts": [{"RawString": {"value": "cd"}}]}
                        },
                        "scope": "global",
                    }
                },
                {
                    "If": {
                        "test": {"Var": {"name": "x"}},
                        "body": [{"Delete": {"name": "x"}}],
                        "orelse": [],
                    }
                },
            ]
        }
    },
    {
        "String": {
            "parts": [{"RawString": {"value": "cd "}}, {"EnvVar": {"name": "HOME"}}]
        }
    },
    {
        "Command": {
            "args": [
                {"RawString": {"value": "echo"},},
                {"String": {"parts": [{"EnvVar": {"name": "HOME"}}]}},
            ]
        }
    },
    {
        "CapturedCommand": {
            "args": [
                {"RawString": {"value": "echo"},},
                {"String": {"parts": [{"EnvVar": {"name": "HOME"}}]}},
            ]
        }
    },
    {
        "If": {
            "test": {"Var": {"name": "x"}},
            "body": [
                {"Delete": {"name": "x"}},
                {
                    "Assign": {
                        "name": "x",
                        "value": {
                            "String": {"parts": [{"RawString": {"value": "cd"}}]}
                        },
                        "scope": "global",
                    }
                },
            ],
            "orelse": [
                {
                    "If": {
                        "test": {"Var": {"name": "y"}},
                        "body": [
                            {"Delete": {"name": "y"}},
                            {
                                "Assign": {
                                    "name": "y",
                                    "value": {
                                        "String": {
                                            "parts": [{"RawString": {"value": "ls"}}]
                                        }
                                    },
                                    "scope": "global",
                                }
                            },
                        ],
                        "orelse": [{"Pass": {}}],
                    }
                }
            ],
        }
    },
    {
        "For": {
            "target": {"Var": {"name": "x"}},
            "iter": {
                "String": {
                    "parts": [
                        {"RawString": {"value": "ls "}},
                        {"EnvVar": {"name": "HOME"}},
                    ]
                }
            },
            "body": [
                {"Comment": {"value": "I am a comment"}},
                {
                    "Assign": {
                        "name": "y",
                        "value": {
                            "String": {"parts": [{"RawString": {"value": "cd"}}]}
                        },
                        "scope": "global",
                    }
                },
            ],
        }
    },
    {
        "Function": {
            "name": "f",
            "body": [
                {"Comment": {"value": "I am a comment"}},
                {"Statement": {"node": {"Var": {"name": "x"}}}},
            ],
        }
    },
]
COMPOUND_DICT_CASES = {
    "compound-" + next(iter(c.keys())).lower(): c for c in COMPOUND_DICT_CASES
}
DICT_CASES.update(COMPOUND_DICT_CASES)


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
