#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import pygame
import sys
from pygame.locals import *
from random import shuffle
import random
import time
import os
from Instrucciones import *

size = width, height = 500, 400

class Opcion:

    def __init__(self, font, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = font.render(titulo, 1, (255, 255, 255))
        self.imagen_destacada = font.render(titulo, 1, (200, 0, 0))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

    def update(self):
        destino_x = 105
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada
        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()


class Cursor:

    def __init__(self, x, y, dy):
        self.image = pygame.image.load('images/cursor.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y_inicial = y
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

    def update(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)


class Menu:

    def __init__(self, opciones):
        self.opciones = []
        font = pygame.font.Font('font/Dirty Harry.ttf', 22)
        x = 90
        y = 140
        paridad = 1

        self.cursor = Cursor(x - 30, y, 28)

        for titulo, funcion in opciones:
            self.opciones.append(Opcion(font, titulo, x, y, paridad, funcion))
            y += 30
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def update(self,sound,ok):
        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                sound.play()
                self.seleccionado -= 1
            elif k[K_DOWN]:
                sound.play()
                self.seleccionado += 1
            elif k[K_RETURN]:
                ok.play()
                # Invoca a la función asociada a la opción.
                self.opciones[self.seleccionado].activar()

        # procura que el cursor esté entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1
        
        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.update()
     
        for o in self.opciones:
            o.update()

    def imprimir(self, screen):
        """Imprime sobre 'screen' el texto de cada opción del menú."""

        self.cursor.imprimir(screen)

        for opcion in self.opciones:
            opcion.imprimir(screen)
            
def abc_game():
    pygame.mixer.music.stop()
    lose = pygame.mixer.Sound("sound/gameover.wav")
    pygame.mixer.music.load("sound/abc_sound.mp3")
    pygame.mixer.music.play(-1)
    goto = True
    screen = pygame.display.set_mode((800, 504), 0, 32)
    global j

    def Ayuda(screen):      
        Instrucciones(screen, ["CONTROLES:",
        "",
        "Teclas: Letras",                 
        "",
        "OBJETIVO:",
        "Teclea todo el abecedario para ganar",
        "Si te equivocas, empezaras de nuevo y el",
        "juego te dara una ayuda, crees poder",
        "lograrlo?"])
        goto = False


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

    while goto:
        help = Ayuda(screen)
        goto = False
    j = Juego()

def mate_game():
    pygame.mixer.music.stop()
    lose = pygame.mixer.Sound("sound/gameover.wav")
    pygame.mixer.music.load("sound/mate_music.mp3")
    pygame.mixer.music.play(-1)
    goto = True
    screen = pygame.display.set_mode((800, 504), 0, 32)
    global py

    def Ayuda(screen):      
        Instrucciones(screen, ["CONTROLES:",
        "",
        "Teclas: Numeros",                 
        "",
        "OBJETIVO:",
        "Realiza las operaciones para avanzar!!",
        "Si te equivocas, no importa el juego",
        "te dara una ayuda, cuantos puntos",
        "obtendras?"])
        goto = False

    class Program():
        def __init__(self):
                self.size = (300,400)
                self.screen = pygame.display.set_mode(self.size)
                self.pi = 3.14159265358979323846264
                self.digit = 0
                self.right = 0
                self.wrong = 0
                self.digit_a = 1
                self.digit_b = 2
                self.digit_c = 1
                self.digit_d = 2
                self.answer = ""
                self.done = False
                self.operation = "*"
                self.move_on = True
                self.objects = []
                #colors
                self.black = (0,0,0)
                self.white = (255,255,255)
                self.blue = (0,0,255)
                self.green = (0,255,0)
                self.red = (255,0,0)
                #configuration
                self.clock = pygame.time.Clock()
                self.background_image = pygame.image.load("images/backmate.png").convert()
                pygame.font.init()
                self.font1 = pygame.font.Font (None,70)
                self.operand = self.font1.render("*",True,self.red)

        def end_option(self):
                self.operand = py.font1.render(self.operation,True,py.red)
                self.move_on = False
                self.done = True

        def multi(self):
                self.digit_a = 1
                self.digit_b = 100
                self.digit_c = 2
                self.digit_d = 10
                self.operation = "*" 
                self.end_option()

        def addi(self):
                self.digit_a = 100
                self.digit_b = 1000
                self.digit_c = 100
                self.digit_d = 1000
                self.operation = "+"
                self.end_option()

        def subt(self):
                self.digit_a = 100
                self.digit_b = 1000
                self.digit_c = 10
                self.digit_d = 100
                self.operation = "-"
                self.end_option()

        def divid(self):
                self.digit_a = 100
                self.digit_b = 1000
                self.digit_c = 2
                self.digit_d = 10
                self.operation = "/"
                self.end_option()

        def draw(self,algo = True):
                for i in xrange(len(self.objects[h])):
                        self.screen.blit(self.objects[h][i].format,self.objects[h][i].xy)

    while goto:
        help = Ayuda(screen)
        goto = False

    py = Program()

    class Numbers():
        def __init__(self,x,y,a,b,font = 'font1',color = 'black'):
                self.rand = random.randrange(a,b)
                self.format = eval('py.%s.render("%s",True,py.%s)' % (font,self.rand,color))
                self.xy = x,y

    pygame.display.set_caption("Matematicas")

    selec = random.randint(1,4)

    while True:
            py.screen.blit(py.background_image,[0,0])
            pos = pygame.mouse.get_pos()
            x,y = (pos[0],pos[1])
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            sys.exit()
                    
                    if selec == 1:
                            py.multi()
                            break
                    if selec == 2:
                            py.addi()
                            break
                    if selec == 3:
                            py.subt()
                            break
                    if selec == 4:
                            py.divid()
                    
            time.sleep(.005)
            pygame.display.flip()

            py.clock.tick(10)
            once = 0
            selec = random.randint(1,4)
            
            first_number = Numbers(130,90,py.digit_a,py.digit_b)
            second_number = Numbers(130,135,py.digit_c,py.digit_d)
                                    
            py.answered = True
            while py.answered:
                    pos = pygame.mouse.get_pos()
                    x,y = (pos[0],pos[1])
                    py.screen.blit(py.background_image,[0,0])

                    if py.operation == "*":
                            correct = str(first_number.rand * second_number.rand)
                    elif py.operation == "/":
                            correct = str(first_number.rand / second_number.rand)
                    elif py.operation == "+":
                            correct = str(first_number.rand + second_number.rand)
                    elif py.operation == "-":
                            correct = str(first_number.rand - second_number.rand)
                    if py.answer == correct:
                            if not once:
                                    py.right += 1
                                    selec = random.randint(1,4)
                                    if selec == 1:
                                            py.multi()
                                    if selec == 2:
                                            py.addi()
                                    if selec == 3:
                                            py.subt()
                                    if selec == 4:
                                            py.divid()

                            time.sleep(.005)
                            pygame.display.flip()

                            py.answer = ""
                            break
                    elif py.answer != correct:
                            if len(str(correct)) <= len(py.answer):
                                    if not once:
                                            py.wrong += 1
                                            selec = random.randint(1,4)
                                            once = 1
                                            
                                    correct_out = py.font1.render(correct,True,py.black)
                                    py.screen.blit(correct_out,[125,220])

                    for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                    sys.exit()
                    
                            if event.type == pygame.KEYDOWN:
                                    if event.key >= 48 and event.key <= 57:
                                        py.answer += str(event.key - 48)
                                        #print py.answer
                                    elif event.key >= 256 and event.key <= 265:
                                        py.answer += str(event.key - 256)
                                    elif event.key == pygame.K_BACKSPACE:
                                        py.answer = py.answer[0:-1]
                                        py.screen.blit(py.background_image,[0,0])
                                    elif event.key == pygame.K_ESCAPE:
                                        main()

                            py.screen.blit(first_number.format,first_number.xy)
                            py.screen.blit(second_number.format,second_number.xy)
                            py.screen.blit(py.operand,[80,130])
                            pygame.draw.line(py.screen,py.red,[105,190],[210,190],5)

                            py.screen.blit(pygame.font.SysFont("tahoma", 30).render("BIEN!", True, py.green), (50, 270))
                            py.screen.blit(pygame.font.SysFont("tahoma", 30).render("Mal", True, py.red), (200, 270))
                            
                            wrong_out = py.font1.render(str(py.wrong),True,py.black)
                            py.screen.blit(wrong_out,[200,330])

                            right_out = py.font1.render(str(py.right),True,py.black)
                            py.screen.blit(right_out,[70,330])

                            answer_out = py.font1.render(py.answer,True,py.black)
                            py.screen.blit(answer_out,[125,180])

                            pygame.display.flip()
    
def memo_game():
    pygame.mixer.music.stop()
    push = pygame.mixer.Sound("sound/menuok.wav")
    pygame.mixer.music.load("sound/mega.mp3")
    pygame.mixer.music.play(-1)
    algo = True
    
    screen = pygame.display.set_mode((800, 504), 0, 32)

    def Ayuda(screen):      
        Instrucciones(screen, ["CONTROLES:",
        "",
        "Movimiento: Con el raton o mouse",
        "Voltear carta: Click",
        "Regresar: Boton Escape (ESC)",                 
        "",
        "OBJETIVO:",
        "Encuentra todos los pares para ganar!!",
        "Pero ojo!, si te equivocas perderas",
        "oportunidades, en cuanto tiempo lo",
        "lograras?"])
        algo = False
            
    ncelx =  5 
    ncely =  4
    vidas =  20
    cellsize = 80
    orange = (230, 95, 0)

    set_ = list("1234567890")

    verde = pygame.Color("green")
    gris   = pygame.Color("grey20")
    negro   = pygame.Color("black")
    blanco  = pygame.Color("white")

    pygame.mixer.init(44100, -16, 2, 1024)
    pygame.mixer.music.set_volume(0.8)

    while algo:
        help = Ayuda(screen)
        algo = False

    def play_again():
        pygame.mixer.music.stop()
        main()
        #texto = police.render('click para jugar otra vez',1,gris,verde)
        #pygame.display.update(scr.blit(texto,texto.get_rect(center=scrrect.center)))
        #while True:
        #e = pygame.event.wait()
        #if e.type   == pygame.MOUSEBUTTONDOWN: return True
        #elif e.type == pygame.QUIT: return False

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
    pygame.mouse.set_visible(True)
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
                push.play()
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
                        vidas -=1
                        pygame.time.wait(500)
                        pygame.display.update((scr.fill(negro,r),scr.fill(negro,firstr)))
                        
                        if vidas == 0:
                            play_again()
                    
                    primcarta = None
        else:
            pygame.time.wait(500)
        if play_again(): continue
        break

    pygame.quit()
    
def inva_game():
    pygame.mixer.music.stop()
    lose = pygame.mixer.Sound("sound/gameover.wav")
    pygame.mixer.music.load("sound/tema.mp3")
    pygame.mixer.music.play(-1)
    black = (0, 0, 0)
    white = (255, 255, 255)
    algo = True

    def highscore(score):
        Guardar(score)    

    def Ayuda(screen):
        Instrucciones(screen, ["CONTROLES:",
        "",
        "Movimiento: Con el raton o mouse(mira)",
        "Disparo: Click",
        "Regresar: Boton Escape (ESC)",                 
        "",
        "OBJETIVO:",
        "Dispara a tantos aliens como puedas!!",
        "Pero ojo!, dispara solo al de color para",
        "ganar puntos y avanzar en los niveles"])
        algo = False

    screen = pygame.display.set_mode((800, 504), 0, 32)

    x_pos = 0
    y_pos = 0
    prueba = 0
    x_click = 0
    y_click = 0

    x_alien = 0
    y_alien = randint(0, 404)
    x_alien2 = 0
    y_alien2 = randint(0, 404)
    x_alien3 = 0
    y_alien3 = randint(0, 404)

    if y_alien == y_alien2:
        prueba += 1
        y_alien2 = randint(0, 404)

    points = 0
    level = 0
    vidas = 3
    velocity = 2
    errorState = False

    pygame.mixer.init(44100, -16, 2, 1024)
    pygame.mixer.music.set_volume(0.8)

    while algo:
        help = Ayuda(screen)
        algo = False

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                x_pos, y_pos = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONDOWN:
                x_click, y_click = pygame.mouse.get_pos()
                shot = pygame.mixer.Sound("sound/Shotgun.wav")
                shot.play()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
        
        position = (x_pos - 40, y_pos - 40)
        
        x_alien += 1
        x_alien2 += 1
        x_alien3 += 1
        if x_alien * velocity > 800 and not errorState:
            x_alien = 0
            y_alien = randint(0, 404)
            x_alien2 = 0
            y_alien2 = randint(0, 404)
            x_alien3 = 0
            y_alien3 = randint(0, 404)
            if y_alien == y_alien2:
                y_alien2 = randint(0, 404)
            lose.play()
            pygame.mixer.music.stop()
            main()

            errorState = True

        screen.fill(black)
        pygame.mouse.set_visible(False)

        screen.blit(pygame.image.load("images/background_game.png"), (0, 0))
        screen.blit(pygame.font.SysFont("tahoma", 30).render("Puntos: " + str(points), True, black), (650, 450))
        screen.blit(pygame.font.SysFont("tahoma", 30).render("Nivel: " + str(level), True, black), (650, 420))
        screen.blit(pygame.font.SysFont("tahoma", 30).render("Verde", True, black), (650, 390))
        screen.blit(pygame.font.SysFont("tahoma", 30).render("Vidas:" + str(vidas), True, black), (650, 360))

        if (x_click in range(x_alien * velocity - 30, x_alien * velocity + 30) and y_click in range(y_alien - 30, y_alien + 30)):

            points += 5
            velocity += 1
            x_alien = 0
            y_alien = randint(50, 404)
            x_alien2 = 0
            y_alien2 = randint(50, 404)
            x_alien3 = 0
            y_alien3 = randint(50, 404)

            if y_alien == y_alien2:
                y_alien2 = randint(0, 404)
            
        if points == 20:
            level += 1
            velocity = 1
            points = 0
        if vidas == 0:
            lose.play()
            pygame.mixer.music.stop()
            print "testeo: ", prueba
            main()
        screen.blit(pygame.image.load("images/verde.png").convert_alpha(), (x_alien * velocity, y_alien))

        if (x_click in range(x_alien2 * velocity - 30, x_alien2 * velocity + 30) and y_click in range(y_alien2 - 30, y_alien2 + 30)):

            points -= 5
            velocity += 1
            vidas -= 1
            x_alien = 0
            y_alien = randint(50, 404)
            x_alien2 = 0
            y_alien2 = randint(50, 404)
            x_alien3 = 0
            y_alien3 = randint(50, 404)
            if y_alien == y_alien2:
                y_alien2 = randint(0, 404)
            

        if (x_click in range(x_alien3 * velocity - 30, x_alien3 * velocity + 30) and y_click in range(y_alien3 - 30, y_alien3 + 30)):

            points -= 5
            vidas -= 1
            velocity += 1
            x_alien = 0
            y_alien = randint(50, 404)
            x_alien2 = 0
            y_alien2 = randint(50, 404)
            x_alien3 = 0
            y_alien3 = randint(50, 404)
            if y_alien == y_alien2:
                y_alien2 = randint(0, 404)
            

        if  level >= 1:
            screen.blit(pygame.image.load("images/azul.png").convert_alpha(), (x_alien2 * velocity, y_alien2))

        if  level >= 3:
            screen.blit(pygame.image.load("images/rojo.png").convert_alpha(), (x_alien3 * velocity, y_alien3))

        if errorState:
            x_alien = -40
            y_alien = -40     

        screen.blit(pygame.image.load("images/scope.png").convert_alpha(), position)

        pygame.display.update()
        
def highscore():
    #!/usr/bin/python
# vim: set fileencoding=utf-8 :
import os
import sys
import pygame
import cPickle
from pygame import *
"niño" #codificación 
def Guardar(loescrito):
    archivo = open("puntajes.txt", 'w')
    cPickle.dump(loescrito, archivo)
    archivo.close()

def abrir():
    archivo = open("puntajes.txt", 'r')
    puntaje_recuperado=cPickle.load(archivo)
    archivo.close()
    return puntaje_recuperado

puntajes = abrir()
#En esta parte podriamos comparar el
#puntaje obtenido en el juego
#y si es mayor que el menor de la lista

Ancho = 450
Alto = 500
DSM = None
Black = (0,0,0)
White = (250,250,250)

def load_image(name, colorkey=False):
    #crea una ruta a la carpeta de datos
    #al escribirlo de esa forma, nos aseguramos
    #de que pueda abrir en todos los S.O.
    #donde este instalado python
    fullname = os.path.join(name)
    #comprobamos si existe la imagen
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'No se puede cargar la imagen: ', fullname
        raise SystemExit, message
    #combierte la imagen para que pygame la pueda usar
    image = image.convert()
    #En este punto asignamos el colorkey
    #es decir, un color de base al que se
    #borrara dejando solo el canal alfa (transparencia)
    if colorkey:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    #devuelve la imagen y la recta de la imagen
    return (image, image.get_rect())

"""Mira, el objeto con el que se remplaza el "ratón"..."""
class Mira(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        (self.image, self.rect) = load_image('mira.png', True)
    def update(self):
        posicion = pygame.mouse.get_pos()
        self.rect.center = posicion
        # Evita que la mira salga del rango permitido.
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 450:
            self.rect.right = 450
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 450:
            self.rect.bottom = 450
            
""" Creamos una clase para el botton"""
class OKButton(pygame.sprite.Sprite):
    def __init__(self, initialpos):
        (self.initialx, self.initialy)=initialpos
        pygame.sprite.Sprite.__init__(self)
        (self.image, self.rect) = load_image('Ok.png', True)
    def update(self):
        posicion= self.initialx, self.initialy
        self.rect.center = posicion

"""La clase que se encarga de resivir el texto"""
class Escritura():
    def __init__(self):
        self.line = 0
        self.strings = ['',]
        #self.font = pygame.font.Font('dejavu.ttf', 12) #(*1)
        self.font = pygame.font.Font(DSM, 28)
        self.dist = 20
        self.ipos_x = 50
        self.ipos_y = 50
       
    def update(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.strings.append('')
                    self.line += 1
                    print self.line
                elif event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_BACKSPACE:
                    if self.strings[self.line] == '' and self.line > 0:
                        self.strings = self.strings[0:-1]
                        self.line -= 1
                    else:
                        self.strings[self.line] = self.strings[self.line][0:-1]
                else:
                    self.strings[self.line] = (str(self.strings[self.line] + event.unicode))
                   
    def draw(self, screen):
        #print self.strings, self.line
        screen.fill((0, 0, 0))
        for line in range(len(self.strings)):
            img_line = self.font.render(self.strings[line], 1, (255, 255, 255))
            screen.blit(img_line, (self.ipos_x, self.ipos_y + self.dist * line))
    def que_escribio(self):
        return self.strings[0]#Esto es para salvar solo la primera linea del nombre

"""Esta muestra los puntajes"""
def Lospuntajes():
    pygame.init()
    size = (Ancho,Alto)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Puntajes más altos")
    # creamos la ventana y le indicamos un titulo:
    posx = Ancho
    posy = Alto
    #definimos la fuente
    fuente1 = pygame.font.Font(DSM, 25)
    pygame.mouse.set_visible(False)
    sprites = pygame.sprite.RenderClear()
    boton = OKButton((400,400))
    pygame.init()
    mira=Mira()
    sprites.add(mira)
    sprites.add(boton)
    #Reordenamos los elementos de la lista
    puntajes.sort() #Ordena los elementos de menor a mayor
    puntajes.reverse() #Los colocamos de mayor a menor
    cuantos_hay = len(puntajes)
    puntajes.remove(puntajes[cuantos_hay-1])#asi elimina el ultimo de la lista
    i=0
    j=0
    Ejemplo = True
    while Ejemplo:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                Ejemplo = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                Ejemplo = False
        screen.fill(Black)
        puntos1 = str(puntajes[0][0])
        puntos2 = str(puntajes[1][0])
        puntos3 = str(puntajes[2][0])
        nombre1 = puntajes[0][1]
        nombre2 = puntajes[1][1]
        nombre3 = puntajes[2][1]
        #Les asignamos la fuente
        _1 = fuente1.render(u"1°", 1, White)
        _2 = fuente1.render(u"2°", 1, White)
        _3 = fuente1.render(u"3°", 1, White)
        ###########################
        a1 = fuente1.render(puntos1, 1, White)
        a2 = fuente1.render(nombre1, 1, White)
        b1 = fuente1.render(puntos2, 1, White)
        ###########################
        b2 = fuente1.render(nombre2, 1, White)
        c1 = fuente1.render(puntos3, 1, White)
        c2 = fuente1.render(nombre3, 1, White)
        #pasamos a dibujarlos
        screen.blit(_1,(5,(Alto*1/8)))
        screen.blit(a1,((Ancho*3/4),(Alto*1/8)))
        screen.blit(a2,((Ancho/4),(Alto*1/8)))
        #############################
        screen.blit(_2,(5,(Alto*2/8)))
        screen.blit(b1,((Ancho*3/4),(Alto*2/8)))
        screen.blit(b2,((Ancho/4),(Alto*2/8)))
        ##############################
        screen.blit(_3,(5,(Alto*3/8)))
        screen.blit(c1,((Ancho*3/4),(Alto*3/8)))
        screen.blit(c2,((Ancho/4),(Alto*3/8)))
        #####################
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((Ancho, Alto))
    pygame.display.set_caption("Guardar Puntos; Escribe tu nombre")
    pygame.mouse.set_visible(False)
    sprites = pygame.sprite.RenderClear()
    boton = OKButton((400,400))
    pygame.init()
    mira=Mira()
    sprites.add(mira)
    sprites.add(boton)
    escritura = Escritura()
    salir = False
    while salir == False:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                salir = True
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and pygame.sprite.collide_rect(mira, boton):
                print "\n!!!!!!!!!!!!Contanto contacto!!!!!!!!!!!!\n"
                puntajes.insert(0,[3000,escritura.que_escribio()])
                puntajes.sort() #Ordena los elementos de menor a mayor
                puntajes.reverse() #Los colocamos de mayor a menor
                cuantos_hay = len(puntajes)
                puntajes.remove(puntajes[cuantos_hay-1])#asi elimina el ultimo de la lista
                Guardar(puntajes)
                Lospuntajes()
        escritura.update(events)
        display.update()
        sprites.update()
        escritura.draw(screen)
        sprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': 
    main()
    print "Puntos"


def options():
    print "Mustra opciones."

def credits():
    from credit import credit

    text = """CREDITSS
    _                                                 _

    INVASORES

    _Creado por_\\Obed Guevara

    _Sonido_\\http://soundfxnow.com/
    \\http://musicaq.net/

    _Imagenes_\\http://www.bghq.com/

    GRACIAS POR JUGAR!!
    _                                                 _

    ©Copyright 2014"""

    #~ utiliser '\\' pour aligner les lignes de texte
    font = pygame.font.Font('font/Dirty Harry.ttf', 13)
    color = 0xa0a0a000

    credit(text,font,color)


def exit_game():
    print "Saliendo del programa."
    sys.exit(0)

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    print "iniciando juego"

    sound = pygame.mixer.Sound("sound/menumove.wav")
    ok = pygame.mixer.Sound("sound/menuok.wav")
    pygame.mixer.music.load("sound/intro.mp3")
    pygame.mixer.music.play(-1)

    menu_game = [
        ("Invasores", inva_game),
        ("Memorama", memo_game),
        ("Matematicas", mate_game),
        ("Abecedario", abc_game),
        ("Opciones", options),
        ("Creditos", credits),
        ("Puntuacion", highscore),
        ("Salir", exit_game)
        ]

    screen = pygame.display.set_mode(size)
    background = pygame.image.load("images/background.jpg").convert()
    menu = Menu(menu_game)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        screen.blit(background, (0, 0))
        menu.update(sound,ok)
        menu.imprimir(screen)

        pygame.display.flip()
        pygame.time.delay(10)

if __name__ == '__main__':
    main()
