from plates import is_valid

def test_length():
    assert is_valid("a") == False
    assert is_valid("ab") == True
    assert is_valid("abc") == True
    assert is_valid("abcd") == True
    assert is_valid("abcde") == True
    assert is_valid("abcdef") == True
    assert is_valid("abcdefg") == False

def test_alpha_start():
    assert is_valid("123456") == False
    assert is_valid("a12345") == False
    assert is_valid("ab1234") == True
    assert is_valid("abc123") == True
    assert is_valid("abcd12") == True
    assert is_valid("abcde1") == True
    assert is_valid("abcdef") == True

def test_num_start_to_finish():
    assert is_valid("ab1234") == True
    assert is_valid("abc123") == True
    assert is_valid("abcd12") == True
    assert is_valid("abcde1") == True
    assert is_valid("ab1cde") == False
    assert is_valid("abc1de") == False
    assert is_valid("abcd1e") == False

def test_zero_placement():
    assert is_valid("ab0123") == False
    assert is_valid("abc012") == False
    assert is_valid("abcd01") == False
    assert is_valid("abcde0") == False
    assert is_valid("ab1023") == True
    assert is_valid("abc102") == True
    assert is_valid("abcd10") == True

def test_punctuation():
    assert is_valid("he!!o") == False

def test_valid():
    assert is_valid("hello") == True
    assert is_valid("he110") == True

