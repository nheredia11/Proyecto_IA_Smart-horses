
from typing import List, Tuple

class Horse:
    def __init__(self, x: int, y: int, is_white: bool):
        self.x = x
        self.y = y
        self.is_white = is_white
        self.points = 0
        self.has_multiplier = False
        
    def get_valid_moves(self, other_horse: 'Horse') -> List[Tuple[int, int]]:
        moves = []
        possible_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
        ]
    
        for dx, dy in possible_moves:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                if (new_x, new_y) != (other_horse.x, other_horse.y):
                    moves.append((new_x, new_y))
        return moves
