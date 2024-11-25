
import pygame
import time
import random
from typing import List, Tuple, Optional
from board import Board
from game_state import GameState
from decision_node import DecisionNode
from horse import Horse

WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 8
SCREEN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

class SmartHorsesGame:
    def __init__(self, ia1_difficulty, ia2_difficulty):
        self.board = Board()
        self.ia1_difficulty = ia1_difficulty
        self.ia2_difficulty = ia2_difficulty
        self.current_turn = True  # True para IA1, False para IA2
        self.game_state = GameState.PLAYING
        self.game_over = False
        self.selected_horse = None
        self.valid_moves = []
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.last_move_time = time.time()
        self.moves_without_points = 0
        self.state_counts_white = {}
        self.state_counts_black = {}
        self.max_state_repetitions = 5
        self.last_positions_white = []  
        self.last_positions_black = []  
        self.max_positions_memory = 50
        self.recent_positions_limit = 50
        self.move_delay = 1.5  # Segundos entre movimientos
        
        # Cargar las imágenes de los caballos
        try:
            self.white_horse_image = pygame.image.load('SmartHorses/images/white_horse.png').convert_alpha()
            self.black_horse_image = pygame.image.load('SmartHorses/images/black_horse.png').convert_alpha()
            # Escalar imágenes al tamaño de la celda
            self.white_horse_image = pygame.transform.scale(self.white_horse_image, (CELL_SIZE, CELL_SIZE))
            self.black_horse_image = pygame.transform.scale(self.black_horse_image, (CELL_SIZE, CELL_SIZE))
        except pygame.error as e:
            print(f"Error al cargar imágenes: {e}")
            self.white_horse_image = None
            self.black_horse_image = None
    
    def draw(self):
        # Dibujar tablero
        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (139, 69, 19)
                pygame.draw.rect(pygame.display.get_surface(), color, 
                               (col * 75, row * 75, 75, 75))
                
                # Dibujar puntos
                pos = (col, row)
                if pos in self.board.points:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(self.board.points[pos]), True, (0, 0, 255))
                    text_rect = text.get_rect(center=(col * 75 + 37, row * 75 + 37))
                    pygame.display.get_surface().blit(text, text_rect)
                
                # Dibujar multiplicadores
                if pos in self.board.multipliers:
                    font = pygame.font.Font(None, 36)
                    text = font.render("x2", True, (255, 215, 0))
                    text_rect = text.get_rect(center=(col * 75 + 37, row * 75 + 37))
                    pygame.display.get_surface().blit(text, text_rect)
        
        # Dibujar caballos
        self.draw_horse(self.board.white_horse)
        self.draw_horse(self.board.black_horse)
        
        # Dibujar puntuaciones
        self.draw_scores()
        
        # Si el juego ha terminado, mostrar el ganador
        if self.game_over:
            self.show_winner()
        
        pygame.display.flip()
    
    def draw_horse(self, horse: Horse):
      GOLD = (255, 215, 0)
      # Seleccionar la imagen del caballo
      image = self.white_horse_image if horse.is_white else self.black_horse_image

      # Calcular las coordenadas para centrar la imagen en la celda
      x = horse.x * CELL_SIZE
      y = horse.y * CELL_SIZE
      width, height = image.get_size()  # Obtener el tamaño de la imagen

      # Dibujar la imagen del caballo
      SCREEN.blit(image, (x, y))

      # Si el caballo tiene un multiplicador, dibujar un borde adaptado
      if horse.has_multiplier:
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, GOLD, rect, 3)  # Borde dorado alrededor de la imagen
    
    def draw_scores(self):
        font = pygame.font.Font(None, 36)
        white_text = font.render(f"White: {self.board.white_horse.points}", True, (0, 0, 0))
        black_text = font.render(f"Black: {self.board.black_horse.points}", True, (0, 0, 0))
        pygame.display.get_surface().blit(white_text, (10, 10))
        pygame.display.get_surface().blit(black_text, (10, 40))

    def build_decision_tree(self, horse, opponent, depth, is_maximizing):
        if depth == 0 or self.game_over:
            current_score = self.utility_ia1(horse, opponent) if is_maximizing else self.utility_ia2(horse, opponent)
            return DecisionNode(self.get_state_hash(horse), score=current_score)

        node = DecisionNode(self.get_state_hash(horse))
        valid_moves = self.get_filtered_valid_moves(horse, opponent)

        for move in valid_moves:
            # Guardar el estado antes del movimiento
            old_x, old_y = horse.x, horse.y
            old_points = horse.points
            old_multiplier = horse.has_multiplier
            old_board_points = self.board.points.copy()
            old_board_multipliers = self.board.multipliers.copy()

            # Realizar movimiento
            self.make_move(horse, move[0], move[1])
            child_node = self.build_decision_tree(opponent, horse, depth - 1, not is_maximizing)
            child_node.move = move
            node.children.append(child_node)

            # Restaurar el estado
            horse.x, horse.y = old_x, old_y
            horse.points = old_points
            horse.has_multiplier = old_multiplier
            self.board.points = old_board_points
            self.board.multipliers = old_board_multipliers

        return node

    def evaluate_tree_with_minimax(self, node, alpha, beta, is_maximizing):
        if not node.children:  # Nodo hoja
            return node.score, node.move

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            for child in node.children:
                eval_score, _ = self.evaluate_tree_with_minimax(child, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = child.move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            # Introducir aleatoriedad si todos los movimientos son iguales
            if len(set(child.score for child in node.children)) == 1:
                random_child = random.choice(node.children)
                return random_child.score, random_child.move

            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for child in node.children:
                eval_score, _ = self.evaluate_tree_with_minimax(child, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = child.move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

        return min_eval, best_move


    def minimax(self, depth: int, alpha: float, beta: float, is_maximizing: bool) -> Tuple[float, Optional[Tuple[int, int]]]:
        # Construir y evaluar el árbol de decisiones
        current_horse = self.board.white_horse if is_maximizing else self.board.black_horse
        opponent = self.board.black_horse if is_maximizing else self.board.white_horse
        decision_tree = self.build_decision_tree(current_horse, opponent, depth, is_maximizing)
        best_value, best_move = self.evaluate_tree_with_minimax(decision_tree, alpha, beta, is_maximizing)
        return best_value, best_move

    def get_filtered_valid_moves(self, horse: Horse, other_horse: Horse) -> List[Tuple[int, int]]:
        #Primero obtenemos todos los movimientos válidos básicos
        basic_moves = horse.get_valid_moves(other_horse)

        #Si el caballo tiene un multiplicador activo, se debe filtrar las casillas con multiplicador
        if horse.has_multiplier:
            return [move for move in basic_moves if move not in self.board.multipliers]
        
        #Si no tiene multiplicador, retorna los movimientos válidos
        return basic_moves
    
    def utility_ia1(self, horse: Horse, opponent: Horse) -> float:
        score = horse.points * 3.0

        #analisis de movimientos validos
        valid_moves = horse.get_valid_moves(opponent)
        points_map = {move: self.board.points.get(move,0) for move in valid_moves}

        if points_map:
            #priorizar movimientos con mayor potencial de puntos
            best_move = max(points_map,key=points_map.get)
            score += points_map[best_move]*4.0

            #bonus por puntos totales disponibles
            total_avaliable_points = sum(points_map.values())
            score += total_avaliable_points * 2.5

        # Bonus por multiplicadores
        if horse.has_multiplier:
            score += 50.0

        # Penalización por estados repetidos
        state_hash = self.get_state_hash(horse)
        state_counts = self.state_counts_white if horse.is_white else self.state_counts_black
        repetition_penalty = state_counts.get(state_hash, 0) * 10
        score -= repetition_penalty

        #estrategia de control de tablero
        board_control = len(valid_moves)/64
        score += board_control * 30.0

        # Penalización por falta de progreso
        if self.moves_without_points > 3:
            score -= 50
        
        #bonus por distancia
        distances_to_opponent = abs(horse.x-opponent.x) + abs(horse.y-opponent.y)
        if 3 <= distances_to_opponent <= 5:
            score += 20.0
        return score

    def utility_ia2(self, horse: Horse, opponent: Horse) -> float:
        score = horse.points * 2.5
    
        # Evaluar movimientos disponibles priorizando puntos altos
        valid_moves = horse.get_valid_moves(opponent)
        points_available = [self.board.points.get(move, 0) for move in valid_moves]
        
        if points_available:
            max_point_move = max(points_available)
            score += max_point_move* 3.0
            score += sum(points_available)*2.0
    
        # Bonus por multiplicadores
        if horse.has_multiplier:
            score += 40.0
        
        # Penalización por estados repetidos
        state_hash = self.get_state_hash(horse)
        state_counts = self.state_counts_white if horse.is_white else self.state_counts_black
        repetition_penalty = state_counts.get(state_hash, 0) * 15
        score -= repetition_penalty

        #bonus por exploracion del tablero
        board_coverage = len(valid_moves)/64  #proporción de movimientos posibles
        score += board_coverage*20.0

        # Penalización por falta de progreso
        if self.moves_without_points > 3:
            score -= 30
        
        #penalizar cercania al oponente
        distance_to_opponent = abs(horse.x - opponent.x) + abs(horse.y - opponent.y)
        if distance_to_opponent > 4:
            score += 15.0
        elif distance_to_opponent < 2:
            score -= 10.0
    
        return score
    
    def get_state_hash(self, horse: Horse) -> tuple:
        return (
            horse.x,
            horse.y,
            horse.has_multiplier,
            horse.points,
            tuple(sorted(self.board.points.keys())),
            tuple(sorted(self.board.multipliers))
        )

    def update_last_positions(self, horse: Horse):
        positions = self.last_positions_white if horse.is_white else self.last_positions_black
        positions.append((horse.x, horse.y))
        if len(positions) > self.max_positions_memory:
            positions.pop(0)

    def make_move(self, horse: Horse, x: int, y: int):
        # Validar estado repetido antes de hacer el movimiento
        pos = (x, y)
        state_counts = self.state_counts_white if horse.is_white else self.state_counts_black
        
        # Incrementar contador para estados repetidos
        state_hash = self.get_state_hash(horse)
        state_counts[state_hash] = state_counts.get(state_hash, 0) + 1
        
        #Actualizar posicion del caballo
        horse.x, horse.y = x,y
        if state_counts.get(pos, 0) >= self.max_state_repetitions:
            return  # Evitar el movimiento si se repite demasiadas veces

        # Recoger puntos si es posible
        if pos in self.board.points:
            points = self.board.points[pos]
            if horse.has_multiplier:
                points *= 2
                horse.has_multiplier = False
            horse.points += points
            del self.board.points[pos]
            self.moves_without_points = 0  # Reiniciar inactividad
            self.state_counts_white.clear()
            self.state_counts_black.clear()
        else:
            self.moves_without_points += 1

        # Recoger multiplicador si es posible
        if pos in self.board.multipliers:
            horse.has_multiplier = True
            self.board.multipliers.remove(pos)

        # Verificar fin del juego
        self.game_over = len(self.board.points) == 0

    def check_game_over(self) -> bool:
        return len(self.board.points) == 0
    
    def update(self):
        current_time = time.time()
    
        if self.game_state == GameState.PLAYING and not self.game_over:
            # Verifica si es momento de realizar un movimiento
            if current_time - self.last_move_time >= self.move_delay:
                previous_turn = self.current_turn
                self.make_ai_move()  # Realiza el movimiento de la IA
                if self.current_turn != previous_turn:
                    self.last_move_time = current_time

        elif self.game_over:
            self.game_state = GameState.FINISHED

    def show_winner(self):
        font = pygame.font.Font(None, 74)
        if self.board.white_horse.points > self.board.black_horse.points:
            text = font.render("White Wins!", True, (0, 0, 0))
        elif self.board.white_horse.points < self.board.black_horse.points:
            text = font.render("Black Wins!", True, (0, 0, 0))
        else:
            text = font.render("It's a Tie!", True, (0, 0, 0))
        
        text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2-50))
        SCREEN.blit(text, text_rect)

        pygame.display.flip()
    
    
    def make_ai_move(self):
        if self.game_over:
            return
    
        difficulty = self.ia1_difficulty if self.current_turn else self.ia2_difficulty
        current_horse = self.board.white_horse if self.current_turn else self.board.black_horse
        opponent_horse = self.board.black_horse if self.current_turn else self.board.white_horse
        
        #obtener todos los movimientos validos
        valid_moves = self.get_filtered_valid_moves(current_horse,opponent_horse)

        #Obtener movimientos con puntos
        moves_with_point = [
            move for move in valid_moves
            if move in self.board.points
        ]

        #obtener el mejor movimiento con minimax
        _, best_move = self.minimax(difficulty.value, float('-inf'), float('inf'), self.current_turn)

        #Si no hay movimientos con puntos o el mejor movimiento no contiene puntos
        if not best_move or best_move not in self.board.points:
            #priorizar movimientos con puntos si existen
            if moves_with_point:
                best_move = random.choice(moves_with_point)
            elif valid_moves:
                best_move = random.choice(valid_moves)

        if best_move:
            self.make_move(current_horse, best_move[0], best_move[1])
            self.current_turn = not self.current_turn
