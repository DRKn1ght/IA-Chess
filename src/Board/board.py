import numpy as np
from Piece.pawn import Pawn
from Piece.king import King
from Piece.rook import Rook
from Piece.knight import Knight
from Piece.queen import Queen
from Piece.bishop import Bishop
from Piece.new_game import create_white_pieces, create_black_pieces, FEN_to_board

class Board:
    """ A class to manage the board """

    def __init__(self, ai_game):
        """ Create a new board """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.square = np.full((8, 8), None, dtype = object)
        self.fifty_movements = 0
        self.total_turns = 0
        self.last_move = None
        self.PGN = ""
        self.positions = {}
        self.board_stack = []
        self.game_active = True
        self.game_active_AI = [True, None]
        self.turn = 'w'
        self.last_move_AI = []

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
        if len(castling_rights) == 0:
            castling_rights = "-"

        en_passant_target = '-'

        fen_notation = f"{fen_position} {active_color} {castling_rights} {en_passant_target} {self.fifty_movements} {self.total_turns}"
        return fen_notation

    def update_PGN(self, old_pos):
        letter = 'abcdefgh'
        piece, square, has_capture = self.last_move
        old_x, _ = old_pos
                
        if self.turn == "w":
            self.PGN += str(self.total_turns) + ". "
        if type(piece) is King: 
            print(old_pos, square)
            # short castles
            if old_pos[0] == 4 and square[0] == 6:
                self.PGN += "O-O "
                return
            
            # long castles
            if old_pos[0] == 4 and square[0] == 2:
                self.PGN += "O-O-O "
                return
            
        pos_str = self.movement_to_pos(self.last_move)
        if has_capture:
            if type(piece) is Pawn:
                pos_str = letter[old_x] + pos_str[:0] + "x" + pos_str[0:]
            else:
                pos_str = letter[old_x] + pos_str[:1] + "x" + pos_str[1:]
        if type(piece) is not Pawn:
            self.PGN += pos_str[:1] + letter[old_x] + pos_str[1:] + " "
        else:
            self.PGN += pos_str + " "

    def get_piece_at_square(self, square):
        piece = self.square[square]
        if(piece):
            return piece
        return None
    
    def get_en_passant_target(self):
        en_passant_target = '-'
        friendly_pieces = self.white_pieces if self.turn == "w" else self.black_pieces
        enemy_pieces = self.white_pieces if self.turn == "b" else self.black_pieces
        for piece in friendly_pieces:
            if type(piece) is Pawn:
                target = piece.move_en_passant(enemy_pieces)
                if len(target) > 0:
                    target = target[0]
                    en_passant_target = self.movement_to_pos((Pawn, target, None))
                    break
        return en_passant_target
    
    def movement_to_pos(self, movement):
        piece, square, _ = movement
        letter = 'abcdefgh'
        nums = '87654321'
        piece_mapping = {
        Rook: 'R',
        Knight: 'N',
        Bishop: 'B',
        Queen: 'Q',
        King: 'K',
        Pawn: '',
        }
        
        return piece_mapping[type(piece)] + letter[square[0]] + nums[square[1]]
    
    def pos_to_movement(self, pos):
        file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        file = file_map[pos[0]]
        rank = 8 - int(pos[1])
        return (file, rank)

    
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

    def fake_push(self, move):
        piece, square = move
        new_move = (piece, piece.square)
        capture = piece.movement(square)
        if capture is not None:
            enemy_pieces = self.white_pieces if capture.color == 'w' else self.black_pieces
            enemy_pieces.remove(capture)
            if type(capture) is King:
                self.game_active_AI = [False, capture.color]
        self.last_move_AI.append((new_move, capture))
        # Update the turn


    def pop(self):
        if len(self.board_stack) > 0:
            fen_position = self.board_stack.pop()
            self._init_from_FEN(fen_position)

    def fake_pop(self):
        if len(self.last_move_AI) > 0:
            #print(self.last_move_AI)
            old_state = self.last_move_AI.pop()
            old_piece, old_move = old_state[0]
            old_piece.movement(old_move)
            if old_state[1]:
                enemy_pieces = self.white_pieces if old_state[1].color == 'w' else self.black_pieces
                enemy_pieces.add(old_state[1])
                self.square[old_state[1].square] = old_state[1]

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
            possible_captures = piece.possible_movements(self.white_pieces, self.black_pieces, king)
            if len(possible_captures) > 0:
                legal_moves.append((piece, possible_captures))
        return legal_moves
    
    def print_board(self):
        for i in range(8):
                for j in range(8):
                        if (self.square[j][i]):
                            print(self.square[j][i].color, end=" ")
                        else:
                            print(" ", end=" ")
                print()