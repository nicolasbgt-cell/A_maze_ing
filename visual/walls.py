"""Representer les coordonnees, les cellules et leurs murs."""

from typing import TypeAlias


Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = list[list[int]]

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST


def is_inside(
    coordinate: Coordinate,
    width: int,
    height: int,
) -> bool:
    """Verifier que la cellule appartient a la grille."""
    x, y = coordinate
    return 0 <= x < width and 0 <= y < height


def neighbours(
    coordinate: Coordinate,
    width: int,
    height: int,
) -> list[Coordinate]:
    """Renvoyer les voisines situees dans la grille."""
    x, y = coordinate
    candidates = (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
    )
    return [
        candidate
        for candidate in candidates
        if is_inside(candidate, width, height)
    ]


def open_passage(
    grid: Grid,
    current: Coordinate,
    neighbour: Coordinate,
) -> None:
    """Ouvrir symetriquement le mur entre deux cellules voisines."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    if (
        not is_inside(current, width, height)
        or not is_inside(neighbour, width, height)
    ):
        raise ValueError("Les cellules doivent appartenir a la grille.")

    x, y = current
    nx, ny = neighbour
    dx = nx - x
    dy = ny - y

    if dx == 1 and dy == 0:
        grid[y][x] &= ~EAST
        grid[ny][nx] &= ~WEST
    elif dx == -1 and dy == 0:
        grid[y][x] &= ~WEST
        grid[ny][nx] &= ~EAST
    elif dx == 0 and dy == 1:
        grid[y][x] &= ~SOUTH
        grid[ny][nx] &= ~NORTH
    elif dx == 0 and dy == -1:
        grid[y][x] &= ~NORTH
        grid[ny][nx] &= ~SOUTH
    else:
        raise ValueError("Les cellules doivent etre voisines.")
