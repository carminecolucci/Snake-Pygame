import pygame
import random
import tkinter as tk
from tkinter.messagebox import showinfo
pygame.init()
pygame.font.init()

WIDTH, HEIGTH = 600, 600
ROWS = 20

class Cube:
    rows = ROWS
    width = WIDTH
    heigth = HEIGTH
    def __init__(self, pos, dirX = 0, dirY = -1, color = (0, 255, 0)):
        self.pos = pos
        self.dirX = dirX
        self.dirY = dirY
        self.color = color
    
    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)
    def draw(self, win, eyes=False):
        gapX = self.width // self.rows
        gapY = self.heigth // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(win, self.color, (i * gapX , j * gapY , gapX , gapY ))
        if eyes:
            centre = gapX // 4
            radius = 3
            if self.dirX == 1: # destra
                leftEye = ((i * gapX) + gapX - centre, j * gapY + centre)
                rightEye = ((i * gapX) + gapX - centre, j * gapY + gapY - centre)
            elif self.dirX == -1: # sinistra
                leftEye = (i * gapX + centre, j * gapY + gapY - centre)
                rightEye = (i * gapX + centre, j * gapY + centre)
            elif self.dirY == 1: # sotto
                leftEye = ((i * gapX) + gapX - centre, j * gapY + gapY - centre)
                rightEye = (i * gapX + centre, j * gapY + gapY - centre)
            elif self.dirY == -1: # sopra
                leftEye = (i * gapX + centre, j * gapY + centre)
                rightEye = ((i * gapX) + gapX - centre, j * gapY + centre)                
            
            pygame.draw.circle(win, (0, 0, 0), leftEye, radius)
            pygame.draw.circle(win, (0, 0, 0), rightEye, radius)


class Snake:
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1
        self.pos = pos
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.dirY != 1:
                self.dirX = 0
                self.dirY = -1
                self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
        if keys[pygame.K_DOWN]:
            if self.dirY != -1:
                self.dirX = 0
                self.dirY = 1
                self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
        if keys[pygame.K_LEFT]:
            if self.dirX != 1:
                self.dirX = -1
                self.dirY = 0
                self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
        if keys[pygame.K_RIGHT]:
            if self.dirX != -1:
                self.dirX = 1
                self.dirY = 0
                self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirX == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirX == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                elif c.dirY == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                else:
                    c.move(c.dirX, c.dirY)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirX = 0
        self.dirY = -1

    def eat(self):
        tail = self.body[-1]
        dirX, dirY = tail.dirX, tail.dirY
        if dirX == 1 and dirY == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]), dirX, dirY))
        elif dirX == -1 and dirY == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1]), dirX, dirY))
        elif dirX == 0 and dirY == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1), dirX, dirY))
        elif dirX == 1 and dirY == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1), dirX, dirY))
        

    def draw(self):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(WIN, True)
            else:
                c.draw(WIN)

def update_score(score):
    prec_score = high_score()
    with open('score.txt', 'w') as f:
        if int(prec_score) > score:
            f.write(str(prec_score))
        else:
            f.write(str(score))


def high_score():
    with open('score.txt', 'r') as f:
        line = f.readlines()
        prec_score = line[0].strip()
    return prec_score

def showScore():
    score = len(s.body)
    max_score = high_score()
    update_score(score)
    title = 'Hai perso, Riprova!'
    message = f'Score: {score}\nMax Score: {max_score}'
    win = tk.Tk()
    win.attributes('-topmost', True)
    win.withdraw()
    showinfo(title, message)
    

WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption('Snake Game')
snakeX = ROWS // 2
snakeY = ROWS // 2
s = Snake((0, 255, 0), (snakeX,  snakeY))


def drawGrid(win):
    gapX = WIDTH // ROWS
    gapY = HEIGTH // ROWS
    x = 0
    y = 0
    for i in range(ROWS):
        x += gapX
        y += gapY

        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, HEIGTH))
        pygame.draw.line(win, (255, 255, 255), (0, y), (WIDTH, y))

def redrawWIN(win):
    global ROWS, s, apple
    win.fill((0, 0, 0))
    s.draw()
    apple.draw(WIN)
    drawGrid(win)
    pygame.display.update()

def spawnApple(snake):
    positions = snake.body
    while True:
        x = random.randrange(ROWS)
        y = random.randrange(ROWS)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y

apple = Cube(spawnApple(s), color=(255, 0, 0))

def main():
    global ROWS, s, apple
    clock = pygame.time.Clock()
    
    run = True
    while run:
        pygame.time.delay(150)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        s.move()
        if s.head.pos == apple.pos:
            s.eat()
            apple = Cube(spawnApple(s), color=(255, 0, 0))
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1 :])):
                showScore()
                s.reset((snakeX, snakeY))
                break
        redrawWIN(WIN)
        

main()
pygame.quit()
