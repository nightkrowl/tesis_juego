# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pygame
from random import shuffle

ncelx =  5 
ncely =  4
cellsize = 80

set_ = list("abcdefghijkl") 

verde = pygame.Color("green")
gris   = pygame.Color("grey20")
negro   = pygame.Color("black")
blanco  = pygame.Color("white")

def play_again():
    texto = police.render('click para jugar otra vez',1,gris,verde)
    pygame.display.update(scr.blit(texto,texto.get_rect(center=scrrect.center)))
    while True:
        e = pygame.event.wait()
        if e.type   == pygame.MOUSEBUTTONDOWN: return True
        elif e.type == pygame.QUIT: return False

def draw_hidden():
    scr.fill(verde)
    for y in range(0,scrrect.h,cellsize):
        for x in range(0,scrrect.w,cellsize):
            scr.fill(negro,(x+1,y+1,cellsize-2,cellsize-2))
    pygame.display.flip()

def make_set():
    nb_cartas = (ncelx*ncely)//2
    cartas = set_*int(nb_cartas//len(set_))
    cartas += set_[:nb_cartas%len(set_)]
    cartas *= 2
    shuffle(cartas)
    return cartas

scr = pygame.display.set_mode((ncelx*cellsize,ncely*cellsize))
scrrect = scr.get_rect()

pygame.font.init()
police = pygame.font.Font(None,int(cellsize//1.5))

primcarta = None 

while True:

    cartas = make_set()
    draw_hidden()

    pygame.event.clear()
    pygame.time.set_timer(pygame.USEREVENT,1000)
    secondes = 0

    while any(cartas):
        e = pygame.event.wait()
        if e.type == pygame.QUIT: break
        elif e.type == pygame.USEREVENT:
            secondes += 1
            pygame.display.set_caption(str(secondes))
        elif e.type == pygame.MOUSEBUTTONDOWN:
            index = e.pos[1]//cellsize*ncelx+e.pos[0]//cellsize
            if cartas[index] and index!=primcarta:
                r = scr.fill(blanco,(index%ncelx*cellsize+1,index//ncelx*cellsize+1,cellsize-2,cellsize-2))
                move = police.render(str(cartas[index]),1,gris)
                scr.blit(move,move.get_rect(center=(r.center)))
                pygame.display.update(r)
                if primcarta is None: 
                    primcarta = index 
                    firstr = r 
                    continue
                if cartas[index] == cartas[primcarta]:
                    scr.fill(verde,r,special_flags=pygame.BLEND_MIN)
                    scr.fill(verde,firstr,special_flags=pygame.BLEND_MIN)
                    pygame.time.wait(500)
                    pygame.display.update((r,firstr))
                    cartas[index] = cartas[primcarta] = None
                else:
                    pygame.time.wait(500)
                    pygame.display.update((scr.fill(negro,r),scr.fill(negro,firstr)))
                primcarta = None
    else:
        pygame.time.wait(500)
        if play_again(): continue
    break

pygame.quit()

