from functools import reduce
import pandas as pd

def _factors(n):
    '''
    Returns the factors of n
    '''
    # From https://stackoverflow.com/a/6800214     
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
def is_constant_rotation_of_n(df,grp,n):
    '''
    Determines if the crop sequence is a constant rotation of length n.
    This accounts for the factors of n, eliminating rotations which are smaller
        e.g. ABABABAB is not a 4 year rotation
    Inputs
    ______
        df: Dataframe with sequences of interest
        grp: the group of column names corresponding to the sequences
        max_syl: the maximum syllable size
    Output
    ______
        Pandas Series with T/F values if the each sequence is a constant rotation. 
    '''
    results = []
    for i in range(n):
        for j in range(n+i,len(grp),n):
            results.append(df[grp[i]]==df[grp[j]])
    df_s = pd.concat(results,axis=1).all(axis=1)
    for f in _factors(n)-{n}:
        results = []
        for i in range(f):
            for j in range(f+i,len(grp),f):
                results.append(df[grp[i]]==df[grp[j]])
        df_j = pd.concat(results,axis=1).all(axis=1)     
        df_s = (df_s) & (df_j==False)
    return df_s
def is_constant_rotation(df,grp,max_rot=3):
    '''
    Determines if the crop sequence is a constant rotation.
    Inputs
    ______
        df: Dataframe with sequences of interest
        grp: the group of column names corresponding to the sequences
        max_syl: the maximum syllable size
    Output
    ______
        Pandas Series with T/F values if the each sequence is a constant rotation. 
    '''
    results = []
    for n in range(1,max_rot+1):
        results.append(pd.concat([df[grp[i]]==df[grp[j]] 
                    for i in range(n)
                    for j in range(n+i,len(grp),n)],
                axis=1
            ).all(axis=1))
    return pd.concat(results,axis=1).any(axis=1)

def is_partially_ordered(df,grp,max_syl=3):
    '''
    Determines if sequence is partially ordered given a specific rotation length. 
    For example, if 0,1,1,2,0 and the max rotation is 3 it is partially ordered, if 4 it is not.
    Inputs
    ______
        df: Dataframe with sequences of interest
        grp: the group of column names corresponding to the sequences
        max_syl: the maximum syllable size
    Output
    ______
        Pandas Series with T/F values if the each sequence is partially ordered or not. 
    '''
    # Generate test conditions
    results = []
    for i in range(2,len(grp)):
        pre = grp[i-1]
        dif = grp[max(0,i-max_syl):i-1]
        results.append(
            pd.concat(
                [df[pre]==df[grp[i]],
                    pd.concat([(df[d]!=df[grp[i]]) for d in dif],axis=1).all(axis=1)],
                axis=1
            ).any(axis=1)
        )
    return pd.concat(results,axis=1).all(axis=1)

def diff_rotation(seq,tf=False):
    '''
    If the rotations are different returns the type of transition
    Inputs
    ______
        seq: the sequence of interest
        tf: If True, returns a Boolean rather than string types
    Outputs
    _______
        List, one length shorter than seq containing
        If tf==False:
            'Kept': The rotation is kept
            'Same': The rotation is offset between years ((0,1),0) transitions to ((0,1),0)
            'SameCrop': If the set of crops in the new rotation are a subset of the crops in the old rotation
            'SomeCrop': If the set of crops in the new rotation intersect with the crops in the old rotation
            'NewCrop': If the set of crops in the new rotation are disjoint from the crops in the old rotation
        If tf==True:
            True: The rotation is kept without any offsets
            False: The rotation has a transition.
    '''
    if tf:
        return [True if ((a[0],(a[1]+1)%(len(a[0])))==b) else False for a,b in zip(seq[:-1],seq[1:])]    
    returns = []
    for a,b in zip(seq[:-1],seq[1:]):
        # Keep the same rotation
        if (a[0],(a[1]+1)%(len(a[0])))==b:
            returns.append('Kept')
        # Keep the same rotation but shift it
        elif a[0]==b[0]:
            returns.append('Same')
        # If all the same crops are used
        elif set(b[0])<=set(a[0]):
            returns.append('SameCrop')
        # If there is overlap in the crops
        elif set(b[0])&set(a[0]):
            returns.append('SomeCrop')
        # If there are only new crops
        else:
            returns.append('NewCrop')
    return returns