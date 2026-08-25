"""Representer et generer un labyrinthe."""

import random
from typing import TypeAlias


Coordinate: TypeAlias = tuple[int, int]

NORTH = 1  # binaire 0001
EAST = 2   # binaire 0010
SOUTH = 4  # binaire 0100
WEST = 8   # binaire 1000
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
        self._random = random.Random(seed)

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

    def _open_passage(
        self,
        current: Coordinate,
        neighbour: Coordinate,
    ) -> None:
        """Ouvrir les murs communs entre deux cellules voisines."""
        if not self._is_inside(current) or not self._is_inside(neighbour):
            raise ValueError("Les cellules doivent appartenir a la grille.")

        x, y = current
        nx, ny = neighbour
        dx = nx - x
        dy = ny - y

        if dx == 1 and dy == 0:
            self.grid[y][x] &= ~EAST
            self.grid[ny][nx] &= ~WEST
        elif dx == -1 and dy == 0:
            self.grid[y][x] &= ~WEST
            self.grid[ny][nx] &= ~EAST
        elif dx == 0 and dy == 1:
            self.grid[y][x] &= ~SOUTH
            self.grid[ny][nx] &= ~NORTH
        elif dx == 0 and dy == -1:
            self.grid[y][x] &= ~NORTH
            self.grid[ny][nx] &= ~SOUTH
        else:
            raise ValueError("Les cellules doivent etre voisines.")

    def _reset_grid(self) -> None:
        """Refermer toutes les cellules avant une nouvelle generation."""
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _add_loops(self) -> None:
        """Ouvrir quelques murs supplementaires pour un labyrinthe imparfait."""
        closed_passages: list[tuple[Coordinate, Coordinate]] = []

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if x + 1 < self.width and cell & EAST:
                    closed_passages.append(((x, y), (x + 1, y)))
                if y + 1 < self.height and cell & SOUTH:
                    closed_passages.append(((x, y), (x, y + 1)))

        self._random.shuffle(closed_passages)
        loop_count = min(
            len(closed_passages),
            max(1, self.width * self.height // 10),
        )

        for current, neighbour in closed_passages[:loop_count]:
            self._open_passage(current, neighbour)

    def generate(self) -> None:
        """Generer le labyrinthe avec un parcours en profondeur iteratif.

        Un labyrinthe parfait est un arbre : toutes les cellules sont
        accessibles et il n'existe qu'un chemin entre deux cellules. Lorsque
        ``perfect`` vaut ``False``, quelques murs supplementaires sont ouverts
        apres le DFS afin de creer des boucles.
        """
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Les dimensions doivent etre strictement positives.")
        if not self._is_inside(self.entry) or not self._is_inside(self.exit):
            raise ValueError("L'entree et la sortie doivent appartenir a la grille.")

        self._reset_grid()
        self._random.seed(self.seed)

        visited: set[Coordinate] = {self.entry}
        stack: list[Coordinate] = [self.entry]

        while stack:
            current = stack[-1]
            unvisited = [
                neighbour
                for neighbour in self._neighbours(current)
                if neighbour not in visited
            ]

            if not unvisited:
                stack.pop()
                continue

            neighbour = self._random.choice(unvisited)
            self._open_passage(current, neighbour)
            visited.add(neighbour)
            stack.append(neighbour)

        if not self.perfect and self.width * self.height > 1:
            self._add_loops()
