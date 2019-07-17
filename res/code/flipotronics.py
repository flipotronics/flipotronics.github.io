#!/usr/bin/env python3

import os, pygame
from pygame.locals import *
from sys import exit
import redis
import math
import time

def getParam(param):
  return int(127 * float(param))

def drawParam(x,y,val):
  radius = 90
  cx, cy = x + 90, y+90
  angle = val * 360 / 127
  p = [(cx, cy)]
  for n in range(270, int(angle + 270)):
    xp = cx + int((radius) * math.cos(n*math.pi/180))
    yp = cy + int((radius) * math.sin(n*math.pi/180))
    p.append((xp, yp))
  p.append((cx, cy))
  if len(p) > 2:
    pygame.draw.polygon(screen, (255,255,255), p)

  pygame.draw.circle(screen,ENCODERBG,[x+90,y+90],radius - 10)

  # Float Value 
  textsurface = font3.render("{0:.3f}".format(val / 127.0), False, (255, 255, 255))
  screen.blit(textsurface,(x + 50,y + 30))

  # Param Name
  pygame.draw.rect(screen,(0,0,0),(x+20,y+72,140,36))
  textsurface = font2.render("Volume".center(180), False, (255, 255, 255))
  w = textsurface.get_width()
  o = ( 180 - w) / 2
  screen.blit(textsurface,(x + o,y+70))

  # Midi Value
  textsurface = font3.render("{:>3}".format(val), False, (255, 255, 255))
  screen.blit(textsurface,(x + 65,y+125))
  
  

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
ENCODERCOLOR=(128,128,128)
ENCODERBG=(0,128,128)
lineCol=(128,128,120)

running = True
radius=80

pygame.init()
font = pygame.font.SysFont('Arial', 90)
font2 = pygame.font.SysFont('FreeMonoBold', 55)
font3 = pygame.font.SysFont('FreeMonoBold', 45)

while running:
    mouse = pygame.mouse.get_pos()
    page = int(r.get('page')) 
    screen.fill(bgcolor)
    pygame.draw.line(screen,lineCol,(0,240),(720,240))
    pygame.draw.line(screen,lineCol,(180,0),(180,480))
    pygame.draw.line(screen,lineCol,(360,0),(360,480))
    pygame.draw.line(screen,lineCol,(540,0),(540,480))

    key = "pagename" + str(page)
    name = r.get(key)
    textsurface = font.render(name, False, (255, 255, 255))
    screen.blit(textsurface,(10,185))
    
    positions = [0,1,2,3]
    for x in positions:
        key = "param" + str(page * 8 + x)
        val = getParam(r.get(key))
        drawParam(x*180,0,val)

    positions = [0,1,2,3]
    for x in positions:
        key = "param" + str(page * 8 + x + 4)
        val = getParam(r.get(key))
        drawParam(x*180,290,val)

    pygame.display.update()
    if mouse[0] > 700:
      running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  


    time.sleep(0.1)