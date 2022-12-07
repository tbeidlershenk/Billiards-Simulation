import pygame
from sys import exit
import Config as cg
from Game import Game
 
pygame.init()

pygame.display.set_caption(cg.FRAME_NAME)
game = Game()
print("Controls: space to shoot toward mouse, r to reset.")
clock = pygame.time.Clock()
time = 0

while True:
    
    game.handle_events(pygame.event.get())

    # game.train_network()

    if not game.game_paused:
        game.draw_game_components()

    game.update_game_state()

    pygame.display.update() 
    time = time + 1
    clock.tick(cg.FRAMERATE)

