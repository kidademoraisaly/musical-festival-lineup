import random
from musical_festival_lineup.musical_festival_lineup_genetic import MusicalFestivalGASolution
from library.algorithms.genetic_algorithms import crossover, mutation

class RouletteWheel(MusicalFestivalGASolution):
    
    def __init__(self, population, mutation_function=mutation.swap_mutation, crossover_function=crossover.partial_crossover):
        super().__init__(population, mutation_function, crossover_function)
        self.population = population

    def roulette_wheel_selection(self):
        # Calculate the total fitness of all individuals
        total_fitness = sum(individual.fitness() for individual in self.population)
        
        selection_point = random.uniform(0, total_fitness)
        
        # Select an individual based on the selection point
        cumulative_fitness = 0
        for individual in self.population:
            cumulative_fitness += individual.fitness()
            if cumulative_fitness >= selection_point:
                return individual  # Return the selected individual
        
        # If nothing is selected return the last individual
        return self.population[-1]

