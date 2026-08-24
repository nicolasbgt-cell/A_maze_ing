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
                    raise ConfigError (f"Invalid line: {line!r}") from error
                pairs[key.strip()] = value.strip()
    except FileNotFoundError as error:
        raise ConfigError(f"Configuration file not found: {path!r}") from error
    return pairs


def load_config(path: str) -> Config:

    pairs = _read_pairs(path)
    if not pairs:
        raise ConfigError("Configuration file is empty.")
    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    missing = []
    
    for key in required_keys:
        if key not in pairs:
            missing.append(key)
    if missing:
        raise ConfigError(f"Missing keys in configuration file: {missing}")

    if "SEED" in pairs:
        seed: int | None = int(pairs["SEED"])
    else:
        seed: int | None = None

    try:
        width: int = int(pairs["WIDTH"])
        height: int = int(pairs["HEIGHT"])
        entry_parts = pairs["ENTRY"].split(",")
        entry: Coordinate = (int(entry_parts[0]), int(entry_parts[1]))
        exit_parts = pairs["EXIT"].split(",")
        exit_coord: Coordinate = (int(exit_parts[0]), int(exit_parts[1]))
        perfect: bool = pairs["PERFECT"] == "True"
    except (ValueError, IndexError) as error:
        raise ConfigError("Invalid numeric value in configuration :"
                          f"{error}") from error

    return Config(width=width, height=height, entry=entry, exit=exit_coord,
                  output_file=pairs["OUTPUT_FILE"], perfect=perfect, seed=seed)
