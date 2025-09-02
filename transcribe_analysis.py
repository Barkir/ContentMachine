# This is a file where we will analyze transcribed data

import nltk
from nltk.corpus import treebank


lines = "".join(open("posts/5ada3554-04d3-483d-b0ce-3b33351643bd.post").readlines())
tokens = nltk.word_tokenize(lines)
tagged = nltk.pos_tag(tokens)
print(tagged)