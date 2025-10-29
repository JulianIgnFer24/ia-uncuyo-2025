"""
N-Queens problem implementation using CSP with backtracking and forward checking.
"""
import time
from typing import List, Set, Dict, Optional, Tuple
import copy


class NQueensCSP:
    """
    N-Queens problem formulated as a Constraint Satisfaction Problem.
    
    Variables: Q1, Q2, ..., Qn (one queen per column)
    Domain: {1, 2, ..., n} (row positions for each queen)
    Constraints: No two queens can attack each other
    """
    
    def __init__(self, n: int):
        self.n = n
        self.variables = list(range(n))  # columns 0, 1, ..., n-1
        self.domains = {var: set(range(n)) for var in self.variables}  # rows 0, 1, ..., n-1
        self.assignment = {}  # column -> row assignment
        self.nodes_explored = 0
        
    def is_complete(self) -> bool:
        """Check if all variables are assigned."""
        return len(self.assignment) == self.n
    
    def is_consistent(self, var: int, value: int) -> bool:
        """Check if assigning value to var is consistent with current assignment."""
        for assigned_var, assigned_value in self.assignment.items():
            if assigned_var != var:
                # Same row
                if assigned_value == value:
                    return False
                # Same diagonal
                if abs(assigned_var - var) == abs(assigned_value - value):
                    return False
        return True
    
    def get_unassigned_variable(self) -> Optional[int]:
        """Get the next unassigned variable (MRV heuristic - Minimum Remaining Values)."""
        unassigned = [var for var in self.variables if var not in self.assignment]
        if not unassigned:
            return None
        
        # Choose variable with smallest domain (MRV)
        return min(unassigned, key=lambda var: len(self.domains[var]))
    
    def get_domain_values(self, var: int) -> List[int]:
        """Get domain values for variable, ordered by least constraining value."""
        return list(self.domains[var])
    
    def assign(self, var: int, value: int):
        """Assign value to variable."""
        self.assignment[var] = value
    
    def unassign(self, var: int):
        """Remove assignment for variable."""
        if var in self.assignment:
            del self.assignment[var]
    
    def backtrack(self) -> bool:
        """Backtracking search algorithm."""
        self.nodes_explored += 1
        
        if self.is_complete():
            return True
        
        var = self.get_unassigned_variable()
        if var is None:
            return False
        
        for value in self.get_domain_values(var):
            if self.is_consistent(var, value):
                self.assign(var, value)
                
                if self.backtrack():
                    return True
                
                self.unassign(var)
        
        return False
    
    def forward_check(self, var: int, value: int) -> Dict[int, Set[int]]:
        """
        Apply forward checking: remove inconsistent values from future variables.
        Returns the removed values for potential restoration.
        """
        removed = {}
        
        for future_var in self.variables:
            if future_var not in self.assignment and future_var != var:
                to_remove = set()
                
                for domain_value in self.domains[future_var]:
                    # Check if future assignment would conflict with current assignment
                    temp_assignment = self.assignment.copy()
                    temp_assignment[var] = value
                    temp_assignment[future_var] = domain_value
                    
                    # Same row conflict
                    if domain_value == value:
                        to_remove.add(domain_value)
                    # Diagonal conflict
                    elif abs(var - future_var) == abs(value - domain_value):
                        to_remove.add(domain_value)
                
                if to_remove:
                    removed[future_var] = to_remove
                    self.domains[future_var] -= to_remove
        
        return removed
    
    def restore_domains(self, removed: Dict[int, Set[int]]):
        """Restore domain values that were removed during forward checking."""
        for var, values in removed.items():
            self.domains[var] |= values
    
    def backtrack_with_forward_checking(self) -> bool:
        """Backtracking search with forward checking."""
        self.nodes_explored += 1
        
        if self.is_complete():
            return True
        
        var = self.get_unassigned_variable()
        if var is None:
            return False
        
        # Check if any domain is empty
        for future_var in self.variables:
            if future_var not in self.assignment and len(self.domains[future_var]) == 0:
                return False
        
        for value in list(self.domains[var]):  # Copy to avoid modification during iteration
            if self.is_consistent(var, value):
                self.assign(var, value)
                
                # Apply forward checking
                removed = self.forward_check(var, value)
                
                # Check if any domain became empty
                empty_domain = any(len(self.domains[future_var]) == 0 
                                 for future_var in self.variables 
                                 if future_var not in self.assignment)
                
                if not empty_domain and self.backtrack_with_forward_checking():
                    return True
                
                # Backtrack: restore domains and unassign
                self.restore_domains(removed)
                self.unassign(var)
        
        return False
    
    def solve_backtrack(self) -> Tuple[Optional[List[int]], int, float]:
        """
        Solve using backtracking.
        Returns: (solution, nodes_explored, time_taken)
        """
        self.assignment = {}
        self.nodes_explored = 0
        self.domains = {var: set(range(self.n)) for var in self.variables}
        
        start_time = time.time()
        success = self.backtrack()
        end_time = time.time()
        
        if success:
            solution = [self.assignment[i] for i in range(self.n)]
            return solution, self.nodes_explored, end_time - start_time
        else:
            return None, self.nodes_explored, end_time - start_time
    
    def solve_forward_checking(self) -> Tuple[Optional[List[int]], int, float]:
        """
        Solve using backtracking with forward checking.
        Returns: (solution, nodes_explored, time_taken)
        """
        self.assignment = {}
        self.nodes_explored = 0
        self.domains = {var: set(range(self.n)) for var in self.variables}
        
        start_time = time.time()
        success = self.backtrack_with_forward_checking()
        end_time = time.time()
        
        if success:
            solution = [self.assignment[i] for i in range(self.n)]
            return solution, self.nodes_explored, end_time - start_time
        else:
            return None, self.nodes_explored, end_time - start_time


def is_valid_solution(solution: List[int]) -> bool:
    """Check if a solution is valid (no attacking queens)."""
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            # Same row
            if solution[i] == solution[j]:
                return False
            # Same diagonal
            if abs(i - j) == abs(solution[i] - solution[j]):
                return False
    return True


def print_board(solution: List[int]):
    """Print the board with queens placed."""
    n = len(solution)
    print("\nSolution:")
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()


if __name__ == "__main__":
    # Test the implementation
    n = 4
    csp = NQueensCSP(n)
    
    print(f"Solving {n}-Queens problem...")
    
    # Test backtracking
    print("\n--- Backtracking ---")
    solution, nodes, time_taken = csp.solve_backtrack()
    if solution:
        print(f"Solution found: {solution}")
        print(f"Nodes explored: {nodes}")
        print(f"Time taken: {time_taken:.6f} seconds")
        print(f"Valid solution: {is_valid_solution(solution)}")
        print_board(solution)
    else:
        print("No solution found")
    
    # Test forward checking
    print("\n--- Forward Checking ---")
    solution, nodes, time_taken = csp.solve_forward_checking()
    if solution:
        print(f"Solution found: {solution}")
        print(f"Nodes explored: {nodes}")
        print(f"Time taken: {time_taken:.6f} seconds")
        print(f"Valid solution: {is_valid_solution(solution)}")
        print_board(solution)
    else:
        print("No solution found")
