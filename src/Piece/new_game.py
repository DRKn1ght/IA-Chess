from pygame.sprite import Group

from .pawn import Pawn
from .king import King
from .bishop import Bishop
from .knight import Knight
from .queen import Queen
from .rook import Rook

def create_white_pieces(ai_game):
    """ Get a the white pieces in the initial position """
    white_pieces = Group()

    for i in range(8):
        pawn = Pawn(ai_game, (i,6), "w")
        white_pieces.add(pawn)
        ai_game.square[i][6] = pawn

    for i in range(2):
        rook = Rook(ai_game, (7*i,7), "w")
        knight = Knight(ai_game, (5*i+1,7), "w")
        bishop = Bishop(ai_game, (3*i+2,7), "w")
        white_pieces.add(rook)
        white_pieces.add(knight)
        white_pieces.add(bishop)
        ai_game.square[7*i][7] = rook
        ai_game.square[5*1+1][7] = knight
        ai_game.square[3*i+2][7] = bishop
    queen = Queen(ai_game, (3,7), "w")
    white_pieces.add(queen)
    white_king = King(ai_game, (4,7), "w")
    white_pieces.add(white_king)
    ai_game.square[3][7] = queen
    ai_game.square[4][7] = white_king

    return white_king, white_pieces


def create_black_pieces(ai_game):
    """ Get a the white pieces in the initial position """
    black_pieces = Group()

    for i in range(8):
        pawn = Pawn(ai_game, (i,1), "b")
        black_pieces.add(pawn)
        ai_game.square[i][1] = pawn

    for i in range(2):
        rook = Rook(ai_game, (7*i,0), "b")
        knight = Knight(ai_game, (5*i+1,0), "b")
        bishop = Bishop(ai_game, (3*i+2,0), "b")
        black_pieces.add(rook)
        black_pieces.add(knight)
        black_pieces.add(bishop)
        ai_game.square[7*i][0] = rook
        ai_game.square[5*1+1][0] = knight
        ai_game.square[3*i+2][0] = bishop
    queen = Queen(ai_game, (3,0), "b")
    black_pieces.add(queen)
    black_king = King(ai_game, (4,0), "b")
    black_pieces.add(black_king)
    ai_game.square[3][0] = queen
    ai_game.square[4][0] = black_king   

    return black_king, black_pieces

def FEN_to_board(ai_game, FEN):
    """Converts FEN notation to white and black pieces groups"""
    piece_mapping = {
        'r': Rook,
        'n': Knight,
        'b': Bishop,
        'q': Queen,
        'k': King,
        'p': Pawn,
        'R': Rook,
        'N': Knight,
        'B': Bishop,
        'Q': Queen,
        'K': King,
        'P': Pawn,
    }

    board_position, active_color, castling_rights = FEN.split()

    white_pieces = Group()
    black_pieces = Group()
    row = 0  # Start from the bottom row for white pieces
    col = 0

    for char in board_position:
        if char.isdigit():
            col += int(char)
        elif char == '/':
            row += 1
            col = 0
        else:
            piece_class = piece_mapping[char]
            piece_color = 'w' if char.isupper() else 'b'
            piece = piece_class(ai_game, (col, row), piece_color)
            if (piece_color == 'w'):
                if type(piece) is Pawn and row != 6:
                    piece.already_moved = True
                if type(piece) is King:
                    white_king = piece
                white_pieces.add(piece)
            else:
                if type(piece) is Pawn and row != 1:
                    piece.already_moved = True
                if type(piece) is King:
                    black_king = piece
                black_pieces.add(piece)
            ai_game.square[(col, row)] = piece
            col += 1
    return white_king, white_pieces, black_king, black_pieces
