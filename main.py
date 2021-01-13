import pygame
import sys
from colorama import init
from juego import *

def main():
    pygame.init()

    screen = pygame.display.set_mode(tamaño)
    pygame.display.set_caption('Tres en raya')

    done = False
    
    clock = pygame.time.Clock()

    game = Juego()

    while not done:
        done = game.proceso_eventos()
        game.correr_logica()
        game.frame_pantalla(screen)
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()