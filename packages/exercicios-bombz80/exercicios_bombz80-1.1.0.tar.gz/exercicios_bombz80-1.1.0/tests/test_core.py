import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from cursofiap.core import exercicio_1
def test_exercicio_1():
    assert 1+1 == 2
