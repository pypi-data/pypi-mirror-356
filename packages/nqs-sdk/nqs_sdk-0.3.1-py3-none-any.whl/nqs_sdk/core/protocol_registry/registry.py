from typing import Any, Callable, Dict, Optional, Type

from nqs_pycore import implementations

from nqs_sdk.interfaces import ProtocolFactory

from .errors import DuplicateProtocolError, InvalidProtocolFactoryError, ProtocolNotFoundError
from .protocol_id import ProtocolID


class ProtocolRegistry:
    _factories: Dict[ProtocolID, Type[ProtocolFactory]] = {}
    _default_namespace = "nqs_sdk"
    _metadata: Dict[ProtocolID, Dict[str, str]] = {}

    @classmethod
    def register(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Callable[[Type[ProtocolFactory]], Type[ProtocolFactory]]:
        def decorator(factory_class: Type[ProtocolFactory]) -> Type[ProtocolFactory]:
            tmp_factory = factory_class()

            protocol_name = name if name is not None else tmp_factory.id()
            protocol_namespace = namespace if namespace is not None else cls._default_namespace

            id = ProtocolID(protocol_namespace, protocol_name, version)

            cls._validate_factory(factory_class, id)
            cls._factories[id] = factory_class

            if metadata:
                cls._metadata[id] = metadata
            else:
                cls._metadata[id] = {"name": str(id), "description": factory_class.__doc__ or "No description provided"}

            return factory_class

        return decorator

    @classmethod
    def get_factory(cls, protocol_id: str) -> ProtocolFactory:
        print("_factories")
        print(cls._factories)

        try:
            id = ProtocolID.from_string(protocol_id)
            if id in cls._factories:
                factory_class = cls._factories[id]
                factory_from_class: ProtocolFactory = factory_class()
                return factory_from_class
        except Exception:
            pass

        default_id = ProtocolID(cls._default_namespace, protocol_id)
        if default_id in cls._factories:
            factory_class = cls._factories[default_id]
            factory_from_class = factory_class()
            return factory_from_class

        for id, factory_class in cls._factories.items():
            if id.name == protocol_id:
                factory_from_class = factory_class()
                return factory_from_class

        factory_name = f"{protocol_id}_factory"
        if hasattr(implementations, factory_name):
            factory_func = getattr(implementations, factory_name)
            factory_from_func: ProtocolFactory = factory_func()
            return factory_from_func

        available_protocols = list(cls.get_available_protocols().keys())
        raise ProtocolNotFoundError(
            f"Protocol '{protocol_id}' not found. " f"Available protocols are: {available_protocols}"
        )

    @classmethod
    def get_factory_by_id(cls, id: ProtocolID) -> ProtocolFactory:
        if id in cls._factories:
            factory_class = cls._factories[id]
            factory_from_class: ProtocolFactory = factory_class()
            return factory_from_class
        raise ProtocolNotFoundError(f"No factory registered for id: {id}")

    @classmethod
    def _validate_factory(cls, factory_class: Type[ProtocolFactory], protocol_id: ProtocolID) -> None:
        required_methods = ["id", "build"]
        for method in required_methods:
            if not hasattr(factory_class, method) or not callable(getattr(factory_class, method)):
                raise InvalidProtocolFactoryError(f"Factory class must implement method: {method}")

        if protocol_id in cls._factories:
            raise DuplicateProtocolError(f"Protocol ID '{protocol_id}' is already registered")

    @classmethod
    def get_available_protocols(cls) -> Dict[str, str]:
        result = {}

        for id in cls._factories:
            result[str(id)] = id.namespace

        native_protocols = [
            name.replace("_factory", "")
            for name in dir(implementations)
            if callable(getattr(implementations, name)) and name.endswith("_factory")
        ]

        for protocol_id in native_protocols:
            if protocol_id not in result:
                result[protocol_id] = "native"

        return result

    @classmethod
    def set_default_namespace(cls, namespace: str) -> None:
        cls._default_namespace = namespace

    @classmethod
    def get_protocol_metadata(cls, protocol_id: Optional[ProtocolID] = None) -> Any:
        if protocol_id:
            if protocol_id in cls._metadata:
                return cls._metadata[protocol_id]
            raise ProtocolNotFoundError(f"Protocol '{protocol_id}' not found")

        return cls._metadata

    @classmethod
    def unregister(cls, protocol_id: ProtocolID) -> bool:
        if protocol_id in cls._factories:
            del cls._factories[protocol_id]
            if protocol_id in cls._metadata:
                del cls._metadata[protocol_id]
            return True
        return False
