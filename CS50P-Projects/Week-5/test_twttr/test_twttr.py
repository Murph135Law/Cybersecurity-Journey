from twttr import shorten

def test_argument():
    assert shorten("Hello, world!") == "Hll, wrld!"

def test_lowercase():
    assert shorten("hello, world!") == "hll, wrld!"

def test_uppercase():
    assert shorten("HELLO, WORLD!") == "HLL, WRLD!"

def test_numbers():
    assert shorten("H3ll0, w0rld!") == "H3ll0, w0rld!"


