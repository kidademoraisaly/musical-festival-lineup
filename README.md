# 🎶 Musical Festival Lineup Optimisation

## Introduction

This project analyses optimisation algorithms — with a focus on **Genetic Algorithms (GA)** — to solve the **Musical Festival Lineup Problem**: scheduling artists across multiple stages and time slots while balancing three objectives:
- Ensuring headliners perform last.
- Maximising genre diversity.
- Avoiding conflicts between artists with overlapping fanbases.

The project defines the problem, solution representation, and fitness function, explores **Simulated Annealing (SA)** tuning, implements **Genetic Algorithms** with various crossover and mutation operators, and compares both approaches.

To ensure statistically reliable results, all experiments were run **30 times** due to the non-deterministic nature of these algorithms. Results are presented with performance plots and statistical tests to support conclusions.

---

##  Problem Definition & Solution Representation

We aim to schedule **35 artists** across **5 stages** and **7 time slots**, with each artist performing exactly once. All stages operate simultaneously during each time slot.

**Representation:**  
A solution is a list of 35 artist IDs, organised by time slots:
- **Positions 0–4 → Time Slot 1 (Stages 1–5)**
- **Positions 5–9 → Time Slot 2 (Stages 1–5)**  
... and so on.

This **slot-based representation** was chosen because:
- It better aligns with the fitness function, which evaluates artists playing at the same time on different stages.
- It makes it easier to preserve time slot groupings during crossover operations in the GA.

---

## 📊 Fitness Function

The quality of a festival lineup is determined by balancing **three equally weighted objectives**:

| Objective               | Description                                          | Calculation                                   | Normalisation                                       | Weight |
|:------------------------|:-----------------------------------------------------|:------------------------------------------------|:----------------------------------------------------|:--------|
| **Prime Slot Popularity** | Popularity of artists in final time slot             | Sum of popularity scores for the 5 final-slot artists | Divided by sum of top 5 popularity scores in dataset | 1/3 |
| **Genre Diversity**       | Variety of genres in each time slot                  | Count of unique genres in each slot             | Divided by 5 (max distinct genres per slot)          | 1/3 |
| **Conflict Penalty**       | Penalty for overlapping fan bases                    | Sum of conflict values for artist pairs in a slot | Divided by sum of top 10 conflict values in dataset  | 1/3 |

**Fitness Calculation:**  
For each lineup:
- Iterate through the lineup by time slot groups.
- Accumulate **genre diversity** and **conflict penalties**.
- In the final slot, add **prime slot popularity**.
- Final fitness is:
Fitness = Avg(Genre Diversity) + Prime Slot Popularity – Avg(Conflict Penalty)


**Range:**  
From **-1** (worst) to **2** (best).

---

## 🧪 Experiments & Results

- **Simulated Annealing (SA)** was tuned with different parameter settings.
- **Genetic Algorithms (GA)** were tested using various crossover methods:
  - Partial Mapped
  - Cycle
  - Order
  - Edge Recombination
- And various mutation strategies:
  - Swap
  - Insert
  - Inverse

Special **slot-wise** versions of these operators were implemented to preserve time slot groupings.

Each configuration was evaluated over **30 independent runs**, with performance compared using:
- Convergence curves
- Final fitness distributions
- Non-parametric tests (Wilcoxon, Kruskal-Wallis)

---

## 📁 Project Structure

```
Musical-festival-lineup/
│
├── data/                          # Artist data: popularity, genres, conflicts
│
├── library/                       # GA, SA and HC implementations
│
├── results/                       # CSV files with results of experiments
│
├── musical_festival_lineup/
│   ├── utils.py                   # Helper functions for visualisation purposes mainly
│   ├── mf_lineup_data.py          # Class that organises artist data and provides fitness metric functions
│   ├── mf_lineup.py               # Class defining the solution representation and fitness calculation
│   ├── mf_lineup_HC.py            # HC solution class, implements the get_neighbors function
│   ├── mf_lineup_SA.py            # SA solution class, implements the get_neighbor function
│   ├── mf_lineup_GA.py            # GA solution class, implements crossover and mutation methods
│   └── mf_lineup_solver.py        # Helper functions to run each algorithm with its solution instance
│
├── notebooks/
│   ├── data_preprocessing.ipynb        # Notebook for basic data exploration and preprocessing
│   ├── experimental_analysis.ipynb     # Main notebook with full experimental analysis
│   ├── musical_festival_lineup_GA.ipynb  # Notebook exploring GA operators: crossovers and mutations
│   └── musical_festival_lineup.ipynb     # Notebook explaining solution representation and fitness functions
```

## 🛠️ Requirements

- Python 3.9+
- NumPy
- Pandas
- SciPy
- Matplotlib
- Seaborn
- Jupyter Notebook

Install all dependencies with:

```bash
pip install -r requirements.txt