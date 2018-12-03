import os
from parseDictionary import parse_dictionary

def PhenomeToText(path):
    cuvinteRezultate = list()
    dict1 = parse_dictionary("dictionary.txt")


    file = open(path)
    for line in file:
        #print(line)
        cuvinte = line.split("SIL")
        for i in cuvinte:
            i = i.strip(" ")
            #pentru cuvintele rezultate din audio->foneme:
            for x in dict1:
                if i == x:
                    cuvinteRezultate.append(dict1[x])
            #incerc sa recunosc cuvintele:
            k = ""
            for j in i:
                k = k + j
                #print(k)
                for y in dict1:
                   if k == y:
                       cuvinteRezultate.append(dict1[y])
                       k = ""  #caut urmatorul cuvant
                       break
    return cuvinteRezultate

if __name__ == '__main__':
    print(PhenomeToText("fonemeRezultate.txt"))
