from .piece import Piece

class Bishop(Piece):
    """ A class to representing a bishop """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}B")
        self.color = color
        self.name = f"{color}Bishop"

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the bishop """
        dirs = [(1,1),(1,-1),(-1,-1),(-1,1)]
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        friendly_pieces = black_pieces if self.color == "b" else white_pieces
        movements = []
        for direction in dirs:
            temporary_square = self.square 
            flag = True
            while flag:
                temporary_square = (temporary_square[0]+direction[0], 
                                    temporary_square[1]+direction[1])
                for piece in enemy_pieces:
                    if piece.square == temporary_square:
                        movements.append(temporary_square)
                        flag = False
                for piece in friendly_pieces:
                    if piece.square == temporary_square:
                        flag = False
                if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                        temporary_square[1] < 0 or temporary_square[1] > 7):
                    flag = False
                if flag:
                    movements.append(temporary_square)
        return movements

