"""API publique du paquet de generation de labyrinthes."""

from .generator import MazeGenerator
from .walls import ALL_WALLS, EAST, NORTH, SOUTH, WEST, Coordinate

__all__ = [
    "ALL_WALLS",
    "EAST",
    "NORTH",
    "SOUTH",
    "WEST",
    "Coordinate",
    "MazeGenerator",
]
