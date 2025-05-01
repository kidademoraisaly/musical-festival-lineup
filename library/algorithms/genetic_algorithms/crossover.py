import random

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
    if verbose:
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





    

