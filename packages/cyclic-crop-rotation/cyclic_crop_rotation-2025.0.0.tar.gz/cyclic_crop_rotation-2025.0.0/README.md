Cyclic Crop Rotation
====================
Description
-----------
This package implements a method to calculate crop rotation labels from any given sequence.

Installation
------------
```pip install cyclic-crop-rotation```

Simple usage
------------
See example folder for more complex use cases.  

```python
from cyclic_crop_rotation import *

# Crop Sequence
seq = (1,  5,  1,  5,  5,  1,  5,  1)

# Valid words
words = get_valid_words(seq,repeat=False,max_syl=3)

# Select out of the valid words the ones to use
gr = post_selection(greedy_set_cover(words)) 
fo = post_selection(first_observed_cover(words)) 
lr = post_selection(longest_repetition_cover(words)) 

# Get rotation tokens
gr_tok = word2token(seq,gr)
fo_tok = word2token(seq,fo)
lr_tok = word2token(seq,lr)

print(seq)
# Print reordered tokens
print(f'Greedy:{[token2standardtoken(i) for i in gr_tok]}')
print(f'1st Obs:{[token2standardtoken(i) for i in fo_tok]}')
print(f'Long Rep:{[token2standardtoken(i) for i in lr_tok]}')
```
