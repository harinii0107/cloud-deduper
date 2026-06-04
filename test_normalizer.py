import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from normalizer import normalize

def test_basic_dedupe():
    r1 = {"Name": "Harini", "Email": "a@test.com"}
    r2 = {"name": "harini", "email": "a@test.com"}
    assert normalize(r1) == normalize(r2)

def test_strips_spaces():
    r1 = {"email": "  a@test.com  "}
    r2 = {"email": "a@test.com"}
    assert normalize(r1) == normalize(r2)