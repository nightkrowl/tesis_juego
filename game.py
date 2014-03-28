#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import pygame
import sys
from pygame.locals import *
from random import shuffle
import random
import operator


size = width, height = 500, 370

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

    def update(self,sound):
        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                sound.play()
                self.seleccionado -= 1
            elif k[K_DOWN]:
                sound.play()
                self.seleccionado += 1
            elif k[K_RETURN]:
                sound.play()
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


def mate_game():
    pygame.mixer.music.stop()
    lose = pygame.mixer.Sound("sound/gameover.wav")
    pygame.mixer.music.load("sound/mate_music.mp3")
    pygame.mixer.music.play()
    black = (0, 0, 0)
    white = (255, 255, 255)
    orange = (230, 95, 0) 
    green = (127, 255, 0)
    red = (255, 0, 0)
    blue = (0, 23, 69)

    screen = pygame.display.set_mode((400, 400), 0, 32)
    
    nivel = 1
    vidas = 3
    bien = 0
    timepo = 0
    aumento = 0

    pygame.mixer.init(44100, -16, 2, 1024)
    pygame.mixer.music.set_volume(0.8)
    #print "La operacion es:", a, operadores, b, "="

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                pygame.mixer.music.stop()
                sys.exit()
            elif e.type == pygame.KEYDOWN: 
                if e.type == pygame.K_0: 
                    usuario = 0
                elif e.type == pygame.K_1: 
                    usuario = 1
                elif e.type == pygame.K_2: 
                    usuario = 2
                elif e.type == pygame.K_3: 
                    usuario = 3
                elif e.type == pygame.K_4: 
                    usuario = 4  
                elif e.type == pygame.K_5: 
                    usuario = 5
                elif e.type == pygame.K_6: 
                    usuario = 6
                elif e.type == pygame.K_7: 
                    usuario = 7
                elif e.type == pygame.K_8: 
                    usuario = 8
                elif e.type == pygame.K_9: 
                    usuario = 9
    

        operadores = random.choice([operator.add, operator.sub, operator.mul, operator.div])

        a=random.randint(1,10)
        b=random.randint(1,10)

        resultado = operadores(a,b)

        if operadores == operator.add:
            operadores = "+"
            tiempo = 10
        elif operadores == operator.sub:
            operadores = "-"
            tiempo = 10
        elif operadores == operator.mul:
            operadores = "*"
            tiempo = 20
        elif operadores == operator.div:
            operadores = "/"
            tiempo = 20

        screen.blit(pygame.font.SysFont("tahoma", 30).render("Nivel: " + str(nivel), True, orange), (200, 350))
        screen.blit(pygame.font.SysFont("tahoma", 30).render("Vidas: " + str(vidas), True, black), (170, 320))

        screen.blit(pygame.font.SysFont("tahoma", 30).render("Resuelvelo " + str(a) + str(operadores) + str(b), True, white), (150, 200))
       

        screen.fill(blue)

            
        while tiempo > 0:  
            tiempo -= 1 
            screen.blit(pygame.font.SysFont("tahoma", 30).render("Tiempo restante: " + str(tiempo), True, white), (80, 200))
        
            if usuario == resultado:
                screen.blit(pygame.font.SysFont("tahoma", 30).render("BIEN! El resultado es: " + str(resultado), True, green), (150, 200))
                while True:
                    event = pygame.event.wait()
                    if event.type   == pygame.K_KP_ENTER: 
                        return True
                    elif event.type == pygame.QUIT: 
                        return False
                bien += 1
                aumento += 1
                pygame.display.update()

            else:
                screen.blit(pygame.font.SysFont("tahoma", 30).render("Incorrecto, el resultado era: " + str(resultado), True, red), (150, 200))
                while True:
                    event = pygame.event.wait()
                    if event.type   == pygame.K_KP_ENTER:
                        return True
                    elif event.type == pygame.QUIT: 
                        return False
                vidas -= 1
                break
                pygame.display.update()

        #if aumento == 5:
         #   operadores.append(operator.mul)
        #if aumento == 10:
         #   operadores.append(operator.div)

        if bien == 5:
            nivel += 1
            vidas += 1

        if vidas == 0:
            pygame.mixer.music.stop()
            main()

        pygame.display.update()

def memo_game():
        pygame.mixer.music.stop()
    push = pygame.mixer.Sound("sound/menuok.wav")
    pygame.mixer.music.load("sound/mega.mp3")
    pygame.mixer.music.play()
    
    ncelx =  5 
    ncely =  4
        vidas =  6
    cellsize = 80

    set_ = list("abcdefghijkl") 

    verde = pygame.Color("green")
    gris   = pygame.Color("grey20")
    negro   = pygame.Color("black")
    blanco  = pygame.Color("white")

    pygame.mixer.init(44100, -16, 2, 1024)
    pygame.mixer.music.set_volume(0.8)

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
                        vidas -= 1
                pygame.display.update(r)
                        if vidas == 0:
                            play_again()
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

def inva_game():
    pygame.mixer.music.stop()
    lose = pygame.mixer.Sound("sound/gameover.wav")
    pygame.mixer.music.load("sound/tema.mp3")
    pygame.mixer.music.play()
    black = (0, 0, 0)
    white = (255, 255, 255)
    clock = pygame.time.Clock()

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

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                x_pos, y_pos = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONDOWN:
                x_click, y_click = pygame.mouse.get_pos()
        
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
            shot = pygame.mixer.Sound("sound/Shotgun.wav")
            shot.play()

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
            shot = pygame.mixer.Sound("sound/Shotgun.wav")
            shot.play()

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
            shot = pygame.mixer.Sound("sound/Shotgun.wav")
            shot.play()
            
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
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))

def highscore():
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
    pygame.mixer.music.load("sound/intro.mp3")
    pygame.mixer.music.play(-1)

    menu_game = [
        ("Invasores", inva_game),
        ("Memorama", memo_game),
        ("Matematicas", mate_game),
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
        menu.update(sound)
        menu.imprimir(screen)

        pygame.display.flip()
        pygame.time.delay(10)

if __name__ == '__main__':
    main()
