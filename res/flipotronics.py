#!/usr/bin/env python3

import os, pygame
from pygame.locals import *
from sys import exit
import redis
import math

r = redis.Redis(host='localhost', port=6379, db=0)

SCREEN_DEFAULT_SIZE = (720, 480)
screen = pygame.display.set_mode((0,0),  pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

full_screen = True
bgcolor = [0, 0, 0]
screen.fill(bgcolor)
pygame.display.update()
infoObject = pygame.display.Info()
print(infoObject)

# colors
ENCODERCOLOR=(0,128,128)
lineCol=(128,128,120)

running = True
radius=80

pygame.init()
font = pygame.font.SysFont('Arial', 90)

while running:
    mouse = pygame.mouse.get_pos()
    page = int(r.get('page')) 
    screen.fill(bgcolor)
    pygame.draw.line(screen,lineCol,(0,240),(720,240))
    pygame.draw.line(screen,lineCol,(180,0),(180,480))
    pygame.draw.line(screen,lineCol,(360,0),(360,480))
    pygame.draw.line(screen,lineCol,(540,0),(540,480))

    textsurface = font.render('Page ' + str(page + 1), False, (255, 255, 255))
    screen.blit(textsurface,(150,185))
    positions = [0,1,2,3]
    for x in positions:
        key = "param" + str(page * 8 + x)
        pygame.draw.circle(screen,ENCODERCOLOR,[x*180 + 90,90],radius)
        cx, cy = x*180 + 90, 90
        val = int(r.get(key))
        angle = val * 360 / 127
        p = [(cx, cy)]
        for n in range(270, int(angle + 270)):
            x = cx + int((radius-10) * math.cos(n*math.pi/180))
            y = cy + int((radius-10) * math.sin(n*math.pi/180))
            p.append((x, y))
        p.append((cx, cy))
        if len(p) > 2:
            pygame.draw.polygon(screen, (255,255,255), p) 
        
    for x in positions:
        key = "param" + str(page * 8 + 4 + x)
        pygame.draw.circle(screen,ENCODERCOLOR,[x*180 + 90,390],radius)
        cx, cy = x*180 + 90,390
        val = int(r.get(key))
        angle = val * 360 / 127
        p = [(cx, cy)]
        for n in range(270, int(angle + 270)):
            x = cx + int((radius-10) * math.cos(n*math.pi/180))
            y = cy + int((radius-10) * math.sin(n*math.pi/180))
            p.append((x, y))
        p.append((cx, cy))
        if len(p) > 2:
            pygame.draw.polygon(screen, (255,255,255), p)

    pygame.display.update()
    if mouse[0] > 700:
      running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  
                