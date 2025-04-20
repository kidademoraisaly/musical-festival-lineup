import pandas as pd 
import os
from musical_festival_lineup.musical_festival_lineup import NUM_STAGES, NUM_SLOTS
import numpy as np
import math

ARTISTS_CSV_PATH="data/artists.csv"

CONFLICTS_CSV_PATH="data/conflicts.csv"


class MusicalFestivalData:

    def __init__(self, artists_csv=ARTISTS_CSV_PATH, conflicts_csv_path=CONFLICTS_CSV_PATH):
        self.artists=self._get_artists_processed(artists_csv)
        self.conflicts=self._get_conflicts_processed(conflicts_csv_path)
        self.max_popularity_in_prime_slot=self._get_max_popularity()
        self.max_worst_conflit_per_slot=self._get_max_worst_conflict()
        self.max_distinct_genre_per_slot=self._get_max_distinct_genre()

    def _get_artists_processed(self, path):
        artists_df=pd.read_csv(path, index_col=0)
        return artists_df
    
    def _get_conflicts_processed(self,path):
        np_conflicts=np.genfromtxt(CONFLICTS_CSV_PATH, delimiter=",", skip_header=1, usecols=range(1,self.artists.shape[0]+1))
        return np_conflicts
    
    def _get_max_distinct_genre(self, num_stages=NUM_STAGES):
        return min(self.artists["genre"].nunique(), num_stages) #can not be greater than the number of stages, which is maximum number of artists per slot
         
    def _get_max_popularity(self, num_stages=NUM_STAGES):
        return int(self.artists.nlargest(num_stages,"popularity")["popularity"].sum())
    
    def get_max_worst_conflict_loop(self, num_stages=NUM_STAGES):
        list_all_conflicts=[]
        n=self.conflicts.shape[0]
        for i in range(n):
            for j in range(i+1,n):
                list_all_conflicts.append(self.conflicts[i,j])
        top_conflicts=sorted(list_all_conflicts, reverse=True)[:5]
        return sum(top_conflicts)
    
    def _get_max_worst_conflict(self, num_stages=NUM_STAGES):
        n_conflicts=math.comb(num_stages,2)
        mask=np.triu(np.ones_like(self.conflicts, dtype=bool), k=1)
        selected_conflicts=self.conflicts[mask]
        top_conflicts=np.partition(selected_conflicts, -n_conflicts)[-n_conflicts:]
        return np.sum(top_conflicts)
    
    def get_count_distinct_genres(self, artists_ids_list):
        self.artists[self.artists.index.isin(artists_ids_list)].head()
        return self.artists[self.artists.index.isin(artists_ids_list)]["genre"].nunique()

    def get_sum_popularity(self,artists_ids_list):
        return int(self.artists[self.artists.index.isin(artists_ids_list)]["popularity"].sum())
   
    def get_sum_conflicts_loop(self, artists_ids_list):
        sum_conflicts=0
        n=len(artists_ids_list)
        for i in range(n):
            for j in range(i+1,n):
                row_idx=artists_ids_list[i]
                col_idx=artists_ids_list[j]
                sum_conflicts+=self.conflicts[row_idx,col_idx]
        return sum_conflicts
    
    def get_sum_conflicts(self, artists_ids_list):
        selected_conflicts=self.conflicts[np.ix_(artists_ids_list,artists_ids_list)]
        mask=np.triu(np.ones_like(selected_conflicts, dtype=bool), k=1)
        return np.sum(selected_conflicts[mask])
    

    

if __name__=="__main__":
    print(os.getcwd())
    artists_df= pd.read_csv(ARTISTS_CSV_PATH)
    conflicts_df=pd.read_csv(CONFLICTS_CSV_PATH)
    artists_df.head()
    conflicts_df.head()

