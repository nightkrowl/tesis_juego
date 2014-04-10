#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame
from pygame import *

class Pantalla:

    COLOR_OK = (255, 255, 255)
    COLOR_MAL = (255, 0, 0)
    P_ANCHO = 400
    P_ALTO = 300
    Y_INICIAL = 70
    
    def __init__(self):
        pygame.font.init()
        pygame.display.set_icon(pygame.image.load(os.path.join("data", "icono.gif")))
        self.pantalla = pygame.display.set_mode((self.P_ANCHO, self.P_ALTO))
        self.limpiar()
        pygame.display.set_caption("Pi.")
        self.clock = pygame.time.Clock()
        ruta = os.path.join("data", "cubicfive10.ttf")
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
        self.tres()
        self.setCuadraditos()
        self.refresh()
        
    def limpiar(self):
        self.pantalla.fill((0, 0, 0))
        
    def setNumOK(self, num):
        self.setNum(num, self.COLOR_OK)
        
    def setNumMAL(self, num):
        self.setNum(num + "!", self.COLOR_MAL)
        
    def setNum(self, num, color):
        txt = self.font.render(str(num), True, color)
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
        if not self.iniciado:
            self.presentacion()
        self.refresh()
    
    def presentacion(self):
        txt1 = self.fontG.render("Pi x r^2", True, self.COLOR_OK)
        txt2 = self.fontC.render("Franr.com.ar/pi", True, self.COLOR_OK)
        txt3 = self.fontC.render("Francisco Rivera - 2010", True, self.COLOR_OK)
        txt4 = self.fontC.render("[Press Enter]", True, self.COLOR_OK)
        self.pantalla.blit(txt1, ((self.P_ANCHO - txt1.get_width())/2, 10))
        self.pantalla.blit(txt2, ((self.P_ANCHO - txt2.get_width())/2, 240))
        self.pantalla.blit(txt3, ((self.P_ANCHO - txt3.get_width())/2, 260))
        self.pantalla.blit(txt4, ((self.P_ANCHO - txt4.get_width())/2, (self.P_ALTO - txt4.get_height())/2))
    
    def tres(self):
        txt = self.fontG.render("3,", True, self.COLOR_OK)
        self.pantalla.blit(txt, ((self.P_ANCHO - txt.get_width())/2, 10))
        
    def gano(self):
        self.limpiar()
        txt1 = self.fontG.render("Felicidades!", True, self.COLOR_OK)
        txt2 = self.fontC.render("Te aprendiste los primeros 50 decimales de Pi.", True, self.COLOR_OK)
        txt3 = self.fontC.render("Ya te podes morir tranquilo.", True, self.COLOR_OK)
        self.pantalla.blit(txt1, ((self.P_ANCHO - txt1.get_rect().w)/2, 50))
        self.pantalla.blit(txt2, ((self.P_ANCHO - txt2.get_rect().w)/2, 100))
        self.pantalla.blit(txt3, ((self.P_ANCHO - txt3.get_rect().w)/2, 226))
        self.refresh()
        
    def setCuadraditos(self):
        linea = pygame.Surface((30, 5))
        linea.fill(self.COLOR_OK)
        for y in range(1, 6):
            for x in range(0, self.P_ANCHO, 40):
                self.pantalla.blit(linea, (x, self.Y_INICIAL + (40*y + 2)))
    

class HandlerTeclado:

    def __init__(self):
        self.iniciado = False
        
    def update(self, perdio):
        if perdio:
            pygame.event.clear()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                num = u""
                num+=event.unicode
                print event.unicode
                if num == 27:
                    return False
                    
                return str(num)
                #num = None
                #if event.key >= 48 and event.key <= 57:
                #    num = event.key - 48
                #elif event.key >= 256 and event.key <= 265:
                #    num = event.key - 256
                #if num is not None:
                #    return str(num)
        teclas = pygame.key.get_pressed()
        if teclas[K_RETURN]:
            self.iniciado = True
        return True
        
class Juego:

    DEC_PI = "abcdefghijklmnñopqrstuvwxyz"
    
    def __init__(self):
        self.teclado = HandlerTeclado()
        self.pantalla = Pantalla()        
        self.main()
        
    def reiniciar(self):
        self.indice = 0
        self.pantalla.reiniciar()
        
    def check(self, num):
        if self.getDecActual() == num:
            self.indice += 1
            if self.indice == len(self.DEC_PI):
                return "g"
            return True
        else:
            return False
            
    def getDecActual(self):
        return self.DEC_PI[self.indice]
        
    def getDecAnt(self):
        return self.DEC_PI[self.indice - 1]
        
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
                        self.pantalla.setNumOK(self.getDecAnt())                        
                else:
                    self.pantalla.setNumMAL(self.getDecActual())
                    self.pantalla.update()
                    pygame.time.wait(2000)                        
                    self.reiniciar()
                    perdio = True
        pygame.quit()

j = Juego()