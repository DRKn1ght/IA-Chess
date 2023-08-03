from Board.board import Board
import numpy as np
from piece.pawn import Pawn
from piece.king import King
from piece.bishop import Bishop
from piece.knight import Knight
from piece.queen import Queen
from piece.rook import Rook


class Ai:
    def __init__(self, ai_game, depth):
        self.depth = depth
        self.ai_game = ai_game
        self.piece_values = {
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9,
            King: 100,
        }


    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.game_active == False:
            return self.evaluate_board(board)

        legal_moves = board.get_legal_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for piece, possible_moves in legal_moves:
                for move, capture in possible_moves:
                    board.fake_push((piece, move))
                    eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                    if capture:
                        print(capture.name)
                        eval += self.piece_values[type(capture)]
                    board.fake_pop()
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for piece, possible_moves in legal_moves:
                for move, capture in possible_moves:
                    board.fake_push((piece, move))
                    eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                    if capture:
                        #print(capture.name)
                        eval -= self.piece_values[type(capture)]
                    board.fake_pop()
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def get_best_move(self, fen):
        board = Board(self.ai_game)
        board._init_from_FEN(fen)
        board.turn = 'b'
        best_move = None
        max_eval = float('-inf')
        legal_moves = board.get_legal_moves()
        initial_positions = []
        for piece, possible_moves in legal_moves:
            initial_positions.append((piece, piece.square))

        for piece, possible_moves in legal_moves:
            for move, capture in possible_moves:
                board.fake_push((piece, move))
                eval = self.minimax_alpha_beta(board, self.depth - 1, float('-inf'), float('inf'), False)
                if capture:
                    #print(capture.name)
                    eval += self.piece_values[type(capture)]
                board.fake_pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = (piece, move)
        for piece, pos in initial_positions:
            best_piece, move = best_move
            if (piece == best_piece):
                initial_pos = pos
                break
        return initial_pos, best_move[1]

    def evaluate_board(self, board):
        # Implement a board evaluation function here to assign a score to a given board state.
        # The higher the score, the better the board for the AI.
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

        for piece in board.black_pieces:
            score += piece_table[type(piece)][piece.square[0], piece.square[1]]
            score += self.piece_values[type(piece)]
        for piece in board.white_pieces:
            score -= piece_table[type(piece)][piece.square[0], piece.square[1]]
            score -= self.piece_values[type(piece)]
        return score