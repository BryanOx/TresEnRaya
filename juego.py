from pygame.locals import *
import pygame
import numpy as np

ancho = 620
alto = 620
tamaño = (ancho,alto)

ROJO = (255,0,0)
VERDE = (0,255,0)
GRIS = (50,50,50)
BLANCO = (255,255,255)


class Juego(object):
    def __init__(self):
        self.inicio = True
        self.partida = False
        self.jugada = True
        self.movimientos = 9

        self.jugador1 = ''
        self.jugador2 = ''

        #   ESPACIOS DEL TABLERO (RECTANGULOS)
        esp00 = pygame.Rect(0, 0, 200, 200)
        esp01 = pygame.Rect(210, 0, 200, 200)
        esp02 = pygame.Rect(420, 0, 200, 200)
        esp10 = pygame.Rect(0, 210, 200, 200)
        esp11 = pygame.Rect(210, 210, 200, 200)
        esp12 = pygame.Rect(420, 210, 200, 200)
        esp20 = pygame.Rect(0, 420, 200, 200)
        esp21 = pygame.Rect(210, 420, 200, 200)
        esp22 = pygame.Rect(420, 420, 200, 200)
        #--------------------------------------

        self.tablero = np.zeros((3,3))

        self.espTab = {
            '0,0':esp00, '0,1':esp01, '0,2':esp02,
            '1,0':esp10, '1,1':esp11, '1,2':esp12,
            '2,0':esp20, '2,1':esp21, '2,2':esp22
        }

    def colocarFicha(self, pos):
        col = int(pos[0])
        fil = int(pos[2])
        if self.jugada:
            print(col,fil)
            self.tablero[col,fil] = 1
            self.jugada=False
        else:
            self.tablero[col,fil] = 2
            self.jugada=True
        print(self.tablero)
        self.movimientos -= 1

    def proceso_eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
            if event.type == MOUSEBUTTONDOWN:
                for esp in self.espTab:
                    if self.espTab.get(esp).collidepoint(event.pos):
                        if self.tablero[int(esp[0]),int(esp[2])] == 0:
                            self.colocarFicha(esp)
                            print('Ficha colocada en el espacio: ',esp)
        return False
    
    def correr_logica(self):
        if self.tablero[0,0] == 1 and self.tablero[0,1] == 1 and self.tablero[0,2] == 1 or self.tablero[1,0] == 1 and self.tablero[1,1] == 1 and self.tablero[1,2] == 1 or self.tablero[2,0] == 1 and self.tablero[2,1] == 1 and self.tablero[2,2] == 1 or self.tablero[0,0] == 1 and self.tablero[1,1] == 1 and self.tablero[2,2] == 1 or self.tablero[0,2] == 1 and self.tablero[1,1] == 1 and self.tablero[2,0] == 1 or self.tablero[0,0] == 1 and self.tablero[1,0] == 1 and self.tablero[2,0] == 1 or self.tablero[0,1] == 1 and self.tablero[1,1] == 1 and self.tablero[2,1] == 1 or self.tablero[0,2] == 1 and self.tablero[1,2] == 1 and self.tablero[2,2] == 1:
            print('Felicitaciones, el jugador 1 ha ganado!!')
            self.__init__()
        if self.tablero[0,0] == 2 and self.tablero[0,1] == 2 and self.tablero[0,2] == 2 or self.tablero[1,0] == 2 and self.tablero[1,1] == 2 and self.tablero[1,2] == 2 or self.tablero[2,0] == 2 and self.tablero[2,1] == 2 and self.tablero[2,2] == 2 or self.tablero[0,0] == 2 and self.tablero[1,1] == 2 and self.tablero[2,2] == 2 or self.tablero[0,2] == 2 and self.tablero[1,1] == 2 and self.tablero[2,0] == 2 or self.tablero[0,0] == 2 and self.tablero[1,0] == 2 and self.tablero[2,0] == 2 or self.tablero[0,1] == 2 and self.tablero[1,1] == 2 and self.tablero[2,1] == 2 or self.tablero[0,2] == 2 and self.tablero[1,2] == 2 and self.tablero[2,2] == 2:
            print('Felicitaciones, el jugador 2 ha ganado!!')
            self.__init__()
        if self.movimientos == 0:
            print('No hay movimientos para realizar, termina en empate.')
            self.__init__()

    def frame_pantalla(self, screen):
        screen.fill(BLANCO)
        if inicio:
            pass
        elif partida:
            for esp in self.espTab:
                col = int(esp[0])
                fil = int(esp[2])
                pygame.draw.rect(screen, GRIS, self.espTab.get(esp))
                cuadro = self.espTab.get(esp)
                if self.tablero[col,fil] == 1:
                    pygame.draw.line(screen, ROJO, cuadro.topleft, cuadro.bottomright, 10)
                    pygame.draw.line(screen, ROJO, cuadro.topright, cuadro.bottomleft, 10)
                elif self.tablero[col,fil] == 2:
                    pygame.draw.circle(screen, VERDE, cuadro.center, cuadro.width/2, 10)
        pygame.display.flip()