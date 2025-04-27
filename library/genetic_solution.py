from abc import ABC, abstractmethod

class GeneticSolution(ABC):
    
    @abstractmethod
    def mutation(self):
        pass
    @abstractmethod
    def crossover(self,other):
        pass
