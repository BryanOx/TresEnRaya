from pygame.locals import *
import pygame
import numpy as np

ancho = 620
alto = 620
tamaño = (ancho,alto)

ROJO = (255,0,0)
VERDE = (0,255,0)
GRIS = (50,50,50)
GRISclaro = (180,180,180)
NEGRO = (0,0,0)
BLANCO = (255,255,255)


class Juego(object):
    def __init__(self):
        self.COLORstart = NEGRO
        self.COLORback = NEGRO
        self.inicio = True
        self.seleccionNombres = False
        self.partida = False
        self.jugada = True
        self.movimientos = 9

        self.jugador1 = 'Jugador X'
        self.jugador2 = 'Jugador O'

        self.fuente = pygame.font.SysFont('Comic Sans MS', 75)
        self.fuente2 = pygame.font.SysFont('Forte',80)

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
        #   BOTONES DEL MENU DE INICIO
        self.botonINICIO = pygame.Rect(160, 210, 300, 80)
        self.botonSALIR = pygame.Rect(160, 410, 300, 80)
        #--------------------------------------
        #   SELECCION NOMBRES PARA LOS JUGADORES
        self.cuadroJ1 = pygame.Rect(80, 210, 460, 80)
        self.cuadroJ2 = pygame.Rect(80, 410, 460, 80)

        self.botonStart = pygame.Rect(520, 560, 80, 40)
        self.botonBack = pygame.Rect(20, 560, 80, 40)
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
            self.tablero[col,fil] = 1
            self.jugada=False
        else:
            self.tablero[col,fil] = 2
            self.jugada=True
        print(f'Jugada realizada en la posición: {col},{fil}')
        self.movimientos -= 1

    def proceso_eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
            if event.type == MOUSEBUTTONDOWN:
                if self.partida:
                    for esp in self.espTab:
                        if self.espTab.get(esp).collidepoint(event.pos):
                            if self.tablero[int(esp[0]),int(esp[2])] == 0:
                                self.colocarFicha(esp)
                if self.inicio:
                    if self.botonINICIO.collidepoint(event.pos):
                        self.inicio = False
                        self.seleccionNombres = True
                    if self.botonSALIR.collidepoint(event.pos):
                        return True
                if self.seleccionNombres:
                    if self.botonBack.collidepoint(event.pos):
                        self.inicio = True
                        self.seleccionNombres = False
                    if self.botonStart.collidepoint(event.pos):
                        self.seleccionNombres = False
                        self.partida = True
            if event.type == MOUSEMOTION:
                if event.type == MOUSEMOTION:
                    if self.botonStart.collidepoint(event.pos): self.COLORstart = BLANCO
                    else: self.COLORstart = NEGRO
                    if self.botonBack.collidepoint(event.pos): self.COLORback = BLANCO
                    else: self.COLORback = NEGRO
        return False
    
    def correr_logica(self):
        if self.tablero[0,0] == 1 and self.tablero[0,1] == 1 and self.tablero[0,2] == 1 or self.tablero[1,0] == 1 and self.tablero[1,1] == 1 and self.tablero[1,2] == 1 or self.tablero[2,0] == 1 and self.tablero[2,1] == 1 and self.tablero[2,2] == 1 or self.tablero[0,0] == 1 and self.tablero[1,1] == 1 and self.tablero[2,2] == 1 or self.tablero[0,2] == 1 and self.tablero[1,1] == 1 and self.tablero[2,0] == 1 or self.tablero[0,0] == 1 and self.tablero[1,0] == 1 and self.tablero[2,0] == 1 or self.tablero[0,1] == 1 and self.tablero[1,1] == 1 and self.tablero[2,1] == 1 or self.tablero[0,2] == 1 and self.tablero[1,2] == 1 and self.tablero[2,2] == 1:
            print(f'Felicitaciones, {self.jugador1} ha ganado!!')
            self.__init__()
        if self.tablero[0,0] == 2 and self.tablero[0,1] == 2 and self.tablero[0,2] == 2 or self.tablero[1,0] == 2 and self.tablero[1,1] == 2 and self.tablero[1,2] == 2 or self.tablero[2,0] == 2 and self.tablero[2,1] == 2 and self.tablero[2,2] == 2 or self.tablero[0,0] == 2 and self.tablero[1,1] == 2 and self.tablero[2,2] == 2 or self.tablero[0,2] == 2 and self.tablero[1,1] == 2 and self.tablero[2,0] == 2 or self.tablero[0,0] == 2 and self.tablero[1,0] == 2 and self.tablero[2,0] == 2 or self.tablero[0,1] == 2 and self.tablero[1,1] == 2 and self.tablero[2,1] == 2 or self.tablero[0,2] == 2 and self.tablero[1,2] == 2 and self.tablero[2,2] == 2:
            print(f'Felicitaciones, {self.jugador2} ha ganado!!')
            self.__init__()
        if self.movimientos == 0:
            print('No hay movimientos para realizar, termina en empate.')
            self.__init__()

    def frame_pantalla(self, screen):
        screen.fill(BLANCO)
        if self.inicio:
            TRES = self.fuente2.render('¡Tres en', True, NEGRO)
            TRES_rect = TRES.get_rect(center=(ancho/2, 50))
            screen.blit(TRES, TRES_rect)
            RAYA = self.fuente2.render('Raya!', True, NEGRO)
            RAYA_rect = RAYA.get_rect(center=(ancho/2, 120))
            screen.blit(RAYA, RAYA_rect)

            pygame.draw.rect(screen, VERDE, self.botonINICIO, border_radius=10)
            pygame.draw.rect(screen, ROJO, self.botonSALIR, border_radius=10)
            inicio = self.fuente.render('Iniciar', True, NEGRO)
            inicio_rect = inicio.get_rect(center=(ancho/2, 250))
            screen.blit(inicio, inicio_rect)

            salir = self.fuente.render('Salir', True, NEGRO)
            salir_rect = salir.get_rect(center=(ancho/2, 450))
            screen.blit(salir, salir_rect)

        if self.seleccionNombres:
            pygame.draw.rect(screen, GRISclaro, self.cuadroJ1, border_radius=10)
            nombreX = self.fuente.render('Jugador "X"', True, NEGRO)
            nombreX_rect = nombreX.get_rect(center=(ancho/2,150))
            screen.blit(nombreX, nombreX_rect)

            pygame.draw.rect(screen, GRISclaro, self.cuadroJ2, border_radius=10)
            nombreO = self.fuente.render('Jugador "O"', True, NEGRO)
            nombreO_rect = nombreO.get_rect(center=(ancho/2,350))
            screen.blit(nombreO, nombreO_rect)

            pygame.draw.rect(screen, VERDE, self.botonStart, border_radius=20)
            pygame.draw.polygon(screen, self.COLORstart,[(545, 565), (545, 595), (585, 580)])
            pygame.draw.rect(screen, ROJO, self.botonBack, border_radius=20)
            pygame.draw.polygon(screen, self.COLORback, [(75, 565), (75, 595), (35, 580)])

        elif self.partida:
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