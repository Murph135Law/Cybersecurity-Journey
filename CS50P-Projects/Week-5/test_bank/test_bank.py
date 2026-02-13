from bank import value

def test_hello():
    assert value("hello") == 0

def test_hi():
    assert value("hi") == 20

def test_whats_up():
    assert value("whats up") == 100

def test_uppercase():
    assert value("HELLO") == 0
    assert value("HI") == 20
    assert value("WHATS UP") == 100
