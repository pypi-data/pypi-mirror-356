from typing import Any, Dict

from nqs_pycore import ProtocolFactoryAdapter

from .protocol_registry import ProtocolID, ProtocolRegistry


class ProtocolManager:
    def __init__(self, protocol_id: str):
        self.protocol_id = protocol_id

        self.protocol_identifier = ProtocolID.from_string(protocol_id)

        factory = ProtocolRegistry.get_factory(protocol_id)

        if isinstance(factory, ProtocolFactoryAdapter):
            self._factory_instance = factory
        else:
            self._factory_instance = ProtocolFactoryAdapter(factory)

    def get_factory(self) -> Any:
        return self._factory_instance

    @classmethod
    def get_available_protocols(cls) -> Dict[str, str]:
        return ProtocolRegistry.get_available_protocols()

    @classmethod
    def from_id(cls, id: ProtocolID) -> "ProtocolManager":
        return cls(str(id))

    def __str__(self) -> str:
        return f"ProtocolManager for {self.protocol_id}"

    def __repr__(self) -> str:
        return self.__str__()
