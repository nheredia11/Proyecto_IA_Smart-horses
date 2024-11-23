
import pygame
import sys
from menu import Menu
from smart_horses_game import SmartHorsesGame
from game_state import GameState

WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 8
SCREEN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Smart Horses")
    menu = Menu()
    game = None
    game_state = GameState.MENU
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == GameState.MENU:
                    if menu.handle_click(pygame.mouse.get_pos()):
                        game = SmartHorsesGame(menu.ia1_difficulty, menu.ia2_difficulty)
                        game_state = GameState.PLAYING
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_state == GameState.FINISHED:
                    game_state = GameState.MENU
                    menu = Menu()

        if game_state == GameState.MENU:
            menu.draw(SCREEN)
        elif game_state == GameState.PLAYING:
            game.update()
            game.draw()
            if game.game_over:
                game_state = GameState.FINISHED
        
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
