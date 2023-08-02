import pygame
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

        self.square_size = self.settings.square_size

        self.array = []

        self.white_king, self.white_pieces = create_white_pieces(self)
        self.black_king, self.black_pieces = create_black_pieces(self)

        self.fifty_movements = 0
        self.positions = {}

        self.game_active = True
        self.turn = 'w'

        for i in range(8):
            if i%2:
                self.array.append([1 if j%2 else 0 for j in range(8)])
            else:
                self.array.append([0 if j%2 else 1 for j in range(8)])

    def update(self):
        """ Draw the board on the screen """
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.screen, 
                                 self.settings.light_color if self.array[i][j] else self.settings.dark_color, 
                                 (i*self.square_size, j*self.square_size, self.square_size, self.square_size))

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

        fen_notation = f"{fen_position} {active_color} {castling_rights} {en_passant_target}"
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

    def mov(self, piece, square):
        pass