import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from micro_language import Expression

from nqs_sdk.constants import ADJUST_MINT_AMOUNTS
from nqs_sdk.transaction import ABCTransaction
from nqs_sdk.transaction.transaction_helper import ProtocolTransactionHelper
from nqs_sdk.wallet import rescale_to_int

DEFAULT_LP_TOKEN_DECIMALS = 18


class Univ2TransactionType(Enum):
    SWAP = "Swap"
    MINT = "Mint"
    BURN = "Burn"


class ParamsUniv2TransactionType(Enum):
    SWAP = "v2_swap"
    MINT = "v2_mint"
    BURN = "v2_burn"


@dataclass
class TransactionUniv2(ABCTransaction):
    action_type: Univ2TransactionType = field(init=False)


@dataclass
class MintTransactionUniv2(TransactionUniv2):
    amount0: int | Expression
    amount1: int | Expression
    amount0min: int | None = None
    amount1min: int | None = None

    def __post_init__(self) -> None:
        self.action_type = Univ2TransactionType.MINT


@dataclass
class BurnTransactionUniv2(TransactionUniv2):
    amount: int | Expression

    def __post_init__(self) -> None:
        self.action_type = Univ2TransactionType.BURN


@dataclass
class SwapTransactionUniv2(TransactionUniv2):
    amount0_in: int | None | Expression
    amount1_in: int | None | Expression

    def __post_init__(self) -> None:
        self.action_type = Univ2TransactionType.SWAP


class TransactionHelperUniv2(ProtocolTransactionHelper):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def create_mint_transaction(**kwargs: Any) -> MintTransactionUniv2:
        fields = {
            "block_number": None,
            "protocol_id": None,
            "sender_wallet": None,
            "amount0": None,
            "amount1": None,
        }
        fields.update(kwargs)
        mint_transaction = MintTransactionUniv2(**fields)  # type: ignore
        return mint_transaction

    @staticmethod
    def create_burn_transaction(**kwargs: Any) -> BurnTransactionUniv2:
        fields = {
            "block_number": None,
            "protocol_id": None,
            "sender_wallet": None,
            "amount": None,
        }
        fields.update(kwargs)
        burn_transaction = BurnTransactionUniv2(**fields)  # type: ignore
        return burn_transaction

    @staticmethod
    def create_swap_transaction(**kwargs: Any) -> SwapTransactionUniv2:
        fields = {
            "block_number": None,
            "protocol_id": None,
            "sender_wallet": None,
            "amount0_in": None,
            "amount1_in": None,
        }
        fields.update(kwargs)
        swap_transaction = SwapTransactionUniv2(**fields)  # type: ignore
        return swap_transaction

    @property
    def mapping_action_helper(self) -> dict[str, Any]:
        return {
            ParamsUniv2TransactionType.MINT.value: self.create_mint_transaction,
            ParamsUniv2TransactionType.BURN.value: self.create_burn_transaction,
            ParamsUniv2TransactionType.SWAP.value: self.create_swap_transaction,
        }

    @staticmethod
    def quote(amount: int, reserve0: int, reserve1: int) -> int:
        return amount * reserve1 // reserve0

    @staticmethod
    def adjust_mint_amounts(
        transaction: MintTransactionUniv2, symbol0: str, symbol1: str, reserve0: int, reserve1: int
    ) -> MintTransactionUniv2:
        user_wallet = transaction.sender_wallet
        if user_wallet is None:
            raise ValueError("wallet is None")
        wallet_amount0 = user_wallet.holdings[symbol0]
        wallet_amount1 = user_wallet.holdings[symbol1]
        user_input_amount0 = transaction.amount0
        user_input_amount1 = transaction.amount1

        optimal_amount0 = TransactionHelperUniv2.quote(user_input_amount1, reserve0, reserve1)
        optimal_amount1 = TransactionHelperUniv2.quote(user_input_amount0, reserve0, reserve1)

        if optimal_amount0 > wallet_amount0 and optimal_amount1 <= wallet_amount1:
            new_amount0 = wallet_amount0
            new_amount1 = TransactionHelperUniv2.quote(wallet_amount0, reserve0, reserve1)
            transaction.amount0 = new_amount0
            transaction.amount1 = new_amount1
            logging.warning(f"Adjusted amount0 and amount1 for transaction : , {asdict(transaction)}")

        elif optimal_amount0 <= wallet_amount0 and optimal_amount1 > wallet_amount1:
            new_amount0 = TransactionHelperUniv2.quote(wallet_amount1, reserve1, reserve0)
            new_amount1 = wallet_amount1
            transaction.amount0 = new_amount0
            transaction.amount1 = new_amount1
            logging.warning(f"Adjusted amount0 and amount1 for transaction : , {asdict(transaction)}")

        elif optimal_amount0 > wallet_amount0 and optimal_amount1 > wallet_amount1:
            first_test_amount0 = wallet_amount0
            first_test_amount1 = TransactionHelperUniv2.quote(wallet_amount0, reserve0, reserve1)
            if first_test_amount1 <= wallet_amount1:
                transaction.amount0 = first_test_amount0
                transaction.amount1 = first_test_amount1
                logging.warning(f"Adjusted amount0 and amount1 for transaction : , {asdict(transaction)}")
                return transaction
            second_test_amount0 = TransactionHelperUniv2.quote(wallet_amount1, reserve1, reserve0)
            second_test_amount1 = wallet_amount1
            if second_test_amount0 <= wallet_amount0:
                transaction.amount0 = second_test_amount0
                transaction.amount1 = second_test_amount1
                logging.warning(f"Adjusted amount0 and amount1 for transaction : , {asdict(transaction)}")
                return transaction
            raise ValueError("Amounts are not correct")

        return transaction

    def convert_amounts_to_integers(self, transaction: ABCTransaction, **kwargs: Any) -> ABCTransaction:
        symbol0, symbol1, reserve0, reserve1 = (
            kwargs["symbol0"],
            kwargs["symbol1"],
            kwargs["reserve0"],
            kwargs["reserve1"],
        )
        if symbol0 is None or symbol1 is None or reserve0 is None or reserve1 is None:
            raise ValueError("symbol0, symbol1, reserve0, reserve1 cannot be None")
        wallet = transaction.sender_wallet
        if wallet is None:
            raise ValueError("wallet is None")

        decimals0 = wallet.tokens_metadata[symbol0].decimals
        decimals1 = wallet.tokens_metadata[symbol1].decimals
        if isinstance(transaction, SwapTransactionUniv2):
            transaction.amount0_in = (
                rescale_to_int(transaction.amount0_in, decimals0) if transaction.amount0_in is not None else None
            )
            transaction.amount1_in = (
                rescale_to_int(transaction.amount1_in, decimals1) if transaction.amount1_in is not None else None
            )
        elif isinstance(transaction, MintTransactionUniv2):
            transaction.amount0 = rescale_to_int(transaction.amount0, decimals0)
            transaction.amount1 = rescale_to_int(transaction.amount1, decimals1)
        elif isinstance(transaction, BurnTransactionUniv2):
            transaction.amount = rescale_to_int(transaction.amount, DEFAULT_LP_TOKEN_DECIMALS)

        if isinstance(transaction, MintTransactionUniv2) and ADJUST_MINT_AMOUNTS:
            transaction = TransactionHelperUniv2.adjust_mint_amounts(transaction, symbol0, symbol1, reserve0, reserve1)

        return transaction
