"""Analyser la connexite et la topologie d'une grille de labyrinthe."""

from .walls import (
    EAST,
    NORTH,
    SOUTH,
    WEST,
    Coordinate,
    Grid,
    is_inside,
    neighbours,
)


def geometrically_connected(
    width: int,
    height: int,
    blocked: set[Coordinate],
) -> bool:
    """Verifier que les cellules non bloquees forment une seule region."""
    available = {
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in blocked
    }
    if not available:
        return False

    start = next(iter(available))
    reached = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbour in neighbours(current, width, height):
            if neighbour in available and neighbour not in reached:
                reached.add(neighbour)
                stack.append(neighbour)
    return reached == available


def open_neighbours(
    grid: Grid,
    coordinate: Coordinate,
    blocked: set[Coordinate],
) -> list[Coordinate]:
    """Renvoyer les voisines accessibles sans traverser un mur."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    x, y = coordinate
    directions = (
        ((x, y - 1), NORTH),
        ((x + 1, y), EAST),
        ((x, y + 1), SOUTH),
        ((x - 1, y), WEST),
    )
    return [
        neighbour
        for neighbour, wall in directions
        if neighbour not in blocked
        and is_inside(neighbour, width, height)
        and not grid[y][x] & wall
    ]


def reachable(
    grid: Grid,
    start: Coordinate,
    blocked: set[Coordinate],
) -> set[Coordinate]:
    """Renvoyer la region accessible depuis une cellule."""
    reached = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbour in open_neighbours(grid, current, blocked):
            if neighbour not in reached:
                reached.add(neighbour)
                stack.append(neighbour)
    return reached


def closed_passages(
    grid: Grid,
    blocked: set[Coordinate],
) -> list[tuple[Coordinate, Coordinate]]:
    """Lister une seule fois chaque mur interieur encore ferme."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    passages: list[tuple[Coordinate, Coordinate]] = []
    for y in range(height):
        for x in range(width):
            current = (x, y)
            if current in blocked:
                continue
            cell = grid[y][x]
            east = (x + 1, y)
            south = (x, y + 1)
            if (
                east not in blocked
                and is_inside(east, width, height)
                and cell & EAST
            ):
                passages.append((current, east))
            if (
                south not in blocked
                and is_inside(south, width, height)
                and cell & SOUTH
            ):
                passages.append((current, south))
    return passages


def would_create_open_3x3(
    grid: Grid,
    passage: tuple[Coordinate, Coordinate],
    blocked: set[Coordinate],
) -> bool:
    """Indiquer si une ouverture creerait une zone 3x3 sans mur."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    extra = {frozenset(passage)}

    def is_open(first: Coordinate, second: Coordinate) -> bool:
        """Indiquer si deux cellules sont reliees apres l'ouverture testee."""
        if frozenset((first, second)) in extra:
            return True
        return second in open_neighbours(grid, first, blocked)

    first, second = passage
    min_x = min(first[0], second[0])
    max_x = max(first[0], second[0])
    min_y = min(first[1], second[1])
    max_y = max(first[1], second[1])
    origin_x_start = max(0, max_x - 2)
    origin_x_stop = min(min_x, width - 3)
    origin_y_start = max(0, max_y - 2)
    origin_y_stop = min(min_y, height - 3)

    for origin_y in range(origin_y_start, origin_y_stop + 1):
        for origin_x in range(origin_x_start, origin_x_stop + 1):
            horizontal = all(
                is_open((x, y), (x + 1, y))
                for y in range(origin_y, origin_y + 3)
                for x in range(origin_x, origin_x + 2)
            )
            vertical = all(
                is_open((x, y), (x, y + 1))
                for y in range(origin_y, origin_y + 2)
                for x in range(origin_x, origin_x + 3)
            )
            if horizontal and vertical:
                return True
    return False


def loop_count(grid: Grid, blocked: set[Coordinate]) -> int:
    """Compter les cycles independants de la region connectee."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    nodes = width * height - len(blocked)
    edges = sum(
        len(open_neighbours(grid, (x, y), blocked))
        for y in range(height)
        for x in range(width)
        if (x, y) not in blocked
    ) // 2
    return edges - nodes + 1


def dead_ends(grid: Grid, blocked: set[Coordinate]) -> list[Coordinate]:
    """Renvoyer les vraies impasses qui peuvent encore etre ouvertes."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    openable = {
        coordinate
        for passage in closed_passages(grid, blocked)
        for coordinate in passage
    }
    return [
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in blocked
        and len(open_neighbours(grid, (x, y), blocked)) == 1
        and (x, y) in openable
    ]
