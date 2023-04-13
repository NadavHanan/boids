import pygame
import matplotlib.pyplot as plt
import random as rnd
import numpy as np
from matplotlib.animation import FuncAnimation
import math
from statistics import mean

#a1 avoide a2 inside a3 match
a1,a2,a3 = 300, 100, 300

def is_angle2_biger(a1, a2):
    if a1 < math.pi:
        return (a1+math.pi) > a2 > a1
    else:
        return ((2*math.pi) > a2 > a1) or (0.0 < a2 < (a1-math.pi))

def d(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def xytoangle(x1,y1,x2,y2):
    if(x1 == x2):
        return math.pi*.5 if y2>y1 else -math.pi*.5
    a = math.atan((y2-y1)/(x2-x1))
    return  (a if x2>x1 else a+math.pi)%(2*math.pi)

def angletoxy(angle, l):
    return [l*math.cos(angle), l*math.sin(angle)]

def reg(x):
    pass


class boid:
    def __init__(self, x, y, angle, grop):
        self.x = x
        self.y = y
        self.angle = angle
        self.v_angle = .2
        self.grop = grop

    def draw(self, win):
        l = 3

        a = l*math.cos((math.pi/2-self.angle))
        b = l*math.sin(math.pi/2-self.angle)
        c = 4*l*math.cos(self.angle)
        d = 4*l*math.sin(self.angle)
        x1 = round(self.x + a)
        y1 = round(self.y - b)
        x3 = round(self.x + c)
        y3 = round(self.y + d)
        x2 = round(self.x - a)
        y2 = round(self.y + b)
        color = (255,0,0) if self.grop==1 else (0,0,255)
        pygame.draw.polygon(win, color, ((x1,y1),(x2,y2),(x3,y3)))

    def angleto(self, x, y):
        a = xytoangle(self.x, self.y, x, y)
        self.angle += self.v_angle if is_angle2_biger(self.angle, a) else -self.v_angle
        self.angle = self.angle % (2*math.pi)

    def move(self):
        a = angletoxy(self.angle, 10)
        self.x += a[0]
        self.y += a[1]

    def avoide(self, lb, i):
        lx = []
        ly = []
        for j in lb:
            if (j != i) and d(self.x, self.y, j.x, j.y)<30:
                lx.append(j.x)
                ly.append(j.y)

        x = self.x - mean(lx) if len(lx) else 0.
        y = self.y - mean(ly) if len(ly) else 0.
        if (x or y):
            x, y = angletoxy(xytoangle(0., 0., x, y), a1)

        return x+self.x, y+self.y

    def inside(self, win_size):
        if self.x < a2:
            x = a2
        elif self.x > win_size-a2:
            x = win_size-a2
        else:
            x = None

        if self.y < a2:
            y = a2
        elif self.y > win_size-a2:
            y = win_size-a2
        else:
            y = None
        if x == self.x or y == self.y:
            return None,None
        return x, y

    def match(self, lb, i):
        lx = []
        ly = []
        for j in lb:
            if j != i:
                x, y = angletoxy(j.angle, a3)
                lx.append(x)
                ly.append(y)
        x = self.x + mean(lx)
        y = self.y + mean(ly)
        return x, y

class sqr():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (255,0,0),(self.x, self.y, 10,10))

class sqr():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (255,0,0),(self.x, self.y, 10,10))

lx = []
ly = []

pygame.init()
win_size = 700
win = pygame.display.set_mode((win_size, win_size))

lb1 = [boid(win_size*.5+rnd.randint(-50,50), win_size*.5+rnd.randint(-50,50), rnd.uniform(0.,math.pi*2),1) for i in range(20)]
lb2 = [boid(win_size*.5+rnd.randint(-50,50), win_size*.5+rnd.randint(-50,50), rnd.uniform(0.,math.pi*2),2) for i in range(20)]
s1 = sqr(250, 250)
s2 = sqr(250, 250)
s = []
#[s.append(sqr(350, 550+5*i)) for i in range(20)]

# mainloop
t = 0
run = True
while run:
    t += 1
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill((0, 0, 0))

    s1.x = mean([lb1[i].x for i in range(len(lb1))])
    s1.y = mean([lb1[i].y for i in range(len(lb1))])
    lx.append(s1.x)
    ly.append(s1.y)
    [i.draw(win) for i in s]

    for i in range(len(lb1)):
        lb1[i].draw(win)
        lb1[i].move()
        xa, ya = lb1[i].avoide(lb1+lb2+s, i)
        xw, yw = lb1[i].inside(win_size)
        xm, ym = lb1[i].match(lb1, i)
        x = [xa, xw, xm, s1.x]
        y = [ya, yw, ym, s1.y]
        x = mean([i for i in x if i])
        y = mean([i for i in y if i])
        lb1[i].angleto(x, y)

    s2.x = mean([lb2[i].x for i in range(len(lb2))])
    s2.y = mean([lb2[i].y for i in range(len(lb2))])
    for i in range(len(lb2)):
        lb2[i].draw(win)
        lb2[i].move()
        xa, ya = lb2[i].avoide(lb2+lb1+s, i)
        xw, yw = lb2[i].inside(win_size)
        xm, ym = lb2[i].match(lb2, i)
        x = [xa, xw, xm, s2.x]
        y = [ya, yw, ym, s2.y]
        x = mean([i for i in x if i])
        y = mean([i for i in y if i])
        lb2[i].angleto(x, y)

    pygame.display.update()

pygame.quit()


plt.scatter(lx,ly,s= 1)
plt.show()