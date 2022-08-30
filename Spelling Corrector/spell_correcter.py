import math
from decimal import Decimal

eps = 0.0001
interp_lambda = 0.001

class NGramModels:
    def __init__(self, fname):
        self.freqs = {}
        self.freqs2_bigram = {}

        for line in open(fname):
            tokens = line.split()
            for i,t in enumerate(tokens):
                self.freqs[t] = self.freqs.get(t, 0) + 1
                if i + 1 < len(tokens):
                    if (tokens[i], tokens[i + 1]) in self.freqs2_bigram:
                        self.freqs2_bigram[t + " " + tokens[i + 1]] = self.freqs2_bigram.get(t + " " + tokens[i + 1], 0) + 1
                    else:
                        self.freqs2_bigram[(tokens[i], tokens[i + 1])] = 1

        self.num_tokens = sum(self.freqs.values())
        self.types= len(self.freqs)

    def unigram_lm(self, word):
        if word in self.freqs:
            return math.log(self.freqs[word] + 1) - math.log(self.num_tokens + self.types)
        else:
            return float("-inf")

    def bigram_lm(self, word, left_word, right_word):
        if left_word and right_word:
            if word in self.freqs2_bigram:
                word_total = self.freqs2_bigram[word]
            else:
                word_total = 0
            if left_word in self.freqs2_bigram:
                left_total = self.freqs2_bigram[left_word]
            else:
                left_total = 0
            if right_word in self.freqs:
                right_total = self.freqs[right_word]
            else:
                right_total=0
            return  (math.log(word_total + 1) - math.log(right_total + self.types)) + (math.log(left_total + 1) - math.log(right_total + self.types))
        else:
            if word in self.freqs2_bigram:
                word_total = self.freqs2_bigram[word]
            else:
                word_total=0
            if word[1] in self.freqs:
                right_total = self.freqs[word[1]]
            else:
                right_total = 0
            return math.log(word_total + 1) - math.log(right_total + self.types)

    def interpolate_lm(self, word, left_word, right_word):
        if left_word and right_word:
            if word in self.freqs2_bigram:
                word_total = self.freqs2_bigram[word]
            else:
                word_total = 0
            if left_word in self.freqs2_bigram:
                left_total = self.freqs2_bigram[left_word]
            else:
                left_total = 0
            if right_word in self.freqs:
                right_total = self.freqs[right_word]
            else:
                right_total = 0

            if left_word[1] in self.freqs:
                left_word_total = self.freqs[left_word[1]]
            else:
                left_word_total = 0

            uni1 = (left_word_total + 1) / (self.num_tokens + self.types)
            uni2 = (right_total + 1) / (self.num_tokens + self.types)
            bigram1 = left_total / right_total
            bigram2 = word_total / right_total

            return Decimal((((1 - interp_lambda) * bigram2) + (interp_lambda * uni2)) * (((1 - interp_lambda) * bigram1) + (interp_lambda * uni1)))
        else:
            if word in self.freqs2_bigram:
                word_total = self.freqs2_bigram[word]
            else:
                word_total = 0
            if word[1] in self.freqs:
                right_total = self.freqs[word[1]]
            else:
                right_total = 0
            return Decimal((word_total + 1) / (right_total + self.types))

    def in_vocab(self, word):
        if word not in self.freqs:
            self.freqs["UNK"] = 0
        return word in self.freqs

    def check_probs(self):
        for w in self.freqs:
            assert 0 - eps < math.exp(self.unigram_lm(w)) < 1 + eps
        assert 1 - eps < \
            sum([math.exp(self.unigram_lm(w)) for w in self.freqs]) < \
            1 + eps

def delete_edits(w):
    range_letters = 'abcdefghijklmnopqrstuvwxyz'
    split = [(w[:i], w[i:]) for i in range(len(w) + 1)]
    inserts = [left + center + right for left, right in split for center in range_letters]
    deletes = [left + right[1:] for left, right in split if right]
    transposition = [left + right[1] + right[0] + right[2:] for left, right in split if len(right) > 1]
    substitute = [left + center + right[1:] for left, right in split if right for center in range_letters]
    return set(inserts + deletes + transposition + substitute)


if __name__ == '__main__':
    import sys
    train_corpus = 'corpus.txt'
    n = sys.argv[1]
    predict_corpus = sys.argv[2]
    lm = NGramModels(train_corpus)
    lm.check_probs()

    for line in open(predict_corpus):
        target_index,sentence = line.split('\t')
        target_index = int(target_index)
        sentence = sentence.split()
        target_word = sentence[target_index]
        previous_word = sentence[target_index - 1]
        left_word = sentence[target_index + 1]
        candidates = delete_edits(target_word)
        iv_candidates = [c for c in candidates if lm.in_vocab(c)]
        best_prob = float("-inf")
        best_correction = target_word
        
        for ivc in iv_candidates:
            if n=="1":
                ivc_log_prob = lm.unigram_lm(ivc)

            elif n=="2":
                left = (previous_word, ivc)
                right = (ivc, left_word)
                ivc_log_prob = lm.bigram_lm(left, right, ivc)

            elif n == "interp":
                left = (previous_word, ivc)
                right = (ivc, left_word)
                ivc_log_prob = lm.interpolate_lm(left, right, ivc)

            if ivc_log_prob > best_prob:
                best_prob = ivc_log_prob
                best_correction = ivc

        print(best_correction)
