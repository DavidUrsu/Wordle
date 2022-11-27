import random
import math
import socket
import threading

file = open("DATABASE.txt", "r")
WORDS_DATABASE = tuple(rand.strip() for rand in file.readlines())
DEFAULT_LETTERS_DICTIONARY = {chr(let+ord('A')):[0]*5 for let in range(int(ord('Z')-ord('A'))+1)}
for word in WORDS_DATABASE:
    for lett in range(5):
        DEFAULT_LETTERS_DICTIONARY[word[lett]][lett] += 1
DEFAULT_LETTERS_DICTIONARY['sum'] = [len(WORDS_DATABASE)] * 5
DEFAULT_LETTERS_DICTIONARY = {k: tuple(val) for k, val in DEFAULT_LETTERS_DICTIONARY.items()}
file = open("secondGuesses.txt", 'r')
SECOND_GUESS = [x.split() for x in file.readlines()]
SECOND_GUESS = {k[0]: k[1] if len(k) == 2 else '' for k in SECOND_GUESS}
run = True

PORT = 8123
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disc"


class Client:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(ADDR)
        self._message = None

    def send(self, msg):
        self._client.send(msg.encode(FORMAT))

    def receive(self):
        self._message = self._client.recv(5).decode(FORMAT)
        return self.show_message()

    def show_message(self):
        return self._message

    def close(self):
        self._client.close()


def entropy_math_calc(probability):
    if probability == 0:
        return 0
    return -probability * math.log2(probability)


def calculate_word_entropy(word, lett_dict):
    word_ent = 0
    seen_letters = set()
    for pos, lett in enumerate(word):
        x = lett_dict[lett][pos]
        s = lett_dict['sum'][pos]
        green_prob = x/s
        sum = 0
        if lett not in seen_letters:
            grey_prob = 1
            for y in range(5):
                grey_prob *= 1 - lett_dict[lett][y]/lett_dict['sum'][y]
            yellow_prob = 1 - green_prob - grey_prob
        else:
            yellow_prob = 1 - x / s
            grey_prob = 0

        word_ent += entropy_math_calc( grey_prob) +entropy_math_calc( yellow_prob) +entropy_math_calc( green_prob)
        seen_letters.add(lett)
    return word_ent


def filtreazaBazaDeDate(raspuns, myword, lett_dict, cuvinte_database):
    new_database = []
    for cuvant in cuvinte_database:
        for i in range(5):
            if raspuns[i] == '2' and not cuvant[i] == myword[i]:
                break
            elif raspuns[i] == '1' and ((myword[i] not in cuvant) or (myword[i] == cuvant[i])):
                break
            elif raspuns[i] == '0' and myword[i] in cuvant:
                break
        else:
            new_database.append(cuvant)
    cuvinte_database = new_database
    for key, val in lett_dict.items():
        for y in range(5):
            lett_dict[key][y] = 0

    for word in cuvinte_database:
        for lett in range(5):
            lett_dict[word[lett]][lett] += 1
            lett_dict['sum'][lett] += 1

    return cuvinte_database


def calculate_best_word(lett_dict, remaining_words):
    mx = 0
    rez = None
    if len(remaining_words) <= 2:
        return remaining_words[0]
    for x in WORDS_DATABASE:
        k = calculate_word_entropy(x, lett_dict)
        if k > mx:
            rez = x
            mx = k
    return rez


def solve_word():
    lett_dict = {k: list(val) for k, val in DEFAULT_LETTERS_DICTIONARY.items()}
    remaining_words = WORDS_DATABASE[:]
    # myword = calculate_best_word(lett_dict, remaining_words)
    myword = 'TAREI'
    guesses = 1
    total_guesses = []
    while True:
        client.send(myword)
        total_guesses.append(myword)
        raspuns = client.receive()
        if raspuns == '22222':
            break
        if raspuns == '!disc':
            global run
            run = False
            break
        remaining_words = filtreazaBazaDeDate(raspuns, myword, lett_dict, remaining_words)
        if guesses == 1:
            myword = SECOND_GUESS[raspuns]
        else:
            myword = calculate_best_word(lett_dict, remaining_words)
        guesses += 1
    return total_guesses


client = Client()

#THE FUNCTION WE USED FOR CREATING secondGuess.txt

def generate_second_guesses():
    patterns = []
    file = open('secondGuesses.txt', 'w')
    def generate_pattern(k, s=''):
        if k == 5:
            patterns.append(s)
            return
        for i in ('0', '1', '2'):
            t = s+i
            generate_pattern(k+1, t)
    generate_pattern(0)
    for patt in patterns:
        print(patt)
        lett_dict = {k: list(val) for k, val in DEFAULT_LETTERS_DICTIONARY.items()}
        cuvinte = WORDS_DATABASE[:]
        cuvinte = filtreazaBazaDeDate(patt, 'TAREI', lett_dict, cuvinte)
        x = None
        if len(cuvinte) >= 1:
            x = calculate_best_word(lett_dict, cuvinte)
        file.write(f'{patt} {x if x is not None else ""}\n')
    file.close()


file = open("Answers.txt", 'w')
if __name__ == "__main__":
    s = 0
    i = 1
    while run:
        x = solve_word()
        print(x)
        s += len(x)
        rez = str(x[-1]) + ':'
        for y in x:
            rez += ' ' + str(y)
        file.write(f'{rez}\n')
    average = s/len(WORDS_DATABASE)
    file.write(f'Average number of guesses is {average}\n')
    file.close()
    client.close()
