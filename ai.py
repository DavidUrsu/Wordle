import random
import math

log_values = {}

def calculate_word_entropy(word, cuvinte_database):
    lungimeDatabase = len(cuvinte_database)
    dict = {}
    for cuv in cuvinte_database:
        pattern = []
        for i in range(5):
            if word[i] == cuv[i]:
                pattern.append(2)
            elif cuv[i] in word:
                pattern.append(1)
            else:
                pattern.append(0)
        pattern = tuple(pattern)
        if pattern in dict:
            dict[pattern] += 1
        else:
            dict[pattern] = 1
    s = 0
    for x in dict.values():
        if x not in log_values:
            log_values[x] = math.log2(x / lungimeDatabase)
        s -= (x / lungimeDatabase) * log_values[x]
    return s

def calculeazaProbabilitati(cuvinte_database):
    probabilitatiLitere = []
    for i in range(5):
        probabilitatiLitere.append([0]*26)

    for cuvant in cuvinte_database:
        for litera in list(range(5)):
            probabilitatiLitere[litera][ ord(cuvant[litera]) - ord('A') ] += 1
    lungimeDatabase = len(cuvinte_database)


    #probabilitate
    #for i in range(len(probabilitatiLitere)):
    #    probabilitatiLitere[i] = list(map(lambda x: x/lungimeDatabase, probabilitatiLitere[i]))

    #entropie
    """
    for i in range(len(probabilitatiLitere)):
        for j in range(len(probabilitatiLitere[i])):
            if probabilitatiLitere[i][j] != 0:
                probabilitatiLitere[i][j] = -(probabilitatiLitere[i][j] * math.log(probabilitatiLitere[i][j], 2))
    """
    for i in probabilitatiLitere:
        print(i)
    
    return probabilitatiLitere

def calculeazaProbabilitateCuvinte(probabilitatiLitere, cuvinte_database):
    probabilitatiCuvinte = []
    for cuvant in cuvinte_database:
        probabiliate = 0
        for i in range(5):
            probabiliate += probabilitatiLitere[i][ord(cuvant[i]) - ord('A')]
        probabilitatiCuvinte.append(probabiliate)

    return probabilitatiCuvinte

def filtreazaBazaDeDate(raspuns, cuvantul_actual, cuvinte_database):
    cuvinte_database.pop( cuvinte_database.index(cuvantul_actual) )
    for raspuns_pozitie in range(5):

        if raspuns[raspuns_pozitie] == "2":
            lungimeDatabase = len(cuvinte_database)
            i=0
            while i < lungimeDatabase:
                if cuvinte_database[i][raspuns_pozitie] != cuvantul_actual[raspuns_pozitie]:
                    cuvinte_database.pop(i)
                    lungimeDatabase -= 1
                    i -= 1
                i += 1

        if raspuns[raspuns_pozitie] == "1":
            lungimeDatabase = len(cuvinte_database)
            i=0
            while i < lungimeDatabase:
                #de adaugat si daca e diferita lista
                if (cuvantul_actual[raspuns_pozitie] not in cuvinte_database[i]) or (cuvinte_database[i][raspuns_pozitie] == cuvantul_actual[raspuns_pozitie]):
                    cuvinte_database.pop(i)
                    lungimeDatabase -= 1
                    i -= 1
                i += 1

        if raspuns[raspuns_pozitie] == "0":
            lungimeDatabase = len(cuvinte_database)
            i=0
            while i < lungimeDatabase:
                #de adaugat si daca e diferita lista
                if cuvantul_actual[raspuns_pozitie] in cuvinte_database[i]:
                    cuvinte_database.pop(i)
                    lungimeDatabase -= 1
                    i -= 1
                i += 1
    #print(len(cuvinte_database))
    return cuvinte_database

def verificaCuvant(cuvant_de_ghicit, cuvantul_actual):
    raspuns = ""
    for i in range(len(cuvantul_actual)):
        if cuvantul_actual[i]==cuvant_de_ghicit[i]:
            raspuns += "2"
            next
        elif cuvantul_actual[i] in cuvant_de_ghicit:
            raspuns += "1"
            next
        else:
            raspuns+="0"
    return raspuns

def ghicireCuvant(cuvant_de_ghicit, cuvinte_database):
    cuvantul_actual = ""
    con = 1
    """
    while cuvant_de_ghicit != cuvantul_actual:
        probabilitatiLitere = calculeazaProbabilitati(cuvinte_database)

        probabilitatiCuvinte = calculeazaProbabilitateCuvinte(probabilitatiLitere, cuvinte_database)

        cuvantul_actual = cuvinte_database[probabilitatiCuvinte.index(max(probabilitatiCuvinte))]

        cuvinte_database = filtreazaBazaDeDate(verificaCuvant(cuvant_de_ghicit, cuvantul_actual), cuvantul_actual, cuvinte_database)

        print(cuvantul_actual, verificaCuvant(cuvant_de_ghicit, cuvantul_actual))
        con = con + 1
    """

    cuvantul_actual = "CARTI"
    
    cuvinte_database = filtreazaBazaDeDate(verificaCuvant(cuvant_de_ghicit, cuvantul_actual), cuvantul_actual, cuvinte_database)
    #print(cuvantul_actual, verificaCuvant(cuvant_de_ghicit, cuvantul_actual))

    while cuvant_de_ghicit != cuvantul_actual:
        probabilitatiCuvinte = []
        for i in cuvinte_database:
            probabilitatiCuvinte.append(calculate_word_entropy(i, cuvinte_database))

        cuvantul_actual = cuvinte_database[probabilitatiCuvinte.index(max(probabilitatiCuvinte))]

        cuvinte_database = filtreazaBazaDeDate(verificaCuvant(cuvant_de_ghicit, cuvantul_actual), cuvantul_actual, cuvinte_database)

        #print(cuvantul_actual, verificaCuvant(cuvant_de_ghicit, cuvantul_actual))
        con = con + 1
    return con

def driverCode():
    with open("cuvinte_wordle.txt") as cuvinte_database:
        cuvinte_database_nemodificat = tuple([rand.strip() for rand in cuvinte_database])
        sum = 0
        numarIncercari = 100
        for _ in range(numarIncercari):
            cuvinte_database = list(cuvinte_database_nemodificat)
            #print(len(cuvinte_database))
            cuvant_de_ghicit = random.choice(cuvinte_database)
            sum += ghicireCuvant(cuvant_de_ghicit, cuvinte_database)
            #print("_"*20)
        print("Media numarului de incercari: " + str(sum/numarIncercari))

if __name__=="__main__":
    driverCode()