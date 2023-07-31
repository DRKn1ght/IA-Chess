from .piece import Piece

class Knight(Piece):
    """ A class to representing a knight """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}N")
        self.color = color
        self.name = f"{color}Knight"

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the knight """
        dirs = [(2,1),(2,-1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]
        friendly_pieces = white_pieces if self.color == "w" else black_pieces
        movements = []
        for direction in dirs:
            flag = True # If flag is true, the square is available
            temporary_square = (self.square[0]+direction[0],
                                self.square[1]+direction[1])
            for piece in friendly_pieces:
                if piece.square == temporary_square:
                    flag = False
            if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                    temporary_square[1] < 0 or temporary_square[1] > 7):
                flag = False
            if flag:
                movements.append(temporary_square)
        return movements

