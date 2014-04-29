#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import sys
import time

class Program():
        def __init__(self):
                self.size = (300,400)
                self.screen = pygame.display.set_mode(self.size)
                self.pi = 3.14159265358979323846264 #from memory :)
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

        def draw(self,h):
                for i in xrange(len(self.objects[h])):
                        self.screen.blit(self.objects[h][i].format,self.objects[h][i].xy)
                        
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