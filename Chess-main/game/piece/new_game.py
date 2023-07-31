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
        white_pieces.add(Pawn(ai_game, (i,6), "w"))

    for i in range(2):
        white_pieces.add(Rook(ai_game, (7*i,7), "w"))
        white_pieces.add(Knight(ai_game, (5*i+1,7), "w"))
        white_pieces.add(Bishop(ai_game, (3*i+2,7), "w"))
    white_pieces.add(Queen(ai_game, (3,7), "w"))
    white_king = King(ai_game, (4,7), "w")
    white_pieces.add(white_king)    

    return white_king, white_pieces


def create_black_pieces(ai_game):
    """ Get a the white pieces in the initial position """
    black_pieces = Group()

    for i in range(8):
        black_pieces.add(Pawn(ai_game, (i,1), "b"))

    for i in range(2):
        black_pieces.add(Rook(ai_game, (7*i,0), "b"))
        black_pieces.add(Knight(ai_game, (5*i+1,0), "b"))
        black_pieces.add(Bishop(ai_game, (3*i+2,0), "b"))
    black_pieces.add(Queen(ai_game, (3,0), "b"))
    black_king = King(ai_game, (4,0), "b")
    black_pieces.add(black_king)    

    return black_king, black_pieces
