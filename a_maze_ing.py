import sys

from app.config import load_config, ConfigError
from app.output import write_maze
from app.display import run
from mazegen.generator import MazeGenerator


def main() -> int:

    """Lit la config, génère le labyrinthe, écrit le fichier et
    lance le menu interactif."""

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return 1

    try:
        config = load_config(sys.argv[1])
    except ConfigError as error:
        print(f"Configuration error: {error}")
        return 1

    mg = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        seed=config.seed,
        perfect=config.perfect,
    )

    try:
        mg.generate()
    except ValueError as error:
        print(f"Maze generation error: {error}")
        return 1

    write_maze(
        config.output_file,
        mg.grid,
        mg.entry,
        mg.exit,
        mg.shortest_path(),
    )

    run(mg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
