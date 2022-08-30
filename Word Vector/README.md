In this (short) project you will examine and interact with word vectors.

1)Polysemy and homonymy
Polysemy and homonymy are the phenomena of words having multiple meanings/senses. The nearest neighbours (under cosine similarity) for a given word can indicate whether it has multiple senses.

2) Synonyms and antonyms
Find three words (w1 , w2 , w3 ) such that w1 and w2 are synonyms (i.e., have roughly the same meaning), and w1 and w3 are antonyms (i.e., have opposite meanings), but the similarity between w1 and w3 > the similarity between w1 and w2. Note that this should be counter to your expectations, because synonyms (which mean roughly the same thing) would be expected to be more similar than antonyms (which have opposite meanings). Explain why you think this unexpected situation might have occurred.

3) Analogies
Analogies such as man is to king as woman is to X can be solved using word embeddings. This analogy can be expressed as X = woman + king − man. The following code snippet shows how to solve this analogy with gensim. Notice that the model gets it correct! I.e., queen is the most similar word.

4) Bias
Consider the examples below. The first shows the words that are most similar to man and worker and least similar to woman. The second shows the words that are most similar to woman and worker and least similar to man.
