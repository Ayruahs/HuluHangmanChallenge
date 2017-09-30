readfile = "./count_1w.txt"

wordSet = set()
with open(readfile, 'r') as rf:
    for line in rf:
        wordSet.add(line)

