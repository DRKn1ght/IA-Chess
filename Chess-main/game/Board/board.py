import pygame
import time
import copy
from piece.piece import Piece
from piece.pawn import Pawn
from piece.king import King
from piece.rook import Rook
from piece.knight import Knight
from piece.queen import Queen
from piece.bishop import Bishop
from piece.new_game import create_white_pieces, create_black_pieces, FEN_to_board

class Board:
    """ A class to manage the board """

    def __init__(self, ai_game):
        """ Create a new board """
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.white_king, self.white_pieces = create_white_pieces(self)
        self.black_king, self.black_pieces = create_black_pieces(self)
        self.board_arr: list[[Piece]] = [
             [Rook(ai_game, (0, 0), 'b'),   Pawn(ai_game, (0, 1), 'b'), None, None, None, None, Pawn(ai_game, (0, 6), 'w'), Rook(ai_game, (0, 7), 'w')],
             [Knight(ai_game, (1, 0), 'b'), Pawn(ai_game, (1, 1), 'b'), None, None, None, None, Pawn(ai_game, (1, 6), 'w'), Knight(ai_game, (1, 7), 'w')],
             [Bishop(ai_game, (2, 0), 'b'), Pawn(ai_game, (2, 1), 'b'), None, None, None, None, Pawn(ai_game, (2, 6), 'w'), Bishop(ai_game, (2, 7), 'w')],
             [Queen(ai_game, (3, 0), 'b'),  Pawn(ai_game, (3, 1), 'b'), None, None, None, None, Pawn(ai_game, (3, 6), 'w'), Queen(ai_game, (3, 7), 'w')],
             [self.black_king,              Pawn(ai_game, (4, 1), 'b'), None, None, None, None, Pawn(ai_game, (4, 6), 'w'), self.white_king],
             [Bishop(ai_game, (5, 0), 'b'), Pawn(ai_game, (5, 1), 'b'), None, None, None, None, Pawn(ai_game, (5, 6), 'w'), Bishop(ai_game, (5, 7), 'w')],
             [Knight(ai_game, (6, 0), 'b'), Pawn(ai_game, (6, 1), 'b'), None, None, None, None, Pawn(ai_game, (6, 6), 'w'), Knight(ai_game, (6, 7), 'w')],
             [Rook(ai_game, (7, 0), 'b'),   Pawn(ai_game, (7, 1), 'b'), None, None, None, None, Pawn(ai_game, (7, 6), 'w'), Rook(ai_game, (7, 7), 'w')]
            ]
        self.fifty_movements = 0
        self.positions = {}
        self.board_stack = []
        self.game_active = True
        self.turn = 'w'
        self.last_move = []

    def _get_position(self):
        """ Return a string representing the position """
        actual_position = []
        for piece in self.white_pieces:
            if type(piece) is Pawn:
                piece_status = f"{piece.name}, {piece.square}, {piece.en_passant} "
            elif type(piece) is King or type(piece) is Rook:
                piece_status = f"{piece.name}, {piece.square}, {piece.already_moved} "
            else:
                piece_status = f"{piece.name}, {piece.square} "
            actual_position.append(piece_status)
        for piece in self.black_pieces:
            if type(piece) is Pawn:
                piece_status = f"{piece.name}, {piece.square}, {piece.en_passant} "
            elif type(piece) is King or type(piece) is Rook:
                piece_status = f"{piece.name}, {piece.square}, {piece.already_moved} "
            else:
                piece_status = f"{piece.name}, {piece.square} "
            actual_position.append(piece_status)
        return "".join(sorted(actual_position))

    def _get_FEN_position(self):
        """ Return a string representing the position in FEN notation """
        def get_piece_symbol(piece):
            if isinstance(piece, Pawn):
                return "P" if piece.color == 'w' else "p"
            if isinstance(piece, Knight):
                return "N" if piece.color == 'w' else "n"
            if isinstance(piece, Bishop):
                return "B" if piece.color == 'w' else "b"
            if isinstance(piece, Rook):
                return "R" if piece.color == 'w' else "r"
            if isinstance(piece, Queen):
                return "Q" if piece.color == 'w' else "q"
            if isinstance(piece, King):
                return "K" if piece.color == 'w' else "k"
            return None
        board_rows = []
        for row in range(8):
            empty_squares = 0
            fen_row = ""
            for col in range(8):
                square = (col, row)
                piece = Board.get_piece_at_square(self, square)
                if piece is None:
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        fen_row += str(empty_squares)
                        empty_squares = 0
                    fen_row += get_piece_symbol(piece)
            if empty_squares > 0:
                fen_row += str(empty_squares)
            board_rows.append(fen_row)

        fen_position = "/".join(board_rows)

        active_color = "w" if self.turn == 'w' else "b"
        castling_rights = ""
        if len(self.white_king.short_castle(self.white_pieces, self.black_pieces)[0]) > 0:
            castling_rights += 'K'
        if len(self.white_king.large_castle(self.white_pieces, self.black_pieces)[0]) > 0:
            castling_rights += 'Q'

        if len(self.black_king.short_castle(self.white_pieces, self.black_pieces)[0]) > 0:
            castling_rights += 'k'
        if len(self.black_king.large_castle(self.white_pieces, self.black_pieces)[0]) > 0:
            castling_rights += 'q'

        en_passant_target = Board.get_en_passant_target(self)

        fen_notation = f"{fen_position} {active_color} {en_passant_target}"
        return fen_notation

    def get_piece_at_square(self, square):
        all_pieces = self.white_pieces.sprites() + self.black_pieces.sprites()
        for piece in all_pieces:
            if (piece.square == square):
                return piece
        return None
    
    def get_en_passant_target(self):
        letter = 'abcdefgh'
        nums = '87654321'
        en_passant_target = '-'
        friendly_pieces = self.white_pieces if self.turn == "w" else self.black_pieces
        enemy_pieces = self.white_pieces if self.turn == "b" else self.black_pieces
        for piece in friendly_pieces:
            if type(piece) is Pawn:
                target = piece.move_en_passant(enemy_pieces)
                if len(target) > 0:
                    target = target[0]
                    en_passant_target = letter[target[0]] + nums[target[1]]
                    break
        return en_passant_target
    
    def _reset_all(self):
        """ Reset all and init a new game """
        self.white_king, self.white_pieces = create_white_pieces(self)
        self.black_king, self.black_pieces = create_black_pieces(self)

        self.turn = "w"
        self.active_piece = None
        self.fifty_movements = 0
        self.positions = {}

        self.game_active = True

    def _init_from_FEN(self, FEN):
        """ init a new game from FEN """
        self.white_king, self.white_pieces, self.black_king, self.black_pieces = FEN_to_board(self, FEN)

        self.turn = "w"
        self.active_piece = None
        self.fifty_movements = 0
        self.positions = {}

        self.game_active = True

    def test(self):
        legal_moves = self.get_legal_moves()
        first = (legal_moves[0][0], legal_moves[0][1][0])
        print(first)
        #self.push(first)
        #self.black_king.movement((3, 5))


    def push(self, move):
        piece, square = move
        self.board_stack.append(self._get_FEN_position())

        piece.movement(square)
        self.turn = 'b' if self.turn == 'w' else 'w'

    def fake_push(self, move, capture = None):
        piece, square = move
        new_move = (piece, piece.square)
        piece.movement(square)
        if capture is not None:
            enemy_pieces = self.white_pieces if capture.color == 'w' else self.black_pieces
            enemy_pieces.remove(capture)
        self.last_move.append((new_move, capture))
        # Update the turn


    def pop(self):
        if len(self.board_stack) > 0:
            fen_position = self.board_stack.pop()
            self._init_from_FEN(fen_position)

    def fake_pop(self):
        if len(self.last_move) > 0:
            #print(self.last_move)
            old_state = self.last_move.pop()
            old_piece, old_move = old_state[0]
            if old_state[1]:
                enemy_pieces = self.white_pieces if old_state[1].color == 'w' else self.black_pieces
                enemy_pieces.add(old_state[1])
            old_piece.movement(old_move)

    def get_legal_moves(self):
        friendly_pieces = self.white_pieces if self.turn == "w" else self.black_pieces
        king = self.white_king if self.turn == "w" else self.black_king
        legal_moves = []
        for piece in friendly_pieces:
            possible_captures = piece.possible_captures(self.white_pieces, self.black_pieces, king)
            if len(possible_captures) > 0:
                legal_moves.append((piece, possible_captures))
        return legal_moves
    
    def get_specific_legal_moves(self, color):
        friendly_pieces = self.white_pieces if color == 'w' else self.black_pieces
        king = self.white_king if color == 'w' else self.black_king
        legal_moves = []
        for piece in friendly_pieces:
            possible_captures = piece.possible_captures(self.white_pieces, self.black_pieces, king)
            if len(possible_captures) > 0:
                legal_moves.append((piece, possible_captures))
        return legal_moves