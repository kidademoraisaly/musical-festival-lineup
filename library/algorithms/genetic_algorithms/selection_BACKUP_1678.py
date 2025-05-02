import random
from copy import deepcopy

from library.solution import Solution


def fitness_proportionate_selection(population: list[Solution], maximization: bool):
    if maximization:
        fitness_values = []
        for ind in population:
            if ind.fitness() < 0:
                # If fitness is negative (invalid solution like in Knapsack)
                # Set fitness to very small positive value
                # Probability of selecting this individual is nearly 0.
                fitness_values.append(0.0000001)
            else:
                fitness_values.append(ind.fitness())
    else:
        # Minimization: Use the inverse of the fitness value
        # Lower fitness should have higher probability of being selected
        fitness_values = [1 / ind.fitness() for ind in population]

    total_fitness = sum(fitness_values)
    # Generate random number between 0 and total
    random_nr = random.uniform(0, total_fitness)
    # For each individual, check if random number is inside the individual's "box"
    box_boundary = 0
    for ind_idx, ind in enumerate(population):
        box_boundary += fitness_values[ind_idx]
        if random_nr <= box_boundary:
            return deepcopy(ind)
<<<<<<< HEAD
        
def tournament_selection(population: list[Solution], tournament_size: int, maximization: bool):
    # Select a random subset of the population
    tournament = random.sample(population, tournament_size)
    tournament_solution = [] 
    len_tornament_solution = len(tournament_solution)

    def fitness_key(ind):
        return ind.fitness()
    
    while len_tornament_solution < len(population):
        for ind in tournament:
            # Find the best individual in the tournament
            if maximization:
                best_individual = max(tournament, key=fitness_key)
            else:
                best_individual = min(tournament, key=fitness_key)
            tournament_solution.append(best_individual)
        len_tornament_solution += 1
        
    return deepcopy(tournament_solution)
=======
>>>>>>> 04e55446cf5e33e234244b6e8422fa45d7f2d7a5
