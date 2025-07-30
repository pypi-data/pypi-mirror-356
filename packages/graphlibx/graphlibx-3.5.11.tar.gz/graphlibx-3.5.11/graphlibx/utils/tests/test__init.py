import pytest


def test_utils_namespace():
    """Ensure objects are not unintentionally exposed in utils namespace."""
    with pytest.raises(ImportError):
        from graphlibx.utils import nx
    with pytest.raises(ImportError):
        from graphlibx.utils import sys
    with pytest.raises(ImportError):
        from graphlibx.utils import defaultdict, deque
