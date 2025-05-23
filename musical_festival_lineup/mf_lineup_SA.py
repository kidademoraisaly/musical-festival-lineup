from library.solution import Solution
from musical_festival_lineup.mf_lineup import MFLineupSolution
from musical_festival_lineup.mf_lineup_data import MFLineupData


class MFLineupSASolution(MFLineupSolution):

    def __init__(self,data:MFLineupData, neighbor_function ,repr=None):
        super().__init__(
            data=data,
            repr=repr
        )
        self.neighbor_function=neighbor_function
    
    def get_random_neighbor(self):
        new_repr=self.neighbor_function(self.repr,mut_prob=1)
        return MFLineupSASolution(
            data=self.data,
            neighbor_function=self.neighbor_function,
            repr=new_repr

        )

