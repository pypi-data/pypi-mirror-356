import math


def sqrt(x: int) -> int:
    if x > 3:
        z = x
        x = x // 2 + 1
        while x < z:
            z = x
            x = (x + x // x) // 2
    else:
        z = 1
    return z


def mul(x: int, y: int) -> int:
    if y == 0 or (x * y) // y == x:
        return x * y
    else:
        raise OverflowError("ds-math-mul-overflow")


def theoritical_il(spot_ratio: float) -> float:
    return (2 * math.sqrt(spot_ratio) / (1 + spot_ratio)) - 1


""" Solidity code : https://github.com/Uniswap/v2-core/blob/master/contracts/libraries/Math.sol"""
