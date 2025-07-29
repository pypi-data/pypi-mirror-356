import json
from pathlib import Path
from typing import Any, Dict, Tuple, Union


class ConfigLoader:
    @staticmethod
    def load(config: Union[str, dict, Path]) -> Tuple[str, str]:
        if isinstance(config, dict):
            return json.dumps(config), "json"

        if isinstance(config, (str, Path)):
            if isinstance(config, str):
                try:
                    json.loads(config)
                    return config, "json"
                except json.JSONDecodeError:
                    if config.strip().startswith("{") or config.strip().startswith("["):
                        raise ValueError("The provided string appears to be JSON but is malformed")

                    if config.strip().startswith("---") or ":" in config.splitlines()[0]:
                        return config, "yaml"

                    path = Path(config)
            else:
                path = config
        else:
            raise ValueError(f"Unsupported configuration type: {type(config)}")

        if not path.exists():
            raise FileNotFoundError(f"Configuration file '{path}' does not exist")

        content = path.read_text()

        if path.suffix.lower() in (".yml", ".yaml"):
            format_type = "yaml"
        elif path.suffix.lower() == ".json":
            format_type = "json"
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        return content, format_type

    @staticmethod
    def merge_configs(base_config: Dict[str, Any], update_config: Dict[str, Any]) -> Dict[str, Any]:
        result = base_config.copy()

        for key, value in update_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigLoader.merge_configs(result[key], value)
            else:
                result[key] = value

        return result
