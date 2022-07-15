from asyncio.windows_events import NULL
import pygame
from colour import Color

pygame.init()
font = pygame.font.SysFont(pygame.font.get_fonts()[0], 30)

WHITE = (255, 255, 255)
LIGHT = (244, 236, 195)
BROWN = (123, 100, 25)
BLUE = (82, 185, 240)
GRAY = (125, 125, 125)
GREEN = (94, 150, 70)
PINK = (193, 95, 190)
RED = (200, 0, 0)
PURPLE = (44, 7, 53)
BLACK = (0, 0, 0)
GRADIENT1 = Color("red")
GRADIENT2 = Color("green")

SPEED = 50

BORDER_BOTTOM = 260

class Interface:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h+BORDER_BOTTOM
        self.blockW = w/300
        self.blockH = h/82

        #init display
        self.display= pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Trabalho 1')
        self.clock = pygame.time.Clock()
    
    def add_map(self, map):
        self.map = map
    
    def add_percorreu(self, percorreu):
        self.percorreu = percorreu
    
    def add_andou(self, path):
        self.andou = path

    def add_steps(self, steps):
        self.steps = steps
    
    def update(self,percorreu, path, step, custos):
        self.add_percorreu(percorreu)
        self.add_andou(path)
        self._update_ui(step, custos)
        self.clock.tick(SPEED)
    
    def _update_ui(self, step, custos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.display.fill(WHITE)
        
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.percorreu[i][j] != 0:
                    pygame.draw.rect(self.display, RED, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                else:
                    terrain = self.map[i][j]
                    if terrain == ".":
                        pygame.draw.rect(self.display, LIGHT, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                    elif terrain == "R":
                        pygame.draw.rect(self.display, BROWN, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                    elif terrain == "F":
                        pygame.draw.rect(self.display, GREEN, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                    elif terrain == "A":
                        pygame.draw.rect(self.display, BLUE, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                    elif terrain == "M":
                        pygame.draw.rect(self.display, GRAY, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                    else:
                        pygame.draw.rect(self.display, PINK, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
        for ponto in self.andou:
            pygame.draw.rect(self.display, PURPLE, pygame.Rect(ponto[1]*self.blockW, ponto[0]*self.blockH, self.blockW, self.blockH))
        text = font.render('Etapa: ' + str(step+1), True, BLACK)
        self.display.blit(text, [0, 0])
        s = "CUSTOS\n"
        for i in range(31):
            if i != 0 and i%8 == 0:
                s += "\n"
            if i < len(custos):
                custo = custos[i]
                s += "Etapa "+ str(i+1).zfill(2)+": "+ str(int(custo)).zfill(3)+"  "
            else:
                s += "Etapa "+ str(i+1).zfill(2)+": 000  "
        s = s.split("\n")
        linhas = []
        for linha in s:
            linhas.append(font.render(linha, True, BLACK))
        for i in range(len(linhas)):
            self.display.blit(linhas[i], [0, self.h-BORDER_BOTTOM+i*30])
        pygame.display.flip()
    
    def finish(self, path):
        self.add_andou(path)
        count = 0
        for etapa in self.andou:
            count += len(etapa)
        self.add_steps(count)
        self.update_finish()
        self.clock.tick(SPEED)
    
    def update_finish(self, participants = NULL, custos = 0, dificuldade = 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        colors = list(GRADIENT1.range_to(GRADIENT2,self.steps))
        self.display.fill(WHITE)
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                terrain = self.map[i][j]
                if terrain == ".":
                    pygame.draw.rect(self.display, LIGHT, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                elif terrain == "R":
                    pygame.draw.rect(self.display, BROWN, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                elif terrain == "F":
                    pygame.draw.rect(self.display, GREEN, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                elif terrain == "A":
                    pygame.draw.rect(self.display, BLUE, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                elif terrain == "M":
                    pygame.draw.rect(self.display, GRAY, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                else:
                    pygame.draw.rect(self.display, PINK, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
        count = 0
        for etapa in self.andou:
            for ponto in etapa:
                pygame.draw.rect(self.display, (Color(colors[count]).red*255,Color(colors[count]).green*255,Color(colors[count]).blue*255), pygame.Rect(ponto[1]*self.blockW, ponto[0]*self.blockH, self.blockW, self.blockH))
                count += 1
        if (participants == NULL):
            self.display.blit(font.render("Calculando participantes de cada etapa(Pode levar algum tempo)", True, BLACK), [0, self.h-BORDER_BOTTOM])
        else:
            custo = 0
            s = ""
            for i in range(len(custos)):
                custo += custos[i]
            for i in range(7):
                if (i == 0):
                    s += "Aang: "
                elif (i == 1):
                    s += "Zukko: "
                elif (i == 2):
                    s += "Toph: "
                elif (i == 3):
                    s += "Katara: "
                elif (i == 4):
                    s += "Sokka: "
                elif (i == 5):
                    s += "Appa: "
                else:
                    s += "Momo: "
                for j, val in enumerate(participants[i]):
                    if val == 1:
                        s += str(j+1) + "  "
                #aux = " ".join(str(e) for e in participants[i])
                #s += aux
                s += "\n"
            s = s.split("\n")
            linhas = []
            for linha in s:
                linhas.append(font.render(linha, True, BLACK))
            for i in range(len(linhas)):
                self.display.blit(linhas[i], [0, self.h-BORDER_BOTTOM+i*30])
            self.display.blit(font.render("Custo total: {:} + {:.6f} = {:.6f}".format(custo, dificuldade, custo+dificuldade), True, BLACK), [0, self.h-BORDER_BOTTOM+7*30])
        print("FIM")
        pygame.display.flip()