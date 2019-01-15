import sys

# Parseaza un log de sphinxtrain (dat ca argument; ex. ro_db.html) si gaseste cuvintele care nu apar in dictionar (missing_words.txt)

words = {}
	
lines = open(sys.argv[1]).readlines()

for line in lines:
	if "WARNING: This word:" in line:
		line = line.strip()
		word = line.split("This word:")[1].split("was in the transcript")[0].strip()
		words[word] = words.get(word, 0) + 1
		#print(word + '\t' + str(bytearray(word, 'utf-8')))

wf = open("missing_words.txt", "w")
for w in sorted(words, key=lambda x: words[x], reverse=True):
	wf.write(w + '\n')