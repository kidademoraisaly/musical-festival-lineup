import random
from copy import deepcopy
from musical_festival_lineup.mf_lineup import NUM_SLOTS,NUM_STAGES

ERX_SIZE=5

def partial_crossover(parent1_repr, parent2_repr, verbose=False):
    if not (isinstance(parent1_repr, (list,str)) ):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length") 
    if verbose: 
        print(f"Parent 1 {parent1_repr}")
        print(f"Parent 2 {parent2_repr}")
    #xo_point_1,xo_point_2=sorted(random.sample(range(1, len(parent1_repr)-1),2))
    xo_point_1,xo_point_2=sorted(random.sample(range(0, len(parent1_repr)-1),2))
    if verbose:
        print(f"Crossover point1 {xo_point_1} e crossover point2 {xo_point_2}")

    segment_1=parent1_repr[xo_point_1:xo_point_2]
    segment_2=parent2_repr[xo_point_1:xo_point_2]

    maps_1=dict(zip(segment_1,segment_2))
    maps_2=dict(zip(segment_2,segment_1))
    
    if verbose:
        print(f"OffSpring 1: segment {segment_1} maps {maps_1}")
        print(f"OffSpring 2: segment {segment_2} maps {maps_2}")
    
    def get_maps(segment, source,maps):
        new_seg=[]
        for value in source:
            while value in  segment:
                value=maps[value]
            new_seg.append(value)
        return new_seg
    
    head_1=get_maps(segment_1,parent2_repr[:xo_point_1], maps_1)
    head_2=get_maps(segment_2, parent1_repr[:xo_point_1] , maps_2)
    tail_1=get_maps(segment_1, parent2_repr[xo_point_2:], maps_1)
    tail_2=get_maps(segment_2, parent1_repr[xo_point_2:],maps_2)
  
    if verbose:
        print(f"OffSpring 1: head {head_1} | segment {segment_1} | tail  {tail_1}")
        print(f"OffSpring 2: head {head_2} | segment {segment_2} | tail  {tail_2}")
    
    offspring_1=head_1+segment_1+tail_1
    offspring_2=head_2+segment_2+tail_2
    
    assert sorted(parent1_repr)==sorted(offspring_1)
    assert sorted(parent1_repr)==sorted(offspring_2)
    
    return offspring_1,offspring_2

def order_crossover(parent1_repr, parent2_repr,verbose=False):
    if not (isinstance(parent1_repr, (list,str)) ):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length") 
    if verbose: 
        print(f"Parent 1 {parent1_repr}")
        print(f"Parent 2 {parent2_repr}")
    
    #xo_point_1,xo_point_2=sorted(random.sample(range(len(parent1_repr)),2))
    xo_point_1,xo_point_2=sorted(random.sample(range(0, len(parent1_repr)-1),2))
    if verbose:
        print(f"Cross over point_1 {xo_point_1}, point_2 {xo_point_2}")
    
    def get_offspring(parent1, parent2):
        offspring=[None]*len(parent1)
        parent2=parent2[xo_point_2:]+parent2[:xo_point_2]
        segment=parent1[xo_point_1:xo_point_2]
        offspring[xo_point_1:xo_point_2]=segment
        if verbose:
            print(f"Segment {segment}")
            print(f"Parent 2 for xo point_2: {parent2}")
        parent2=[gene for gene in parent2 if gene not in segment]
        parent2_pos=0
        if verbose:
            print(f"Parent 2 with_out genes from segment: {parent2}")
        for  i in range(len(offspring)):
            if offspring[i] is  None:
                offspring[i]=parent2[parent2_pos]
                parent2_pos+=1
        if verbose:
            print(f"Final offspring::{offspring}")
        return offspring
    
    offspring_1=get_offspring(parent1_repr,parent2_repr)
    offspring_2=get_offspring(parent2_repr,parent1_repr)
    return offspring_1,offspring_2
    

def cycle_crossover(parent1_repr: str | list, parent2_repr: str | list, verbose=False):
    """
    Performs Cycle Crossover (CX) between two parents

    Cycle Crossover preserves the position of elements by identifying a cycle
    of indices where the values from each parent will be inherited by each offspring.
    The remaining indices are filled with values from the other parent, maintaining valid permutations.

    Args:
        parent1_repr (str or list): The first parent representation.
        parent2_repr (str or list): The second parent representation.
            Both parents must have the same length and type.

    Returns:
        tuple: Two offspring permutations resulting from the crossover.
    """
    # Randomly choose a starting index for the cycle
    initial_random_idx = random.randint(0, len(parent1_repr)-1)

    # Initialize the cycle with the starting index
    cycle_idxs = [initial_random_idx]
    current_cycle_idx = initial_random_idx

    # Traverse the cycle by following the mapping from parent2 to parent1
    while True:
        value_parent2 = parent2_repr[current_cycle_idx]
        # Find where this value is in parent1 to get the next index in the cycle
        next_cycle_idx = parent1_repr.index(value_parent2)

        # Closed the cycle -> Break
        if next_cycle_idx == initial_random_idx:
            break

        cycle_idxs.append(next_cycle_idx)
        current_cycle_idx = next_cycle_idx
    
    offspring1_repr = []
    offspring2_repr = []
    for idx in range(len(parent1_repr)):
        if idx in cycle_idxs:
            # Keep values from parent1 in offspring1 in the cycle indexes
            offspring1_repr.append(parent1_repr[idx])
            # Keep values from parent2 in offspring2 in the cycle indexes
            offspring2_repr.append(parent2_repr[idx])
        else:
            # Swap elements from parents in non-cycle indexes
            offspring1_repr.append(parent2_repr[idx])
            offspring2_repr.append(parent1_repr[idx])

    # To keep the same type as the parents representation
    if isinstance(parent1_repr, str) and isinstance(parent2_repr, str):
        offspring1_repr = "".join(offspring1_repr)
        offspring2_repr = "".join(offspring2_repr)

    return offspring1_repr, offspring2_repr


# Edge recombination slotwise adaptation
def edge_recomb_xo_slotwise(parent1_repr, parent2_repr,verbose=False):
    if not (isinstance(parent1_repr, (list,str)) ):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length")    
    if verbose: 
        print(f"Parent 1 {parent1_repr}")
        print(f"Parent 2 {parent2_repr}")

    def group_elements_size(p):
        return [ p[i:i+ERX_SIZE] for i in range(0,len(p),ERX_SIZE)]
    
    group_p1=group_elements_size(parent1_repr)
    group_p2=group_elements_size(parent2_repr)
    
    if verbose:
        print(f"Elements of parent 1 grouped {group_p1}")
        print(f"Elements of parent 2 grouped {group_p2}")

    def get_group_neighbors(idx,gene):
        idx_group_1=idx//ERX_SIZE
        idx_group_2=parent2_repr.index(gene)//ERX_SIZE
        neighbors=set(group_p1[idx_group_1]+group_p2[idx_group_2])
        return {i for i in neighbors if i !=gene}    
    
    def build_edge_table():
        edge_table={}
        for idx,gene in enumerate(parent1_repr):
            edge_table[gene]=get_group_neighbors(idx,gene)
        return edge_table
    
    edge_table=build_edge_table()
    if verbose:
        print(f"Edge table : {edge_table}")
    
    def build_child(parent):
        off_spring=[]
        idx_of_current=random.randint(0, len(parent1_repr)-1)
        current_gene=parent[idx_of_current]
        current_edge_table=deepcopy(edge_table)
        while len(off_spring)<len(parent):
            if verbose:
                print("========Starting the generation of next gene====")
                print(f"Adding  {current_gene} to the offspring and removing it from the edge table ")
            off_spring.append(current_gene)
            for values in current_edge_table.values():
                values.discard(current_gene)
            
            if verbose:
                print(f"Current Edge table {current_edge_table}")

            neighbors_current_gene=current_edge_table[current_gene]
            if neighbors_current_gene:
                min_len_of_neigh=min(len(current_edge_table[n]) for n in neighbors_current_gene)
                next_current_gene_list=[n for n in neighbors_current_gene if len(current_edge_table[n])==min_len_of_neigh]
                if verbose:
                    print(f"Min len: {min_len_of_neigh}")
                    print(f"Current gene neighbors {next_current_gene_list}")
                   
                
            else:
                next_current_gene_list= [gene for gene in parent if gene not in off_spring]
            if next_current_gene_list:
                current_gene=random.choice(next_current_gene_list)
            if verbose:
                print(f"Random picked {current_gene}")
                print(f"Offspring {off_spring}")

        return off_spring
    
    offspring_1=build_child(parent=parent1_repr)
    offspring_2=build_child(parent=parent2_repr)
    if verbose:
        print(f"Offspring 1 {offspring_1}")
        print(f"Offspring 2 {offspring_2}")
    return offspring_1, offspring_2

  
def edge_recomb_xo(parent1, parent2, verbose=False):
    if not isinstance(parent1, (list, str)):
        raise ValueError("Parent 1 must be a list or a string.")
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be the same length.")
    
    # 1. Build the edge table
    def build_edge_table(p1, p2):
        edge_table = {}
        size = len(p1)
        for i in range(size):
            gene = p1[i]
            neighbors = set()
            neighbors.update([p1[(i-1)%size], p1[(i+1)%size]])
            idx_p2 = p2.index(gene)
            neighbors.update([p2[(idx_p2-1)%size], p2[(idx_p2+1)%size]])
            edge_table[gene] = neighbors
        return edge_table

    edge_table = build_edge_table(parent1, parent2)
    if verbose:
        print("Initial Edge Table:")
        for gene, neighbors in edge_table.items():
            print(f"{gene}: {neighbors}")

    # 2. Build offspring
    def build_offspring(start_gene):
        offspring = []
        current_gene = start_gene
        current_edge_table = deepcopy(edge_table)
        while len(offspring) < len(parent1):
            offspring.append(current_gene)
            # Remove current gene from all neighbor lists
            for neighbors in current_edge_table.values():
                neighbors.discard(current_gene)
            if verbose:
                print(f"Added {current_gene}, updated edge table:")
                for gene, neighbors in current_edge_table.items():
                    print(f"{gene}: {neighbors}")

            # Get neighbors of current gene
            neighbors_current = current_edge_table[current_gene]
            del current_edge_table[current_gene]

            # Choose next gene
            if neighbors_current:
                # Select neighbor with fewest neighbors itself (tie-break randomly)
                min_neighbor_count = min(len(current_edge_table[n]) for n in neighbors_current)
                candidates = [n for n in neighbors_current if len(current_edge_table[n]) == min_neighbor_count]
                current_gene = random.choice(candidates)
            else:
                # No neighbors left — pick random from remaining genes
                remaining_genes = list(current_edge_table.keys())
                if remaining_genes:
                    current_gene = random.choice(remaining_genes)

        return offspring

    # Pick random starting gene for each offspring
    offspring1 = build_offspring(random.choice(parent1))
    offspring2 = build_offspring(random.choice(parent2))

    return offspring1, offspring2

    

def partial_crossover_slotwise(parent1_repr, parent2_repr, verbose=False):
    if not (isinstance(parent1_repr, (list,str)) ):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length") 
    if verbose: 
        print(f"Parent 1 {parent1_repr}")
        print(f"Parent 2 {parent2_repr}")
     # Only pick crossover points at slot boundaries
    slot_boundaries = [i for i in range(0, len(parent1_repr) + 1, NUM_STAGES)]
    xo_point_1, xo_point_2 = sorted(random.sample(slot_boundaries, 2))

    if verbose:
        print(f"Crossover point1 {xo_point_1} e crossover point2 {xo_point_2}")

    segment_1=parent1_repr[xo_point_1:xo_point_2]
    segment_2=parent2_repr[xo_point_1:xo_point_2]

    maps_1=dict(zip(segment_1,segment_2))
    maps_2=dict(zip(segment_2,segment_1))
    
    if verbose:
        print(f"OffSpring 1: segment {segment_1} maps {maps_1}")
        print(f"OffSpring 2: segment {segment_2} maps {maps_2}")
    
    def get_maps(segment, source,maps):
        new_seg=[]
        for value in source:
            while value in  segment:
                value=maps[value]
            new_seg.append(value)
        return new_seg
    
    head_1=get_maps(segment_1,parent2_repr[:xo_point_1], maps_1)
    head_2=get_maps(segment_2, parent1_repr[:xo_point_1] , maps_2)
    tail_1=get_maps(segment_1, parent2_repr[xo_point_2:], maps_1)
    tail_2=get_maps(segment_2, parent1_repr[xo_point_2:],maps_2)
  
    if verbose:
        print(f"OffSpring 1: head {head_1} | segment {segment_1} | tail  {tail_1}")
        print(f"OffSpring 2: head {head_2} | segment {segment_2} | tail  {tail_2}")
    
    offspring_1=head_1+segment_1+tail_1
    offspring_2=head_2+segment_2+tail_2
    
    assert sorted(parent1_repr)==sorted(offspring_1)
    assert sorted(parent1_repr)==sorted(offspring_2)
    
    return offspring_1,offspring_2



def rand_choice_crossover(parent1_repr, parent2_repr, verbose=False):
    """
    Randomly selects a crossover function (excluding standard_crossover)
    and applies it to the given parent representations.
    
    Parameters:
        parent1_repr (list or str): First parent.
        parent2_repr (list or str): Second parent.
        verbose (bool): If True, prints internal details of the chosen crossover.

    Returns:
        tuple: A pair of offspring representations.
    """
    crossover_funcs = [
        partial_crossover_slotwise,
        edge_recomb_xo_slotwise,
        cycle_crossover,
    ]

    chosen_crossover = random.choice(crossover_funcs)
    if verbose:
        print(f"Chosen crossover: {chosen_crossover.__name__}")

    offspring1, offspring2 = chosen_crossover(parent1_repr, parent2_repr, verbose=verbose)
    return offspring1, offspring2


    
