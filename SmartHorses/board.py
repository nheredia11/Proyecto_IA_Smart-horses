
import random
from horse import Horse

class Board:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.points = {}
        self.multipliers = set()
        self.setup_board()
    
    def setup_board(self):
        white_pos = (random.randint(0, 7), random.randint(0, 7))
        black_pos = (random.randint(0, 7), random.randint(0, 7))
        while black_pos == white_pos:
            black_pos = (random.randint(0, 7), random.randint(0, 7))
        
        self.white_horse = Horse(*white_pos, True)
        self.black_horse = Horse(*black_pos, False)
        
        available_positions = [(x, y) for x in range(8) for y in range(8)
                             if (x, y) != white_pos and (x, y) != black_pos]
        
        point_positions = random.sample(available_positions, 10)
        for i, pos in enumerate(point_positions):
            self.points[pos] = i + 1
            available_positions.remove(pos)
        
        multiplier_positions = random.sample(available_positions, 4)
        self.multipliers = set(multiplier_positions)
