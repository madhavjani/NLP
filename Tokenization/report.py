import sys
fname = sys.argv[1]
token = 0
types = 0
hapax = 0
with open(fname, mode='r', encoding='utf-8') as tokenFile:
    lines = tokenFile.readline()
    while lines:
        count, word = lines.split()
        types += 1 
        token += int(count)
        if count == '1':
            hapax += 1
        lines = tokenFile.readline()

print("Types : "+str(types)+"\nTokens : "+str(token)+"\nHapax : "+str(hapax) )

    