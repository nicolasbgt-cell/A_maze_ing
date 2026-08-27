*This activity has been created as part of the 42 curriculum by nbigot, tiplalon.*

# a_maze_ing

## Description

`a_maze_ing` is a Python project that generates, solves, displays and exports mazes. Its goal is to produce either a perfect maze or a Pac-Man-like playable
maze containing a centered, fully closed “42” pattern.

The project is divided into two independent layers:

- `mazegen`: a reusable maze-generation package
- `app`: configuration parsing, terminal display, and output serialization.

The application creates a `MazeGenerator`, calls `generate()` or
`regenerate()`, reads `grid` and calls `shortest_path()` when it needs the solution.

### Features

- randomized iterative DFS generation
- reproducible generation with a seed
- perfect mode: connected maze with no cycle
- default mode: multiple routes and no more than two real dead ends
- centered “42” pattern made of 20 fully closed cells
- symmetric wall encoding and closed external borders
- shortest-path calculation with BFS
- terminal ASCII rendering
- hexadecimal output in the required format
- reusable package buildable as `.whl` and `.tar.gz`

### Architecture

The repository combines three functional directories with four project-level
files. `app/` contains the application layer, `mazegen/` provides the reusable
maze-generation package, and `tests/` contains the verification suite. At the
repository root, `.gitignore`, `config.txt`, `pyproject.toml`, and `README.md`
respectively manage generated-file exclusions, the default configuration,
package construction, and project documentation. The tree below reflects the
actual directory structure; each annotation summarizes the responsibility of
the corresponding item.

```text
AMAZING/
├── .gitignore              # Excludes caches and .txt files except config.txt
├── config.txt              # Provides the default reproducible configuration
├── README.md               # Explains the project, its use, and its organization
├── pyproject.toml          # Defines how the mazegen distribution is built
│
├── app/                    # Application layer
│   ├── __init__.py         # Marks app as an importable Python package
│   ├── config.py           # Reads and validates the configuration file
│   ├── display.py          # Converts a grid into a terminal ASCII display
│   └── output.py           # Writes the grid and solution in the required format
│
├── mazegen/                # Reusable maze-generator package
│   ├── __init__.py         # Exposes MazeGenerator and the public wall constants
│   ├── generator.py        # Generates, regenerates, braids, and solves mazes
│   ├── pattern.py          # Finds, centers, and closes the “42” pattern
│   ├── topology.py         # Analyzes reachability, cycles, dead ends, and open areas
│   └── walls.py            # Defines coordinates, wall bits, neighbours, and passages
│
└── tests/                  # Unit and integration test package
    ├── __init__.py         # Marks tests as an importable Python package
    ├── test_generator.py   # Tests modes, seeds, regeneration, and shortest paths
    ├── test_integration.py # Tests configuration-to-output integration
    ├── test_pattern.py     # Tests that the “42” pattern is centered
    └── test_walls.py       # Tests wall openings and invalid coordinates
```

### Main functions inside `mazegen`

The tables below document the principal functions and methods implemented in
the reusable generator. Names ending with `()` identify callable objects. A
leading `_` marks an internal implementation detail outside the public API.

#### `mazegen/generator.py`

| Function or method | Responsibility |
|---|---|
| `generate()` | Builds the maze with a randomized iterative DFS |
| `regenerate()` | Resets and generates the maze with a new seed |
| `shortest_path()` | Finds a shortest entry-to-exit path with BFS |
| `_reset_grid()` | Restores a grid in which every wall is closed |
| `_reconnect()` | Reconnects corridors after closing the “42” pattern |
| `_braid()` | Adds loops and reduces dead ends in default mode |

#### `mazegen/walls.py`

| Function or method | Responsibility |
|---|---|
| `is_inside()` | Checks whether a coordinate belongs to the grid |
| `neighbours()` | Returns valid adjacent coordinates |
| `open_passage()` | Opens the two shared walls symmetrically |

#### `mazegen/topology.py`

| Function or method | Responsibility |
|---|---|
| `open_neighbours()` | Returns neighbours linked by open passages |
| `reachable()` | Finds the region reachable from one cell |
| `closed_passages()` | Lists neighbouring cells separated by a wall |
| `would_create_open_3x3()` | Prevents a completely open `3 × 3` area |
| `loop_count()` | Counts independent cycles in the maze |
| `dead_ends()` | Finds cells with only one possible exit |

#### `mazegen/pattern.py`

| Function or method | Responsibility |
|---|---|
| `find_pattern_cells()` | Chooses a valid centered “42” placement |
| `close_pattern()` | Closes pattern cells and neighbouring walls |

### Main functions inside `app`

This section follows the same file-by-file format as the generator section. It
must be completed by nbigot after the final application code has been
integrated. Add one row per principal function and replace every placeholder
before submission.

#### `app/config.py`

| Function or method | Responsibility |
|---|---|
| `To be completed` | Configuration loading and validation |

#### `app/display.py`

| Function or method | Responsibility |
|---|---|
| `To be completed` | ASCII rendering and user interactions |

#### `app/output.py`

| Function or method | Responsibility |
|---|---|
| `To be completed` | Hexadecimal grid and solution serialization |

### Data representation

Public coordinates use `(x, y)`, where `x` is the column and `y` is the row.
The internal access order is therefore `grid[y][x]`.

Each cell is an integer whose four least significant bits encode closed walls:

| Bit | Value | Direction |
|---:|---:|---|
| 0 | `1` | North |
| 1 | `2` | East |
| 2 | `4` | South |
| 3 | `8` | West |

A bit set to `1` means that the wall is closed. Consequently, `15`, hexadecimal
`F`, means that all four walls are closed. Opening a passage is symmetric:
opening the east wall also opens the west wall of the eastern neighbour.

## Instructions

### Requirements

- Python 3.10 or later
- `setuptools` and `build` to build the reusable package
- `flake8` and `mypy` for optional quality checks

### Configuration file

The application reads one `KEY=VALUE` pair per line. Blank lines and lines beginning with `#` are ignored.

The repository provides `config.txt` as a ready-to-use default configuration.
It generates a reproducible `20 × 15` playable maze with seed `42` and writes
the serialized result to `maze.txt`.

Complete content of the default file:

```ini
# Default reproducible configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

| Key | Required | Format | Meaning |
|---|---|---|---|
| `WIDTH` | yes | positive integer | number of columns |
| `HEIGHT` | yes | positive integer | number of rows |
| `ENTRY` | yes | `x,y` | entrance inside the grid |
| `EXIT` | yes | `x,y` | exit inside the grid, different from entry |
| `OUTPUT_FILE` | yes | path | destination of the serialized maze |
| `PERFECT` | yes | exactly `True` or `False` | generation mode |
| `SEED` | no | integer | reproducible pseudo-random generation |

Invalid or missing numeric values raise `ConfigError`. Invalid dimensions,
coordinates, or identical entry and exit coordinates raise `ValueError` when
generation begins.

### Run the current pipeline

Use the provided `config.txt`, then run from the repository root:

```bash
python3 - <<'PY'
from app.config import load_config
from app.display import display
from app.output import write_maze
from mazegen import MazeGenerator

config = load_config("config.txt")
maze = MazeGenerator(
    config.width,
    config.height,
    config.entry,
    config.exit,
    config.perfect,
    config.seed,
)
maze.generate()
path = maze.shortest_path()
print(display(maze.grid))
write_maze(config.output_file, maze.grid, maze.entry, maze.exit, path)
PY
```

### Reusable generator example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=False,
    seed=42,
)
maze.generate()
grid = maze.grid
path = maze.shortest_path()

maze.regenerate()      # generate with a new random seed
maze.regenerate(1234)  # reproduce generation with seed 1234
```

`generate()` and `regenerate()` update `maze.grid` and return `None`.
`shortest_path()` returns coordinates from entry to exit, including endpoints.

### Output-file format

The grid is written row by row, with one hexadecimal digit per cell. After an
empty line, the file contains the entry, exit, and shortest path as a sequence
of `N`, `E`, `S`, and `W`. Every line ends with `\n`.

```text
<hexadecimal grid>

0,0
19,14
EESS...
```

### Build and install the reusable package

```bash
python3 -m pip install build
python3 -m build --outdir .
```

The standard build produces at the repository root:

```text
mazegen-1.0.0-py3-none-any.whl
mazegen-1.0.0.tar.gz
```

Install and check the wheel in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install ./mazegen-1.0.0-py3-none-any.whl
python3 -c "from mazegen import MazeGenerator; print(MazeGenerator)"
```

The distribution and the imported Python package are both named `mazegen`.

### Tests and quality checks

```bash
python3 -m unittest discover -v
flake8 --jobs=1 mazegen app tests
mypy mazegen app tests
```

Tests cover wall symmetry, all four opening directions, parameter validation,
seed reproducibility, perfect and playable topology, centered “42” placement,
shortest-path validity, and the complete configuration-to-output pipeline.

## Technical choices

### Maze-generation algorithm and rationale

The initial maze is generated with a randomized iterative depth-first search:

1. put the entrance on a stack and mark it as visited
2. inspect the cell at the top of the stack
3. choose a random unvisited neighbour
4. open the shared wall, mark the neighbour and push it
5. if no unvisited neighbour remains, pop the current cell
6. continue until the stack is empty

The iterative form avoids Python's recursion-depth limit. Random neighbour selection produces different layouts, while a dedicated `random.Random` instance makes a result reproducible with a seed.

DFS was chosen because it is simple to explain and verify, visits every cell and naturally produces a spanning tree. A connected graph without a cycle has one path between every pair of vertices, which directly satisfies perfect-maze
generation.

In default mode, the generator braids the maze by opening selected passages.
This adds independent routes, reduces dead ends and avoids fully open `3 × 3` areas.

The shortest path is calculated separately with breadth-first search. BFS explores by increasing distance from the entrance, so the first route found to the exit is a shortest route in an unweighted grid.

### Reusable code

The complete `mazegen/` directory is reusable independently of `app/`. It does
not depend on terminal rendering, configuration files, or output formatting.

Its public interface, exported by `mazegen/__init__.py`, contains:

- `MazeGenerator`;
- `Coordinate`;
- `NORTH`, `EAST`, `SOUTH`, `WEST`, and `ALL_WALLS`.

Application code normally needs only:

```python
from mazegen import MazeGenerator
```

Names beginning with `_` and implementation functions in `walls.py`,
`topology.py`, and `pattern.py` remain internal details.

### Display and advanced features

The project uses terminal ASCII rather than MiniLibX. This keeps the program
portable and makes encoded walls directly testable. The final application is
intended to support the required interactions:

- regenerate and redisplay the maze
- show or hide a valid shortest path
- identify entry and exit clearly
- change wall colours

Advanced generator features include two modes, deterministic seeds, centered
pattern placement, regeneration, and automatic shortest-path calculation.

## Team and project management

### Roles

- **nbigot (Nicolas):** application layer, configuration, ASCII display,
  output serialization and user interactions
- **tiplalon (Tiphaine):** reusable generator, wall model, DFS and BFS,
  playable topology, centered “42”, tests and package construction.

Architecture, integration, documentation, and final validation are shared.

### Anticipated planning

1. read the subject and agree on data and interface contracts
2. work in parallel on generator and application layers
3. connect both layers through a shared integration test
4. complete interactions, checks, packaging, and documentation
5. merge validated work and run the final analyzer together

### How the planning evolved

The generator initially concentrated several responsibilities in one module.
As it grew, wall operations, topology analysis and pattern placement were
moved to dedicated files. The default mode required additional work to combine
loops, few dead ends, connectivity, the closed “42” and no open `3 × 3` area.

Integration began before the final phase: the application display was tested
with real grids and an integration test was added for configuration,
generation, resolution, display and output. Pattern placement was later
refined to favour valid positions near the center.

This retrospective must be updated after the final interactions, merge and
peer-evaluation preparation.

### What worked well

- stable `(x, y)` and `grid[y][x]` conventions
- symmetric wall-opening contracts
- separate responsibilities and parallel branches
- frequent tests of the display with real generated grids
- reproducible tests using explicit seeds
- modular refactoring and shared integration tests

### What could be improved

- agree on the command-line entry point earlier
- add focused tests with every new requirement
- synchronize branches more frequently during interaction development
- define README, license and packaging metadata earlier
- schedule a shared integration session after every major feature

### Tools

- Python 3
- Git and GitHub
- `unittest`, `flake8`, and `mypy`
- `venv`, `setuptools`, and `build`
- the provided `maze_analyzer.py`
- terminal ANSI escape sequences for colours

## Resources

### References

- [Python `random` documentation](https://docs.python.org/3/library/random.html)
  for seeded pseudo-random generation
- [Python `collections.deque` documentation](https://docs.python.org/3/library/collections.html#collections.deque)
  for the BFS queue
- [Python `unittest` documentation](https://docs.python.org/3/library/unittest.html)
  for the test suite
- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
  for `pyproject.toml`, wheel, and source distributions
- [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) and
  [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
  for graph-traversal principles
- the `a_maze_ing` subject and provided `maze_analyzer.py` for requirements and
  output validation.

### Use of AI

An AI assistant was used as a learning and review tool to:

- reformulate and clarify requirements from the subject
- compare algorithms and explain DFS, BFS, bit masks, seeds, wall symmetry,
  and packaging
- discuss architecture and interface contracts
- suggest debugging steps, manual checks and test cases
- review error messages and help identify inconsistencies
- help structure working notes and draft documentation

The team remained responsible for understanding, adapting, running, testing,
and validating every retained change. AI suggestions were treated as proposals
and checked against the subject, program behaviour, tests, and analyzer.
