"""Tests Xonsh functionality"""
import pytest

from asht.xonsh import toxonsh

from .cases import zip_cases, mark_cases

TOXONSH_EXP = {
    "empty-script": "",
    "empty-comment": "# \n",
    "empty-string": '""',
    "empty-rawstring": "",
    "empty-var": "_",
    "empty-envvar": "$_",
    "empty-command": "![echo]",
    "empty-capturedcommand": "$(echo)",
    "empty-and": "_ and _",
    "empty-or": "_ or _",
    "empty-not": "not _",
    "empty-assign": '_ = ""\n',
    "empty-delete": 'del _\n',
    "empty-envassign": '$_ = ""\n',
    "empty-envdelete": 'del $_\n',
    "empty-aliasassign": 'aliases["_"] = ""\n',
    "empty-aliasdelete": 'del aliases["_"]\n',
    "empty-pass": 'pass\n',
    "empty-if": 'if _:\n    pass\n',
    "empty-for": 'for _ in "":\n    pass\n',
    "empty-function": "def f():\n    pass\n",
    "minimal-script": "pass\n",
    "minimal-comment": "# I am a comment\n",
    "minimal-string": '"cd"',
    "minimal-rawstring": "ls",
    "minimal-var": "x",
    "minimal-envvar": "$HOME",
    "minimal-command": "![echo Wow Mom]",
    "minimal-capturedcommand": "$(echo Wow Mom)",
    "minimal-and": "x and y",
    "minimal-or": "x or y",
    "minimal-not": "not x",
    "minimal-assign": 'x = "cd"\n',
    "minimal-delete": "del x\n",
    "minimal-envassign": '$HOME = "/path/to/home"\n',
    "minimal-envdelete": "del $HOME\n",
    "minimal-aliasassign": 'aliases["gg"] = "cd /path/to/home"\n',
    "minimal-aliasdelete": 'del aliases["gg"]\n',
    "minimal-if": "if x:\n    pass\nelse:\n    pass\n",
    "minimal-for": 'for x in "cd":\n    pass\n',
    "minimal-function": "def f():\n    x\n",
    "compound-script": """
# I am a comment
x = "cd"
if x:
    del x
""".lstrip(),
    "compound-string": '"cd $HOME"',
    "compound-command": '![echo "$HOME"]',
    "compound-capturedcommand": '$(echo "$HOME")',
    "compound-if": """
if x:
    del x
    x = "cd"
elif y:
    del y
    y = "ls"
else:
    pass
""".lstrip(),
    "compound-for": """
for x in "ls $HOME":
    # I am a comment
    y = "cd"
""".lstrip(),
    "compound-function": """
def f():
    # I am a comment
    x
""".lstrip(),
}


@mark_cases(TOXONSH_EXP)
def test_toxonsh(inp, exp):
    obs = toxonsh(inp)
    assert obs == exp
