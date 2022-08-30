import sys

fname = sys.argv[1]
word_freq = {}

with open(fname) as infile:
    for word in infile:
        word = word.lower()
        word_freq[word]= word_freq.get(word,0) + 1
for word in sorted(word_freq, key=lambda x : word_freq[x], reverse=True):
    print(word_freq[word], word, end=" ")