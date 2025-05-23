from copy import deepcopy
from musical_festival_lineup.mf_lineup import NUM_SLOTS,NUM_STAGES
import random



def swap_mutation(representation, mut_prob):
    """
    Applies swap mutation to a solution representation with a given probability.

    Swap mutation randomly selects two different positions (genes) in the 
    representation and swaps their values. This operator is commonly used for 
    permutation-based representations but works for any list or string.

    The function preserves the type of the input representation: if the input is 
    a string, the output will also be a string; if it's a list, the output will 
    remain a list.

    Parameters:
        representation (str or list): The solution to mutate.
        mut_prob (float): The probability of performing the swap mutation.

    Returns:
        str or list: A new solution with two genes swapped, of the same type as the input.
    """

    new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        # Strings are not mutable. Let's convert temporarily to a list
        if isinstance(representation, str):
            new_representation = list(new_representation)

        first_idx = random.randint(0, len(representation) - 1)

        # To guarantee we select two different positions
        second_idx = first_idx
        while second_idx == first_idx:
            second_idx = random.randint(0, len(representation) - 1)

        new_representation[first_idx] = representation[second_idx]
        new_representation[second_idx] = representation[first_idx]

        # If representation was a string, convert list back to string
        if isinstance(representation, str):
            new_representation = "".join(new_representation)
    
    return new_representation

def swap_mutation_between_slots(representation, mut_prob, slot_size=5):
    new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        num_slots = len(representation) // slot_size
        idx1 = random.randint(0, len(representation) - 1)

        # Pick another artist from a different slot
        idx1_slot = idx1 // slot_size
        possible_idxs = [i for i in range(len(representation)) if i // slot_size != idx1_slot]
        idx2 = random.choice(possible_idxs)

        new_representation[idx1], new_representation[idx2] = new_representation[idx2], new_representation[idx1]

        if isinstance(representation, str):
            new_representation = "".join(new_representation)

    return new_representation


def insert_mutation(repr, mut_prob,verbose=False):
    if random.random()>mut_prob:
        if verbose:
            print("Mutation not happening.")
        return repr
    new_repr=deepcopy(repr)
    if isinstance(new_repr,str):
        new_repr=list(new_repr)
    idx_1, idx_2= sorted(random.sample(range(0,len(new_repr)-1),2))
    value=new_repr.pop(idx_1)
    new_repr.insert(idx_2, value)
    if isinstance(new_repr,str):
        new_repr="".join(new_repr)
    if verbose:
        print("Mutation happened.")
        print(f"Random indexes. Index to pop: {idx_1}. Index to get insertion {idx_2}")
        print(f"Removing value {value}")
    
    return new_repr

def inversion_mutation(representation: str | list, mut_prob):
    """
    Applies inversion mutation to a representation.

    Inversion mutation selects two random indices and reverses the 
    subsequence between them, with a certain probability.

    Parameters:
    ----------
    representation : str or list
        The individual to mutate. Should represent a valid permutation.
    mut_prob : float
        Probability of applying the mutation (between 0 and 1).

    Returns:
    -------
    str or list
        A new individual with the mutated representation (if mutation occurs),
        or a copy of the original.
    """
    if random.random() <= mut_prob:
        # Select two distinct indices
        first_idx = random.randint(0, len(representation)-1)
        second_idx = first_idx
        # We want to get two indexes that are at least 2 genes away 
        while abs(second_idx-first_idx) <= 1 :
            second_idx = random.randint(0, len(representation)-1)
    
        # Ensure first_idx < second_idx
        if first_idx > second_idx:
            first_idx, second_idx = second_idx, first_idx

        # Reverse between first and second index
        reversed_subsequence = list(reversed(representation[first_idx:second_idx]))
        # Convert back to string if original representation is a string
        if isinstance(representation, str):
            reversed_subsequence = "".join(reversed_subsequence)

        # Keep everything from second index (excluding it) until the end
        new_representation = representation[:first_idx] + reversed_subsequence + representation[second_idx:]
        return new_representation
    else:
        return deepcopy(representation)
    
