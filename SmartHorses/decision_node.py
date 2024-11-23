
class DecisionNode:
    def __init__(self, state, move=None, score=0):
        self.state = state
        self.move = move
        self.score = score
        self.children = []
