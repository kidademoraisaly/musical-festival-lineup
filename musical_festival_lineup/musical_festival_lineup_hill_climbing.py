from copy import deepcopy
import random
from musical_festival_lineup.musical_festival_lineup import MusicalFestivalSolution

class MusicalFestivalHillClimbingSolution(MusicalFestivalSolution):
    def get_neighbors(self):
        """
        Generate neighboring solutions by swapping two random artists in the lineup.
        """
        neighbors = []

        for _ in range(10):  # Generate 10 neighbors
            new_solution = deepcopy(self)
            
            # Randomly select two indices to swap
            idx1, idx2 = random.sample(range(len(new_solution.repr)), 2)
            new_solution.repr[idx1], new_solution.repr[idx2] = new_solution.repr[idx2], new_solution.repr[idx1]

            neighbors.append(new_solution)

        return neighbors