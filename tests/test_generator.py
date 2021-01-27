import pytest

from rost.generator import _has_argument


def foo():
    """Test data for ``_has_argument`` tests."""


def boo(x):
    """Test data for ``_has_argument`` tests."""


@pytest.mark.parametrize(
    "func, expected",
    [
        (foo, False),
        (boo, True)
    ]
)
def test_has_arguments(func, expected):
    assert _has_argument(func) == expected
