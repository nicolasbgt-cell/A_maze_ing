def _cell_to_hex(value: int) -> str:
    return hex(value)[2:].upper()


def _direction(current: Coordinate, next_cell: Coordinate) -> str:
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
