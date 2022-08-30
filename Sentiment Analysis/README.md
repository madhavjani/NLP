In this project you will write your own sentiment analysis system. You will implement an unsupervised lexicon-based method and two variants of a naive Bayes classifier. You will then compare the various approaches

Models:
Sentiment Lexicon Baseline
A simple baseline approach is to use a polarity lexicon (i.e., the lists of positive and negative words you’ve been provided with) to determine the number of positive and negative tokens in a test document, and then output the class label associated with the most tokens. In the event of a tie, select the neutral class. Note that this approach ignores the training data.

Naive Bayes
Implement multinomial naive Bayes, i.e., as described in 4.1–4.3 of the text book.

Naive Bayes with Binary Features
Also implement multinomial naive Bayes with binary features. Recall that in this model, the frequency of a given word in a given document is either 0 (if the word does not occur in the document) or 1 (if the word occurs 1 or more times in the document). Repeated occurrences of a word are ignored. (Implementing this model should only require a very small change to your previous implementation of naive Bayes.) This model is discussed in 4.4 of the text book.



