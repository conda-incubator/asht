"""Tests Bash functionality"""
import pytest

from asht.bash import tobash

from .cases import DICT_CASES


@pytest.mark.parametrize("case", DICT_CASES)
def test_tobash(case):
    pass