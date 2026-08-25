from dataclasses import dataclass
from mazegen.generator import Coordinate


class ConfigError(Exception):
    """Class qui souleve les erreurs de configuration"""


@dataclass
class Config:
    """Options de generation validees, pretes a etre transmises au moteur."""

    width: int
    height: int
    entry: Coordinate
    exit: Coordinate
    output_file: str
    perfect: bool = False
    seed: int | None = None


def _read_pairs(path: str) -> dict[str, str]:
    pairs: dict[str, str] = {}
    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    key, value = line.split("=", 1)
                except ValueError as error:
                    raise ConfigError(f"Invalid line: {line!r}") from error
                pairs[key.strip()] = value.strip()
    except FileNotFoundError as error:
        raise ConfigError(f"Configuration file not found: {path!r}") from error
    return pairs


def load_config(path: str) -> Config:

    pairs = _read_pairs(path)
    if not pairs:
        raise ConfigError("Configuration file is empty.")
    required_keys = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
            ]
    missing = []
    for key in required_keys:
        if key not in pairs:
            missing.append(key)
    if missing:
        raise ConfigError(f"Missing keys in configuration file: {missing}")

    try:
        seed = int(pairs["SEED"]) if "SEED" in pairs else None
        width: int = int(pairs["WIDTH"])
        height: int = int(pairs["HEIGHT"])
        entry_x, entry_y = pairs["ENTRY"].split(",")
        entry: Coordinate = (int(entry_x), int(entry_y))
        exit_x, exit_y = pairs["EXIT"].split(",")
        exit_coord: Coordinate = (int(exit_x), int(exit_y))
    except (ValueError, IndexError) as error:
        raise ConfigError("Invalid numeric value in configuration :"
                          f"{error}") from error

    perfect_value = pairs["PERFECT"]
    if perfect_value not in {"True", "False"}:
        raise ConfigError("PERFECT must be True or False.")
    perfect = perfect_value == "True"

    return Config(width=width, height=height, entry=entry, exit=exit_coord,
                  output_file=pairs["OUTPUT_FILE"], perfect=perfect, seed=seed)
