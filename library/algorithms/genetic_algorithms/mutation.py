from copy import deepcopy
import random

def binary_standard_mutation(representation: str | list, mut_prob):
    """
    Applies standard binary mutation to a binary string or list representation.

    This function supports both binary strings (e.g., "10101") and binary lists 
    (e.g., [1, 0, 1, 0, 1]) containing either string characters ("0", "1") or 
    integers (0, 1). Each gene in the representation is independently flipped 
    with a given mutation probability, while preserving the original data type 
    of the genes.

    The function preserves the type of the input representation: if the input is 
    a string, the output will also be a string; if it's a list, the output will 
    remain a list.

    Parameters:
        representation (str or list): The binary representation to mutate.
        mut_prob (float): The probability of flipping each gene.

    Returns:
        str or list: A new mutated representation of the same type as the input.

    Raises:
        ValueError: If the input contains elements other than 0, 1, "0", or "1".
    """

    # Initialize new representation as a copy of current representation
    new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        # Strings are not mutable. Let's convert temporarily to a list
        if isinstance(representation, str):
            new_representation = list(new_representation)

        for char_ix, char in enumerate(representation):
            if char == "1":
                new_representation[char_ix] = "0"
            elif char == 1:
                new_representation[char_ix] = 0
            elif char == "0":
                new_representation[char_ix] = "1"
            elif char == 0:
                new_representation[char_ix] = 1
            else:
                raise ValueError(f"Invalid character {char}. Can not apply binary standard mutation")
    
        # If representation was a string, convert list back to string
        if isinstance(representation, str):
            new_representation = "".join(new_representation)

    return new_representation


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

def reverse_mutation(repr, mut_prob, verbose=False):
    if random.random()>mut_prob:
        if verbose:
            print("Mutation not happening.")
        return repr
    
    new_repr=deepcopy(repr)
    
    if isinstance(new_repr,str):
        new_repr=list(new_repr)
    idx_1,idx_2=sorted(random.sample(range(0,len(new_repr)-1),2))
    to_reverse=new_repr[idx_1:idx_2]
    new_repr[idx_1:idx_2]=reversed(to_reverse)

    if verbose:
        print("Mutation happened.")
        print(f"Random indexes. Reverse from idx: {idx_1} to {idx_2}")
        print(f"List to reverse {to_reverse}")
        print(f"Reversed {new_repr[idx_1:idx_2]}")      
    if isinstance(new_repr,str):
        new_repr="".join(new_repr)
    if verbose:
        print(f"New Repr {new_repr}")     
    return new_repr
    
def rand_choice_mutation(repr, mut_prob, verbose=False):
    if random.random()>mut_prob:
        if verbose:
            print("Mutation not happening.")
        return repr
    new_repr=deepcopy(repr)
    if isinstance(new_repr,list):
        new_repr=list(new_repr)
    mut_type=random.choice(["swap","insert","reverse"])
    if verbose:
        print("Mutation happened.")
        print(f"Selected mutation is {mut_type}")
    if mut_type=="swap":
        new_repr=swap_mutation(new_repr, mut_prob=1)
    elif mut_type=="insert":
        new_repr=insert_mutation(new_repr,mut_prob=1,verbose=verbose)
    elif mut_type=="reverse":
        new_repr=reverse_mutation(new_repr,mut_prob=1,verbose=verbose)

    if isinstance(new_repr,str):
        new_repr="".join(new_repr)     
    if verbose:
        print(f"The new representation after mutation is {new_repr}")
    return new_repr
    
    



