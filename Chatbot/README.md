In this project you will implement a corpus-based chatbot based on ideas from information retrieval and vector semantics. You will then analyze your chatbot’s behavior and discuss this in a report.

Chatbot Model:
Given a user turn (i.e., a “user query” as in 24.1 of the textbook), your chatbot will respond with the most similar line (i.e., response / system turn) in the Guteberg corpus (i.e., guteberg.txt). Represent the user turn, and all of the lines from the Guteberg corpus, using the vector-based approach to turn representation described below. Measure the similarity between the user turn and each of the lines from the Guteberg corpus using cosine similarity. Output the most similar line from the Guteberg corpus as the system turn.

Approaches to learning word embeddings, like word2vec and fastText, give us a vector for each word (type). One way to represent the meaning of a (short) document is to simply add together the vectors for the words in the document. In this approach it’s often helpful to normalize the length of the vectors before adding them.
For example, consider a text t with n tokens. Let vi be the embedding (vector) for the type corresponding to token i.

If a word (token) in the text does not have a corresponding vector, just ignore it in forming the representation of the text. If all words in the user query do not have a vector, and as such a vector representing this turn cannot be formed, then just output a default response (e.g., “I’m sorry?”, “I don’t understand”).
