import sys

# corecteaza un dictionar cu transcrieri fonetice (dat ca argument) dupa o lista de reguli (ro_db.dic), scoate un fisier cu toate fonemele (ro_db.phone) si un fisier cu un exemplu pentru fiecare fonem (phonex.txt)

lines = open(sys.argv[1]).readlines() + open("missing_dict.txt").readlines()

changes = {
    '@': 'a1',
    '1': 'a2',
    'dZ': 'dz1',
    'Z': 'z1',
    'e_X': 'ex',
    'tS': 'ts1',
    'o_X': 'ox',
    'S': 's1',
    'i_0': 'i0'
}

phonelist = []
phonex = []
new_lines = []
words = {}
alpha = {}

lines.sort()

for line in lines:
    l = line[0]
    if l not in alpha:
        print(l)
        alpha[l] = True
    line = line.replace('-', '')
    if len(line.strip()) == 0:
        continue
    line = line.strip().split()
    if line[0] in words:
        continue
    words[line[0]] = True

    for i in range(1, len(line)):
        if line[i] in changes:
            line[i] = changes[line[i]]
    for p in line[1:]:
        if p not in phonelist:
            phonelist.append(p)
            phonex.append([p, line[0], line[1:]])

    new_lines.append(line)

ps = open("ro_db.phone", "w")
for p in phonelist:
    ps.write("{}\n".format(p))

dc = open("ro_db.dic", "w")

for line in new_lines:
    dc.write("{}\t".format(line[0]))
    for p in line[1:-1]:
        dc.write("{} ".format(p))
    dc.write("{}\n".format(line[-1]))

ex = open("phonex.txt", "w")

for p in phonex:
    ex.write("{}\t{}\t{}\n".format(p[0], p[1], p[2]))
