-Echipa:
    Boeriu Cosmin 152
    Pasarin David 152
    Lutu Adrian 152
    Strejaru Mihai 152


-Numarul mediu de incercari : 4.197660206041557


-Ghid rulare:
    -Proiectul contine 2 script-uri python(wordle.py si ai.py). Acestea comunica intre ele utilizand socket-uri, 
wordle.py este server-ul, iar ai.py clientul.
    -Proiectul nostru are 2 moduri de fuctionare: - Rulare pe intreaga baza de date (variabila TYPE_OF_RUN == 1)
                                                  - Rezolvare pentru un cuvant random din baza de date(variabila TYPE_OF_RUN == 0)
                                                  
    !!!PENTRU RULARE: 1. Setam valoarea variabilei TYPE_OF_RUN la linia 147 din wordle.py
                      2. Rulam wordle.py
                      3. Rulam ai.py
                      


-Descriere:
    Pentru a stabilii cel mai bun cuvant de inceput am creat un dictionar(DEFAULT_LETTERS_DICTIONARY) in care am
numarat aparitiile fiecarei litere pe fiecare pozitie. Utilizand dictionarul am calculat entropia tuturor cuvintelor
din baza din baza de date(WORDS_DATABASE/DATABASE.txt) si am obtinut cuvantul TAREI ca fiind optim. 

-Entropia unui cuvant este calculata astfel:

    Notatii: Gi: probabilitatea ca litera de pe pozitia i(i = 0->4) sa fie verde
             Yi: probabilitatea ca litera de pe pozitia i(i = 0->4) sa fie galbena
             GRi: probabilitatea ca litera de pe pozitia i(i = 0->4) sa fie gri
             Ei: entropia literei de pe pozitia i(i = 0->4)
             E: entropia cuvantului

    Ei = -Gi*log2(Gi) -Yi*log2(Yi) -GRi*log2(GRi)
    E = sum(Ei) , i = 0 -> 4

-Obtinerea fisierului secondGuesses.txt:

        -Un raspuns este un sir de caractere de forma "bbbbb" (b apartine {0,1,2}) primit de catre ai.py de la wordle.py,
ce reprezinta culorile literelor(2 - verde, 1 - galben, 0 - gri)

        Pentru a forma fisierul secondGuesses.txt am generat toate posibilitatile de raspunsuri simuland ca prima
incercare cuvantul TAREI. Utilizand fiecare raspuns, pe rand, filtram baza de date, unde raman doar cuvintele
ce se potrivesc raspunsului. Pe acesta noua baza de date calculam cel mai bun cuvant pentru a doua incercare.


    

    

    
    
    
!!!!Recomandam utilizarea Debuggerului pentru o mai buna intelegere a proiectului!!!!