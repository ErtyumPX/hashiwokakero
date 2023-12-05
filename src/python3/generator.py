from node import Node
from random import randint, choice
from grid_visualizer import draw_grid
import os

"""
Generator Algorithm
-------------------
islands = []
choose a random node and add to islands
for _ in range(step_per_cycle):
    get a random node from islands
    get a random possible direction 
    get a random bridge thickness (1, 2)
    get a random bridge length
    establish the bridge
print the grid
get input from user
Y -> continue another cycle
n -> exit
"""

"""
Saving Puzzles
--------------

inside general_puzzles/puzzle.{i}.csv:

width;;height;;empty_grid;;solution_grid

w;;h;;000010502007....0050;;0012513106133610....0125120

empty_grid: 
    0 -> empty
    any other positive integer -> island

solution_grid: 
    0 -> empty
    positive integers -> island
    negative integers -> bridge
        -1 -> horizontal single
        -2 -> horizontal double
        -3 -> vertical single
        -4 -> vertical double

"""

def get_random_direction(grid: list[list[Node]], x: int, y: int) -> int:
    """0->left, 1->up, 2->right, 3->down, -1->no possible direction"""
    assert grid[x][y].n_type == 1
    assert x >= 0 and x < len(grid)
    assert y >= 0 and y < len(grid[0])
    possible_directions = []
    if x > 1 and grid[x-1][y].n_type == 0 and grid[x-2][y].n_type == 0:
        possible_directions.append(0)
    if y > 1 and grid[x][y-1].n_type == 0 and grid[x][y-2].n_type == 0:
        possible_directions.append(1)
    if x < len(grid)-2 and grid[x+1][y].n_type == 0 and grid[x+2][y].n_type == 0:
        possible_directions.append(2)
    if y < len(grid[0])-2 and grid[x][y+1].n_type == 0 and grid[x][y+2].n_type == 0:
        possible_directions.append(3)
    if len(possible_directions) == 0: return -1
    return choice(possible_directions)


def get_random_bridge_thickness(grid: list[list[Node]], x: int, y: int) -> int:
    assert grid[x][y].n_type == 1
    assert x >= 0 and x < len(grid)
    assert y >= 0 and y < len(grid[0])
    if  8 - grid[x][y].i_count > 1:
        return choice([1, 2])
    return 1

def direction_to_vector(direction: int) -> tuple[int, int]:
    assert direction >= 0 and direction < 4
    return [(-1, 0), (0, -1), (1, 0), (0, 1)][direction]

def get_random_bridge_length(grid: list[list[Node]], x: int, y: int, direction: int) -> int:
    assert grid[x][y].n_type == 1
    assert x >= 0 and x < len(grid)
    assert y >= 0 and y < len(grid[0])
    assert direction >= 0 and direction < 4
    dir_vector = direction_to_vector(direction)
    max_length = 1
    check_x = x + dir_vector[0] * (max_length + 2)
    check_y = y + dir_vector[1] * (max_length + 2)
    while True:
        if check_x < 0 or check_x >= len(grid) or check_y < 0 or check_y >= len(grid[0]):
            break
        if grid[check_x][check_y].n_type != 0:
            break
        max_length += 1
        check_x += dir_vector[0]
        check_y += dir_vector[1]
    return randint(1, max_length)


step_per_cycle = 100
def generate(w, h):
    grid = [[Node(i, j) for j in range(h)] for i in range(w)]
    islands = []
    islands.append(grid[randint(0, w-1)][randint(0, h-1)])
    islands[0].make_island(0)
    is_dead_end = False
    while True:

        for _ in range(step_per_cycle):
            if len(islands) == 0:
                is_dead_end = True
                break
            current_node = choice(islands)
            direction = get_random_direction(grid, current_node.x, current_node.y)
            if direction == -1: # no possible direction
                islands.remove(current_node)
                continue
            thickness = get_random_bridge_thickness(grid, current_node.x, current_node.y)
            length = get_random_bridge_length(grid, current_node.x, current_node.y, direction)
            dir_vector = direction_to_vector(direction)
            x = current_node.x
            y = current_node.y
            last_node = grid[x + dir_vector[0] * (length + 1)][y + dir_vector[1] * (length + 1)]
            #print(f'Node {x}x{y} - dir: {direction} - thck: {thickness} - len: {length}')
            for i in range(length):
                grid[x + dir_vector[0] * (i + 1)][y + dir_vector[1] * (i + 1)].make_bridge(thickness, direction % 2)
            last_node.make_island(thickness)
            islands.append(last_node)
            current_node.i_count += thickness
        #draw_grid(grid)
        #if is_dead_end or input("Continue? (Y/n): ").lower() == 'n':
        break
    return grid


def show_grid(grid: list[list[Node]]):
    for line in grid:
        for node in line:
            print(node.n_type, end="  ")
        print('\n')

def check_if_grid_full(grid: list[list[Node]]) -> bool:
    w = len(grid)
    h = len(grid[0])
    if [grid[i][0].n_type for i in range(w)].count(0) == w:
        return False
    if [grid[i][h-1].n_type for i in range(w)].count(0) == w:
        return False
    if [grid[0][i].n_type for i in range(h)].count(0) == h:
        return False
    if [grid[w-1][i].n_type for i in range(h)].count(0) == h:
        return False
    return True

def save_grid(grid: list[list[Node]], path: str = None) -> bool:
    if not check_if_grid_full(grid): 
        print("Grid is not full, generating another one...")
        return False
    if path is None:
        path = f"general_puzzles/puzzle_{len(os.listdir('general_puzzles'))}.csv"
    empty_grid: str = ""
    solution_grid: str = ""
    for line in grid:
        for node in line:
            if node.n_type == 1: 
                empty_grid += str(node.i_count)
                solution_grid += str(node.i_count)
            elif node.n_type == 0:
                empty_grid += '0'
                solution_grid += '0'
            else:
                empty_grid += '0'
                bridge_code = (node.b_thickness * -1) + (-2 * (node.b_dir))
                solution_grid += str(bridge_code)

    with open(path, 'w') as file:
        file.write(f"{len(grid)};;{len(grid[0])};;")
        file.write(f"{empty_grid};;")
        file.write(f"{solution_grid}\n")
    return True

def import_solution_grid(path: str) -> list[list[Node]]:
    if not os.path.isfile(path) or not path.endswith(".csv"):
        print("ERROR: File does not exist")
        return
    grid: list[list[Node]] = []
    w = None
    h = None
    solution_grid = None
    with open(path, 'r') as file:
        w, h, _, solution_grid = file.readline().split(";;")
        w = int(w)
        h = int(h)
        solution_grid = list(map(int, solution_grid))
    for i in range(w):
        grid.append([])
        for j in range(h):
            cursor = i * h + j
            grid[i].append(Node(i, j))
            if solution_grid[cursor] > 0:
                grid[i][j].make_island(solution_grid[cursor])
            elif solution_grid[cursor] < 0:
                bridge_info = [(1, 0), (2, 0), (1, 1), (2, 1)][(solution_grid[cursor] * -1) - 1]
                grid[i][j].make_bridge(*bridge_info)
    return grid

def import_empty_grid(path: str) -> list[list[Node]]:
    if not os.path.isfile(path) or not path.endswith(".csv"):
        print("ERROR: File does not exist")
        return
    grid: list[list[Node]] = []
    w = None
    h = None
    solution_grid = None
    with open(path, 'r') as file:
        w, h, empty_grid, _ = file.readline().split(";;")
        w = int(w)
        h = int(h)
        empty_grid = list(map(int, empty_grid))
    for i in range(w):
        grid.append([])
        for j in range(h):
            cursor = i * h + j
            grid[i].append(Node(i, j))
            if solution_grid[cursor] > 0:
                grid[i][j].make_island(solution_grid[cursor])
    return grid

"""
bridge thickness: 1-2
bridge dire: 1->vertical, 2->horizontal

negative integers -> bridge
    -1 -> horizontal single
    -2 -> horizontal double
    -3 -> vertical single
    -4 -> vertical double
"""

def main():
    generated = False
    while not generated:
        grid = generate(10, 10)
        generated = save_grid(grid)
        if generated: draw_grid(grid)

if __name__ == "__main__":
    main()