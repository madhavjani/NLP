Spelling Correction:
In class project I looked at the problems of spelling error detection and correction. The problem was to write your own spelling corrector. I have implement a noisy channel model for spelling correction. In this I implemented a very simple error model, and three different language models for comparison.
 
Language Models:
1) Unigram Model:
Implemented a unigram language model with Laplace (add 1) smoothing. Treat any unknown word as a single word (e.g., UNK) which appears in the training data (corpus.txt) with frequency 0.5

2) Bigram Model
Implemented a bigram language model with Laplace smoothing. Again treat any unknown word as a single word (e.g., UNK) which appears in the training data with frequency 0.
Note that in Equation 1 we write P (w) for the language model. Really, though, we’re interested in the probability of the entire sentence, with w replacing x. For a bigram language model, a given word (token) only participates in two bigrams, one with the word before it and one with the word after it. To take this into consideration, compute P(w) as below:
P (w) ≈ P (w|wn−1) · P (wn+1|w) (2) where here w is the word at position n (i.e., wn).

3) Interpolated Model:
Implement a language model that interpolates a unigram and bigram language model: 
Pˆ(wn|wn−1) = (1 − λ)P(wn|wn−1) + λP(wn)
