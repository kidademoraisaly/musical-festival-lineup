from musical_festival_lineup.mf_lineup import MFLineupSolution
from library.genetic_solution import GeneticSolution
from musical_festival_lineup.mf_lineup_data import MFLineupData

class MFLineupGASolution(MFLineupSolution,GeneticSolution):
    def __init__(self, data : MFLineupData, mutation_function, crossover_function, repr=None ):
        super().__init__(
            data=data,
            repr=repr
        )

        self.mutation_function=mutation_function
        self.crossover_function=crossover_function
    
    def mutation(self, mut_prob):
        repr=self.mutation_function(self.repr, mut_prob)
        return MFLineupGASolution(
            data=self.data,
            mutation_function=self.mutation_function,
            crossover_function=self.crossover_function,
            repr=repr

        )
    
    def crossover(self, other):
        offspring1_repr, offspring2_repr=self.crossover_function(self.repr, other.repr)
        return(
            MFLineupGASolution(
                data=self.data,
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                repr=offspring1_repr
            ),
            MFLineupGASolution(
                data=self.data,
                mutation_function=self.mutation_function,
                crossover_function=self.crossover_function,
                repr=offspring2_repr
                
            )
        )
    

