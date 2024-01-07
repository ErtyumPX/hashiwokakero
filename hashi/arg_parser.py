from node import Node

def parse_args(argv: list[str]) -> list[list[Node]]:
    """
    Parse the system arguments and returns the grid, empty or solution according to flags.
    """
    import os
    from export import import_empty_grid, import_solution_grid
    if len(argv) != 3:
        print("Usage: python3 ___.py <-e||-s> <path_to_grid_file>")
        return -1
    path = argv[2]
    if not os.path.isfile(path):
        print("ERROR: File does not exist")
        return -1
    if argv[1] == "-e":
        grid = import_empty_grid(path)
    elif argv[1] == "-s":
        grid = import_solution_grid(path)
    else:
        print("Usage: python3 ___.py <-e||-s> <path_to_grid_file>")
        return -1
    return grid


def parse_args_empty(argv: list[str]) -> list[list[Node]]:
    """
    Parse the system arguments and returns the empty grid.
    """
    import os
    from export import import_empty_grid
    if len(argv) != 2:
        print(f"Usage: python3 ___.py <path>")
        return -1
    path = argv[1]
    if not os.path.isfile(path):
        print("ERROR: File does not exist")
        return -1
    grid = import_empty_grid(path)
    return grid


def parse_to_path(argv: list[str]) -> str:
    """
    Parse the system arguments and returns the path.
    """
    import os
    if len(argv) != 2:
        print(f"Usage: python3 ___.py <path>")
        return -1
    path = argv[1]
    if os.path.isfile(path):
        print(f"ERROR: There is an existing file at '{path}'")
        return -1
    return path


def parse_to_amount(argv: list[str]) -> int:
    """
    Parse the system arguments and returns the amount.
    """
    if len(argv) != 2:
        print(f"Usage: python3 ___.py <amount>")
        return -1
    # safely check if argv[1] is an integer
    try:
        amount = int(argv[1])
        if amount <= 0:
            print(f"ERROR: '{argv[1]}' is not a positive integer")
            return -1
    except ValueError:
        print(f"ERROR: '{argv[1]}' is not an integer")
        return -1
    return amount
