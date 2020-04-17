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
    "empty-command": "echo",
    "empty-capturedcommand": "$(echo)",
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
    "minimal-command": "echo Wow Mom",
    "minimal-capturedcommand": "$(echo Wow Mom)",
    "minimal-and": "$x && $y",
    "minimal-or": "$x || $y",
    "minimal-not": "! $x",
    "minimal-assign": 'x="cd"\n',
    "minimal-envassign": 'export HOME="/path/to/home"\n',
    "minimal-delete": "unset x\n",
    "minimal-envdelete": "unset HOME\n",
    "minimal-if": "if $x; then\n  :\nelse\n  :\nfi\n",
    "minimal-for": 'for x in "cd"; do\n  :\ndone\n',
    "compound-script": """
# I am a comment
x="cd"
if $x; then
  unset x
fi
""".lstrip(),
    "compound-string": '"cd $HOME"',
    "compound-command": 'echo "$HOME"',
    "compound-capturedcommand": '$(echo "$HOME")',
    "compound-if": """
if $x; then
  unset x
  x="cd"
elif $y; then
  unset y
  y="ls"
else
  :
fi
""".lstrip(),
    "compound-for": """
for x in "ls $HOME"; do
  # I am a comment
  y="cd"
done
""".lstrip(),
}


@mark_cases(TOBASH_EXP)
def test_tobash(inp, exp):
    obs = tobash(inp)
    assert obs == exp
