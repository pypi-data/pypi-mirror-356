import copy
import math
from decimal import Decimal
from typing import Optional

from nqs_pycore import Wallet

from nqs_sdk.protocol import ABCProtocol
from nqs_sdk.protocol.amm.uniswapv2.events import Burn, Create, Mint, Swap, Update
from nqs_sdk.protocol.utils import rollback_on_failure
from nqs_sdk.state import ABCProtocolState, StateUniv2
from nqs_sdk.transaction.abc_transaction import ABCTransaction
from nqs_sdk.transaction.uniswapv2 import (
    BurnTransactionUniv2,
    MintTransactionUniv2,
    SwapTransactionUniv2,
    TransactionUniv2,
)
from nqs_sdk.wallet.arbitrageur_wallet import ArbitrageurWallet
from nqs_sdk.wallet.utils import UniswapV2LiquidityError, UniswapV2MintAmountsError

from .math import mul

SPOT_TOLERANCE = 10**-6


class UniswapV2(ABCProtocol):
    def __init__(self, state: StateUniv2, gas_fee: int = 0, gas_fee_ccy: Optional[str] = None):
        super().__init__(state, gas_fee, gas_fee_ccy)
        self.__reset_from_state(state)
        # constants
        self.lp_token_name = str("Univ2_LP_") + state.name
        self.minimum_liquidity = 1000
        self.fee_multiplicator = 3
        self.fee_denominator = 1000

    def __reset_from_state(self, state: StateUniv2) -> None:
        self.check_state(state)
        state = copy.deepcopy(state)
        self.block_number = state.block_number
        self.block_timestamp = state.block_timestamp
        self.token0 = state.token0
        self.token1 = state.token1
        self.symbol0 = state.symbol0
        self.symbol1 = state.symbol1
        self.decimals0 = state.decimals0
        self.decimals1 = state.decimals1
        self.total_supply = state.total_supply
        self.reserve0 = state.reserve0
        self.reserve1 = state.reserve1
        self.events_ready_to_collect: list = []

    def check_state(self, state: StateUniv2) -> None:  # noqa: C901
        if not isinstance(state, StateUniv2):
            raise ValueError("Can only restore from StateUniv2")
        if state.reserve0 == 0:
            if state.reserve1 != 0:
                raise ValueError("Reserve0 is 0 but reserve1 is not 0")
            if state.total_supply != 0:
                raise ValueError("Reserve0 is 0 but total_supply is not 0")
        if state.reserve1 == 0:
            if state.reserve0 != 0:
                raise ValueError("Reserve1 is 0 but reserve0 is not 0")
            if state.total_supply != 0:
                raise ValueError("Reserve1 is 0 but total_supply is not 0")
        if state.token0 == state.token1:
            raise ValueError("Token0 and Token1 are the same")
        if state.symbol0 == state.symbol1:
            raise ValueError("Symbol0 and Symbol1 are the same")
        if state.total_supply < 0:
            raise ValueError("Total supply is negative")
        if state.reserve0 < 0:
            raise ValueError("Reserve0 is negative")
        if state.reserve1 < 0:
            raise ValueError("Reserve1 is negative")

    def get_state(self, block_timestamp: int) -> StateUniv2:
        state = StateUniv2(
            id=self.id,
            name=self.name,
            block_number=self.block_number,
            block_timestamp=block_timestamp,
            token0=self.token0,
            token1=self.token1,
            symbol0=self.symbol0,
            symbol1=self.symbol1,
            decimals0=self.decimals0,
            decimals1=self.decimals1,
            total_supply=self.total_supply,
            reserve0=self.reserve0,
            reserve1=self.reserve1,
        )
        state = copy.deepcopy(state)
        return state

    def get_dex_spot(self) -> Decimal:
        return (Decimal(self.reserve1) / Decimal(self.reserve0)).scaleb(self.decimals0 - self.decimals1)

    def get_raw_dex_spot(self) -> Decimal:
        return Decimal(self.reserve1 / self.reserve0)

    def restore_from_state(self, state: ABCProtocolState) -> None:
        if not isinstance(state, StateUniv2):
            raise ValueError("Can only restore from StateUniv2")
        self.__reset_from_state(state)

    def get_quote(self, amount: int, zero_for_one: bool) -> int:
        if zero_for_one:
            return mul(amount, self.reserve1) // self.reserve0
        else:
            return mul(amount, self.reserve0) // self.reserve1

    def process_transactions(self, transactions: list[ABCTransaction]) -> None:
        for transaction in transactions:
            self.process_single_transaction(transaction)

    def process_single_transaction(self, transaction: ABCTransaction) -> None:
        if not isinstance(transaction, TransactionUniv2):
            message = "Can only process instances of TransactionUniswapV2"
            message = (
                f"Action {transaction.action_name} - " + message if transaction.action_name is not None else message
            )
            raise ValueError(message)
        self._handle_transaction(transaction=transaction, msg_sender=transaction.sender_wallet)

    @rollback_on_failure
    def _handle_transaction(self, transaction: ABCTransaction, msg_sender: Wallet) -> None:
        self.block_number = transaction.block_number
        self.block_timestamp = transaction.block_timestamp
        if isinstance(transaction, SwapTransactionUniv2):
            if transaction.sender_wallet is None or (not (transaction.amount0_in == 0 or transaction.amount1_in == 0)):
                self._update_from_swap(
                    amount0_in=transaction.amount0_in,
                    amount1_in=transaction.amount1_in,
                    msg_sender=transaction.sender_wallet,
                    action_name=transaction.action_name,
                )
            else:
                message = (
                    f"Swap transaction at block {transaction.block_number} from "
                    f"{transaction.sender_wallet.agent_name} is not executed as the swap amount is 0"
                )
                message = (
                    f"Action {transaction.action_name} - " + message if transaction.action_name is not None else message
                )
                self.logger.warning(message)
        elif isinstance(transaction, MintTransactionUniv2):
            if (
                transaction.amount0 is not None
                and transaction.amount0 > 0
                or transaction.amount1 is not None
                and transaction.amount1 > 0
            ):
                self._update_from_mint(
                    amount0desired=transaction.amount0,
                    amount1desired=transaction.amount1,
                    amount0min=transaction.amount0min if transaction.amount0min is not None else 0,
                    amount1min=transaction.amount1min if transaction.amount1min is not None else 0,
                    msg_sender=transaction.sender_wallet,
                    action_name=transaction.action_name,
                )
            else:
                if transaction.sender_wallet is not None:
                    message = (
                        f"Mint transaction at block {transaction.block_number} from "
                        f"{transaction.sender_wallet.agent_name} is not executed as the mint amount is 0"
                    )
                    message = (
                        f"Action {transaction.action_name} - " + message
                        if transaction.action_name is not None
                        else message
                    )
                    self.logger.warning(message)
        elif isinstance(transaction, BurnTransactionUniv2):
            if transaction.amount > 0:
                self._update_from_burn(
                    amount=transaction.amount, msg_sender=transaction.sender_wallet, action_name=transaction.action_name
                )
            else:
                if transaction.sender_wallet is not None:
                    message = (
                        f"Burn transaction at block {transaction.block_number} from "
                        f"{transaction.sender_wallet.agent_name} is not executed as the burn amount is 0"
                    )
                    message = (
                        f"Action {transaction.action_name} - " + message
                        if transaction.action_name is not None
                        else message
                    )
                    self.logger.warning(message)
        else:
            raise ValueError("Actions of type {} are not supported".format(transaction.action_type))

        self.logger.debug(transaction)

    def get_optimal_amounts(
        self,
        amount0desired: int,
        amount1desired: int,
        amount0min: int | None,
        amount1min: int | None,
        action_name: str | None = None,
    ) -> tuple[int, int]:
        if amount0desired is None and amount1desired is None:
            message = "Only one of amount0desired and amount1desired should be provided"
            message = f"Action {action_name} - " + message if action_name is not None else message
            raise ValueError(message)

        if self.reserve0 == 0 and self.reserve1 == 0:
            amount0, amount1 = amount0desired, amount1desired
        else:
            amount1optimal = self.get_quote(amount0desired, True)
            if amount1optimal <= amount1desired:
                if amount1min is not None and amount1min >= amount1desired:
                    message = "The computed amount of token1 is less than the minimum amount set by the user"
                    message = f"Action {action_name} - " + message if action_name is not None else message
                    raise UniswapV2MintAmountsError(message)
                amount0, amount1 = amount0desired, amount1optimal
            else:
                amount0optimal = self.get_quote(amount1desired, False)
                if amount0optimal <= amount0desired:
                    if amount0min is not None and amount0min >= amount0desired:
                        message = "The computed amount of token0 is less than the minimum amount set by the user"
                        message = f"Action {action_name} - " + message if action_name is not None else message
                        raise UniswapV2MintAmountsError(message)
                    amount0, amount1 = amount0optimal, amount1desired
                else:
                    message = f"""UniswapV2: Trying to mint with invalid
                                 amounts amount0 :{amount0desired} and amount1 : {amount1desired}"""
                    message = f"Action {action_name} - " + message if action_name is not None else message
                    raise UniswapV2MintAmountsError(message)
        return amount0, amount1

    def _update_from_mint(  # noqa: C901
        self,
        amount0desired: int,
        amount1desired: int,
        amount0min: int | None,
        amount1min: int | None,
        msg_sender: Wallet | None,
        action_name: str | None = None,
    ) -> None:
        amount0, amount1 = self.get_optimal_amounts(amount0desired, amount1desired, amount0min, amount1min, action_name)

        balance0 = self.reserve0 + amount0
        balance1 = self.reserve1 + amount1

        if self.total_supply == 0:
            liquidity = round(math.sqrt(amount0 * amount1)) - self.minimum_liquidity
            self.total_supply += self.minimum_liquidity
            # permanently lock the first MINIMUM_LIQUIDITY tokens
        else:
            liquidity = min(
                mul(amount0, self.total_supply) // self.reserve0, mul(amount1, self.total_supply) // self.reserve1
            )

        if liquidity <= 0:
            message = "The amount of liquidity minted is zero"
            message = f"Action {action_name} - " + message if action_name is not None else message
            raise UniswapV2LiquidityError(message)

        self.total_supply += liquidity

        if msg_sender is not None:
            msg_sender.transfer_from(self.symbol0, amount0)
            msg_sender.transfer_from(self.symbol1, amount1)

            if msg_sender.get_balance_of(self.lp_token_name) == 0:
                create_event = Create(
                    block_number=self.block_number,
                    block_timestamp=self.block_timestamp,
                    liquidity=liquidity,
                    amount0=amount0,
                    amount1=amount1,
                    token_id=self.make_token_id(msg_sender),
                )
                self.events_ready_to_collect.append(create_event)

            else:
                update_event = Update(
                    block_number=self.block_number,
                    block_timestamp=self.block_timestamp,
                    liquidity=liquidity,
                    token_id=self.make_token_id(msg_sender),
                    amount0=amount0,
                    amount1=amount1,
                )
                self.events_ready_to_collect.append(update_event)

            msg_sender.transfer_to(self.lp_token_name, liquidity)

        self.reserve0 = balance0
        self.reserve1 = balance1

        mint_event = Mint(
            block_number=self.block_number,
            block_timestamp=self.block_timestamp,
            amount0=amount0,
            amount1=amount1,
        )
        msg = f"Transaction: Mint - Status: Succeeded - Comment: {mint_event}"
        if isinstance(msg_sender, Wallet) and not isinstance(msg_sender, ArbitrageurWallet):
            self.logger.info(
                f"Key: {self.logger_key_tx} - Timestamp: {self.block_timestamp} - Block number: {self.block_number} - "
                f"Agent: {msg_sender.agent_name} - " + msg
            )
        else:
            self.logger.debug(msg)

        self.events_ready_to_collect.append(mint_event)

    def _update_from_burn(
        self,
        amount: int,
        msg_sender: Wallet | None,
        action_name: str | None = None,
    ) -> None:
        if amount is None:
            message = "Amount should not be None"
            message = f"Action {action_name} - " + message if action_name is not None else message
            raise ValueError(message)
        amount0 = mul(self.reserve0, amount) // self.total_supply
        amount1 = mul(self.reserve1, amount) // self.total_supply

        if amount0 <= 0 or amount1 <= 0:
            message = "The amount of liquidity burned is zero"
            message = f"Action {action_name} - " + message if action_name is not None else message
            raise UniswapV2LiquidityError(message)

        if amount > self.total_supply - self.minimum_liquidity:
            message = "Trying to burn too much liquidity"
            message = f"Action {action_name} - " + message if action_name is not None else message
            raise UniswapV2LiquidityError(message)

        self.total_supply -= amount
        self.reserve0 -= amount0
        self.reserve1 -= amount1

        if msg_sender is not None:
            msg_sender.transfer_to(self.symbol0, amount0)
            msg_sender.transfer_to(self.symbol1, amount1)
            update_event = Update(
                block_number=self.block_number,
                block_timestamp=self.block_timestamp,
                liquidity=-1 * amount,
                token_id=self.make_token_id(msg_sender),
                amount0=amount0,
                amount1=amount1,
            )
            self.events_ready_to_collect.append(update_event)
            msg_sender.transfer_from(self.lp_token_name, amount, action_name)

        burn_event = Burn(block_number=self.block_number, block_timestamp=self.block_timestamp, amount=amount)
        burn = f"Transaction: Burn - Status: Succeeded - Comment: {burn_event}"
        if isinstance(msg_sender, Wallet) and not isinstance(msg_sender, ArbitrageurWallet):
            self.logger.info(
                f"Key: {self.logger_key_tx} - Timestamp: {self.block_timestamp} - Block number: {self.block_number} - "
                f"Agent: {msg_sender.agent_name} - " + burn
            )
        else:
            self.logger.debug(burn)

        self.events_ready_to_collect.append(burn_event)

    def get_amount_out(self, amount_in: int, reserve_in: int, reserve_out: int) -> int:
        amount_in_with_fee = mul(amount_in, (self.fee_denominator - self.fee_multiplicator))
        numerator = mul(amount_in_with_fee, reserve_out)
        denominator = mul(reserve_in, self.fee_denominator) + amount_in_with_fee
        return numerator // denominator

    def _update_from_swap(
        self,
        amount0_in: int | None,
        amount1_in: int | None,
        msg_sender: Wallet | None,
        action_name: str | None = None,
    ) -> None:
        amount0_out: int | None
        amount1_out: int | None

        if amount0_in is not None:
            fee_amount = mul(amount0_in, self.fee_multiplicator) // self.fee_denominator
            amount0_out = None
            amount1_out = self.get_amount_out(amount0_in, self.reserve0, self.reserve1)
            self.reserve0 += amount0_in
            self.reserve1 -= amount1_out

            if msg_sender is not None:
                msg_sender.transfer_from(self.symbol0, amount0_in)
                msg_sender.transfer_to(self.symbol1, amount1_out)

        elif amount1_in is not None:
            fee_amount = mul(amount1_in, self.fee_multiplicator) // self.fee_denominator
            amount0_out = self.get_amount_out(amount1_in, self.reserve1, self.reserve0)
            amount1_out = None
            self.reserve0 -= amount0_out
            self.reserve1 += amount1_in

            if msg_sender is not None:
                msg_sender.transfer_from(self.symbol1, amount1_in)
                msg_sender.transfer_to(self.symbol0, amount0_out)

        swap_event = Swap(
            block_number=self.block_number,
            block_timestamp=self.block_timestamp,
            amount0_in=amount0_in if amount0_in is not None else 0,
            amount1_in=amount1_in if amount1_in is not None else 0,
            amount0_out=amount0_out if amount0_out is not None else 0,
            amount1_out=amount1_out if amount1_out is not None else 0,
            zero_for_one=True if amount0_in is not None else False,
            fee_amount=fee_amount,
        )
        self.events_ready_to_collect.append(swap_event)

        swap = f"Transaction: Swap - Status: Succeeded -  Comment: {swap_event}"
        if isinstance(msg_sender, Wallet) and not isinstance(msg_sender, ArbitrageurWallet):
            self.logger.info(
                f"Key: {self.logger_key_tx} - Timestamp: {self.block_timestamp} - Block number: {self.block_number} - "
                f"Agent: {msg_sender.agent_name} - " + swap
            )
        else:
            self.logger.debug(swap)

    def make_token_id(self, msg_sender: Wallet) -> str:
        return f"{self.lp_token_name}-{msg_sender.agent_name}"
