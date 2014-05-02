#!/usr/bin/env python
import sys, os, math, random
import pygame
from pygame.locals import *

class Score(pygame.sprite.Sprite):

    def __init__(self, xy,points):
        pygame.sprite.Sprite.__init__(self)
        self.score = points

class NameSprite(pygame.sprite.Sprite):

    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.xy = xy
        self.text = ''
        self.color = (0, 255, 0)
        self.font = pygame.font.Font(None, 35) 
        self.reRender()

    def addLetter(self, letter):
        self.text += str(letter)
        self.reRender()

    def removeLetter(self):
        if len(self.text) == 1:
            self.text = ''
        else:
            self.text = self.text[:-1]
        self.reRender()

    def reRender(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.xy


class Game(object):

    def __init__(self,points):
        print points
        pygame.init()
        self.window = pygame.display.set_mode((520, 545))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pygame Tutorial 4 - Breakout")
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        self.background = pygame.image.load(os.path.join('images','background.JPG'))
        self.window.blit(self.background, (0,0))
        pygame.display.flip()
        self.isReset = True
        self.playing = True
        self.enteringname = False
        self.score = Score((75, 575), points)
        self.namesprites = pygame.sprite.RenderUpdates()
        self.handleHighScores()


    def run(self):
        print 'Empezando'

        running = True
        while running:
            self.clock.tick(60)
            running = self.handleEvents()
            pygame.display.set_caption('Puntuaciones')

            if self.enteringname:
                font = pygame.font.Font(None, 35)
                color = (0, 255, 0)
                nameimage = font.render('Enter Name:', True, color)
                namerect = nameimage.get_rect()
                namerect.center = 260, 250
                self.window.blit(nameimage,namerect)

                self.namesprites.clear(self.window, self.background)
                dirty = self.namesprites.draw(self.window)
                pygame.display.update(dirty+[namerect])

        print 'Saliendo'

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False

                if self.enteringname:
                    if event.key == K_BACKSPACE:
                        self.namesprite.removeLetter()
                    elif event.key == K_RETURN:
                        self.nameEntered()

                    else:
                        try:
                            char = chr(event.key)
                            if str(char) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_':
                                self.namesprite.addLetter(char)
                        except:
                            pass
        return True

    def handleHighScores(self):
        highscores = self.parseHighScores()

        if self.score.score > int(highscores[-1][1]):
            self.enteringname = True
            self.namesprite = NameSprite( (260, 310) )
            self.namesprites.add(self.namesprite)
        else:
            self.showHighScores(highscores)

    def nameEntered(self):
        self.enteringname = False
        username = self.namesprite.text

        self.window.blit(self.background, (0,0))
        pygame.display.flip()

        highscores = self.parseHighScores()

        newscores = []
        for name, score in highscores:
            if self.score.score > int(score):
                newscores.append((username, str(self.score.score)))
                self.score.score = 0
            newscores.append((name, score))
        newscores = newscores[0:10]

        highscorefile = 'highscores.txt'
        f = open(highscorefile, 'w')
        for name, score in newscores:
            f.write("%s:%s\n" % (name, score))
        f.close()

        self.showHighScores(newscores)

    def parseHighScores(self):
        highscorefile = 'highscores.txt'
        if os.path.isfile(highscorefile):
            f = open(highscorefile, 'r')
            lines = f.readlines()
            scores = []
            for line in lines:
                scores.append( line.strip().split(':'))
            return scores
        else:
            f = open(highscorefile, 'w')
            f.write("""obed:10000
elisa:9000
marlen:8000
GGG:7000
FFF:6000
EEE:5000
DDD:4000
CCC:3000
BBB:2000
AAA:1000""")
            f.close()
            return self.parseHighScores()

    def showHighScores(self, scores):
        font = pygame.font.Font(None, 35)
        color = (0, 255, 0)

        for i in range(len(scores)):
            name, score = scores[i]
            nameimage = font.render(name, True, color)
            namerect = nameimage.get_rect()
            namerect.left, namerect.y = 40, 40 + (i*(namerect.height + 20))
            self.window.blit(nameimage,namerect)

            scoreimage = font.render(score, True, color)
            scorerect = scoreimage.get_rect()
            scorerect.right, scorerect.y = 480, namerect.y
            self.window.blit(scoreimage, scorerect)

            for d in range(namerect.right + 25, scorerect.left-10, 25):
                pygame.draw.rect(self.window, color, pygame.Rect(d, scorerect.centery, 5, 5))

        pygame.display.flip()