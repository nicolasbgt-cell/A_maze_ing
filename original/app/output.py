from mazegen.generator import Coordinate


def _cell_to_hex(value: int) -> str:
    return hex(value)[2:].upper()


def _direction(current: Coordinate, next_cell: Coordinate) -> str:

    """Renvoie la lettre de direction (N/E/S/W)
    entre deux cellules voisines."""

    dx = next_cell[0] - current[0]
    dy = next_cell[1] - current[1]

    if dx == 0 and dy == -1:
        return "N"
    elif dx == 1 and dy == 0:
        return "E"
    elif dx == 0 and dy == 1:
        return "S"
    elif dx == -1 and dy == 0:
        return "W"
    else:
        raise ValueError(f"Cellules non voisines: {current} -> {next_cell}")


def path_to_directions(path: list[Coordinate]) -> str:

    """Convertit une liste de coordonnées en chaîne
    de directions N/E/S/W."""

    directions = ""

    for i in range(len(path) - 1):
        directions += _direction(path[i], path[i + 1])

    return directions


def _row_to_hex(row: list[int]) -> str:

    """Convertit une rangée de cellules en chaîne hexadécimale
    (un digit par cellule)."""

    line = ""

    for value in row:
        line += _cell_to_hex(value)

    return line


def write_maze(
        output_file: str,
        grid: list[list[int]],
        entry: Coordinate,
        exit: Coordinate,
        path: list[Coordinate],
        ) -> None:

    """Écrit le labyrinthe, l'entrée, la sortie et le chemin
    dans le fichier de sortie."""

    lines = []

    for row in grid:
        lines.append(_row_to_hex(row))

    lines.append("")
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit[0]},{exit[1]}")
    lines.append(path_to_directions(path))

    with open(output_file, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
