# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pygame
from random import shuffle

ncelx =  5 
ncely =  4 

celsize = 40 

set_ = list("abcdefghijkl") 

verde   = pygame.Color("green") 
gris    = pygame.Color("grey20")     
negro   = pygame.Color("black")      
blancoo  = pygame.Color("white")

def make_set():
    nb_cartas = (ncelx*ncely)//2
    cartas = set_*int(nb_cartas//len(set_))
    cartas += set_[:nb_cartas%len(set_)]
    cartas *= 2
    shuffle(cartas)
    return cartas

screen = pygame.display.set_mode((ncelx*celsize,ncely*celsize))
screenrect = screen.get_rect()

pygame.font.init()
police = pygame.font.Font(None,int(celsize//1.5))

primcarta = None

while True:

    cartas = make_set()
    pygame.event.clear()
    pygame.time.set_timer(pygame.USEREVENT,1000)
    secondes = 0

    while any(cartas):
    ev = pygame.event.wait()
        if ev.type == pygame.QUIT: break 
        elif ev.type == pygame.USEREVENT:
            secondes += 1
            pygame.display.set_caption(str(secondes))
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            index = ev.pos[1]//celsize*ncelx+ev.pos[0]//celsize
            if cartas[index] and index!=primcarta: 
                r = screen.fill(blanco,(index%ncelx*celsize+1,index//ncelx*celsize+1,celsize-2,celsize-2))
                motif = police.render(str(cartas[index]),1,gris)
                screen.blit(motif,motif.get_rect(center=(r.center)))
                pygame.display.update(r)
                if primcarta is None:
                    primcarta = index
                    firstr = rt
                    continue
                if cartas[index] == cartas[primcarta]:
                    screen.fill(green,r,special_flags=pygame.BLEND_MIN)
                    screen.fill(green,firstr,special_flags=pygame.BLEND_MIN)
                    pygame.time.wait(500)
                    pygame.display.update((r,firstr))
                    cartas[index] = cartas[primcarta] = None
                else:
                    pygame.time.wait(500)
                    pygame.display.update((screen.fill(negro,r),screen.fill(negro,firstr)))
                primcarta = None
    break

pygame.quit()