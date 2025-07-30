import pandas as pd
from itertools import combinations
from cyclic_crop_rotation import all_seqs,get_valid_words,greedy_set_cover,first_observed_cover,longest_repetition_cover,post_selection,word2token,token2standardtoken,get_window_tokens

seq_len=8
grp_norm = [f'N{i:02}' for i in range(0,seq_len)]
# Gets a list of all possible general sequences
seq_ls = all_seqs(seq_len)
results = []
for i,seq in enumerate(seq_ls):
    dt = {}
    for max_syl in range(2,5):
        for repeat in [False,True]:
            # Get the valid words for the maximum syllable length and if repeats are required
            words = get_valid_words(seq,repeat=repeat,max_syl=max_syl)
            # Use those words as the basis for selecting based on one of the three algorithms
            # Then use the post selectiong process to eliminate words which are covered by other words, mostly a concern with the greedy and longest repetition algorithm
            # Then convert the words to a token representation.
            dt[('GR',max_syl,repeat)] = word2token(seq,post_selection(greedy_set_cover(words)))
            dt[('RP',max_syl,repeat)] = word2token(seq,post_selection(longest_repetition_cover(words)))
            dt[('FO',max_syl,repeat)] = word2token(seq,post_selection(first_observed_cover(words)))
            if repeat==False:
                # Windows don't have as complicated of a process. It is just one call.
                dt[('WI',max_syl,repeat)] = get_window_tokens(seq,max_syl)
    df = pd.DataFrame(dt).T
    df['idx'] = i
    df = df.set_index('idx',append=True)
    results.append(df)
# Run the token standardization on the entire collection
# Element handling in pandas makes this more efficient to do here
df = pd.concat(results).applymap(token2standardtoken)
# Comparing results of algorithms.
df_1 = df.unstack(level=[0,1,2])
for rot in range(2,5):
    for rep in [True,False]:
        same = pd.concat([
            (df_1.xs((a1,rot,rep),axiss=1,level=[1,2,3])==df_1.xs((a2,rot,rep),axis=1,level=[1,2,3])).all(axis=1)
            for a1,a2 in combinations(['FO','GR','RP'],2)],axis=1).all(axis=1).sum()
        print(f'{rot},{rep}: {same}')