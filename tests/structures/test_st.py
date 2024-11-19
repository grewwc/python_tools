import pytest
import sys
from structures import ST


@pytest.fixture
def st1():
    st = ST()
    st.put(1, 2)
    st.put(2, 3)
    st.put(3, 4)
    st.put(100, 5)
    st.put(200, 5)

    return st

def test_get(st1):
    assert st1.get(2) == 3


def test_delete(st1):
    assert 3 in st1
    assert st1.contains(3)
    st1.delete(3)
    assert 3 not in st1
    assert not st1.contains(3)


def test_get_beween(st1):
    print(st1.get_between(2))


def test_to_dict(st1):
    assert st1.to_dict() == {1: 2, 2: 3, 3: 4, 100: 5, 200: 5}
