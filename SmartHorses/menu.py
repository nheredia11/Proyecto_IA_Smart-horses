
import pygame
from button import Button
from difficulty import Difficulty
from typing import Tuple

class Menu:
    def __init__(self):
        self.buttons_ia1 = [
            Button(50, 150, 120, 40, "Beginner", (0, 255, 0)),
            Button(50, 200, 120, 40, "Amateur", (0, 0, 255)),
            Button(50, 250, 120, 40, "Expert", (255, 0, 0))
        ]
        self.buttons_ia2 = [
            Button(430, 150, 120, 40, "Beginner", (0, 255, 0)),
            Button(430, 200, 120, 40, "Amateur", (0, 0, 255)),
            Button(430, 250, 120, 40, "Expert", (255, 0, 0))
        ]
        self.start_button = Button(250, 400, 100, 50, "Start", (0, 255, 0))
        self.ia1_difficulty = None
        self.ia2_difficulty = None
        self.font = pygame.font.Font(None, 32)

    def draw(self, surface):
        surface.fill((255, 255, 255))
        title = self.font.render("Smart Horses - AI vs AI", True, (0, 0, 0))
        ia1_text = self.font.render("AI 1 Difficulty", True, (0, 0, 0))
        ia2_text = self.font.render("AI 2 Difficulty", True, (0, 0, 0))
        
        surface.blit(title, (300 - title.get_width()//2, 50))
        surface.blit(ia1_text, (50, 100))
        surface.blit(ia2_text, (430, 100))

        for button in self.buttons_ia1 + self.buttons_ia2:
            button.draw(surface)
        self.start_button.draw(surface)

        pygame.display.flip()

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        for i, button in enumerate(self.buttons_ia1):
            if button.is_clicked(pos):
                self.ia1_difficulty = list(Difficulty)[i]
                for b in self.buttons_ia1:
                    b.selected = False
                button.selected = True

        for i, button in enumerate(self.buttons_ia2):
            if button.is_clicked(pos):
                self.ia2_difficulty = list(Difficulty)[i]
                for b in self.buttons_ia2:
                    b.selected = False
                button.selected = True

        if self.start_button.is_clicked(pos) and self.ia1_difficulty and self.ia2_difficulty:
            return True
        return False
