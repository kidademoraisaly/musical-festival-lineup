from library.solution import Solution
from musical_festival_lineup.mf_lineup_data import MFLineupData
import random
import pandas as pd

NUM_STAGES=5
NUM_SLOTS=7
REPR_NUM_ELEMENTS=NUM_SLOTS*NUM_STAGES 
REPR_ELEMENTS_LEN=2
REPR_LOWER_BOUND=0
REPR_UPPER_BOUND=34

class MFLineupSolution(Solution):
    def __init__(self, data:MFLineupData, repr=None):
        if repr:
            if isinstance(repr, str):                
                repr=MFLineupSolution._get_repr_list(repr)  
            MFLineupSolution._validate_repr(repr=repr)                  
        super().__init__(repr=repr)
        self.data=data
        self._fitness=None
    
    @staticmethod
    def _get_repr_list(repr:str):
        repr_list=[]
        for i in range(0,len(repr),REPR_ELEMENTS_LEN):
            num=int(repr[i:i+REPR_ELEMENTS_LEN])
            repr_list.append(num)
        return repr_list
    
    @staticmethod
    def _validate_repr(repr):
        if isinstance(repr,list):
            if not len(repr)==REPR_NUM_ELEMENTS:
                raise ValueError(f"Representation should be of size {REPR_NUM_ELEMENTS}")  
            if len(repr) != len(set(repr)):
                raise ValueError(f"Representation can not contain duplicates. One artist has to appear once.")  
            for ar in repr:
                if not (ar>=REPR_LOWER_BOUND 
                        and ar<=REPR_UPPER_BOUND):
                    raise ValueError(f"The Values within a string/list should be between {REPR_LOWER_BOUND} and {REPR_UPPER_BOUND}.\
                                    If it is a string the values with 1 digit should be precided by 0")            
        else:
            raise ValueError("Representation should be a string or list")

    
     
    
    def random_initial_representation(self):
        repr_list=random.sample(range(REPR_LOWER_BOUND,
                                       REPR_UPPER_BOUND+1),
                                REPR_NUM_ELEMENTS
                                 ) 
        MFLineupSolution._validate_repr(repr_list)      
        return repr_list

    
    def _get_slot_repr_list(self,slot):
        if 0<=slot<NUM_SLOTS:
            idx_bound=slot*NUM_STAGES
            return self.repr[idx_bound:idx_bound+NUM_STAGES]
        else: 
            print(f"Slot should be between 0 and {NUM_SLOTS-1}")


    def _get_genre_diversity_normalized(self, artists_ids_list):
        genre_normalized=self.data.get_count_distinct_genres(artists_ids_list)/self.data.max_distinct_genre_per_slot
        if not(0<=genre_normalized<=1):
            raise ValueError("The genre normalized should be between 0 and 1")
        return genre_normalized
 
    def _get_conflicts_normalized(self,artists_ids_list):
        conflicts_normalized=self.data.get_sum_conflicts(artists_ids_list)/self.data.max_worst_conflit_per_slot
        if not(0<=conflicts_normalized<=1):
            raise ValueError("The conflitcs normalized should be between 0 and 1")
        return conflicts_normalized
    
    def _get_popularity_normalized(self, artists_ids_list):
        populatirity_normalized=self.data.get_sum_popularity(artists_ids_list)/self.data.max_popularity_in_prime_slot
        if not(0<=populatirity_normalized<=1):
            raise ValueError("The populatity normalized should be between 0 and 1")
        return populatirity_normalized
    

    def fitness(self,verbose=False):
        if self._fitness is None:
            self._fitness=self.compute_fitness(verbose)
        return self._fitness


    def compute_fitness(self, verbose=False):
        conflicts_normalized=[]
        genres_normalized=[]
        sum_popularity=0
        for i in range(NUM_SLOTS):
            slot_list_artists=self._get_slot_repr_list(i)
            conflict_normalized=self._get_conflicts_normalized(slot_list_artists)
            genre_normalized=self._get_genre_diversity_normalized(slot_list_artists)
            conflicts_normalized.append(conflict_normalized)
            genres_normalized.append(genre_normalized)
            if i==NUM_SLOTS-1:
                sum_popularity=self._get_popularity_normalized(slot_list_artists)
            if verbose:
                print("Slot of artists:" , slot_list_artists)
                print(f"Slot {i}: Conflitcs: {conflict_normalized}, genres: {genre_normalized}, sum_popularity: {sum_popularity}")
                print(f"Slot {i}: List of  Conflitcs: {conflicts_normalized}, List of genres: {genres_normalized}, Popularity of the prime slot: {sum_popularity}")
        avg_conflicts= sum(conflicts_normalized) / len(conflicts_normalized)
        avg_genres=sum(genres_normalized)/len(genres_normalized)
        fitness= avg_genres+sum_popularity-avg_conflicts
        if  not (-1 <=fitness<=2):
            raise ValueError("Fitness should be between -1 and 2 ")
        if verbose:
            print(f"Average of conflits: {avg_conflicts}, Average of distinct genres {avg_genres}, and Popularity in prime slot: {sum_popularity}")
            print(f"Fitness: {fitness}")
        return fitness
    
