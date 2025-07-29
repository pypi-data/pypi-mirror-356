from dataclasses import dataclass

from nqs_sdk.state import ABCProtocolState


@dataclass(kw_only=True)
class StateUniv2(ABCProtocolState):
    token0: str
    token1: str
    symbol0: str
    symbol1: str
    decimals0: int
    decimals1: int
    total_supply: int
    reserve0: int
    reserve1: int
