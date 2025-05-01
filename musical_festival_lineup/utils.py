import pandas as pd  
from musical_festival_lineup.musical_festival_lineup import NUM_STAGES, NUM_SLOTS, REPR_ELEMENTS_LEN
from musical_festival_lineup.musical_festival_lineup import MusicalFestivalSolution

def visualize_musical_lineup(repr: list|str,artists_df):
    if isinstance(repr,str):
        repr=MusicalFestivalSolution._get_repr_list(repr)
    MusicalFestivalSolution._validate_repr(repr)
    lineup_list=[]
    idx_bound = NUM_STAGES
    for i in range(0, NUM_SLOTS ):
        row={"Slot": f"Slot {i+1}"}     
        for stage in range(NUM_STAGES):
            j = i * idx_bound + stage
            artist_id = repr[j]
            artist_name=artists_df.loc[artist_id, "name"]
            artist_genre=artists_df.loc[artist_id,"genre"]
            artist_popularity=artists_df.loc[artist_id,"popularity"]
            row[f"Stage {stage+1}"]=f"{artist_id}: {artist_name}|{artist_genre}|{artist_popularity}"
        lineup_list.append(row)
    df=pd.DataFrame(lineup_list)
    return df


# def visualize_musical_lineup(repr,artists_df):
#     lineup_list=[]
#     idx_bound = REPR_ELEMENTS_LEN *NUM_STAGES
#     for i in range(0, NUM_SLOTS ):
#         row={"Slot": f"Slot {i+1}"}     
#         for stage in range(NUM_STAGES):
#             j = i * idx_bound + stage*REPR_ELEMENTS_LEN
#             artist_id = int(repr[j:j + REPR_ELEMENTS_LEN])
#             artist_name=artists_df.loc[artist_id, "name"]
#             artist_genre=artists_df.loc[artist_id,"genre"]
#             artist_popularity=artists_df.loc[artist_id,"popularity"]
#             row[f"Stage {stage+1}"]=f"{artist_id}: {artist_name}|{artist_genre}|{artist_popularity}"
#         lineup_list.append(row)
#     df=pd.DataFrame(lineup_list)
#     return df
