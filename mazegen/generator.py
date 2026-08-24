"""Representer les murs et les dimensions du labyrinthe."""

from typing import TypeAlias


Coordinate: TypeAlias = tuple[int, int]

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST


class MazeGenerator:
    """Memoriser les parametres et representer un labyrinthe."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit: Coordinate,
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        """Initialiser une grille dont tous les murs sont fermes.

        Args:
            width: Nombre de colonnes
            height: Nombre de lignes
            entry: Coordonnees de l'entree au format (x, y)
            exit: Coordonnees de la sortie au format (x, y)
            perfect: Indique si le labyrinthe doit etre parfait
            seed: Valeur utilisee pour reproduire la generation
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

        self.grid: list[list[int]] = []

        for _ in range(self.height):
            row: list[int] = []

            for _ in range(self.width):
                row.append(ALL_WALLS)

            self.grid.append(row)

    def _is_inside(
            self,
            coordinate: Coordinate,
    ) -> bool:
        """Verifier qu'une cellule (x, y) existe dans les limites du labyrinthe."""
        x, y = coordinate
        return 0 <= x < self.width and 0 <= y < self.height

    def _neighbours(
            self,
            coordinate: Coordinate,
    ) -> list[Coordinate]:
        """Renvoyer les coordonnees voisines situees dans la grille."""
        x, y = coordinate

        candidates: list[Coordinate] = [
            (x, y - 1),  # Nord
            (x + 1, y),  # Est
            (x, y + 1),  # Sud
            (x - 1, y),  # Ouest
        ]

        neighbours: list[Coordinate] = []

        for candidate in candidates:
            if self._is_inside(candidate):
                neighbours.append(candidate)

        return neighbours