from musical_festival_lineup.mf_lineup_data import MFLineupData
from musical_festival_lineup.mf_lineup_GA import MFLineupGASolution
from musical_festival_lineup.mf_lineup_HA import MFLineupHCSolution
from musical_festival_lineup.mf_lineup_SA import MFLineupSASolution
from library.algorithms.hill_climbing import hill_climbing
from library.algorithms.simulated_annealing import simulated_annealing
from library.algorithms.genetic_algorithms.algorithm import genetic_algorithm
from library.algorithms.genetic_algorithms import mutation, selection, algorithm,crossover
import itertools
import os
import pandas as pd

import itertools
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed

def __init__(self,data):
    self.data=data
    
def run_HC(data:MFLineupData, max_iter=100, verbose=False):   
    best_solution = hill_climbing(initial_solution=MFLineupHCSolution(data=data),
                                      maximization=True,
                                      max_iter=max_iter,
                                      verbose=verbose)
    if verbose:
        print("Best solution of HA", best_solution)
        print("Fitness", best_solution.fitness())
    return best_solution
    
def run_SA(data:MFLineupData, neighbor_function, C, L, H,max_iter=100, verbose=False):
    best_solution, fitness_over_iter= simulated_annealing(
                                        initial_solution=MFLineupSASolution(data=data,
                                                                            neighbor_function=neighbor_function
                                                                            ), 
                                        maximization=True,
                                        C=C,
                                        L=L, 
                                        H=H,
                                        max_iter=max_iter,
                                        verbose=verbose)
    if verbose:
        print("Best solution of SA", best_solution)
        print("Fitness", best_solution.fitness())
    return best_solution,fitness_over_iter

def run_GA(data:MFLineupData,pop_size, max_gen, selection_algorithm,mutation_function, crossover_function,xo_prob=0.9, mut_prob=0.2,elitism=True,verbose=False):
    initial_population=[
        MFLineupGASolution(
            data=data,
            mutation_function=mutation_function,
            crossover_function=crossover_function
            )
            for _ in range(pop_size)
        ]
    best_solution,fitness_over_gen=genetic_algorithm(
    initial_population=initial_population,
    selection_algorithm=selection_algorithm,
    max_gen=max_gen,
    mut_prob=mut_prob,
    xo_prob=xo_prob,
    maximization=True,
    verbose=verbose,
    elitism=elitism,
    )
    if verbose:
        print("Best solution of GA", best_solution)
        print("Fitness", best_solution.fitness())
    return best_solution,fitness_over_gen


def run_algorithms_grid_search(
    algorithm_func,         
    param_grid,             
    fixed_params=None,      
    runs_per_config=30,
    output_csv_path="results.csv",
    verbose=False
):
    fixed_params = fixed_params or {}

    # Create all combinations of varying parameters
    keys, values = zip(*param_grid.items())
    grid = list(itertools.product(*values))

    all_rows = []
    for param_combo in grid:
        # Build param dict for this combo
        params = dict(zip(keys, param_combo))
        # Merge fixed params in
        full_params = {**fixed_params}

        # Now flatten any dict values in params into full_params
        for param_key, param_value in params.items():
            if isinstance(param_value, dict):
                for k, v in param_value.items():
                    full_params[k] = v  # e.g. mutation_function, mutation_mut_prob
            else:
                full_params[param_key] = param_value  # e.g. elitism=True

        # Build config label dynamically
        label_parts = []

        for param_key, param_value in params.items():
            if isinstance(param_value, dict) :
                for k, v in param_value.items():
                        value_name=v.__name__ if callable(v) else v
                        label_parts.append(f"{k}={value_name}")
            else:
                param_value=param_value.__name__ if callable(param_value) else param_value
                label_parts.append(f"{param_key}={param_value}")

        config_label = "__".join(label_parts)

        print(f"Running config: {config_label}")

        for run_nr in range(runs_per_config):
            # Call the algorithm with unpacked parameters
            result = algorithm_func(**full_params)

            # Handle result format:
            if isinstance(result, tuple) and len(result) == 2:
                best_solution, fitness_over_gens = result
            else:
                best_solution = result
                fitness_over_gens = [best_solution.fitness()]
                # fitness_over_gens = getattr(best_solution, "fitness_over_gens", None)
                # if fitness_over_gens is None:
                #     fitness_over_gens = [best_solution.fitness()]

            # Create row with config label, run number, and fitness per generation
            row = {"config_label": config_label, "run_nr": run_nr, "best_fitness":best_solution.fitness(), "best_solution":best_solution.repr}
            if verbose:
                print(row)         
            #  Add each parameter value as a separate column   
            for param_key, param_value in params.items():
                if isinstance(param_value, dict):
                    for k, v in param_value.items():
                        value_name = v.__name__ if callable(v) else v
                        row[k] = value_name
                else:
                    value_name = param_value.__name__ if callable(param_value) else param_value
                    row[param_key] = value_name
            for gen_idx, fitness in enumerate(fitness_over_gens):
                row[f"{gen_idx}"] = fitness

            all_rows.append(row)

    df = pd.DataFrame(all_rows)
    df.to_csv(output_csv_path, index=False)
    print(f"Saved results to {output_csv_path}")

    return df

