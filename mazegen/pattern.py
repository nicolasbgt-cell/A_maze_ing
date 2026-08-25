"""Placer et fermer le motif obligatoire « 42 »."""

import random

from .topology import geometrically_connected
from .walls import ALL_WALLS, EAST, NORTH, SOUTH, WEST, Coordinate, Grid
from .walls import neighbours


FORTY_TWO = (
    "#.#.###",
    "#.#...#",
    "###.###",
    "..#.#..",
    "..#.###",
)


def _key_cells(width: int, height: int) -> set[Coordinate]:
    """Renvoyer les coins et les cellules centrales a garder ouvertes."""
    cells = {
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
    }
    centre_x = (
        {width // 2}
        if width % 2
        else {width // 2 - 1, width // 2}
    )
    centre_y = (
        {height // 2}
        if height % 2
        else {height // 2 - 1, height // 2}
    )
    cells.update((x, y) for x in centre_x for y in centre_y)
    return cells


def find_pattern_cells(
    width: int,
    height: int,
    entry: Coordinate,
    exit: Coordinate,
    generator: random.Random,
) -> set[Coordinate]:
    """Trouver un emplacement valide pour le motif ferme « 42 »."""
    pattern_width = len(FORTY_TWO[0])
    pattern_height = len(FORTY_TWO)
    if width < pattern_width or height < pattern_height:
        print("Warning: maze too small to contain the '42' pattern.")
        return set()

    corners = {
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
    }
    centre_candidates = _key_cells(width, height) - corners
    reserved = corners | {entry, exit}
    placements: list[set[Coordinate]] = []
    for origin_y in range(height - pattern_height + 1):
        for origin_x in range(width - pattern_width + 1):
            cells = {
                (origin_x + offset_x, origin_y + offset_y)
                for offset_y, row in enumerate(FORTY_TWO)
                for offset_x, value in enumerate(row)
                if value == "#"
            }
            if (
                cells.isdisjoint(reserved)
                and not centre_candidates.issubset(cells)
            ):
                placements.append(cells)

    generator.shuffle(placements)
    for cells in placements:
        if geometrically_connected(width, height, cells):
            return cells

    print("Warning: maze too small to place a valid '42' pattern.")
    return set()


def close_pattern(grid: Grid, pattern: set[Coordinate]) -> None:
    """Fermer le motif et les murs correspondants de ses voisines."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    for x, y in pattern:
        grid[y][x] = ALL_WALLS
        for nx, ny in neighbours((x, y), width, height):
            dx = nx - x
            dy = ny - y
            if dx == 1:
                grid[ny][nx] |= WEST
            elif dx == -1:
                grid[ny][nx] |= EAST
            elif dy == 1:
                grid[ny][nx] |= NORTH
            else:
                grid[ny][nx] |= SOUTH
