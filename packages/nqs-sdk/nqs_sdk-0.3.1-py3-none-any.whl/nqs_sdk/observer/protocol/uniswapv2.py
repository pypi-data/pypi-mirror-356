import logging
import math
from decimal import Decimal
from typing import Dict, Optional, Sequence

from nqs_pycore import Wallet

from nqs_sdk.constants import CAP_FEES_TO_LVR, PROFIT_MULTIPLICATOR
from nqs_sdk.observer import DEFAULT_DECIMALS, ABCObserver, SingleObservable
from nqs_sdk.observer.metric_names import Uniswapv2Metrics
from nqs_sdk.observer.protocol.buffer import TimeSeriesBuffer
from nqs_sdk.observer.protocol.protocol_observer import ProtocolObserver
from nqs_sdk.observer.protocol.token_metrics import TokenMetricsUniv2
from nqs_sdk.protocol.amm.uniswapv2.events import Burn, Create, Mint, Swap, Update
from nqs_sdk.protocol.amm.uniswapv2.math import mul
from nqs_sdk.protocol.amm.uniswapv2.uniswap_v2 import UniswapV2
from nqs_sdk.transaction import ABCTransaction
from nqs_sdk.transaction.uniswapv2 import SwapTransactionUniv2


class TokenNotFoundError(Exception):
    "Exception raised when the token id of the agent is not found in the token metrics."

    def __init__(self, message: str) -> None:
        super().__init__(message)


class UniswapV2Observer(ProtocolObserver):
    def __init__(self, protocol: UniswapV2) -> None:
        super().__init__()
        self.amm: UniswapV2 = protocol
        self.total_volume0 = 0
        self.total_volume1 = 0
        self.total_volume_num = 0
        self.total_fee0 = 0
        self.total_fee1 = 0
        self.total_fee_num = 0
        self.buffer = TimeSeriesBuffer()
        self.logger = logging.getLogger("UniswapV2ObserverLogger")
        self.token_metrics: dict[str, TokenMetricsUniv2] = {}

    def set_environment(self, observable_id: str, env_observers: Optional[Dict[str, ABCObserver]]) -> None:
        if env_observers is None:
            raise ValueError("Uniswap v2 observer needs to be provided with environment observers")
        self._observer_id = observable_id
        self.metric_names = Uniswapv2Metrics(self._observer_id, self.amm.symbol0, self.amm.symbol1)

    def get_all_observables(self, block_number: int, block_timestamp: int) -> dict[str, SingleObservable]:
        new_observables: dict[str, SingleObservable] = {}
        market_spot = self.spot_oracle.get_token_numeraire_spot([self.amm.symbol0, self.amm.symbol1], block_timestamp)

        self.update_from_protocol_events(market_spot)
        self._update_timeseries_buffer(block_number, block_timestamp)
        new_observables.update(self._get_pool_dex_spot())
        new_observables.update(self._get_pool_liquidity())
        new_observables.update(self._get_pool_holdings(market_spot))
        new_observables.update(self._get_pool_volumes())
        new_observables.update(self._get_pool_fees())
        return new_observables

    def update_from_protocol_events(self, market_spot: dict[tuple[str, str], float]) -> None:
        events = self.amm.events_ready_to_collect
        if len(events) == 0:
            return None
        self._update_volumes_and_fees(events, market_spot)
        self._update_token_metrics(events, market_spot)
        self.amm.events_ready_to_collect.clear()

    def _update_token_metrics(
        self, events: list[Swap | Mint | Burn | Create | Update], market_spots: dict[tuple[str, str], float]
    ) -> None:
        for event in events:
            if isinstance(event, Create):
                if event.token_id in self.token_metrics.keys():
                    # token already exists so we consider it an update event
                    self.logger.debug(f"Update event: {event}")
                    market_spot = market_spots[(self.amm.symbol1, self.spot_oracle.numeraire)]
                    self.token_metrics[event.token_id].update_from_update_event(
                        block_number=event.block_number,
                        delta_amount=event.liquidity,
                        price=float(str(self.amm.get_dex_spot())),
                        market_spot=market_spot,
                        amount0=event.amount0,
                        amount1=event.amount1,
                    )
                    return None

                self.logger.debug(f"Create event: {event}")
                market_spot = market_spots[(self.amm.symbol1, self.spot_oracle.numeraire)]
                token_metrics = TokenMetricsUniv2(
                    token_id=event.token_id,
                    block_number=event.block_number,
                    block_timestamp=event.block_timestamp,
                    decimal0=self.amm.decimals0,
                    decimal1=self.amm.decimals1,
                    numeraire_decimals=self.numeraire_decimals,
                    liquidity=event.liquidity,
                    market_spot=market_spot,
                    initial_amount0=event.amount0,
                    initial_amount1=event.amount1,
                    price=float(str(self.amm.get_dex_spot())),
                )
                self.token_metrics[event.token_id] = token_metrics
            elif isinstance(event, Update):
                self.logger.debug(f"Update event: {event}")
                market_spot = market_spots[(self.amm.symbol1, self.spot_oracle.numeraire)]
                try:
                    self.token_metrics[event.token_id].update_from_update_event(
                        block_number=event.block_number,
                        delta_amount=event.liquidity,
                        price=float(str(self.amm.get_dex_spot())),
                        market_spot=market_spot,
                        amount0=event.amount0,
                        amount1=event.amount1,
                    )
                except KeyError:
                    raise ValueError("Token does not exist")
        return None

    def _get_pool_dex_spot(self) -> dict[str, SingleObservable]:
        spot = self.amm.get_dex_spot()
        return {
            self.metric_names.spot: SingleObservable(round(Decimal(spot).scaleb(DEFAULT_DECIMALS)), DEFAULT_DECIMALS)
        }

    def _get_pool_liquidity(self) -> dict[str, SingleObservable]:
        return {self.metric_names.pool_liquidity: SingleObservable(self.amm.total_supply, DEFAULT_DECIMALS)}

    def _get_pool_holdings(self, market_spot: dict[tuple[str, str], float]) -> dict[str, SingleObservable]:
        tvl_num = round(
            Decimal(self.amm.reserve0).scaleb(-self.amm.decimals0)
            * Decimal(market_spot[(self.amm.symbol0, self.spot_oracle.numeraire)]).scaleb(self.numeraire_decimals)
            + Decimal(self.amm.reserve1).scaleb(-self.amm.decimals1)
            * Decimal(market_spot[(self.amm.symbol1, self.spot_oracle.numeraire)]).scaleb(self.numeraire_decimals)
        )
        return {
            self.metric_names.holding0: SingleObservable(self.amm.reserve0, self.amm.decimals0),
            self.metric_names.holding1: SingleObservable(self.amm.reserve1, self.amm.decimals1),
            self.metric_names.tvl_num: SingleObservable(tvl_num, self.numeraire_decimals),
        }

    def _get_pool_volumes(self) -> dict[str, SingleObservable]:
        volumes_observables: dict[str, SingleObservable] = {}
        volumes_observables.update(
            {self.metric_names.volume0: SingleObservable(self.total_volume0, self.amm.decimals0)}
        )
        volumes_observables.update(
            {self.metric_names.volume1: SingleObservable(self.total_volume1, self.amm.decimals1)}
        )
        volumes_observables.update(
            {self.metric_names.volume_num: SingleObservable(self.total_volume_num, self.numeraire_decimals)}
        )
        return volumes_observables

    def _get_pool_fees(self) -> dict[str, SingleObservable]:
        fees_observables: dict[str, SingleObservable] = {}
        fees_observables.update({self.metric_names.fees0: SingleObservable(self.total_fee0, self.amm.decimals0)})
        fees_observables.update({self.metric_names.fees1: SingleObservable(self.total_fee1, self.amm.decimals1)})
        fees_observables.update(
            {self.metric_names.total_fees_pool: SingleObservable(self.total_fee_num, self.numeraire_decimals)}
        )
        return fees_observables

    def _update_volumes_and_fees(
        self, events: list[Swap | Mint | Burn], market_spot: dict[tuple[str, str], float]
    ) -> None:
        for event in events:
            if isinstance(event, Swap):
                if event.zero_for_one:
                    fee0 = event.fee_amount
                    volume0 = event.amount0_in
                    spot0num = market_spot[(self.amm.symbol0, self.spot_oracle.numeraire)]
                    self.total_volume0 += volume0
                    self.total_fee0 += fee0
                    self.total_volume_num += round(
                        Decimal(volume0).scaleb(-self.amm.decimals0) * Decimal(spot0num).scaleb(self.numeraire_decimals)
                    )
                    fee_num = round(
                        Decimal(fee0).scaleb(-self.amm.decimals0) * Decimal(spot0num).scaleb(self.numeraire_decimals)
                    )
                    self.total_fee_num += fee_num
                    self._update_agent_fees(is_zero=True, fee_token=fee0, fee_num=fee_num)
                    self.logger.debug(f"Swap event zero for one: volume={volume0} and fee={fee0}")
                else:
                    fee1 = event.fee_amount
                    volume1 = event.amount1_in
                    spot1num = market_spot[(self.amm.symbol1, self.spot_oracle.numeraire)]
                    self.total_volume1 += volume1
                    self.total_fee1 += fee1
                    self.total_volume_num += round(
                        Decimal(volume1).scaleb(-self.amm.decimals1) * Decimal(spot1num).scaleb(self.numeraire_decimals)
                    )
                    fee_num = round(
                        Decimal(fee1).scaleb(-self.amm.decimals1) * Decimal(spot1num).scaleb(self.numeraire_decimals)
                    )
                    self.total_fee_num += fee_num
                    self._update_agent_fees(is_zero=False, fee_token=fee1, fee_num=fee_num)
                    self.logger.debug(f"Swap event zero for one: volume={volume1} and fee={fee1}")
        return None

    def _update_agent_fees(self, is_zero: bool, fee_token: int, fee_num: int) -> None:
        for token_id, token_metrics in self.token_metrics.items():
            liquidity = token_metrics.liquidity
            if is_zero:
                token_metrics.cumulative_fee0 += round(Decimal(fee_token * liquidity / self.amm.total_supply))
                token_metrics.cumulative_fee_num += round(Decimal(fee_num * liquidity / self.amm.total_supply))
            else:
                token_metrics.cumulative_fee1 += round(Decimal(fee_token * liquidity / self.amm.total_supply))
                token_metrics.cumulative_fee_num += round(Decimal(fee_num * liquidity / self.amm.total_supply))
        return None

    def _update_timeseries_buffer(self, block_number: int, block_timestamp: int) -> None:
        if self.buffer.updatable(block_number):
            price = float(str(self.amm.get_dex_spot()))
            self.buffer.update_from_swap_event(price=price, block_number=block_number, block_timestamp=block_timestamp)

    def exists_arbitrage_opportunity(self, block_number: int, block_timestamp: int) -> bool:
        dex_spot_data = self._get_pool_dex_spot()[self.metric_names.spot]
        dex_spot = dex_spot_data.value / 10**dex_spot_data.decimals

        spot_symbol = [(self.amm.symbol0, self.amm.symbol1)]
        market_spot = self.spot_oracle.get_selected_spots(spot_symbol, block_timestamp)[spot_symbol[0]]
        fees = self.amm.fee_multiplicator / self.amm.fee_denominator
        if abs(dex_spot / market_spot - 1) > PROFIT_MULTIPLICATOR * fees and self.amm.total_supply > 0:
            self.arbitrage_prices = (dex_spot, market_spot)
            return True
        else:
            self.arbitrage_prices = (-1, -1)
            return False

    def create_arbitrage_transactions(
        self, block_number: int, block_timestamp: int, arbitrageur_wallet: Wallet
    ) -> Sequence[ABCTransaction]:
        amount0_in, amount1_in = self._get_arbitrage_value()
        if amount0_in == 0 and amount1_in is None or amount0_in is None and amount1_in == 0:
            return []
        else:
            return [
                SwapTransactionUniv2(
                    block_number=block_number,
                    protocol_id=self._observer_id,
                    sender_wallet=arbitrageur_wallet,
                    amount0_in=amount0_in,
                    amount1_in=amount1_in,
                )
            ]

    def _get_arbitrage_value(self) -> tuple[int | None, int | None]:
        if self.arbitrage_prices == (-1, -1):
            raise ValueError("There is no arbitrage opportunity, this function should not be called")
        dex_spot, market_spot = self.arbitrage_prices
        fees = self.amm.fee_multiplicator / self.amm.fee_denominator
        liquidity = self.amm.total_supply
        liquidity_tolerance = 0
        delta_amount0: int | None
        delta_amount1: int | None

        if (market_spot / dex_spot - 1) < -fees and liquidity > liquidity_tolerance:
            delta_amount0 = round(self.amm.reserve0 * (math.sqrt(dex_spot / market_spot) - 1) / (1 - fees))
            delta_amount1 = None
            return delta_amount0, delta_amount1

        elif (market_spot / dex_spot - 1) > fees and liquidity > liquidity_tolerance:
            delta_amount1 = round(self.amm.reserve1 * (math.sqrt(market_spot / dex_spot) - 1) / (1 - fees))
            delta_amount0 = None
            return delta_amount0, delta_amount1

        return 0, None

    def agents_id_to_update(self) -> list[str]:
        return []

    def get_agent_net_position(
        self, wallet: Wallet, market_spots: dict[tuple[str, str], float]
    ) -> tuple[Decimal, Decimal, Decimal]:
        lp_token_symbol = self.amm.lp_token_name
        lp_token_balance_agent = int(wallet.get_balance_of(lp_token_symbol))
        if lp_token_balance_agent == 0:
            return Decimal(0), Decimal(0), Decimal(0)
        token0_value = Decimal(mul(self.amm.reserve0, lp_token_balance_agent) // self.amm.total_supply)
        token1_value = Decimal(mul(self.amm.reserve1, lp_token_balance_agent) // self.amm.total_supply)
        total_position_in_token_1_unit = token0_value * self.amm.get_raw_dex_spot() + token1_value
        token_1_spot_num = market_spots[self.amm.symbol1, self.spot_oracle.numeraire]
        numeraire_value = (total_position_in_token_1_unit * Decimal(str(token_1_spot_num))).scaleb(
            self.numeraire_decimals - self.amm.decimals1
        )
        return token0_value, token1_value, numeraire_value

    def get_agent_observables(
        self, block_number: int, block_timestamp: int, wallet: Wallet
    ) -> dict[str, SingleObservable]:
        agent_obs: Dict[str, SingleObservable] = {}
        market_spots = self.spot_oracle.get_token_numeraire_spot([self.amm.symbol0, self.amm.symbol1], block_timestamp)
        token0_holdings, token1_holdings, net_position = self.get_agent_net_position(wallet, market_spots)
        agent_obs.update(
            {self.metric_names.token_amount0: SingleObservable(round(token0_holdings), self.amm.decimals0)}
        )
        agent_obs.update(
            {self.metric_names.token_amount1: SingleObservable(round(token1_holdings), self.amm.decimals1)}
        )
        agent_obs.update(
            {self.metric_names.net_position: SingleObservable(round(net_position), self.numeraire_decimals)}
        )
        agent_obs.update(
            {
                self.metric_names.liquidity: SingleObservable(
                    int(wallet.get_balance_of(self.amm.lp_token_name)), DEFAULT_DECIMALS
                )
            }
        )
        try:
            agent_obs.update(
                self._get_agent_il(wallet=wallet, block_timestamp=block_timestamp, market_spots=market_spots)
            )
            agent_obs.update(
                self._get_agent_pl(wallet=wallet, block_timestamp=block_timestamp, market_spots=market_spots)
            )
            agent_obs.update(
                self._get_agent_lvr(wallet=wallet, block_timestamp=block_timestamp, market_spots=market_spots)
            )
            agent_obs.update(self._get_agent_fee_share(wallet=wallet))
        except TokenNotFoundError:
            pass
        return agent_obs

    def _get_agent_il(
        self, wallet: Wallet, block_timestamp: int, market_spots: dict[tuple[str, str], float]
    ) -> dict[str, SingleObservable]:
        token_id = self.amm.make_token_id(wallet)
        symbol_spot_list = [self.amm.symbol0, self.amm.symbol1]
        decimals_list = [self.amm.decimals0, self.amm.decimals1]
        spot_list = [market_spots[(symbol, self.spot_oracle.numeraire)] for symbol in symbol_spot_list]
        try:
            token_metrics = self.token_metrics[token_id]
        except KeyError:
            raise TokenNotFoundError(
                f"Could not retrieve position metrics for agent {wallet.agent_name} in pool {self.amm.name}"
            )
        total_abs_il = Decimal(0)
        total_perc_il = Decimal(0)
        total_static_ptf_value = Decimal(0)
        for position in token_metrics.il_open_positions:
            position_balances = position[1]
            total_static_ptf_value += (
                (Decimal(position_balances[0]) * self.amm.get_raw_dex_spot() + Decimal(position_balances[1]))
                * Decimal(spot_list[1])
            ).scaleb(self.numeraire_decimals - decimals_list[1])

        position_value = self.get_agent_net_position(wallet, market_spots)[2]
        total_abs_il = position_value - total_static_ptf_value

        if total_static_ptf_value == 0:
            total_perc_il = Decimal(0)
        else:
            total_perc_il = Decimal(100) * total_abs_il / total_static_ptf_value
        return {
            self.metric_names.static_ptf_value: SingleObservable(
                round(total_static_ptf_value), self.numeraire_decimals
            ),
            self.metric_names.abs_impermanent_loss: SingleObservable(round(total_abs_il), self.numeraire_decimals),
            self.metric_names.perc_impermanent_loss: SingleObservable(
                round(Decimal(total_perc_il).scaleb(DEFAULT_DECIMALS)), DEFAULT_DECIMALS
            ),
        }

    def _get_agent_fee_share(self, wallet: Wallet) -> dict[str, SingleObservable]:
        token_id = self.amm.make_token_id(wallet)
        try:
            token_metrics = self.token_metrics[token_id]
        except KeyError:
            raise TokenNotFoundError(
                f"Could not retrieve position metrics for agent {wallet.agent_name} in pool {self.amm.name}"
            )
        return {
            self.metric_names.total_fees: SingleObservable(
                round(token_metrics.cumulative_fee_num), self.numeraire_decimals
            ),
            self.metric_names.total_fees_0: SingleObservable(round(token_metrics.cumulative_fee0), self.amm.decimals0),
            self.metric_names.total_fees_1: SingleObservable(round(token_metrics.cumulative_fee1), self.amm.decimals1),
        }

    def _get_agent_pl(
        self, wallet: Wallet, block_timestamp: int, market_spots: dict[tuple[str, str], float]
    ) -> dict[str, SingleObservable]:
        token_id = self.amm.make_token_id(wallet)
        try:
            token_metrics = self.token_metrics[token_id]
        except KeyError:
            raise TokenNotFoundError(
                f"Could not retrieve position metrics for agent {wallet.agent_name} in pool {self.amm.name}"
            )
        return {
            self.metric_names.permanent_loss_num: SingleObservable(
                round(Decimal(token_metrics.abs_pl_num)), self.numeraire_decimals
            )
        }

    def _get_agent_lvr(
        self, wallet: Wallet, block_timestamp: int, market_spots: dict[tuple[str, str], float]
    ) -> dict[str, SingleObservable]:
        token_id = self.amm.make_token_id(wallet)
        try:
            token_metrics = self.token_metrics[token_id]
        except KeyError:
            raise TokenNotFoundError(
                f"Could not retrieve position metrics for agent {wallet.agent_name} in pool {self.amm.name}"
            )
        token_metrics.update_lvr_from_buffer(self.buffer)
        lvr = token_metrics.lvr
        lvr = lvr * market_spots[(self.amm.symbol1, self.spot_oracle.numeraire)]

        if lvr == 0:
            total_fees_relative_to_lvr = 0.0
        else:
            total_fees_relative_to_lvr = 100 * token_metrics.cumulative_fee_num / lvr
        total_fees_relative_to_lvr = min(total_fees_relative_to_lvr, CAP_FEES_TO_LVR)

        return {
            self.metric_names.loss_versus_rebalancing: SingleObservable(
                round(lvr * 10**self.numeraire_decimals), self.numeraire_decimals
            ),
            self.metric_names.total_fees_relative_to_lvr: SingleObservable(
                round(total_fees_relative_to_lvr * 10**DEFAULT_DECIMALS), DEFAULT_DECIMALS
            ),
        }
