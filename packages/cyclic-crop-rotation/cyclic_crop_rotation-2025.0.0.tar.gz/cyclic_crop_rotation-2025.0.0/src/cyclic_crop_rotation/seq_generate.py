def _helper_all_seqs(seq):
    val = max(seq)+1
    return [seq+[i] for i in range(0,val+1)]

def all_seqs(seq_len):
    '''
    Generates all possible normalized sequences for a specified length. 
    Inputs
    ______
        seq_len: integer
    Outputs
    _______
        seqs: List of list, interior list is of normalized sequences. 
                size of list is bell's numbers, see https://oeis.org/A000110
    '''
    if seq_len>12: 
        a = [1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 678570, 4213597, 27644437, 190899322, 1382958545, 10480142147, 82864869804, 682076806159, 5832742205057, 51724158235372, 474869816156751, 4506715738447323, 44152005855084346, 445958869294805289, 4638590332229999353, 49631246523618756274]
        raise Warning(f'Computing a very large list with {a[seq_len]} elements. Consider generating a sample of sequences')
    seqs=[[0]]
    new_seqs = []
    for i in range(seq_len-1):
        for seq in seqs:
            new_seqs.extend(_helper_all_seqs(seq))
        seqs=new_seqs
        new_seqs=[]
    return seqs