from dataclasses import dataclass


@dataclass
class Mint:
    block_number: int
    block_timestamp: int
    amount0: int
    amount1: int


@dataclass
class Create:
    block_number: int
    block_timestamp: int
    liquidity: int
    amount0: int
    amount1: int
    token_id: str


@dataclass
class Update:
    block_number: int
    block_timestamp: int
    liquidity: int
    token_id: str
    amount0: int
    amount1: int


@dataclass
class Burn:
    block_number: int
    block_timestamp: int
    amount: int


@dataclass
class Swap:
    block_number: int
    block_timestamp: int
    amount0_in: int
    amount1_in: int
    amount0_out: int
    amount1_out: int
    zero_for_one: bool
    fee_amount: int
