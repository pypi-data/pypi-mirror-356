

def get_valid_words(seq,repeat=False,max_syl=3):
    '''
    For a given sequence/sentence, produces all of the valid words
    Valid words are constrained by:
    1. Having a single repeating syllable under the designated maximum
    2. Having a word size greater than the syllable length (or at least twice the syllable length if repeat is True)
    3. Not being contained within another word with a smaller syllable size
    Inputs
    ______
        seq: list of values
        repeat: syllables are required to repeat in their entirety
        max_syl: the maximum number of values a syllable can have
    Output
    ______
        A list of all valid words, as indicated by their starting, ending, syllable size, and length.
    '''
    words = []
    for syl_size in range(1,max_syl+1):
        syl_thresh = syl_size*2-1 if repeat else syl_size
        p_gen = iter(range(0,len(seq)-syl_size+1))
        while True:
            try:
                p_min = next(p_gen)
            except StopIteration:
                break
            for p in range(p_min,len(seq)):
                # If the positions are less than the syllable size, continue adding
                # Or if the word is still growing 
                if ((p-p_min<syl_size) and syl_size>1) or (seq[p]==seq[p_min+(p-p_min)%syl_size]):
                    p = p+1
                    continue
                # If the word is longer than the threshold length keep
                elif p-p_min>syl_thresh:
                    words.append((p_min,p,syl_size,p-p_min))
                break
            if (p==len(seq)) and ((p-p_min)>syl_thresh):
                words.append((p_min,p,syl_size,p-p_min))
    # Eliminate words with longer syllables which are contained within words with smaller syllables
    removes = set()
    for i in range(len(words)):
        # The word list is ordered in such a way that we don't have to check previous values.
        for j in range(i,len(words)):
            s1,e1,r1,l1 = words[i]    
            s2,e2,r2,l2 = words[j]
            if i!=j and r1<=r2 and s1<=s2 and e1>=e2:
                removes.add(j)
    words = [words[i] for i in set(range(0,len(words)))-removes]
    # Check to make sure that all positions are covered.
    pos_abs = set(range(len(seq)))-set(i for s,e,r,l in words for i in range(s,e))
    return words+[(p,p+1,1,1) for p in pos_abs]

def _idx_pos_dict(words):
    '''
    Helper function for set coverage algorithms.
    Input
    _____
        words: list of valid words
    Outputs
    _______
        idx_dict: {index of df: set of time positions}
        pos_dict: {time position: index}
        S: {time positions}
    '''
    idx_dict = {
        idx:set(range(val[0],val[1])) for idx,val in enumerate(words)
    }
    S = {j for i in idx_dict.values() for j in i}
    pos_dict = {s:[i for i in range(len(words)) if ((words[i][0]<=s) and (words[i][1]>s)) ] for s in S}
    return idx_dict,pos_dict,S

def _idxs_selector(idxs,words,start_pos=False):
    '''
    Inputs
    ______
        idxs: list of indexes which to look at in the dataframe
        words: list of words to consider
        start_pos: if the start position is used as the first tiebraker and then the smallest window size. 
    Outputs
    _______
        Returns the index value of the row of the data frame which is:
            1. is in idxs
            2. and has the smallest window size
            3. breaks ties using starting position.
    '''
    if start_pos:
        min_sp = min(words[i][0] for i in idxs)
        idxs = [i for i in idxs if words[i][0]==min_sp]
        if len(idxs)==1:
            return idxs[0]    
    min_syl = min(words[i][2] for i in idxs)
    idxs = [i for i in idxs if words[i][2]==min_syl]
    if len(idxs)==1:
        return idxs[0]
    # if that isn't sufficient, get the one with smallest start position
    min_sp = min(words[i][0] for i in idxs)
    idxs = [i for i in idxs if words[i][0]==min_sp]
    if len(idxs)==1:
        return idxs[0]    
    # This shouldn't ever happen if the words are generated through valid words. 
    raise NameError('Set Cover Indeterminant. Need Additional Condition')

def post_selection(words):
    '''
    Takes the set of selected words and processes them into the words which are used, eliminating words which are completely covered by two other words. 
    This will raise an error if there are indeterminate choices. 
    Inputs
    ______
        words: list of words
    Output
    ______
        list of words, a subset of the words in input list.
    '''
    idx_dict,pos_dict,S = _idx_pos_dict(words)
    idxs_final = []
    while S:
        s = min(S)
        idxs = pos_dict[s]
        if len(idxs)==1:
            idx = idxs[0]
        else:
            max_y = max(j for i in idxs for j in idx_dict[i]) 
            idxs = [i for i in idxs if max_y in idx_dict[i]]
            if len(idxs)==1:
                idx = idxs[0]
            else:
                raise NameError('Indeterminant Word Selection')
        S= S-idx_dict[idx]
        idxs_final.append(idx)
    return [words[i] for i in idxs_final]

def greedy_set_cover(words):
    '''
    Greedy set algorithm, selects the largest words first and continues till all positions are covered  
    Input
    _____
        words: list of valid words
    Output
    ______
        list of words, subset of the input
    '''
    idx_dict,pos_dict,S = _idx_pos_dict(words)
    chosen_words = []
    while S:
        max_len = max(len(S & v) for v in idx_dict.values())
        idxs = [i for i,v in idx_dict.items() if len(S & v)==max_len]
        if len(idxs)==1:
            idx = idxs[0]
        else:
            idx= _idxs_selector(idxs,words)            
        S = S-idx_dict[idx]
        chosen_words.append(idx)
    return [words[i] for i in chosen_words]

def first_observed_cover(words,last=False):
    '''
    First observed takes the first (or last) observered value and selects the largest covering word and repeats
    Inputs
    ______
        words: list of valid words
        last: if we use last observed value rather than the first observed values
    Output
    ______
        list of words, a subset of the input
    '''
    idx_dict,pos_dict,S = _idx_pos_dict(words)
    chosen_words = []
    while S:
        e = max(S) if last else min(S)
        dt = {idx:len(S & idx_dict[idx]) for idx in pos_dict[e]}
        max_len = max(dt.values())
        idxs = [i for i,v in dt.items() if v==max_len]
        if len(idxs)==1:
            idx=idxs[0] 
        else:
            idx = _idxs_selector(idxs,words)            
        S = S - idx_dict[idx]
        chosen_words.append(idx)
    return [words[i] for i in chosen_words]

def longest_repetition_cover(words):
    '''
    Selects words based on the largest ratio of word to syllable length.
    Inputs
    ______
        words: list of valid words
        last: if we use last observed value rather than the first observed values
    Output
    ______
        list of words, a subset of the input
    '''
    idx_dict,pos_dict,S = _idx_pos_dict(words)
    chosen_words = []
    while S:
        max_rep = max((len(S & v))/(words[k][2]) for k,v in idx_dict.items())
        idxs = [k for k,v in idx_dict.items() if len(S & v)/words[k][2]==max_rep]
        # If there is only one choice select that choice
        if len(idxs)==1:
            idx=idxs[0] 
        else:
            # If there is a tie, select the rotation with the largest element overall
            # get coverage for each idxs
            max_cov = max([words[i][3] for i in idxs])
            idxs = [i for i in idxs if words[i][3]==max_cov]
            if len(idxs)==1:
                idx = idxs[0]
            else:
                # default to the element that is the shortest rotation and first observed.
                idx = _idxs_selector(idxs,words)            
        S = S - idx_dict[idx]
        chosen_words.append(idx)
    return [words[i] for i in chosen_words]
