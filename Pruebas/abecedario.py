#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame
import unicodedata
from pygame import *

class Pantalla:

    COLOR_NEU = (0, 0, 0)
    COLOR_MAL = (255, 0, 0)
    P_ANCHO = 350
    P_ALTO = 250
    Y_INICIAL = 70
    COLOR_OK = (0, 255, 0)
    def __init__(self):
        pygame.font.init()
        self.pantalla = pygame.display.set_mode((self.P_ANCHO, self.P_ALTO))
        self.limpiar()
        pygame.display.set_caption("Abecedario.")
        self.clock = pygame.time.Clock()
        ruta = os.path.join("font", "cubicfive10.ttf")
        self.fontC = pygame.font.Font(ruta, 12)
        self.font = pygame.font.Font(ruta, 28)
        self.fontG = pygame.font.Font(ruta, 40)
        self.iniciado = False
        
    def iniciar(self):
        self.iniciado = True
        self.reiniciar()
        
    def reiniciar(self):
        self.fx = 0
        self.fy = 80
        self.limpiar()
        self.setCuadraditos()
        self.refresh()
        
    def limpiar(self):
        self.pantalla.fill((245, 245, 220))
        
    def setcharOK(self, char):
        self.setchar(char, self.COLOR_OK)
        
    def setcharMAL(self, char):
        self.setchar(char + "!", self.COLOR_MAL)
        
    def setchar(self, char, color):
        txt = self.font.render(str(char), True, color)
        self.pantalla.blit(txt, (self.fx, self.fy))
        if self.fx + 40 >= self.P_ANCHO:
            self.fx = 0
            self.fy += 40
        else:
            self.fx += 40
        
    def refresh(self):
        pygame.display.update()
        pygame.event.pump()
        self.clock.tick(30)
        
    def update(self):
        self.refresh()
        
    def gano(self):
        self.limpiar()
        txt1 = self.fontG.render("Felicidades!", True, self.COLOR_NEU)
        txt2 = self.fontC.render("Te aprendiste el abecedario.", True, self.COLOR_NEU)
        self.pantalla.blit(txt1, ((self.P_ANCHO - txt1.get_rect().w)/2, 50))
        self.pantalla.blit(txt2, ((self.P_ANCHO - txt2.get_rect().w)/2, 100))
        self.refresh()
        
    def setCuadraditos(self):
        linea = pygame.Surface((25, 5))
        linea.fill(self.COLOR_NEU)
        for y in range(1, 4):
            for x in range(0, self.P_ANCHO, 40):
                self.pantalla.blit(linea, (x, self.Y_INICIAL + (40*y + 2)))
    

class Teclado:

    def __init__(self):
        self.iniciado = False
        
    def update(self, perdio):
        if perdio:
            pygame.event.clear()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                char = None
                if event.key >= 32 and event.key <= 126:
                    char = event.unicode
                    #print char
                if char is not None:
                    return str(char)
        teclas = pygame.key.get_pressed()
        if teclas[K_ESCAPE]:
            return False
        while self.iniciado == False:
            self.iniciado = True
        return True
        
class Juego:

    Abecedario = "abcdefghijklmnopqrstuvwxyz"
    
    def __init__(self):
        self.teclado = Teclado()
        self.pantalla = Pantalla()        
        self.main()
        
    def reiniciar(self):
        self.indice = 0
        self.pantalla.reiniciar()
        
    def check(self, char):
        if self.getDecActual() == char:
            self.indice += 1
            if self.indice == len(self.Abecedario):
                return "g"
            return True
        else:
            return False
            
    def getDecActual(self):
        return self.Abecedario[self.indice]
        
    def getDecAnt(self):
        return self.Abecedario[self.indice - 1]
        
    def gano(self):
        self.pantalla.gano()
        pygame.time.wait(10000)
    
    def main(self):
        while not self.teclado.iniciado:
            self.teclado.update(False)
            self.pantalla.update()
        self.pantalla.iniciar()
        self.reiniciar()
        r = True
        perdio = False
        while r:
            r = self.teclado.update(perdio)
            perdio = False
            self.pantalla.update()
            if r not in (True, False):
                n = self.check(r)
                if n:
                    if n == 'g':
                        self.gano()
                        break
                    else:
                        self.pantalla.setcharOK(self.getDecAnt())                        
                else:
                    self.pantalla.setcharMAL(self.getDecActual())
                    self.pantalla.update()
                    pygame.time.wait(2000)                        
                    self.reiniciar()
                    perdio = True
        pygame.quit()

j = Juego()