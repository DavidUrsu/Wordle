import pygame
import sys
import random
import math
import socket
import threading

pygame.init()

PORT = 8123
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disc"
IMAGE = pygame.image.load("logo.png")
pygame.transform.scale(IMAGE, (IMAGE.get_width()/2, IMAGE.get_height()/2))
MODE = 1
DIMENSION = 60
COLORS = ((145, 145, 142), (232, 213, 39), (29, 184, 71), (255, 255, 255), (0, 0, 0))
"""          grey,              yellow,        green,        white,          black"""
WORDS_DATABASE = open("DATABASE.txt", "r")
WORDS = [x.strip() for x in WORDS_DATABASE.readlines()]
FONT = pygame.font.SysFont("C059, BOLD", 40)
LETTERS = [FONT.render((chr(x)), True, (0, 0, 0)) for x in range(ord('A'), ord('Z')+1)]
SCREEN_RES = (1024, 1024)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_RES)


def verificaCuvant(cuvant_de_ghicit, cuvantul_actual):
    raspuns = ""
    for i in range(len(cuvantul_actual)):
        if cuvantul_actual[i] == cuvant_de_ghicit[i]:
            raspuns += "2"
        elif cuvantul_actual[i] in cuvant_de_ghicit:
            raspuns += "1"
        else:
            raspuns += "0"
    return raspuns


def blit_words(words):
    x = screen.get_height() / 2 - DIMENSION * 5 / 2 - 4 * 5
    y = 200
    screen.blit(IMAGE, (screen.get_width()/2 - IMAGE.get_width()/2, y-IMAGE.get_height()-10))

    for word in words:
        letters = None
        if word[0] is not None:
            letters = [LETTERS[ord(y)-ord('A')] for y in word[0]]
        for lett in range(len(word[1])):
            pygame.draw.rect(screen, COLORS[-1], pygame.Rect(x - 1, y - 1, DIMENSION + 2, DIMENSION + 2))
            pygame.draw.rect(screen, word[1][lett], pygame.Rect(x, y, DIMENSION, DIMENSION))
            if letters is not None:
                screen.blit(letters[lett], (x+DIMENSION/2-letters[lett].get_width()/2,
                                    y+DIMENSION/2-letters[lett].get_height()/2))
            x += DIMENSION + 10
        y += DIMENSION + 10
        x = screen.get_height() / 2 - DIMENSION * 5 / 2 - 4 * 5


class Template:
    def __init__(self, i):
        self._words = [[None, [COLORS[-2]]*5] for x in range(6)]
        self._colors = [[COLORS[-2]]*5 for x in range(6)]
        self._startX = 200
        self._startY = 200
        self._index = 0
        self._win = False
        self._selectedword = WORDS[i]

    def clear(self, i):
        self._index = 0
        try:
            self._selectedword = WORDS[i]
        except IndexError:
            pass
        self._words = [[None, [COLORS[-2]] * 5] for x in range(6)]
        self._colors = [[COLORS[-2]] * 5 for x in range(6)]
        self._win = False

    def get_win_state(self):
        return self._win

    def recolor_word(self, culori):
        for i in range(len(culori)):
            x = int(culori[i])
            self._words[self._index][1][i] = COLORS[x]

    def write_word(self, word):
        if self._index >= len(self._words):
            t = [None, [COLORS[-2]]*5]
            self._words.append(t)
        self._words[self._index][0] = word
        model = verificaCuvant(self._selectedword, word)
        self.recolor_word(model)
        server.send(model)
        if model == '22222':
            self._win = True
        self._index += 1

    def blit(self):
        blit_words(self._words)

    def update(self):
        self.blit()
        if server.server_status():
            if not self._win:
                cuv = server.receive()
                self.write_word(cuv)


class Server:
    def __init__(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(ADDR)
        self._server.listen(1)
        self._message = None
        self._conn, self._addr = None, None
        self._stable = False
        threading.Thread(target=self.accept, daemon=True).start()

    def server_status(self):
        return self._stable

    def accept(self):
        self._conn, self._addr = self._server.accept()
        self._stable = True

    def receive(self):
        self._message = self._conn.recv(5).decode(FORMAT)
        return self.show_message()

    def show_message(self):
        return self._message

    def send(self, msg):
        msg = msg.encode()
        self._conn.send(msg)

    def close(self):
        self._server.close()


server = Server()
flag = 0
TYPE_OF_RUN = 1  # tot databaseul = 1 --- pentru un singur cuvant = 0
i = 0
if TYPE_OF_RUN == 0:
    i = random.randint(0, 11454)
template = Template(i)

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            server.close()
            pygame.quit()
            sys.exit()
    template.update()
    pygame.display.update()
    if template.get_win_state() and not flag:
        template.clear(i)
        print(template._selectedword)
        i += 1
        if i == len(WORDS) or TYPE_OF_RUN == 0:
            server.close()
            flag = 1
