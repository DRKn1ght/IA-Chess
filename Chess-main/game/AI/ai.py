from Board.board import Board
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

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        legal_moves = list(board.legal_moves)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, fen):
        board = Board(self.ai_game)
        board._init_from_FEN(fen)
        best_move = None
        max_eval = float('-inf')
        legal_moves = board.get_legal_moves()
        print(legal_moves)
        # for move in legal_moves:
        #     board.push(move)
        #     eval = self.minimax_alpha_beta(board, self.depth - 1, float('-inf'), float('inf'), False)
        #     board.pop()

        #     if eval > max_eval:
        #         max_eval = eval
        #         best_move = move

        return best_move

    def evaluate_board(self, board):
        # Implement a board evaluation function here to assign a score to a given board state.
        # The higher the score, the better the board for the AI.
        # You can use a simple material-based evaluation or a more complex evaluation function.

        # Sample material-based evaluation function:
        piece_values = {
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9,
            King: 100,
        }

        score = 0
        # for square in chess.SQUARES:
        #     piece = board.piece_at(square)
        #     if piece is not None:
        #         if piece.color == board.turn:
        #             score += piece_values[piece.piece_type]
        #         else:
        #             score -= piece_values[piece.piece_type]

        return score