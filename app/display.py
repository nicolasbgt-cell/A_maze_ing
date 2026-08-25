from mazegen.generator import NORTH, EAST, SOUTH, WEST


CORNER = "+"
WALL_H = "-"
WALL_V = "|"
EMPTY = " "


def _horizontal_border(width: int) -> str:
    return f"{CORNER}{WALL_H * 3}" * width + f"{CORNER}"


def top_segment(cell: int) -> str:
    if cell & NORTH:
        return WALL_H * 3
    else:
        return EMPTY * 3


def left_segment(cell: int) -> str:
    if cell & WEST:
        return WALL_V
    else:
        return EMPTY


def down_segment(cell: int) -> str:
    if cell & SOUTH:
        return WALL_H * 3
    else:
        return EMPTY * 3


def right_segment(cell: int) -> str:
    if cell & EAST:
        return WALL_V
    else:
        return EMPTY


def content_row(row: list[int]) -> str:
    line = ""
    for cell in row:
        line += left_segment(cell) + EMPTY * 3
    line += right_segment(row[-1])
    return line


def bottom_row(row: list[int]) -> str:
    line = CORNER
    for cell in row:
        line += down_segment(cell) + CORNER
    return line


def display(grid: list[list[int]]) -> str:
    lines = [_horizontal_border(len(grid[0]))]
    for row in grid:
        lines.append(content_row(row))
        lines.append(bottom_row(row))
    return "\n".join(lines)
