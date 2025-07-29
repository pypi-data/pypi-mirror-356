import pytest


def test_namespace_alias():
    with pytest.raises(ImportError):
        from graphlibx import nx


def test_namespace_nesting():
    with pytest.raises(ImportError):
        from graphlibx import networkx
