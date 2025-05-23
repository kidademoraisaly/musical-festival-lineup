from copy import deepcopy
import random
from musical_festival_lineup.mf_lineup import MFLineupSolution

class MFLineupHCSolution(MFLineupSolution):
    
    def get_neighbors(self):
        """
        Generate neighboring solutions by swapping two random artists in the lineup.
        """
        neighbors = []
        for i in range(1, len(self.repr)-2):
            new_lineup = deepcopy(self.repr)
            new_lineup[i], new_lineup[i+1] = new_lineup[i+1], new_lineup[i]
            neighbor = MFLineupHCSolution(data=self.data,repr=new_lineup)
            neighbors.append(neighbor)

        return neighbors