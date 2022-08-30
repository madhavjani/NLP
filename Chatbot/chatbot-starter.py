import io, math, re, sys

def tokenize(s):
    tokens = s.lower().split()
    trimmed_tokens = []
    for t in tokens:
        if re.search('\w', t):
            t = re.sub('^\W*', '', t)
            t = re.sub('\W*$', '', t)
        trimmed_tokens.append(t)
    return trimmed_tokens

def most_sim_overlap(query, responses):
    q_tokenized = tokenize(query)
    max_sim = 0
    max_resp = "Sorry, I don't understand"
    for r in responses:
        r_tokenized = tokenize(r)
        sim = len(set(r_tokenized).intersection(q_tokenized))
        if sim > max_sim:
            max_sim = sim
            max_resp = r
    return max_resp

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = list(map(float, tokens[1:]))
    return data


def w2v(query, responsevec, wordvec, denominator):
    q_tokenized = tokenize(query)
    total_length = len(q_tokenized)
    queryvec = {}
    linevec = []
    cos = {}
    query_denom,response_denom = 0,0
    max_resp = "Sorry, I don't understand"

    for q in q_tokenized:
        if q in wordvec:
            linevec.append(wordvec[q])

    queryvec[query] = [sum(x) / total_length for x in zip(*linevec)]

    for r in responsevec:
        if len(responsevec[r]) > 0:
            numerator = 0
            query_square = 0
            response_square = 0
            for i in range(0, len(queryvec[query])):
                numerator = numerator + queryvec[query][i] * responsevec[r][i]
                response_square = response_square + responsevec[r][i] * responsevec[r][i]
                query_square = query_square + queryvec[query][i] * queryvec[query][i]
            query_denom = math.sqrt(query_square)
            response_denom = math.sqrt(response_square)
            cos[r] = numerator / (query_denom * response_denom)
            if query_denom == 0 or response_denom == 0:
                return max_resp
    return str([key for key in cos if cos[key] == max(cos.values())]).strip("['']")


if __name__ == '__main__':
    method = sys.argv[1]
    responses_fname = 'gutenberg.txt'
    vectors_fname = 'cc.en.300.vec.10k'
    responses = [x.strip() for x in open(responses_fname)]

    if method == 'w2v':
        print("Loading vectors...")
        wordvec = load_vectors(vectors_fname)
        linevec = []
        responsevec = {}
        denominator = {}
        for r in responses:
            r_tokens = tokenize(r)
            total_size = len(r_tokens)
            for t in r_tokens:
                if t in wordvec:
                    sqr = 0
                    if t not in denominator:
                        for i in range(0, len(wordvec[t])):
                            sqr = sqr + wordvec[t][i] * wordvec[t][i]
                        denominator[t] = math.sqrt(sqr)
                        for i in range(0, len(wordvec[t])):
                            wordvec[t][i] = wordvec[t][i] / denominator[t]
                    linevec.append(wordvec[t])
            responsevec[r] = [sum(i) / total_size for i in zip(*linevec)]
            linevec = []

    print("Hi! Let's chat")
    while True:
        query = input("YOU:- ")
        if method == 'overlap':
            response = most_sim_overlap(query, responses)
            print("OVERLAP:- ", response)
        elif method == 'w2v':
            response = w2v(query, responsevec, wordvec, denominator)
            print("W2V:- ", response)

        print()
