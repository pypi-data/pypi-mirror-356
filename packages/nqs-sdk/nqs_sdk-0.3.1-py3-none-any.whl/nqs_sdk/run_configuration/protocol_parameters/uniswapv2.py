from dataclasses import dataclass

from nqs_sdk.run_configuration.protocol_parameters.protocol import SimulatedProtocolInformation
from nqs_sdk.run_configuration.utils import DEFAULT_TOKEN_DECIMALS, TokenInfo
from nqs_sdk.state import ABCProtocolState
from nqs_sdk.token_utils import wrap_token


@dataclass(kw_only=True)
class FakeStateUniv2(ABCProtocolState):
    id: int
    name: str
    block_number: int
    block_timestamp: int
    token0: str
    token1: str
    symbol0: str
    symbol1: str
    decimals0: int
    decimals1: int
    initial_balance0: int | None
    initial_balance1: int | None


class Uniswapv2ProtocolInformation(SimulatedProtocolInformation):
    def __init__(
        self,
        protocol_name: str,
        protocol_info: dict,
        id: int,
        block_number_start: int,
        timestamp_start: int,
        token_info_dict: dict[str, TokenInfo],
    ) -> None:
        super().__init__(
            protocol_name=protocol_name,
            id=id,
            block_number_start=block_number_start,
            timestamp_start=timestamp_start,
            protocol_info=protocol_info,
            random_generation_params=protocol_info["random_generation_params"],
            token_info_dict=token_info_dict,
        )
        self.lp_token_symbol = str("Univ2_LP_") + self.protocol_name
        self.set_token_info(self.lp_token_symbol, DEFAULT_TOKEN_DECIMALS, "0x" + self.lp_token_symbol)
        initial_state = protocol_info["initial_state"]
        if "custom_state" in initial_state.keys():
            self.initial_state = self.get_custom_state(custom_states=initial_state["custom_state"])
        elif "historical_state" in initial_state.keys():
            self.historical_state = self.get_historical_state(historical_state=initial_state["historical_state"])
        else:
            raise NotImplementedError("Only custom_state and historical_state are supported")

    def get_custom_state(self, custom_states: dict) -> ABCProtocolState:
        custom_states["symbol0"] = wrap_token(custom_states["symbol_token0"])
        custom_states["symbol1"] = wrap_token(custom_states["symbol_token1"])
        decimals0 = self.get_token_info(token=custom_states["symbol_token0"]).decimals
        decimals1 = self.get_token_info(token=custom_states["symbol_token1"]).decimals
        initial_balance = custom_states["initial_balance"]
        initial_balance0, initial_balance1 = None, None

        if initial_balance["unit"] == "token0":
            initial_balance0 = initial_balance["amount"]
        elif initial_balance["unit"] == "token1":
            initial_balance1 = initial_balance["amount"]
        else:
            raise ValueError("The initial balance unit must be token0 or token1")

        return FakeStateUniv2(
            id=self.id,
            name=self.protocol_name,
            block_number=self.block_number_start,
            block_timestamp=self.timestamp_start,
            token0="0x" + custom_states["symbol0"],
            token1="0x" + custom_states["symbol1"],
            symbol0=custom_states["symbol0"],
            symbol1=custom_states["symbol1"],
            decimals0=decimals0,
            decimals1=decimals1,
            initial_balance0=initial_balance0,
            initial_balance1=initial_balance1,
        )

    def get_historical_state(self, historical_state: dict) -> ABCProtocolState:
        raise NotImplementedError("Historical state is not supported for Uniswapv2 protocol")
