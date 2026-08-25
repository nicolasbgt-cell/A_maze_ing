"""Representer et generer un labyrinthe."""

import random
from collections import deque

from .pattern import close_pattern, find_pattern_cells
from .topology import (
    closed_passages,
    dead_ends,
    loop_count,
    open_neighbours,
    reachable,
    would_create_open_3x3,
)
from .walls import (
    ALL_WALLS,
    EAST,
    NORTH,
    SOUTH,
    WEST,
    Coordinate,
    is_inside,
    neighbours,
    open_passage,
)

__all__ = [
    "ALL_WALLS",
    "EAST",
    "NORTH",
    "SOUTH",
    "WEST",
    "Coordinate",
    "MazeGenerator",
]


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
        self._generated = False

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
        """Verifier que la cellule (x, y) appartient au labyrinthe."""
        return is_inside(coordinate, self.width, self.height)

    def _neighbours(
        self,
        coordinate: Coordinate,
    ) -> list[Coordinate]:
        """Renvoyer les coordonnees voisines situees dans la grille."""
        return neighbours(coordinate, self.width, self.height)

    def _open_passage(
        self,
        current: Coordinate,
        neighbour: Coordinate,
    ) -> None:
        """Ouvrir les murs communs entre deux cellules voisines."""
        open_passage(self.grid, current, neighbour)

    def _reset_grid(self) -> None:
        """Refermer toutes les cellules avant une nouvelle generation."""
        self._generated = False
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _reconnect(self, blocked: set[Coordinate]) -> None:
        """Reconnecter les corridors separes par la fermeture du motif."""
        available = {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in blocked
        }
        reached = reachable(self.grid, self.entry, blocked)
        while reached != available:
            candidates = [
                (current, neighbour)
                for current in reached
                for neighbour in self._neighbours(current)
                if neighbour in available and neighbour not in reached
            ]
            if not candidates:
                raise ValueError("Le motif '42' deconnecte le labyrinthe.")
            current, neighbour = self._random.choice(candidates)
            self._open_passage(current, neighbour)
            reached = reachable(self.grid, self.entry, blocked)

    def _braid(self, blocked: set[Coordinate]) -> None:
        """Ajouter des boucles et reduire les impasses du mode jouable."""
        while (
            loop_count(self.grid, blocked) < 2
            or len(dead_ends(self.grid, blocked)) > 2
        ):
            current_dead_ends = set(dead_ends(self.grid, blocked))
            passages = closed_passages(self.grid, blocked)
            preferred = [
                passage
                for passage in passages
                if (
                    passage[0] in current_dead_ends
                    or passage[1] in current_dead_ends
                )
            ]
            candidates = [
                passage
                for passage in preferred
                if not would_create_open_3x3(
                    self.grid,
                    passage,
                    blocked,
                )
            ]
            if not candidates:
                candidates = [
                    passage
                    for passage in passages
                    if not would_create_open_3x3(
                        self.grid,
                        passage,
                        blocked,
                    )
                ]
            if not candidates:
                raise ValueError("Impossible de creer un plateau jouable.")
            self._open_passage(*self._random.choice(candidates))

    def generate(self) -> None:
        """Generer le labyrinthe avec un parcours en profondeur iteratif.

        Un labyrinthe parfait est un arbre : toutes les cellules sont
        accessibles et il n'existe qu'un chemin entre deux cellules. Lorsque
        ``perfect`` vaut ``False``, quelques murs supplementaires sont ouverts
        apres le DFS afin de creer des boucles.
        """
        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                "Les dimensions doivent etre strictement positives."
            )
        if not self._is_inside(self.entry) or not self._is_inside(self.exit):
            raise ValueError(
                "L'entree et la sortie doivent appartenir a la grille."
            )
        if self.entry == self.exit:
            raise ValueError("L'entree et la sortie doivent etre differentes.")

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

        pattern = find_pattern_cells(
            self.width,
            self.height,
            self.entry,
            self.exit,
            self._random,
        )
        if pattern:
            close_pattern(self.grid, pattern)
            self._reconnect(pattern)

        if not self.perfect:
            if (self.width - 1) * (self.height - 1) < 2:
                raise ValueError(
                    "Dimensions insuffisantes pour creer deux boucles."
                )
            self._braid(pattern)

        self._generated = True

    def regenerate(self, seed: int | None = None) -> None:
        """Generer un nouveau labyrinthe avec une seed optionnelle."""
        if seed is None:
            seed = self._random.getrandbits(64)
        self.seed = seed
        self.generate()

    def shortest_path(self) -> list[Coordinate]:
        """Renvoyer le plus court chemin entre l'entree et la sortie."""
        if not self._generated:
            raise ValueError(
                "Le labyrinthe doit etre genere avant sa resolution."
            )

        blocked = {
            (x, y)
            for y, row in enumerate(self.grid)
            for x, cell in enumerate(row)
            if cell == ALL_WALLS
        }
        parents: dict[Coordinate, Coordinate | None] = {self.entry: None}
        queue = deque([self.entry])

        while queue:
            current = queue.popleft()
            if current == self.exit:
                break
            for neighbour in open_neighbours(self.grid, current, blocked):
                if neighbour not in parents:
                    parents[neighbour] = current
                    queue.append(neighbour)

        if self.exit not in parents:
            raise ValueError("Aucun chemin ne relie l'entree a la sortie.")

        path: list[Coordinate] = []
        cursor: Coordinate | None = self.exit
        while cursor is not None:
            path.append(cursor)
            cursor = parents[cursor]
        path.reverse()
        return path
