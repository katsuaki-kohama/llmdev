from calc import add

# 加算関数 add のテスト
def test_add():
    result = add(2, 3)
    assert result == 5


import pytest

# bが0の場合、ValueErrorを発生させる除算関数
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# 0で除算したときにValueErrorが発生するかをテスト
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# 通常の除算が正しく行われるかをテスト
def test_divide_normal():
    result = divide(10, 2)
    assert result == 5


import pytest
import calc

# 加算関数 add のテスト
def test_add():
    assert calc.add(2, 3) == 5
    assert calc.add(-5, -3) == -8
    assert calc.add(7, -2) == 5
    assert calc.add(0, 5) == 5
    assert calc.add(3, 0) == 3

# 減算関数 subtract のテスト
def test_subtract():
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(-3, -5) == 2
    assert calc.subtract(7, -2) == 9
    assert calc.subtract(5, 0) == 5
    assert calc.subtract(0, 3) == -3

# 乗算関数 multiply のテスト
def test_multiply():
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(-2, -3) == 6
    assert calc.multiply(2, -3) == -6
    assert calc.multiply(5, 0) == 0
    assert calc.multiply(0, 3) == 0

# 除算関数 divide のテスト
def test_divide():
    assert calc.divide(6, 3) == 2
    assert calc.divide(-6, -3) == 2
    assert calc.divide(6, -3) == -2

# 除算関数 divide が0で除算された場合にエラーを返すことを検証する
def test_divide_by_zero():
    with pytest.raises(ValueError, match="0で除算された"):
        calc.divide(5, 0)
    with pytest.raises(ValueError, match="0で除算された"):
        calc.divide(0, 0)

import pytest
import calc

# 加算関数 add のテスト
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-5, -3, -8),
    (7, -2, 5),
    (0, 5, 5),
    (3, 0, 3)
])
def test_add(a, b, expected):
    assert calc.add(a, b) == expected

# 減算関数 subtract のテスト
@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (-3, -5, 2),
    (7, -2, 9),
    (5, 0, 5),
    (0, 3, -3)
])
def test_subtract(a, b, expected):
    assert calc.subtract(a, b) == expected

# 乗算関数 multiply のテスト
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (-2, -3, 6),
    (2, -3, -6),
    (5, 0, 0),
    (0, 3, 0)
])
def test_multiply(a, b, expected):
    assert calc.multiply(a, b) == expected

# 除算関数 divide のテスト
@pytest.mark.parametrize("a, b, expected", [
    (6, 3, 2),
    (-6, -3, 2),
    (6, -3, -2)
])
def test_divide(a, b, expected):
    assert calc.divide(a, b) == expected

# 除算関数 divide が0で除算された場合にエラーを返すことを検証する
@pytest.mark.parametrize("a, b", [
    (5, 0),
    (0, 0)
])
def test_divide_by_zero(a, b):
    with pytest.raises(ValueError, match="0で除算された"):
        calc.divide(a, b)