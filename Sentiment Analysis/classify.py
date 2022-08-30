import math, re
# A simple tokenizer. Applies case folding
def tokenize(s):
    tokens = s.lower().split()
    trimmed_tokens = []
    for t in tokens:
        if re.search('\w', t):
            # t contains at least 1 alphanumeric character
            t = re.sub('^\W*', '', t)  # trim leading non-alphanumeric chars
            t = re.sub('\W*$', '', t)  # trim trailing non-alphanumeric chars
        trimmed_tokens.append(t)
    return trimmed_tokens

class Baseline:
    def __init__(self, klasses):
        self.train(klasses)

    def train(self, klasses):
        klass_freqs = {}
        for k in klasses:
            klass_freqs[k] = klass_freqs.get(k, 0) + 1
        self.mfc = sorted(klass_freqs, reverse=True,
                          key=lambda x: klass_freqs[x])[0]

    def classify(self, test_instance):
        return self.mfc

class Lexicon:
    def __init__(self, klasses):
        self.klass_freqs = {}
        self.train(klasses)

    def train(self, klasses):
        with open("pos-words.txt", encoding='utf-8') as file:
            for f in file:
                self.klass_freqs[f.strip()] = 1

        with open("neg-words.txt", encoding='utf-8') as file:
            for f in file:
                self.klass_freqs[f.strip()] = 0

    def classify(self, test_instance):
        positive_cnt,negative_cnt,neutral_cnt = 0,0,0
        tokens = tokenize(test_instance)
        for t in tokens:
            polarity = self.klass_freqs.get(t, -1)
            if polarity == 1:
                positive_cnt += 1
            elif polarity == 0:
                negative_cnt += 1
            else:
                neutral_cnt += 1

        if positive_cnt > negative_cnt:
            return "positive"
        elif positive_cnt < negative_cnt:
            return "negative"
        else:
            return "neutral"



class NaiveBayes:
    def __init__(self,train_texts,train_klasses):
        self.positive_doc, self.negative_doc, self.neutral_doc = 0,0,0
        self.positive_prior,self.negative_prior,self.neutral_prior = 0,0,0

        self.positive_class_cnt = {}
        self.negative_class_cnt = {}
        self.neutral_class_cnt = {}
        self.total_vocab = {}

        self.train(train_texts,train_klasses)

    def train(self,train_texts,train_klasses):

        for klasses in train_klasses:
            if klasses == "positive":
                self.positive_doc += 1
            elif klasses == "negative":
                self.negative_doc += 1
            else:
                self.neutral_doc += 1

        self.positive_prior = math.log(self.positive_doc) - (math.log(self.positive_doc + self.negative_doc + self.neutral_doc))
        self.negative_prior = math.log(self.negative_doc) - (math.log(self.positive_doc + self.negative_doc + self.neutral_doc))
        self.neutral_prior = math.log(self.neutral_doc) - (math.log(self.positive_doc + self.negative_doc + self.neutral_doc))

        for k in range(len(train_klasses)):
            tokens=tokenize(train_texts[k])
            for t in tokens:
                if train_klasses[k] == "positive":
                    self.positive_class_cnt[t] = self.positive_class_cnt.get(t,0) + 1
                elif train_klasses[k] == "negative":
                    self.negative_class_cnt[t] = self.negative_class_cnt.get(t,0) + 1
                else:
                    self.neutral_class_cnt[t] = self.neutral_class_cnt.get(t,0) + 1

            for t in tokens:
                self.total_vocab[t]=self.total_vocab.get(t,0) + 1


    def classify(self,test_klasses):
        tokens=tokenize(test_klasses)
        positive_prob, negative_prob, neutral_prob = 0,0,0

        for t in tokens:

            positive_prob=math.log((self.positive_class_cnt.get(t,0)+1)) - math.log(sum(self.positive_class_cnt.values()) + len(self.total_vocab))
            negative_prob=math.log((self.negative_class_cnt.get(t,0)+1)) - math.log(sum(self.negative_class_cnt.values()) + len(self.total_vocab))
            neutral_prob=math.log((self.neutral_class_cnt.get(t,0)+1)) - math.log(sum(self.neutral_class_cnt.values()) + len(self.total_vocab))


        if positive_prob > negative_prob:
            return "positive"
        elif positive_prob < negative_prob:
            return "negative"
        else:
            return "neutral"


class BinaryNaiveBayes:
    def __init__(self,train_texts,train_klasses):
        self.positive_doc, self.negative_doc, self.neutral_doc = 0,0,0
        self.positive_prior,self.negative_prior,self.neutral_prior = 0,0,0

        self.positive_class_cnt = {}
        self.negative_class_cnt = {}
        self.neutral_class_cnt = {}
        self.total_vocab = {}

        self.train(train_texts,train_klasses)

    def train(self,train_texts,train_klasses):

        for klasses in train_klasses:
            if klasses == "positive":
                self.positive_doc += 1
            elif klasses == "negative":
                self.negative_doc += 1
            else:
                self.neutral_doc += 1

        self.positive_prior=math.log(self.positive_doc)-(math.log(self.positive_doc + self.negative_doc + self.neutral_doc))
        self.negative_prior=math.log(self.negative_doc)-(math.log(self.positive_doc + self.negative_doc + self.neutral_doc))
        self.neutral_prior=math.log(self.neutral_doc)-(math.log(self.positive_doc + self.negative_doc + self.neutral_doc))

        for k in range(len(train_klasses)):
            tokens=tokenize(train_texts[k])
            token=set(tokens)
            for t in token:
                if train_klasses[k] == "positive":
                    self.positive_class_cnt[t] = self.positive_class_cnt.get(t,0) + 1
                elif train_klasses[k] == "negative":
                    self.negative_class_cnt[t] = self.negative_class_cnt.get(t,0) + 1
                else:
                    self.neutral_class_cnt[t] = self.neutral_class_cnt.get(t,0) + 1

            for t in tokens:
                self.total_vocab[t]=self.total_vocab.get(t,0) + 1


    def classify(self,test_klasses):
        tokens=tokenize(test_klasses)
        positive_prob, negative_prob, neutral_prob = 0,0,0

        for t in tokens:

            positive_prob=math.log((self.positive_class_cnt.get(t,0)+1)) - math.log(sum(self.positive_class_cnt.values()) + len(self.total_vocab))
            negative_prob=math.log((self.negative_class_cnt.get(t,0)+1)) - math.log(sum(self.negative_class_cnt.values()) + len(self.total_vocab))
            neutral_prob=math.log((self.neutral_class_cnt.get(t,0)+1)) - math.log(sum(self.neutral_class_cnt.values()) + len(self.total_vocab))


        if positive_prob > negative_prob:
            return "positive"
        elif positive_prob < negative_prob:
            return "negative"
        else:
            return "neutral"


if __name__ == '__main__':
    import sys

    sys.stdout.reconfigure(encoding='utf-8')
    method = sys.argv[1]
    train_texts_fname = sys.argv[2]
    train_klasses_fname = sys.argv[3]
    test_texts_fname = sys.argv[4]

    train_texts = [x.strip() for x in open(train_texts_fname,
                                           encoding='utf8')]
    train_klasses = [x.strip() for x in open(train_klasses_fname,
                                             encoding='utf8')]
    test_texts = [x.strip() for x in open(test_texts_fname,
                                          encoding='utf8')]

    if method == 'baseline':
        classifier = Baseline(train_klasses)
        results = [classifier.classify(x) for x in test_texts]

    elif method == "lexicon":
        classifier = Lexicon(train_klasses)
        results = [classifier.classify(x) for x in test_texts]

    elif method == "nb":
        classifier = NaiveBayes(train_texts,train_klasses)
        results = [classifier.classify(x) for x in test_texts]

    elif method == "nbbin":
        classifier = BinaryNaiveBayes(train_texts,train_klasses)
        results = [classifier.classify(x) for x in test_texts]

    elif method == 'lr':
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.linear_model import LogisticRegression

        count_vectorizer = CountVectorizer(analyzer=tokenize)
        train_counts = count_vectorizer.fit_transform(train_texts)
        lr = LogisticRegression(multi_class='multinomial',
                                solver='sag',
                                penalty='l2',
                                max_iter=1000,
                                random_state=0)
        clf = lr.fit(train_counts, train_klasses)
        test_counts = count_vectorizer.transform(test_texts)
        results = clf.predict(test_counts)

    for r in results:
        print(r)