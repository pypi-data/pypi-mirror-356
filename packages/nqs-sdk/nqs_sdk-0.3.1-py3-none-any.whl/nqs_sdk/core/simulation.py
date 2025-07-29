import logging
from pathlib import Path
from typing import Any, List, Optional, Union

from nqs_pycore import Simulator, SimulatorBuilder

from nqs_sdk import ProtocolManager

from .config import ConfigLoader
from .protocol_registry import ProtocolID


class Simulation:
    def __init__(
        self,
        protocols: Union[ProtocolManager, List[ProtocolManager]],
        config: Union[str, dict, Path],
        namespace: Optional[str] = None,
    ):
        self.protocols = [protocols] if not isinstance(protocols, list) else protocols
        self.config = config
        self.simulator = None
        self.is_backtest = False  # FIXME: get this from binding instead
        self._build()

    def _build(self) -> None:
        config_content, config_format = ConfigLoader.load(self.config)

        if isinstance(config_content, str):
            self.is_backtest = "backtest" in config_content.lower()
        elif isinstance(self.config, dict):
            self.is_backtest = "backtest" in self.config or any(
                "backtest" in str(k).lower() for k in self.config.keys()
            )

        if config_format == "yaml":
            builder = SimulatorBuilder.from_yaml(config_content)
        else:
            builder = SimulatorBuilder.from_json(config_content)

        for protocol in self.protocols:
            builder.add_factory(protocol.get_factory())

        self.simulator = builder.build()

    def get_protocol(self, protocol_id: str) -> Any:
        if not self.simulator:
            raise RuntimeError("Simulation has not been built yet")

        return self.simulator.get_py_protocol(protocol_id)

    def run(self) -> str:
        if not self.simulator:
            raise RuntimeError("Simulation has not been built yet")
        logging.info("Simulation starting...")
        results = self.simulator.run_to_json()
        logging.info("Simulation ended")
        return results

    def to_json(self) -> str:
        if not self.simulator:
            raise RuntimeError("Simulation has not been built yet")

        return self.simulator.to_json()

    @classmethod
    def from_json(cls, json_data: str) -> "Simulation":
        simulation = cls([], {})
        simulation.simulator = Simulator.from_json(json_data)
        return simulation

    @classmethod
    def from_namespace(cls, namespace: str, protocol_names: List[str], config: Union[str, dict, Path]) -> "Simulation":
        protocol_managers = []
        for name in protocol_names:
            id = ProtocolID(namespace, name)
            protocol_manager = ProtocolManager.from_id(id)
            protocol_managers.append(protocol_manager)

        return cls(protocol_managers, config, namespace=namespace)
