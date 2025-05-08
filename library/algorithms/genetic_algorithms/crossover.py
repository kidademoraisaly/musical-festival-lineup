import random
from copy import deepcopy

ERX_SIZE=5

def standard_crossover(parent1_repr, parent2_repr):
    """
    Performs standard one-point crossover on two parent representations.

    This operator selects a random crossover point (not at the edges) and 
    exchanges the tail segments of the two parents to produce two offspring. 
    The crossover point is the same for both parents and ensures at least one 
    gene is inherited from each parent before and after the point.

    Parameters:
        parent1_repr (str or list): The first parent representation.
        parent2_repr (str or list): The second parent representation.
            Both parents must have the same length and type.

    Returns:
        tuple: A pair of offspring representations (offspring1, offspring2), 
        of the same type as the parents.

    Raises:
        ValueError: If parent representations are not the same length.
    """

    if not (isinstance(parent1_repr, list) or isinstance(parent1_repr, str)):
        raise ValueError("Parent 1 representation must be a list or a string")
    if not (isinstance(parent2_repr, list) or isinstance(parent2_repr, str)):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length")

    # Choose random crossover point
    xo_point = random.randint(1, len(parent1_repr) - 1)

    offspring1_repr = parent1_repr[:xo_point] + parent2_repr[xo_point:]
    offspring2_repr = parent2_repr[:xo_point] + parent1_repr[xo_point:]

    return offspring1_repr, offspring2_repr


def partial_crossover(parent1_repr, parent2_repr, verbose=False):
    if not (isinstance(parent1_repr, (list,str)) ):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length") 
    if verbose: 
        print(f"Parent 1 {parent1_repr}")
        print(f"Parent 2 {parent2_repr}")
    xo_point_1,xo_point_2=sorted(random.sample(range(1, len(parent1_repr)-1),2))
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
    
    xo_point_1,xo_point_2=sorted(random.sample(range(len(parent1_repr)),2))
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
    
    


def cycle_crossover(parent1_repr, parent2_repr,verbose=False):
    if not (isinstance(parent1_repr, (list,str)) ):
        raise ValueError("Parent 1 representation must be a list or a string")
    if len(parent1_repr) != len(parent2_repr):
        raise ValueError("Parent 1 and Parent 2 representations must be the same length") 
    if verbose: 
        print(f"Parent 1 {parent1_repr}")
        print(f"Parent 2 {parent2_repr}")
    
    def get_offspring(parent1, parent2):
        offspring=[None]*len(parent1)
        idx_of_current=0
        first_index=idx_of_current
        while True :
                offspring[idx_of_current]=parent1[idx_of_current] 
                if verbose:
                    print(f"index of current {idx_of_current}")
                    print(f"gene inserted {parent1[idx_of_current] }")
                    print(f"Current Offspring  {offspring}") 
                next_gene=parent2[idx_of_current]
                idx_of_current=parent1.index(next_gene)     
                if first_index==idx_of_current:
                    break          
        if verbose:
            print(f"--Offspring  before parent 2 filling {offspring}")
        offspring=[gene if gene is not None else parent2[i] for i, gene in enumerate(offspring)]       
        return offspring

    offspring_1=get_offspring(parent1_repr,parent2_repr)
    if verbose:
       print(f"--Offspring_1  Final {offspring_1}")
    offspring_2=get_offspring(parent2_repr,parent1_repr)
    if verbose:
       print(f"--Offspring_2  Final {offspring_2}")

    return offspring_1, offspring_2

    





def erx_with_grouped_neighbors(parent1_repr, parent2_repr,verbose=False):
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
        current_gene=parent[0]
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
            

    
  
    




