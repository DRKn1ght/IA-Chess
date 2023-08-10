from .piece import Piece

from .queen import Queen

class Pawn(Piece):
    """ A class to representing a pawn """

    def __init__(self, ai_game, square, color):
        """ Create a new pawn """
        super().__init__(ai_game, square, f"{color}p")
        self.color = color
        self.direction = 1 if self.color == "b" else -1
        self.en_passant = False
        self.name = f"{color}Pawn"

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the pawn """
        movements = []
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        if self._two_squares(white_pieces, black_pieces):
            movements.append((self.square[0], self.square[1]+self.direction))
            movements.append((self.square[0], self.square[1]+2*self.direction))
        elif self._one_square(white_pieces, black_pieces):
            movements.append((self.square[0], self.square[1]+self.direction))
        movements.extend(self._captures(enemy_pieces))
        movements.extend(self.move_en_passant(enemy_pieces))
        return movements

    def _one_square(self, white_pieces, black_pieces):
        """ Check if the pawn can move one square """
        for piece in white_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+self.direction):
                return False
        for piece in black_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+self.direction):
                return False
        return True

    def _two_squares(self, white_pieces, black_pieces):
        """ Check if the pawn can move two squares """
        if self.already_moved or not self._one_square(white_pieces, black_pieces):
            return False
        for piece in white_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+2*self.direction):
                return False
        for piece in black_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+2*self.direction):
                return False
        return True

    def _captures(self, enemy_pieces):
        """ Return the possible captures """
        moves = []
        for piece in enemy_pieces.sprites():
            if piece.square == (self.square[0]+1, self.square[1]+self.direction):
                moves.append(piece.square)
            if piece.square == (self.square[0]-1, self.square[1]+self.direction):
                moves.append(piece.square)
        return moves

    def promotion(self, pieces):
        """ Promotion the pawn """
        if self.square[1] == int(3.5 + self.direction * 3.5):
            pieces.add(Queen(self.ai_game, self.square, self.color))
            pieces.remove(self)

    def move_en_passant(self, enemy_pieces):
        movements = []
        for piece in enemy_pieces:
            if (type(piece) is Pawn and abs(piece.square[0] - self.square[0]) == 1 
                    and piece.square[1] == self.square[1]) and piece.en_passant:
                movements.append((piece.square[0], piece.square[1]+self.direction))
        return movements

