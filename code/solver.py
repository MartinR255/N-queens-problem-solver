from pysat.formula import CNF
from pysat.solvers import Solver
from code.square_list_error import SquareListError

class QueensSolver:

    def __init__(self) -> None:
        self._directions = [(-1, -1), (-1, 0), (-1, 1), 
                            (0, -1),         (0, 1), 
                            (1, -1), (1, 0), (1, 1)]
        


    """
    Checks if the given game board is a valid square grid.

    Args:
        grid (list[list[str]]): The grid to validate, represented as a list of lists of str.
    
    Returns:
        bool: True if the grid is a non-empty square grid, False otherwise.
    """
    def _is_grid_valid(self, grid: list[list[str]]) -> bool:
        if not grid:
            return False
        
        num_rows = len(grid)
        
        for row in grid:
            if len(row) != num_rows:
                return False

        return True


    """
    Encodes a row and column index into a single integer.

    Args:
        row (int): The row index.
        col (int): The column index.
        N (int): The dimension number of the grid.
    
    Returns:
        int: The encoded integer value representing the position in the grid.
    """
    def _encode(self, row: int, col: int, N: int) -> int:
        return row * N + col + 1
    

    """
    Decodes an integer value back into row and column indices.

    Args:
        value (int): The encoded integer value representing the position in the grid.
        N (int): The dimension number of the grid.
    
    Returns:
        tuple[int, int]: A tuple containing the row and column indices.
    """
    def _decode(self, value: int, N: int) -> tuple[int, int]:
        row = (value - 1) // N
        col = (value - 1) % N
        return (row, col)
    

    """
    Represents the logical implication (antecedent -> consequent).

    Args:
        antecedent (int): The antecedent of the implication.
        consequent (int): The consequent of the implication.
    
    Returns:
        list[int]: A list representing the logical implication in conjunctive normal form (CNF).
    """
    def _impl(self, antecedent: int, consequent: int) -> list[int]:
        return [-antecedent, consequent]
    

    """
    Sorts the grid into clusters based on color.

    Args:
        grid (list[list[str]]): The grid to cluster, represented as a 2D list of color codes (strings).
    
    Returns:
        dict: A dictionary where the keys are color codes and the values are lists of (x, y) tuples representing the coordinates of each color in the grid.
    """
    def _sort_grid_into_clusters(self, grid: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
        color_clusters = {
            'v' : [],
            'g' : [],
            'r' : [],
            'o' : [],
            'b' : [],
            'p' : [],
            'y' : [],
            't' : []
        }

        for y, row in enumerate(grid):
            for x, color in enumerate(row):
                color_clusters[color].append((x, y))

        return color_clusters
    

    """
    Generates a formula in Conjunctive Normal Form (CNF) for the N-queens problem on the given grid.

    Args:
        grid (list[list[str]]): The grid represented as a 2D list of color codes (strings).
        N (int): The dimension number of the grid.
    
    Returns:
        list[list[int]]: A list of clauses in CNF.
    """
    def _generate_formula_in_cnf(self, grid: list[list[str]], N: int) -> list:
        cnf_list = []

        # in every row there is at least one queen
        # all position adjacent to queen are empty 
        for row in range(N):
            clause = []
            for col in range(N):
                clause.append(self._encode(row, col, N))

                # postions around queen must be empty
                for direction in self._directions:
                    row_direction, col_direction = direction
                    adjacent_row = row + row_direction
                    adjacent_col = col + col_direction
                
                    if not(0 <= adjacent_row < N and 0 <= adjacent_col < N):
                        continue

                    impl_to_clause = self._impl(self._encode(row, col, N), -self._encode(adjacent_row, adjacent_col, N))
                    cnf_list.append(impl_to_clause)

            cnf_list.append(clause)
            

        # in every row on different positions there is not more than one queen
        for row in range(N):
            for col_1 in range(N):
                for col_2 in range(col_1):
                    impl_to_clause = self._impl(self._encode(row, col_1, N), -self._encode(row, col_2, N))
                    cnf_list.append(impl_to_clause)


        # in every column on different positions there is not more than one queen
        for col in range(N):
            for row_1 in range(N):
                for row_2 in range(row_1):
                    impl_to_clause = self._impl(self._encode(row_1, col, N), -self._encode(row_2, col, N))
                    cnf_list.append(impl_to_clause)


        # in each color sector there is only one queen
        clusters = self._sort_grid_into_clusters(grid)
        for cluster in clusters.values():
            for cluster_index, pos_1 in enumerate(cluster):
                row_1, col_1 = pos_1
                for pos_2 in cluster[:cluster_index]:
                    row_2, col_2 = pos_2
                    impl_to_clause = self._impl(self._encode(row_1, col_1, N), -self._encode(row_2, col_2, N))
                    cnf_list.append(impl_to_clause)

        return cnf_list


    """
    If the game board has a solution, solves N-queens game problem returns queens postion on the board. 

    Args:
        grid (list[list[str]]): The grid represented as a 2D list of color codes (strings).
    
    Returns:
        list[tuple[int, int]]: A list of tuples containing queen positions on game board or empty list.
    """
    def solve(self, grid: list[list[str]]) -> list[int]:
        if not self._is_grid_valid(grid):
            raise SquareListError("Grid is not a square")
            
        N = len(grid)
        cnf_list = self._generate_formula_in_cnf(grid, N)

        cnf = CNF(from_clauses=cnf_list)

        with Solver(bootstrap_with=cnf) as solver:
            status = solver.solve()
            print('formula is', f'{"s" if status else "uns"}atisfiable')

            if status:
                solution = solver.get_model()
                queens = [self._decode(i, N) for i in solution if i > 0]
                return queens

        return []