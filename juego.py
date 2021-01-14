from pygame.locals import *
import pygame
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from clases import *

ancho = 620
alto = 620
tamaño = (ancho,alto)

ROJO = (255,0,0)
VERDE = (0,255,0)
GRIS = (50,50,50)
GRISclaro = (180,180,180)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

Base = declarative_base()

class Perfil(Base):
    __tablename__ = 'perfiles'
    
    Nombre = Column(String(50),  primary_key=True)
    Victorias = Column(Integer)
    Derrotas = Column(Integer)
    Empates = Column(Integer)

class Juego(object):
    def __init__(self):
        self.inicio = True
        self.seleccionNombres = False
        self.partida = False
        self.final = False
        self.empate = False
        self.jugada = False

        self.movimientos = 9

        self.jugador1 = Jugador1('')
        self.jugador2 = Jugador2('')

        self.ganador = ''

        self.fuenteN = pygame.font.SysFont('Comic Sans MS', 65)
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
        self.botonINICIO = pygame.Rect(160, 260, 300, 80)
        self.botonSALIR = pygame.Rect(160, 410, 300, 80)
        #--------------------------------------
        #   SELECCION NOMBRES PARA LOS JUGADORES
        self.cuadroJ1 = pygame.Rect(80, 210, 460, 80)
        self.cuadroJ2 = pygame.Rect(80, 410, 460, 80)
        self.activo1 = False
        self.activo2 = False
        self.colINP1 = GRIS
        self.colINP2 = GRIS

        self.botonStart = pygame.Rect(520, 560, 80, 40)
        self.COLORstart = NEGRO
        self.botonBack = pygame.Rect(20, 560, 80, 40)
        self.COLORback = NEGRO
        #--------------------------------------

        self.tablero = np.zeros((3,3))

        self.espTab = {
            '0,0':esp00, '0,1':esp01, '0,2':esp02,
            '1,0':esp10, '1,1':esp11, '1,2':esp12,
            '2,0':esp20, '2,1':esp21, '2,2':esp22
        }

        #   DATABASE
        engine = create_engine('sqlite:///perfiles.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        #--------------------------------------

    def guardarPartida(self, jug):
        if (self.session.query(Perfil).get(jug.nombre)==None):
            jug = Perfil(
                Nombre = jug.nombre,
                Victorias = jug.Victorias,
                Derrotas = jug.Derrotas,
                Empates = jug.Derrotas
            )
            self.session.add(jug)
            self.session.commit()
        else:
            PerfilG = self.session.query(Perfil).get(jug.nombre)
            PerfilG.Victorias += jug.Victorias
            PerfilG.Derrotas += jug.Derrotas
            PerfilG.Empates += jug.Empates
            self.session.commit()

    def colocarFicha(self, pos):
        col = int(pos[0])
        fil = int(pos[2])
        if self.jugada:
            self.tablero[col,fil] = self.jugador1.num
            self.jugada = not self.jugada
        else:
            self.tablero[col,fil] = self.jugador2.num
            self.jugada = not self.jugada
        print(f'Jugada realizada en la posición: {col},{fil}')
        self.movimientos -= 1
        if self.movimientos > 0:
            print(f'Movimientos restantes: {self.movimientos}')

    def proceso_eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return True
                if self.activo1:
                    if event.key == K_RETURN:
                        self.activo1 = False
                        self.colINP1 = GRIS
                    if event.key == K_BACKSPACE:
                        self.jugador1.nombre = self.jugador1.nombre[:-1]
                    else:
                        if not event.key == K_RETURN:
                            self.jugador1.nombre += event.unicode
                if self.activo2:
                    if event.key == K_RETURN:
                        self.activo2 = False
                        self.colINP2 = GRIS
                    if event.key == K_BACKSPACE:
                        self.jugador2.nombre = self.jugador2.nombre[:-1]
                    else:
                        if not event.key == K_RETURN:
                            self.jugador2.nombre += event.unicode
                if (self.final or self.empate) and event.key == K_SPACE:
                    self.__init__()
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
                    if self.cuadroJ1.collidepoint(event.pos):
                        self.activo1 = not self.activo1
                        self.colINP1 = GRISclaro
                    if self.cuadroJ2.collidepoint(event.pos):
                        self.activo2 = not self.activo2
                        self.colINP2 = GRISclaro
                    if self.botonBack.collidepoint(event.pos):
                        self.inicio = True
                        self.seleccionNombres = False
                    if self.botonStart.collidepoint(event.pos):
                        self.seleccionNombres = False
                        self.partida = True
                        self.jugada = True
            if event.type == MOUSEMOTION:
                if self.botonStart.collidepoint(event.pos): self.COLORstart = BLANCO
                else: self.COLORstart = NEGRO
                if self.botonBack.collidepoint(event.pos): self.COLORback = BLANCO
                else: self.COLORback = NEGRO
        return False
    
    def correr_logica(self):

        if self.tablero[0,0] == 1 and self.tablero[0,1] == 1 and self.tablero[0,2] == 1 or self.tablero[1,0] == 1 and self.tablero[1,1] == 1 and self.tablero[1,2] == 1 or self.tablero[2,0] == 1 and self.tablero[2,1] == 1 and self.tablero[2,2] == 1 or self.tablero[0,0] == 1 and self.tablero[1,1] == 1 and self.tablero[2,2] == 1 or self.tablero[0,2] == 1 and self.tablero[1,1] == 1 and self.tablero[2,0] == 1 or self.tablero[0,0] == 1 and self.tablero[1,0] == 1 and self.tablero[2,0] == 1 or self.tablero[0,1] == 1 and self.tablero[1,1] == 1 and self.tablero[2,1] == 1 or self.tablero[0,2] == 1 and self.tablero[1,2] == 1 and self.tablero[2,2] == 1:
            self.jugador1.Victorias += 1 ; self.jugador2.Derrotas += 1
            self.final = True
            self.ganador = self.jugador1.nombre

        elif self.tablero[0,0] == 2 and self.tablero[0,1] == 2 and self.tablero[0,2] == 2 or self.tablero[1,0] == 2 and self.tablero[1,1] == 2 and self.tablero[1,2] == 2 or self.tablero[2,0] == 2 and self.tablero[2,1] == 2 and self.tablero[2,2] == 2 or self.tablero[0,0] == 2 and self.tablero[1,1] == 2 and self.tablero[2,2] == 2 or self.tablero[0,2] == 2 and self.tablero[1,1] == 2 and self.tablero[2,0] == 2 or self.tablero[0,0] == 2 and self.tablero[1,0] == 2 and self.tablero[2,0] == 2 or self.tablero[0,1] == 2 and self.tablero[1,1] == 2 and self.tablero[2,1] == 2 or self.tablero[0,2] == 2 and self.tablero[1,2] == 2 and self.tablero[2,2] == 2:
            self.jugador2.Victorias += 1 ; self.jugador1.Derrotas += 1
            self.final = True
            self.ganador = self.jugador2.nombre

        elif self.movimientos == 0:
            self.jugador1.Empates += 1 ; self.jugador2.Empates += 1
            self.empate = True

        if self.final or self.empate:
            self.guardarPartida(self.jugador1) ; self.guardarPartida(self.jugador2)

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
            inicio_rect = inicio.get_rect(center=(ancho/2, 300))
            screen.blit(inicio, inicio_rect)

            salir = self.fuente.render('Salir', True, NEGRO)
            salir_rect = salir.get_rect(center=(ancho/2, 450))
            screen.blit(salir, salir_rect)

        if self.seleccionNombres:
            pygame.draw.rect(screen, self.colINP1, self.cuadroJ1, border_radius=10)
            nombreX = self.fuente.render('Jugador "X"', True, NEGRO)
            nombreX_rect = nombreX.get_rect(center=(ancho/2,150))
            screen.blit(nombreX, nombreX_rect)

            nombreJ1 = self.fuenteN.render(self.jugador1.nombre, True, NEGRO)
            screen.blit(nombreJ1, (self.cuadroJ1.x+5, self.cuadroJ1.y+5))

            pygame.draw.rect(screen, self.colINP2, self.cuadroJ2, border_radius=10)
            nombreO = self.fuente.render('Jugador "O"', True, NEGRO)
            nombreO_rect = nombreO.get_rect(center=(ancho/2,350))
            screen.blit(nombreO, nombreO_rect)

            nombreJ2 = self.fuenteN.render(self.jugador2.nombre, True, NEGRO)
            screen.blit(nombreJ2, (self.cuadroJ2.x+5, self.cuadroJ2.y+5))

            pygame.draw.rect(screen, VERDE, self.botonStart, border_radius=20)
            pygame.draw.polygon(screen, self.COLORstart,[(545, 565), (545, 595), (585, 580)])
            pygame.draw.rect(screen, ROJO, self.botonBack, border_radius=20)
            pygame.draw.polygon(screen, self.COLORback, [(75, 565), (75, 595), (35, 580)])

        if self.partida:
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
        
        if self.final:
            print('Felicitaciones, {} ha ganado este juego.')

        if self.empate:
            print('La partida ha terminado en empate.')

        pygame.display.flip()