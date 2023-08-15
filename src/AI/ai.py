import numpy as np
import time
from Board.board import Board
from piece.pawn import Pawn
from piece.king import King
from piece.bishop import Bishop
from piece.knight import Knight
from piece.queen import Queen
from piece.rook import Rook


class Ai:
    def __init__(self, ai_game, depth):
        """Inicializa a classe AI com a profundidade máxima de busca e a referência ao jogo."""
        self.depth = depth
        self.ai_game = ai_game
        self.moves = []
        self.piece_values = {
            Pawn: 10,
            Knight: 30,
            Bishop: 30,
            Rook: 50,
            Queen: 90,
            King: 1000,
        }


    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        """Executa o algoritmo MiniMax com poda alpha-beta para avaliar posições de tabuleiro."""
        
        if depth == 0:
            return self.evaluate_board(board)
        player1 = board.turn
        player2 = 'w' if player1 == 'b' else 'b'
        if maximizing_player:
            legal_moves = board.get_specific_legal_moves(player1)
            max_eval = float('-inf')
            for piece, possible_moves in legal_moves:
                for move in possible_moves:
                    board.fake_push((piece, move))
                    eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    board.fake_pop()
                    if beta <= alpha:
                        return max_eval
            return max_eval
        else:
            min_eval = float('inf')
            legal_moves = board.get_specific_legal_moves(player2)

            for piece, possible_moves in legal_moves:
                for move in possible_moves:
                    board.fake_push((piece, move))
                    eval = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    board.fake_pop()
                    if beta <= alpha:
                        return min_eval
            return min_eval

    def get_best_move(self, fen, color):
        """Obtém a melhor jogada possível para o estado atual do FEN."""
        
        board = Board(self.ai_game)
        board._init_from_FEN(fen)
        board.turn = color
        best_move = None
        max_eval = float('-inf')
        legal_moves = board.get_legal_moves()
        initial_positions = []
        for piece, possible_moves in legal_moves:
            initial_positions.append((piece, piece.square))
        for piece, possible_moves in legal_moves:
            for move in possible_moves:
                board.fake_push((piece, move))
                eval = self.minimax_alpha_beta(board, self.depth - 1, float('-inf'), float('inf'), False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (piece, move)
                   
                board.fake_pop()
        for piece, pos in initial_positions:
            best_piece, move = best_move
            if (piece == best_piece):
                initial_pos = pos
                break
        return initial_pos, best_move[1]

    def evaluate_board(self, board):
        """Calcula a pontuação do tabuleiro atual com base nas posições das peças e o valor de cada uma."""
        
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
                [-3.0, -4.0, -3.0, -4.0, -5.0, -4.0, -3.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
            ]),

            Knight: np.array([
                [-5.0, -3.5, -3.0, -3.0, -3.0, -3.0, -3.5, -5.0],
                [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                [-4.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
            ]),

            Rook: np.array([
                [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0],
                [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [0.0, -1.0, 0.0, 0.5, 0.5, 0.0, -1.0, 0.0]
            ]),

            Pawn: np.array([
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                [1.0, 1.0, 2.0, 4.0, 4.0, 2.0, 1.0, 4.0],
                [0.5, 0.5, 1.0, 4.0, 4.0, 1.0, 0.5, 0.5],
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
        all_pieces = board.black_pieces.sprites() + board.white_pieces.sprites()
        player1 = board.turn
        if player1 == 'b':
            for piece in all_pieces:
                score += piece_table[type(piece)][piece.square[1], piece.square[0]]
                if piece.color == 'w':
                    score += self.piece_values[type(piece)] * -1
                else:
                    score += self.piece_values[type(piece)]
        else:
            for piece in all_pieces:
                score += (piece_table[type(piece)])[piece.square[1], piece.square[0]]
                if piece.color == 'b':
                    score += self.piece_values[type(piece)] * -1
                else:
                    score += self.piece_values[type(piece)]
        return score