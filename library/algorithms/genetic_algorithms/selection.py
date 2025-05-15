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
        
def tournament_selection(population: list[Solution], tournament_size: int, maximization: bool):
    # Select a random subset of the population
    tournament = random.sample(population, tournament_size)

    def fitness_key(ind):
        return ind.fitness()

    # Find the best individual in the tournament
    if maximization:
        best_individual = max(tournament, key=fitness_key)
    else:
        best_individual = min(tournament, key=fitness_key)
        
    return deepcopy(best_individual)

def ranking_selection(population: list[Solution], maximization: bool):

    def fitness_key(ind):
        return ind.fitness()
    
    # Sort the population based on fitness
    # If maximization is True, sort in descending order
    if maximization:
        sort_pop = sorted(population, key=fitness_key, reverse=True)
    else:
        # Minimization: Sort in ascending order
        sort_pop = sorted(population, key=fitness_key, reverse=False)

    N = len(sort_pop)
    rank = list(range(1, N + 1))
    if maximization:
        rank = rank[::-1]

    # Calculate the selection probability for each individual
    rank_sum = sum(rank)
    selection_prob = [r / rank_sum for r in rank]

    # Select an individual based on the selection probability
    selected_ind = random.choices(sort_pop, weights=selection_prob, k=1)[0]
  
            
    return deepcopy(selected_ind)

