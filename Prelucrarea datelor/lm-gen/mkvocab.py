

wordIndex = 0
countIndex = 1

def passesPruning (wordData):
    '''
    if (len(wordData[wordIndex]) < 3):
        return False

    '''

    if (wordData[countIndex] < 2):
        return False

    return True


def createVocabulary (inFilePath, outFilePath):
    try:
        inFile = open(inFilePath, "r")


        freq = dict()

        for line in inFile:
            words = line.split()

            for word in words:
                if word in freq:
                    freq[word] += 1
                else:
                    freq[word] = 1

        sortedFreq = sorted(freq.items(), key = lambda keyVal: keyVal[1])
        sortedFreq = reversed(sortedFreq)



        outFile = open(outFilePath, "w")


        for item in sortedFreq:

            if passesPruning(item):

                outFile.write('{word} {count}\n'

                        .format(count = item[countIndex],
                                word = item[wordIndex]))


        return True


    except Exception as e:
        print (e)
        return False
