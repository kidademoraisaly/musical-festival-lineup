from library.solution import Solution
import random
import pandas as pd

NUM_STAGES=5
NUM_SLOTS=7
REPR_NUM_ELEMENTS=NUM_SLOTS*NUM_STAGES 
REPR_ELEMENTS_LEN=2
REPR_LOWER_BOUND=0
REPR_UPPER_BOUND=34

class MusicalFestivalSolution(Solution):
    def __init__(self, data, repr=None):
        if repr:
            MusicalFestivalSolution._validate_repr(repr=repr)                  
        super().__init__(repr=repr)
        self.data=data
    
    @staticmethod
    def _validate_repr(repr):
        if not isinstance(repr, str):
            raise ValueError("Representation should be a string")
        repr_len=REPR_NUM_ELEMENTS*REPR_ELEMENTS_LEN
        if not len(repr)==repr_len:
            raise ValueError(f"Representation should be of size {repr_len}")     
        for i in (0,len(repr),REPR_NUM_ELEMENTS):
            num=int(repr[i:i+REPR_NUM_ELEMENTS])
            if not (num>=REPR_LOWER_BOUND 
                    and num <=REPR_UPPER_BOUND):
                raise ValueError(f"The Values within a string should be between {REPR_LOWER_BOUND} and {REPR_UPPER_BOUND}.\
                                  The values with 1 digit should be precided by 0")
    
    def random_initial_representation(self):
        repr_list=random.sample(range(REPR_LOWER_BOUND,
                                       REPR_UPPER_BOUND+1),
                                REPR_NUM_ELEMENTS
                                      )
        return "".join([f"{num:02d}" for num in repr_list])
    

    def _get_slot_repr_list(self,slot):
        idx_bound=NUM_STAGES*REPR_ELEMENTS_LEN
        idx_start=slot*idx_bound
        repr_slot=self.repr[idx_start:idx_start+idx_bound]
        repr_list=[]
        for i in range(0,len(repr_slot),2):
            art_id=int(repr_slot[i:i+REPR_ELEMENTS_LEN])
            repr_list.append(art_id)
        return repr_list

    def _get_genre_diversity_normalized(self, slot_list_artists):
        return self.data.get_count_distinct_genres(slot_list_artists)/self.data.max_distinct_genre_per_slot
    
    def _get_conflicts_normalized(self,slot_list_artists):
        return self.data.get_sum_conflicts(slot_list_artists)/self.data.max_distinct_genre_per_slot
    
    def _get_popularity_normalized(self, slot_list_artists):
        return self.get_sum_popularity(slot_list_artists)/self.data.max_popularity_in_prime_slot

    def fitness(self):
        for i in range(NUM_SLOTS):
            slot_list_artists=self._get_slot_repr_list(i)
            fitness=self._get_conflicts_normalized(slot_list_artists)+self._get_genre_diversity_normalized(slot_list_artists)
            if i==NUM_SLOTS-1:
                fitness+=self._get_popularity_normalized(slot_list_artists)
        return fitness
    
  
            
           
            
               
    
            

        