import os
def text_final1(cuvinteRezulate):
    final=open("text_final.txt","a")
    lista=list() #cuvinte scrise lower si fara [] si fara '
    i=0
    for line in cuvinteRezultate:
        #sir rep fiecare cuv in formatul['cuv']
        sir=str(line).lower()
        lista.insert(i,"")
        #
        for x in range(2,len(sir)-2):
            s=lista[i]
            s=s+sir[x]
            lista[i]=s
        i+=1
    #fac literele mari unde e cazul
    k=0
    a = str(lista[0])
    a = a[0].upper() + a[1:]
    lista[0] = a
    for line in lista:
        if k!=i-1:
            if line=="." or line=='!' or line=='?' or line==';':
                a=str(lista[k+1])
                a=a[0].upper()+a[1:]
                lista[k+1]=a
        k+=1

    #scriere fisier + adaugare de spatiu
    for x in range(0,len(lista)):
        a=str(lista[x])
        final.write(a)
        if x!=(i-1):
            if lista[x+1]!="." and lista[x+1]!="!" and lista[x+1]!="?" and lista[x+1]!=";":
                final.write(" ")
if __name__ == '__main__':
    cuvinteRezultate=[['REPPUCCI'], ['REPPUCCI'], ['REH'], ['.'], ['ANA'], ['MERE'], ['!']] #de la teo
    text_final1(cuvinteRezultate)
