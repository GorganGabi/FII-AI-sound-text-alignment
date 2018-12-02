

def PhenomeToText():
    dict1={

             'a':'a',
             'abac':'abak',
             'abtSis@':'abcisă',
             'abrevija':'abrevia',
             'abreviat':'abreviat',
             'abreviativ':'abreviativ',
             'abreviator':'abreviator',
             'abreviere':'abreviere',
             'abriboj':'abriboi',
             'a b r o g a':'abroga',
             'a b r o g a r e':'abrogare',
             'a b r o g a t':'abrogat',
             'a b r o g a t i v':'abrogativ',
             'a b r u d e_X a n a':'abrudeana',
             'abrude_Xan':'abrudean',
             'abrude_Xank@':'abrudeancă',
             'a b r u p t':'abrupt',
             'a b r u p t o a':'abrupto',
             'a b r u t i z a':'abrutiza',
             'a b r u t i z a n t':'abrutizant',
             'a b r u t i z a r e':'abrutizare',
             'a b r u t i z a t':'abrutizat',
             'abstSizie':'abscizie',
             'abstSiziune':'absciziune',
             'a b s k o n s':'abscons',
             'a b s k o n s i t a t e':'absconsitate',
             'a b s k o n z i t a t e':'absconzitate',
             'a p s e n t':'absent',
             'a b s e n t a r e':'absentare',
             'a b s e n t e i s m':'absenteism',
             'a b s e n t e i s t':'absenteist',
             'a p s i d @':'absidă',
             'a p s i d a l':'absidal',
             'a p s i d i a l':'absidial',
             'a p s i d i o l @':'absidiolă',
             'a p s i l':'absil',
             'a p s i n t':'absint',
             'd u p @':'dupa',
             'a tS e s t':'acest',
             'p r o i e c t':'proiect',
             'o':'o'

         }

    with open ('test.txt', encoding='utf8') as f:
        for line in f:
             phenome = ' '.join([dict1.get(word, word) for word in line.split()])
             print(phenome)
     #return phenome

print(PhenomeToText())