import math
from decimal import Decimal
from typing import Any

from nqs_sdk.generator.random.random_generator import RandomGenerator
from nqs_sdk.generator.random.random_transaction_generator import RandomTransactionGenerator
from nqs_sdk.observer.protocol.uniswapv2 import UniswapV2Observer
from nqs_sdk.transaction import ABCTransaction
from nqs_sdk.transaction.uniswapv2 import (
    BurnTransactionUniv2,
    MintTransactionUniv2,
    ParamsUniv2TransactionType,
    SwapTransactionUniv2,
)


class RandomUniv2Generator(RandomTransactionGenerator):
    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        random_generation_parameters: dict,
        random_generator: RandomGenerator,
        mapping_block_timestamps: dict[int, int],
    ):
        super().__init__(id, name, type, random_generation_parameters, random_generator, mapping_block_timestamps)
        self._transaction_types = [transaction_type.value for transaction_type in ParamsUniv2TransactionType]
        self._observer: UniswapV2Observer

    def validate_observer(self) -> None:
        if not isinstance(self._observer, UniswapV2Observer):
            raise ValueError("Observer must be of type UniswapV2Observer")
        return

    def generate_transaction_at_block(self, transaction_type: str, **kwargs: Any) -> ABCTransaction:
        match transaction_type:
            case ParamsUniv2TransactionType.SWAP.value:
                return self.generate_swap_transactions_at_block(**kwargs)
            case ParamsUniv2TransactionType.MINT.value:
                return self.generate_mint_transactions_at_block(**kwargs)
            case ParamsUniv2TransactionType.BURN.value:
                return self.generate_burn_transactions_at_block(**kwargs)
            case _:
                raise ValueError(f"Invalid transaction type: {transaction_type}")

    def generate_swap_transactions_at_block(
        self, block_number: int, value_dict: dict[str, float]
    ) -> SwapTransactionUniv2:
        decimal0, decimal1 = self._observer.amm.decimals0, self._observer.amm.decimals1
        liquidity_decimals = int(0.5 * (decimal0 + decimal1))
        pool_liquidity = Decimal(self._observer.amm.total_supply).scaleb(-liquidity_decimals)
        reserve0 = Decimal(self._observer.amm.reserve0).scaleb(-decimal0)
        reserve1 = Decimal(self._observer.amm.reserve1).scaleb(-decimal1)
        dex_spot = reserve1 / reserve0
        sqrt_spot = Decimal(math.sqrt(dex_spot))

        amount_args = {
            "pct_of_pool": value_dict.get("pct_of_pool", None),
            "amount_token0": value_dict.get("amount_token0", None),
            "amount_token1": value_dict.get("amount_token1", None),
        }

        if (amount_args["pct_of_pool"] is None) == (
            amount_args["amount_token0"] is None or amount_args["amount_token1"] is None
        ):
            raise ValueError("Either pct_of_pool or both amount_token0 and amount_token1 must be provided")

        if amount_args["pct_of_pool"] is not None:
            amount = int(Decimal(amount_args["pct_of_pool"]) * pool_liquidity)
            amount0 = Decimal(amount / sqrt_spot).scaleb(decimal0)
            amount1 = Decimal(amount * sqrt_spot).scaleb(decimal1)
        else:
            if amount_args["amount_token0"] is None or amount_args["amount_token1"] is None:
                raise ValueError("Both amount_token0 and amount_token1 must be provided")

            amount0 = Decimal(amount_args["amount_token0"]).scaleb(decimal0)
            amount1 = Decimal(amount_args["amount_token1"]).scaleb(decimal1)

        if value_dict["token_in"] == 0:
            return SwapTransactionUniv2(
                block_number=block_number,
                protocol_id=self._protocol_id,
                sender_wallet=None,
                amount0_in=int(amount0),
                amount1_in=None,
            )
        else:
            return SwapTransactionUniv2(
                block_number=block_number,
                protocol_id=self._protocol_id,
                sender_wallet=None,
                amount0_in=None,
                amount1_in=int(amount1),
            )

    def generate_mint_transactions_at_block(
        self, block_number: int, value_dict: dict[str, float]
    ) -> MintTransactionUniv2:
        decimal0, decimal1 = self._observer.amm.decimals0, self._observer.amm.decimals1
        liquidity_decimals = int(0.5 * (decimal0 + decimal1))
        amount_args = {
            "amount": value_dict.get("amount", None),
            "pct_of_pool": value_dict.get("pct_of_pool", None),
        }

        if (amount_args["amount"] is None) == (amount_args["pct_of_pool"] is None):
            raise ValueError("Exactly one of amount and pct_of_pool must be provided")

        if amount_args["amount"] is not None:
            amount = int(amount_args["amount"])

        elif amount_args["pct_of_pool"] is not None:
            pool_liquidity = Decimal(self._observer.amm.total_supply).scaleb(-liquidity_decimals)
            amount = int(Decimal(amount_args["pct_of_pool"]) * pool_liquidity)

        reserve0 = Decimal(self._observer.amm.reserve0).scaleb(-decimal0)
        reserve1 = Decimal(self._observer.amm.reserve1).scaleb(-decimal1)
        dex_spot = reserve1 / reserve0
        sqrt_spot = Decimal(math.sqrt(dex_spot))
        amount1 = Decimal(amount * sqrt_spot).scaleb(decimal1)
        amount0 = self._observer.amm.get_quote(int(amount1), False)

        mint_transaction = MintTransactionUniv2(
            block_number=block_number,
            protocol_id=self._protocol_id,
            sender_wallet=None,
            amount0=int(amount0),
            amount1=int(amount1),
        )

        return mint_transaction

    def generate_burn_transactions_at_block(
        self, block_number: int, value_dict: dict[str, float]
    ) -> BurnTransactionUniv2:
        amount_args = {
            "amount": value_dict.get("amount", None),
            "pct_of_pool": value_dict.get("pct_of_pool", None),
        }

        if (amount_args["amount"] is None) == (amount_args["pct_of_pool"] is None):
            raise ValueError("Exactly one of amount and pct_of_pool must be provided")

        if amount_args["amount"] is not None:
            amount = Decimal(amount_args["amount"])

        elif amount_args["pct_of_pool"] is not None:
            pool_liquidity = Decimal(self._observer.amm.total_supply)
            amount = Decimal(amount_args["pct_of_pool"]) * pool_liquidity

        burn_transaction = BurnTransactionUniv2(
            block_number=block_number,
            protocol_id=self._protocol_id,
            sender_wallet=None,
            amount=int(amount),
        )

        return burn_transaction

    @property
    def transaction_types(self) -> list[str]:
        return self._transaction_types
