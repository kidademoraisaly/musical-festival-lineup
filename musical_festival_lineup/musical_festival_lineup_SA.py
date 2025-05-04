from library.solution import Solution
from library.algorithms.simulated_annealing import simulated_annealing
from musical_festival_lineup.musical_festival_solution import MusicalFestivalSolution, NUM_STAGES, NUM_SLOTS, REPR_ELEMENTS_LEN
import numpy as np
from musical_festival_lineup.musical_festival_data import MusicalFestivalData
from copy import deepcopy
import random
import numpy as np
import pandas as pd

class SAMFSolution(MusicalFestivalSolution):
    def get_random_neighbor(self):
        # Convert current representation into 2D list: [slot][stage]
        slot_repr = []
        for i in range(NUM_SLOTS):
            slot = []
            for j in range(NUM_STAGES):
                idx = (i * NUM_STAGES + j) * REPR_ELEMENTS_LEN
                artist_id = int(self.repr[idx:idx + REPR_ELEMENTS_LEN])
                slot.append(artist_id)
            slot_repr.append(slot)

        # Choose two random (stage, slot) pairs
        stage_1, slot_1 = random.randint(0, NUM_STAGES - 1), random.randint(0, NUM_SLOTS - 1)
        stage_2, slot_2 = random.randint(0, NUM_STAGES - 1), random.randint(0, NUM_SLOTS - 1)

        # Avoid swapping an artist with themselves
        while stage_1 == stage_2 and slot_1 == slot_2:
            stage_2, slot_2 = random.randint(0, NUM_STAGES - 1), random.randint(0, NUM_SLOTS - 1)

        # Swap artists
        slot_repr[slot_1][stage_1], slot_repr[slot_2][stage_2] = slot_repr[slot_2][stage_2], slot_repr[slot_1][stage_1]

        # Convert back to string
        new_repr = "".join(f"{artist_id:02d}" for slot in slot_repr for artist_id in slot)

        return SAMFSolution(data=self.data, repr=new_repr)