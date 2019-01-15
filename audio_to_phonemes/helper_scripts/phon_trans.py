import sys

# creaza transcrieri fonetice folosind regulile din alpha_to_phoneme.txt pentru cuvintele din fisierul dat ca argument (ex. missing_words.txt) din missing_dic.txt

alpha_to_phoneme = {}

af = open("alpha_to_phoneme.txt", "r").readlines()
for line in af:
	line = line.split()
	char = line[0]
	phons = line[1:]
	alpha_to_phoneme[char] = phons

print(alpha_to_phoneme)
	
words = [x.strip() for x in open(sys.argv[1]).readlines()]

wf = open("missing_dic.txt", "w")

for w in words:
	s = w + '\t'
	w.replace('ce', '(').replace('ci', '(')
	w.replace('ge', '&').replace('gi', '&')
	for char in w[1:]:
		for y in alpha_to_phoneme[char]:
			s = s + y + ' '
	s = s.strip() + '\n'
	wf.write(s)