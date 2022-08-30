import sys, gzip, random, re
regexp=r"\s+|([^-_'0-9A-Za-z])"
def tokenize(line):
    for i in line:
            encodedToken = i.encode('ascii', 'ignore')
            print(encodedToken.decode('utf-8'))
fname = sys.argv[1]
with gzip.open(fname, mode='rt', encoding='utf-8') as infile:
    for i in infile:
        line = filter(None, re.compile(regexp).split(i))
        tokenize(line)