import pandas as pd  
from musical_festival_lineup.mf_lineup import NUM_STAGES, NUM_SLOTS, REPR_ELEMENTS_LEN
from musical_festival_lineup.mf_lineup import MFLineupSolution
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wilcoxon
import seaborn as sns


def visualize_musical_lineup(repr: list|str,artists_df):
    """
    Generates a readable DataFrame representing the musical festival lineup.

    This function takes a solution representation (as a list or string) and a DataFrame
    containing artist details, then returns a formatted DataFrame showing which artist 
    performs on each stage at each time slot, including their name, genre, and popularity.

    Parameters:
    -----------
    repr : list or str
        The solution representation, either as a list of artist IDs or a string.
        If a string is provided, it is converted to a list using _get_repr_list.

    artists_df : pandas.DataFrame
        A DataFrame containing artist information. It must have the artist IDs 
        as its index and at least the following columns:
        - 'name'
        - 'genre'
        - 'popularity'

    Returns:
    --------
    pandas.DataFrame
        A DataFrame where each row represents a time slot and each column represents 
        a stage, with the cell content in the format:
        "{artist_id}: {artist_name}|{artist_genre}|{artist_popularity}"

    Example:
    --------
        | Slot   | Stage 1                     | Stage 2                        | ... |
        |--------|-----------------------------|--------------------------------|-----|
        | Slot 1 | 12: Blue Horizon|Pop|51      | 5: Echo Chamber|Electronic|98  | ... |
    """
    if isinstance(repr,str):
        repr=MFLineupSolution._get_repr_list(repr)
    MFLineupSolution._validate_repr(repr)
    lineup_list=[]
    idx_bound = NUM_STAGES
    for i in range(0, NUM_SLOTS ):
        row={"Slot": f"Slot {i+1}"}     
        for stage in range(NUM_STAGES):
            j = i * idx_bound + stage
            artist_id = repr[j]
            artist_name=artists_df.loc[artist_id, "name"]
            artist_genre=artists_df.loc[artist_id,"genre"]
            artist_popularity=artists_df.loc[artist_id,"popularity"]
            row[f"Stage {stage+1}"]=f"{artist_id}: {artist_name}|{artist_genre}|{artist_popularity}"
        lineup_list.append(row)
    df=pd.DataFrame(lineup_list)
    return df

def compare_algorithms(df_alg1, df_alg2, alg1_name='Algorithm 1', alg2_name='Algorithm 2', alpha=0.05):
    """
    Compare two algorithms using Wilcoxon signed-rank test across multiple columns (generations).

    Parameters:
        df_alg1 (pd.DataFrame): Results of algorithm 1 (rows = runs, columns = generations)
        df_alg2 (pd.DataFrame): Results of algorithm 2 (same shape as df_alg1)
        alg1_name (str): Name of algorithm 1 (for reporting)
        alg2_name (str): Name of algorithm 2 (for reporting)
        alpha (float): Significance level for hypothesis test (default 0.05)

    Returns:
        pd.DataFrame: Summary table with columns:
            - Generation
            - Wilcoxon_statistic
            - p_value
            - Median_difference (alg1 - alg2)
            - Better_algorithm (string: alg1_name, alg2_name, tie, or no significant difference)
    """

    results = []

    # Check that shapes match
    if df_alg1.shape != df_alg2.shape:
        raise ValueError("Input DataFrames must have the same shape.")
    results = []
    gen_cols = [col for col in df_alg1.columns if col.isdigit()]

    for col in gen_cols:
        alg1_scores = df_alg1[col]
        alg2_scores = df_alg2[col]
        # Calculate differences
        #diffs = alg1_scores - alg2_scores
        diffs = alg1_scores.values - alg2_scores.values
        
        # Perform Wilcoxon signed-rank test
        stat, p_value = wilcoxon(alg1_scores, alg2_scores)
     
        # Median difference for direction
        median_diff = np.median(diffs)

        # Decide which algorithm is better based on significance and median difference
        if p_value < alpha:
            if median_diff > 0:
                better = alg1_name
            elif median_diff < 0:
                better = alg2_name
            else:
                better = 'Tie'
        else:
            better = 'No significant difference'

        results.append({
            'Generation': col,
            'Wilcoxon_statistic': stat,
            'p_value': p_value,
            'Median_difference': median_diff,
            'Better_algorithm': better
        })

    return pd.DataFrame(results)



def plot_fitness_over_gen(results_df: pd.DataFrame, param="config_label"):
    """
    Plots mean and median fitness across generations for each configuration.
    Expects a DataFrame with a param column and generation columns named '0', '1', '2', ...
    """

    #gen_cols = [col for col in results_df.columns if col.isdigit()]
    gen_cols = sorted([col for col in results_df.columns if col.isdigit()], key=lambda x: int(x))
    fig, axes = plt.subplots(1, 2, figsize=(14, 10), sharey=True)
    handles, labels = [], []

    for config_label in results_df[param].unique():
        df_config = results_df[results_df[param] == config_label]

        # Compute mean and median across runs (rows) for each generation
        mean_fitness = df_config[gen_cols].mean(axis=0)
        median_fitness = df_config[gen_cols].median(axis=0)

        # Plot mean and median
        gens = mean_fitness.index.astype(int)
        
        #previous lines without std and IQR
        line1, = axes[0].plot(gens, mean_fitness.values, label=config_label)
        axes[1].plot(gens, median_fitness.values, label=config_label)
      


        handles.append(line1)
        labels.append(config_label)

    axes[0].set_title("Mean Fitness Across Generations")
    axes[1].set_title("Median Fitness Across Generations")

    for ax in axes:
        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness")
        ax.grid(True)

    # Shared legend
    legend = fig.legend(
        handles,
        labels,
        loc='lower center',
        #bbox_to_anchor=(0.5, -0.15),
        ncol=1,
        frameon=True,
        borderpad=1
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.show()

def plot_median_fitness_over_gen(results_df: pd.DataFrame, param="config_label"):
    """
    Plots median fitness across generations for each configuration.
    Expects a DataFrame with a param column and generation columns named '0', '1', '2', ...
    """

    gen_cols = [col for col in results_df.columns if col.isdigit()]
    plt.figure(figsize=(10, 6))
    
    for config_label in results_df[param].unique():
        df_config = results_df[results_df[param] == config_label]

        # Compute median across runs (rows) for each generation
        median_fitness = df_config[gen_cols].median(axis=0)

        # Plot median
        gens = median_fitness.index.astype(int)
        plt.plot(gens, median_fitness.values, label=config_label)

    plt.title("Median Fitness Across Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.legend(title=param)
    plt.tight_layout()
    plt.show()


def plot_fitness_over_2_gen(results_df: pd.DataFrame, param="config_label"):
    """
    Plots mean and median fitness across generations for each configuration.
    Expects a DataFrame with a param column and generation columns named '0', '1', '2', ...
    
    If param is "config_label", behavior is unchanged.
    If param is not "config_label", first groups by config_label, calculates mean/median,
    then calculates mean/median of those values for each unique param value.
    """
    gen_cols = [col for col in results_df.columns if col.isdigit()]
    fig, axes = plt.subplots(1, 2, figsize=(14, 10), sharey=True)
    handles, labels = [], []
    
    if param == "config_label":
        for config_label in results_df[param].unique():
            df_config = results_df[results_df[param] == config_label]
            # Compute mean and median across runs (rows) for each generation
            mean_fitness = df_config[gen_cols].mean(axis=0)
            median_fitness = df_config[gen_cols].median(axis=0)
            # Plot mean and median
            gens = mean_fitness.index.astype(int)
            line1, = axes[0].plot(gens, mean_fitness.values, label=config_label)
            axes[1].plot(gens, median_fitness.values, label=config_label)
            handles.append(line1)
            labels.append(config_label)
    else:

        for param_value in results_df[param].unique():
            df_param = results_df[results_df[param] == param_value]
            
            # Store means and medians for each config_label within this param value
            config_means = []
            config_medians = []
            
            # Calculate mean/median for each config_label in this param group
            for config_label in df_param["config_label"].unique():
                df_config = df_param[df_param["config_label"] == config_label]
                
                # Calculate mean/median across runs for each generation for this config_label
                mean_fitness = df_config[gen_cols].mean(axis=0)
                median_fitness = df_config[gen_cols].median(axis=0)
                
                config_means.append(mean_fitness)
                config_medians.append(median_fitness)
            
            # Calculate mean of means and median of medians
            if config_means:
                # Stack all series and calculate mean/median along axis=0 (across config_labels)
                mean_of_means = pd.concat(config_means, axis=1).mean(axis=1)
                median_of_medians = pd.concat(config_medians, axis=1).median(axis=1)
                
                # Plot mean and median
                gens = mean_of_means.index.astype(int)
                line1, = axes[0].plot(gens, mean_of_means.values, label=param_value)
                axes[1].plot(gens, median_of_medians.values, label=param_value)
                handles.append(line1)
                labels.append(param_value)
    
    axes[0].set_title("Mean Fitness Across Generations")
    axes[1].set_title("Median Fitness Across Generations")
    for ax in axes:
        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness")
        ax.grid(True)
    
    # Shared legend
    legend = fig.legend(
        handles,
        labels,
        loc='lower center',
        ncol=1,
        frameon=True,
        borderpad=1
    )
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.show()

def plot_fitness_over_gen_top_n(results_df: pd.DataFrame, top_n=5):
    """
    Plots mean and median fitness across generations for each configuration.
    Expects a DataFrame with a 'config_label' column and generation columns named '0', '1', '2', ...
    Displays only the top_n configs by final generation mean fitness.
    """

    gen_cols = [col for col in results_df.columns if col.isdigit()]
    fig, axes = plt.subplots(1, 2, figsize=(20, 20), sharey=True)
    handles, labels = [], []

    # Compute final generation mean fitness per config
    final_gen_col = gen_cols[-1]
    config_means = results_df.groupby("config_label")[final_gen_col].mean().sort_values(ascending=False)

    # Pick top_n configs
    top_configs = config_means.head(top_n).index.tolist()

    for config_label in top_configs:
        df_config = results_df[results_df['config_label'] == config_label]

        # Compute mean and median across runs (rows) for each generation
        mean_fitness = df_config[gen_cols].mean(axis=0)
        median_fitness = df_config[gen_cols].median(axis=0)

        # Plot mean and median
        gens = mean_fitness.index.astype(int)
        line1, = axes[0].plot(gens, mean_fitness.values, label=config_label)
        axes[1].plot(gens, median_fitness.values, label=config_label)

        handles.append(line1)
        labels.append(config_label)

    axes[0].set_title("Mean Fitness Across Generations")
    axes[1].set_title("Median Fitness Across Generations")

    for ax in axes:
        ax.set_xlabel("Generation")
        ax.set_ylabel("Fitness")
        ax.grid(True)

    # Shared legend
    legend = fig.legend(
        handles,
        labels,
        loc='lower center',
        ncol=1,
        frameon=True,
        borderpad=1
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.show()




def plot_comparison_summary(summary_df, alpha=0.05,
                            alg1_name='Algorithm 1',
                            alg2_name='Algorithm 2'):
    """
    Plot p-values and better algorithm info from Wilcoxon test summary.

    Parameters:
        summary_df (pd.DataFrame): output from compare_algorithms()
        alpha (float): significance threshold (default 0.05)
        alg1_name, alg2_name (str): algorithm names for legend
    """
    summary_df['Generation'] = summary_df['Generation'].astype(int)
    summary_df = summary_df.sort_values(by='Generation')
    
    generations = summary_df['Generation'].astype(int)
    p_values = summary_df['p_value']
    median_diff = summary_df['Median_difference']
    better = summary_df['Better_algorithm']

    plt.figure(figsize=(14, 6))

    # Plot p-values over generations
    plt.plot(generations, p_values, marker='o', linestyle='-', label='p-value')
    plt.axhline(alpha, color='red', linestyle='--', label=f'Significance level ({alpha})')
    added_labels = set()  # keep track of labels already a
    for gen, p, better_alg in zip(generations, p_values, better):
        if p < alpha:
            if better_alg == alg1_name and alg1_name not in added_labels:
                plt.scatter(gen, p, color='green', s=120, label=alg1_name)
                added_labels.add(alg1_name)
            elif better_alg == alg2_name and alg2_name not in added_labels:
                plt.scatter(gen, p, color='blue', s=120, label=alg2_name)
                added_labels.add(alg2_name)
            else:
                # If label already added, plot without label to avoid duplicates
                color = 'green' if better_alg == alg1_name else 'blue'
                plt.scatter(gen, p, color=color, s=120)
    plt.xlabel('Generation')
    plt.ylabel('P-value')
    plt.title('Wilcoxon Test P-values Across Generations')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_median_difference(summary_df, alpha=0.05, 
                           alg1_name='Algorithm 1', alg2_name='Algorithm 2'):
    """
    Plots the median fitness difference between two algorithms across generations.

    Bars are colored based on whether the median difference favors Algorithm 1 (green) 
    or Algorithm 2 (blue). Bars with significant p-values (below the alpha threshold)
    are highlighted with a red edge.

    Parameters:
    -----------
    summary_df : pandas.DataFrame
        A DataFrame containing at least the following columns:
        - 'Generation' : Generation number
        - 'Median_difference' : Difference in median fitness (alg1 - alg2)
        - 'p_value' : p-value of statistical test at each generation

    alpha : float, optional (default=0.05)
        The significance level for highlighting p-values.

    alg1_name : str, optional
        Display name for Algorithm 1 (shown in plot legend and annotations).

    alg2_name : str, optional
        Display name for Algorithm 2 (shown in plot legend and annotations).

    Returns:
    --------
    None
        Displays a matplotlib bar plot visualizing the median differences and significance.
    """
    summary_df['Generation'] = summary_df['Generation'].astype(int)
    summary_df = summary_df.sort_values(by='Generation')
    generations = summary_df['Generation'].astype(int)
    median_diff = summary_df['Median_difference']
    p_values = summary_df['p_value']

    plt.figure(figsize=(14, 6))
    colors = ['green' if val > 0 else 'blue' for val in median_diff]
    edge_colors = ['red' if p < alpha else 'none' for p in p_values]

    bars = plt.bar(generations, median_diff,
                   color=colors,
                   edgecolor=edge_colors,
                   linewidth=1.5)

    plt.axhline(0, color='black', linestyle='--')
    plt.xlabel('Generation')
    plt.ylabel('Median Difference')
    plt.title('Median Differences Between Algorithms Across Generations\n(Red edges = significant p-value)')

    ylim = plt.ylim()
    y_range = ylim[1] - ylim[0]
    
    # Adjust the limits slightly to add space for text labels
    plt.ylim(ylim[0] - 0.15 * y_range, ylim[1] + 0.15 * y_range)

    # Add directional text outside plot area, just below min and above max y-limits
    plt.text(x=-5, y=ylim[1] + 0.05 * y_range, s=f'{alg1_name} better',
             color='green', fontsize=12, weight='bold', va='bottom', ha='left')

    plt.text(x=-5, y=ylim[0] - 0.05 * y_range, s=f'{alg2_name} better',
             color='blue', fontsize=12, weight='bold', va='top', ha='left')


    plt.legend(handles=[
        plt.Line2D([0], [0], color='green', lw=8, label=alg1_name),
        plt.Line2D([0], [0], color='blue', lw=8, label=alg2_name),
        plt.Line2D([0], [0], color='red', lw=2, label=f'Significant (p < {alpha})')
    ])

    plt.grid(True)
    plt.show()

def concat_with_intersection(df1, df2):
    """
    Concatenates two DataFrames while keeping only the columns they have in common.

    This is useful when merging DataFrames that may not share the same structure,
    ensuring only overlapping columns are included in the final concatenated result.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame to concatenate.

    df2 : pandas.DataFrame
        The second DataFrame to concatenate.

    Returns:
    --------
    pandas.DataFrame
        A concatenated DataFrame containing only the columns present in both input DataFrames.
    """
    # Get common columns
    common_columns = list(set(df1.columns) & set(df2.columns))
    
    # Select only common columns
    df1_common = df1[common_columns]
    df2_common = df2[common_columns]
    
    # Concatenate
    return pd.concat([df1_common, df2_common], ignore_index=True)
