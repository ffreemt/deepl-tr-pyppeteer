"""Test."""
from deepl_tr_pp import __version__


def test_version():
    """test version."""
    assert __version__[:-1] == "0.1."
