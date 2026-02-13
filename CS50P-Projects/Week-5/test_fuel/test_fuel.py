from fuel import convert, gauge
import pytest
"""
CONVERT TEST
"""
def test_convert_fractions():
    assert convert("1/1") == 100
    assert convert("1/2") == 50
    assert convert("1/3") == 33
    assert convert("1/4") == 25
    assert convert("1/5") == 20

def test_convert_zero():
    assert convert("0/1") == 0

def test_convert_zero_division():
    with pytest.raises(ZeroDivisionError):
        convert("1/0")

def test_convert_value_error():
    with pytest.raises(ValueError):
        convert("cat/dog")
    with pytest.raises(ValueError):
        convert("1.5/3")
    with pytest.raises(ValueError):
        convert("3/2")
    with pytest.raises(ValueError):
        convert("-1/2")
"""
GAUGE TEST
"""
def test_gauge_outputs():
    assert gauge(0) == "E"
    assert gauge(1) == "E"

    for percentage in range(2,99):
        assert gauge(percentage) == f"{percentage}%"

    assert gauge(99) == "F"
    assert gauge(100) == "F"
