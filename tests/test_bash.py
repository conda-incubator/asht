"""Tests Bash functionality"""
import pytest

from asht.bash import tobash

from .cases import zip_cases, mark_cases

TOBASH_EXP = {
    "empty-script": "",
    "empty-comment": "# \n",
    "empty-string": '""',
    "empty-rawstring": "",
    "empty-var": "$_",
    "empty-envvar": "$_",
    "empty-and": "$_ && $_",
    "empty-or": "$_ || $_",
    "empty-not": "! $_",
    "empty-assign": '_=""\n',
    "empty-envassign": 'export _=""\n',
    "empty-delete": 'unset _\n',
    "empty-envdelete": 'unset _\n',
    "empty-pass": ':\n',
    "empty-if": 'if $_; then\n  :\nfi\n',
    "empty-for": 'for _ in ""; do\n  :\ndone\n',
    "minimal-script": ":\n",
    "minimal-comment": "# I am a comment\n",
    "minimal-string": '"cd"',
    "minimal-rawstring": "ls",
    "minimal-var": "$x",
    "minimal-envvar": "$HOME",
    "minimal-and": "$x && $y",
    "minimal-or": "$x || $y",
    "minimal-not": "! $x",
    "minimal-assign": 'x="cd"\n',
    "minimal-envassign": 'export HOME="/path/to/home"\n',
    "minimal-delete": "unset x\n",
    "minimal-envdelete": "unset HOME\n",
    "minimal-if": "if $x; then\n  :\nelse\n  :\nfi\n",
    "minimal-for": 'for x in "cd"; do\n  :\ndone\n',
}


@mark_cases(TOBASH_EXP)
def test_tobash(inp, exp):
    obs = tobash(inp)
    assert obs == exp
