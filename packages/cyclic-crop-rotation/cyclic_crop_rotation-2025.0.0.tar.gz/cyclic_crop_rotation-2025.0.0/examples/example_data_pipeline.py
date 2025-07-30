import pandas as pd
from cyclic_crop_rotation import specific2normalize,get_valid_words,greedy_set_cover,post_selection,word2token,normalize2specific,diff_rotation

# Some sample aggirgate data
records = [(0,  5,  1,  5,  1,  5,  1,  5,  1, 9.19325509e+10),
(1,  1,  5,  1,  5,  1,  5,  1,  5, 9.09473389e+10),
(2,  1,  1,  1,  1,  1,  1,  1,  1, 2.27938006e+10),
(3, 24, 24, 24, 24, 24, 24, 24, 24, 2.13716493e+10),
(4, 61, 24, 61, 24, 61, 24, 61, 24, 1.09732086e+10),
(5, 24, 61, 24, 61, 24, 61, 24, 61, 1.06833173e+10),
(6, 37, 37, 37, 37, 37, 37, 37, 37, 9.15163183e+09),
(7,  2,  2,  2,  2,  2,  2,  2,  2, 8.37388390e+09),
(8, 36, 36, 36, 36, 36, 36, 36, 36, 8.13442332e+09),
(9,  0,  0,  0, 37, 37, 37, 37,  0, 7.11807795e+09)]
grp = [f'R{i}' for i in range(8)]
df = pd.DataFrame(records,columns =['idx']+grp+['Shape_Area'])
# Normalize data, this helps when the data is millions of rows
grp_norm = [f'N{i}' for i in range(8)]
df[grp_norm] = specific2normalize(df[grp],grp) #note this operation doesn't preserve index so the index must be ordered already
df_1 = df[grp_norm].drop_duplicates()
grp_rot = [f'NRot{i}' for i in range(8)]
grp_srot = [f'Rot{i}' for i in range(8)]
# Get tokens using the greedy algorithm, a max rotation size of three, and no repeats
df_1[grp_rot] = df_1.apply(lambda x: word2token(list(x[grp_norm]),post_selection(greedy_set_cover(get_valid_words(list(x[grp_norm]),repeat=False,max_syl=3)))),
                           axis=1,result_type='expand')
# Merge the token data with the original data
df_2 = pd.merge(df,df_1,on=grp_norm)
# Convert the general tokens into specific tokens
df_2[grp_srot] = normalize2specific(df_2,grp,grp_norm,grp_rot)
# Identify transition types
grp_trans = [f'T{i}' for i in range(1,len(grp))]
df_2[grp_trans] = df_2[grp_rot].apply(diff_rotation,axis=1,result_type='expand')
