import numpy as np
from piece.pawn import Pawn
from piece.king import King
from piece.bishop import Bishop
from piece.knight import Knight
from piece.queen import Queen
from piece.rook import Rook


class Ai:
    def __init__(self, ai_game, board, depth):
        self.depth = depth
        self.board = board
        self.ai_game = ai_game
        self.piece_values = {
            Pawn: 10,
            Knight: 30,
            Bishop: 30,
            Rook: 50,
            Queen: 90,
            King: 1000,
        }


    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.game_active == False:
            return self.evaluate_board(self.board)


        if maximizing_player:
            legal_moves = self.board.get_specific_legal_moves('b')
            max_eval = float('-inf')
            for piece, possible_moves in legal_moves:
                for move, capture in possible_moves:
                    self.board.fake_push((piece, move), capture)
                    eval = self.minimax_alpha_beta(self.board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    self.board.fake_pop()
                    if beta <= alpha:
                        return max_eval
            return max_eval
        else:
            min_eval = float('inf')
            legal_moves = self.board.get_specific_legal_moves('w')
            for piece, possible_moves in legal_moves:
                for move, capture in possible_moves:
                    self.board.fake_push((piece, move), capture)
                    eval = self.minimax_alpha_beta(self.board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    self.board.fake_pop()
                    if beta <= alpha:
                        return min_eval
            return min_eval

    def get_best_move(self, fen):
        #self.board = self.board(self.ai_game)
        #self.board._init_from_FEN(fen)
        #self.board.turn = 'b'
        best_move = None
        max_eval = float('-inf')
        legal_moves = self.board.get_specific_legal_moves('b')
        initial_positions = []
        for piece, possible_moves in legal_moves:
            initial_positions.append((piece, piece.square))
        print(self.evaluate_board(self.board))
        for piece, possible_moves in legal_moves:
            for move, capture in possible_moves:
                old_pos = piece.square
                self.board.fake_push((piece, move), capture)
                eval = self.minimax_alpha_beta(self.board, self.depth - 1, float('-inf'), float('inf'), False)
                if eval > max_eval:
                    max_eval = eval
                    # print("move: ", move)
                    # print("score: ", max_eval)
                    best_move = (piece, move)
                self.board.fake_pop()
        for piece, pos in initial_positions:
            best_piece, move = best_move
            if (piece == best_piece):
                initial_pos = pos
                break
        print("best: ", max_eval, best_move[1])
        return initial_pos, best_move[1]

    def evaluate_board(self, board):
        # Implement a self.board evaluation function here to assign a score to a given self.board state.
        # The higher the score, the better the self.board for the AI.
        # You can use a simple material-based evaluation or a more complex evaluation function.
        # Sample material-based evaluation function:
        score = 0
        piece_table = {
            Queen: np.array([
                [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
            ]),

            King: np.array([
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
            ]),

            Knight: np.array([
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 2.0, -3.0],
                [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
            ]),

            Rook: np.array([
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
            ]),

            Pawn: np.array([
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ]),

            Bishop: np.array([
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
            ])
            
        }
        all_pieces = self.board.black_pieces.sprites() + self.board.white_pieces.sprites()
        for piece in all_pieces:
            if self.board.turn == 'b':
                score += piece_table[type(piece)][piece.square[0], piece.square[1]]
            else:
                score += np.flip(piece_table[type(piece)])[piece.square[0], piece.square[1]] * (-1)
            if piece.color == 'w':
                score += self.piece_values[type(piece)] * -1
            else:
                score += self.piece_values[type(piece)]
        #print("score", score)
        return score