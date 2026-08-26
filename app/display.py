from mazegen.generator import NORTH, EAST, SOUTH, WEST, ALL_WALLS
from mazegen.generator import MazeGenerator
import os


CORNER = "+"
WALL_H = "-"
WALL_V = "|"
EMPTY = " "
FILL = "\u2588"

RESET = "\033[0m"
COLOR_WALL = "\033[36m"
WALL_COLORS = ["\033[37m", "\033[33m", "\033[35m", "\033[34m"]
COLOR_PATTERN = "\033[97m"
COLOR_PATH = "\033[36m"
COLOR_ENTRY = "\033[32m"
COLOR_EXIT = "\033[31m"


def _horizontal_border(width: int, wall_color: str) -> str:
    return wall_color + (f"{CORNER}{WALL_H * 3}" * width +
                         f"{CORNER}") + RESET


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


def content_row(row: list[int], y: int, path: set[tuple[int, int]],
                entry: tuple[int, int] | None,
                exit: tuple[int, int] | None,
                wall_color: str) -> str:
    line = ""

    for x, cell in enumerate(row):
        if x > 0:
            left_neighbor = row[x - 1]
        else:
            left_neighbor = None

        if x > 0 and (x - 1, y) in path:
            left_on_path = True
        else:
            left_on_path = False

        if (x, y) in path:
            on_path = True
        else:
            on_path = False

        if (x, y) == entry:
            is_entry = True
        else:
            is_entry = False

        if (x, y) == exit:
            is_exit = True
        else:
            is_exit = False

        if is_entry or is_exit:
            inside = "#" * 3
        elif on_path:
            inside = "#" * 3
        elif cell == ALL_WALLS:
            inside = FILL * 3
        else:
            inside = EMPTY * 3

        wall = left_segment(cell)
        segment = wall + inside

        if is_entry:
            line += wall_color + wall + COLOR_ENTRY + inside + RESET
        elif is_exit:
            line += wall_color + wall + COLOR_EXIT + inside + RESET
        elif on_path and left_on_path and wall == EMPTY:
            line += COLOR_PATH + segment + RESET
        elif on_path:
            line += wall_color + wall + COLOR_PATH + inside + RESET
        elif cell == ALL_WALLS or left_neighbor == ALL_WALLS:
            line += COLOR_PATTERN + segment + RESET
        else:
            line += wall_color + segment + RESET

    last_cell = row[-1]
    segment = right_segment(last_cell)

    if last_cell == ALL_WALLS:
        line += COLOR_PATTERN + segment + RESET
    else:
        line += wall_color + segment + RESET

    return line


def bottom_row(row: list[int], next_row: list[int] | None = None,
               wall_color: str = "") -> str:

    line = wall_color + CORNER + RESET

    for x, cell in enumerate(row):

        if next_row is not None:
            below = next_row[x]
        else:
            below = None
        segment = down_segment(cell)

        if cell == ALL_WALLS or below == ALL_WALLS:
            line += COLOR_PATTERN + segment + RESET + CORNER
        else:
            line += wall_color + segment + RESET + CORNER

    return line


def display(grid: list[list[int]], path: list[tuple[int, int]] | None = None,
            entry: tuple[int, int] | None = None,
            exit: tuple[int, int] | None = None,
            wall_color: str = "") -> str:

    if path:
        path_set = set(path)
    else:
        path_set = set()

    lines = [_horizontal_border(len(grid[0]), wall_color)]

    for y, row in enumerate(grid):
        if y + 1 < len(grid):
            next_row = grid[y + 1]
        else:
            next_row = None
        lines.append(content_row(row, y, path_set, entry, exit, wall_color))
        lines.append(bottom_row(row, next_row, wall_color))

    return "\n".join(lines)


def run(mg: MazeGenerator) -> None:
    show_path = False
    color_index = 0

    while True:
        if show_path:
            path = mg.shortest_path()
        else:
            path = None

        wall_color = WALL_COLORS[color_index]

        os.system("clear")
        print(display(mg.grid, path, mg.entry, mg.exit, wall_color))
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = input("Choice? (1-4): ")

        if choice == "1":
            mg.regenerate()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(WALL_COLORS)
        elif choice == "4":
            break
        else:
            print("Invalid choice")
            input("Press Enter to continue...")
