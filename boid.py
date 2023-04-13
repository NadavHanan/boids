import pygame
import matplotlib.pyplot as plt
import random as rnd
import numpy as np
from matplotlib.animation import FuncAnimation
import math
pygame.init()

def d(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def is_angle2_biger(a1,a2):
    if a1<math.pi:
        return a2>a1 and a2<(a1+math.pi)
    else:
        return ((2*math.pi)>a2>a1) or (0.0<a2<(a1-math.pi))

def xytoangle(x1,y1,x2,y2):
    if(x1 == x2):
        return math.pi*.5 if y2>y1 else -math.pi*.5
    a = math.atan((y2-y1)/(x2-x1))
    return  (a if x2>x1 else a+math.pi)%(2*math.pi)

def angletoxy(angle, l):
    return [l*math.cos(angle),l*math.sin(angle)]

win_size = 700
win = pygame.display.set_mode((win_size, win_size))

class boid():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

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

        pygame.draw.polygon(win, (255,255,255), ((x1,y1),(x2,y2),(x3,y3)))

    def angleto(self,x,y):
        v_angle=.1
        a = xytoangle(self.x,self.y,x,y)
        self.angle += v_angle if is_angle2_biger(self.angle,a) else -v_angle
        self.angle = self.angle%(2*math.pi)
        #self.angle += v_angle if a>self.angle else -v_angle

    def move(self):
        a = angletoxy(b.angle, 10)
        self.x += a[0]
        self.y += a[1]

class sqr():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (255,255,255),(self.x, self.y, 10,10))

b = boid(250,250,6)
s = sqr(300,300)

lst = []

print(xytoangle(2,2,1,3))


#mainloop
t = 0
run = True
while run:
    t += 1
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill((0, 0, 0))

    k = pygame.key.get_pressed()
    if(k[pygame.K_UP]):
        s.y-=10
    if(k[pygame.K_DOWN]):
        s.y+=10
    if(k[pygame.K_RIGHT]):
        s.x+=10
    if(k[pygame.K_LEFT]):
        s.x-=10


    b.draw(win)
    s.draw(win)
    b.move()
    b.angleto(s.x, s.y)
    lst.append(b.angle)

    pygame.display.update()

pygame.quit()

#plt.plot(lst)
#plt.show()