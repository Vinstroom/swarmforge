# tests/test_swarmforge_init.py

import pytest
from swarmforge import __version__

def test_version():
    assert __version__ == "0.1.0"
