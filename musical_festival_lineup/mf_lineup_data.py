import pandas as pd
import os
import numpy as np
import math

ARTISTS_CSV_PATH = "data/artists.csv"
CONFLICTS_CSV_PATH = "data/conflicts.csv"
NUM_STAGES = 5
NUM_SLOTS = 10

class MFLineupData:
    def __init__(self, artists_csv=ARTISTS_CSV_PATH, conflicts_csv_path=CONFLICTS_CSV_PATH):
        self.artists_df = pd.read_csv(artists_csv, index_col=0)
        self.artist_ids = self.artists_df.index.values

        # precompute mappings for fast lookup
        self.popularity_array = self.artists_df["popularity"].to_numpy()
        self.genre_array, self.genre_labels = pd.factorize(self.artists_df["genre"])

        self.conflicts = np.genfromtxt(conflicts_csv_path, delimiter=",", skip_header=1, usecols=range(1, self.artists_df.shape[0]+1))

        self.max_popularity_in_prime_slot = self._get_max_popularity()
        self.max_worst_conflit_per_slot = self._get_max_worst_conflict()
        self.max_distinct_genre_per_slot = self._get_max_distinct_genre()

    def _get_max_distinct_genre(self, num_stages=NUM_STAGES):
        return min(len(self.genre_labels), num_stages)

    def _get_max_popularity(self, num_stages=NUM_STAGES):
        return int(np.sort(self.popularity_array)[-num_stages:].sum())

    def _get_max_worst_conflict(self, num_stages=NUM_STAGES):
        n_conflicts = math.comb(num_stages, 2)
        mask = np.triu(np.ones_like(self.conflicts, dtype=bool), k=1)
        selected_conflicts = self.conflicts[mask]
        top_conflicts = np.partition(selected_conflicts, -n_conflicts)[-n_conflicts:]
        return np.sum(top_conflicts)

    def get_count_distinct_genres(self, artist_ids_list):
        genre_codes = self.genre_array[artist_ids_list]
        return np.unique(genre_codes).size

    def get_sum_popularity(self, artist_ids_list):
        return int(self.popularity_array[artist_ids_list].sum())

    def get_sum_conflicts(self, artist_ids_list):
        selected_conflicts = self.conflicts[np.ix_(artist_ids_list, artist_ids_list)]
        mask = np.triu(np.ones_like(selected_conflicts, dtype=bool), k=1)
        return np.sum(selected_conflicts[mask])

   

if __name__=="__main__":
    print(os.getcwd())
    artists_df= pd.read_csv(ARTISTS_CSV_PATH)
    conflicts_df=pd.read_csv(CONFLICTS_CSV_PATH)
    artists_df.head()
    conflicts_df.head()

