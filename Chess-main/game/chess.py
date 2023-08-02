import pygame, sys

from pygame.locals import *

from piece.new_game import create_white_pieces, create_black_pieces
from settings import Settings
from results import Results
from Board.board import Board
from piece.pawn import Pawn
from piece.king import King

class ChessGame:
    """ A class to manage the game """

    def __init__(self):
        """ Create a new game instance """
        pygame.init()

        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Chess Game")

        self.results = Results(self)
        self.clock = pygame.time.Clock()

        self.board = Board(self)

        self.board._init_from_FEN("rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b  -")
        self.sound = pygame.mixer.Sound("Assets/chessmove.wav")

    def run_game(self):
        """ Init the game loop """
        while True:
            self._check_events()
            self._update_screen()

            self.clock.tick(self.settings.FPS)

    def _check_events(self):
        """ Check the game events """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and self.board.game_active:
                self._check_mousebuttondown_events(event)
            elif event.type == KEYDOWN and not self.board.game_active:
                if event.key == K_p:
                    Board._reset_all(self)

    def _check_mousebuttondown_events(self, event):
        """ Respond to mousebuttondown events """
        checked_square = (event.pos[0] // self.settings.square_size,
                          event.pos[1] // self.settings.square_size)

        friendly_pieces = self.board.white_pieces if self.board.turn == "w" else self.board.black_pieces 
        enemy_pieces = self.board.white_pieces if self.board.turn == "b" else self.board.black_pieces
        king = self.board.white_king if self.board.turn == "w" else self.board.black_king

        if self.board.active_piece: 
            if checked_square in self.board.active_piece.possible_movements(self.board.white_pieces, self.board.black_pieces, king):
                self._move(friendly_pieces, enemy_pieces, checked_square)
                #print(self.board.positions)
            else:
                active_piece = None
                for piece in friendly_pieces:
                    if piece.square == checked_square:
                        # Desactive the piece if press it two times
                        if piece == self.board.active_piece:
                            active_piece = None
                        # If press other piece, change the active piece
                        else:
                            active_piece = piece
                        break
                self.board.active_piece = active_piece
        else:
            for piece in friendly_pieces:
                if piece.square == checked_square:
                    self.board.active_piece = piece
                    break

    def _move(self, friendly_pieces, enemy_pieces, square):
        """ Move the active piece, realize the captures and change of turn """
        # The next lines is for the en passant capture 

        # Capture the piece en passant
        if type(self.board.active_piece) is Pawn and square in self.board.active_piece.move_en_passant(enemy_pieces):
            self.board.active_piece.movement((square[0], self.board.active_piece.square[1]))
            pygame.sprite.groupcollide(friendly_pieces, enemy_pieces, False, True)

        # The en passant capture only be made on the movement inmediately after of the enemy pawn 
        # makes the double-step move
        for piece in enemy_pieces:
            if type(piece) is Pawn:
                piece.en_passant = False

        if type(self.board.active_piece) is Pawn:
            if square[1] == self.board.active_piece.square[1] + 2*self.board.active_piece.direction:
                self.board.active_piece.en_passant = True

        # The next lines is for castle
        if type(self.board.active_piece) is King: 
            # Short castle
            movement, rook = self.board.active_piece.short_castle(self.board.white_pieces, self.board.black_pieces)
            if square in movement:
                rook.movement((rook.square[0]-2, rook.square[1]))
                rook.already_moved = True
            # Large castle
            movement, rook = self.board.active_piece.large_castle(self.board.white_pieces, self.board.black_pieces)
            if square in movement:
                rook.movement((rook.square[0]+3, rook.square[1]))
                rook.already_moved = True


        self.board.active_piece.movement(square)
        self.sound.play()
        self.board.active_piece.already_moved = True

        # Check the captures
        capture = pygame.sprite.groupcollide(friendly_pieces, enemy_pieces, False, True)

        if capture or type(self.board.active_piece) is Pawn:
            self.fifty_movements = 0
        else:
            self.fifty_movements += 1

        if type(self.board.active_piece) is Pawn:
            # The pawn is turned into a queen
            self.board.active_piece.promotion(friendly_pieces)

        actual_position = Board._get_position(self.board)
        if actual_position in self.board.positions.keys():
            self.board.positions[actual_position] += 1
        else:
            self.board.positions[actual_position] = 1

        self.board.turn = "b" if self.board.turn == "w" else "w"
        print(Board._get_FEN_position(self.board))
        self.board.active_piece = None

        king = self.board.white_king if self.board.turn == "w" else self.board.black_king
        self._check_checkmate(self.board.turn, enemy_pieces, king)
        self._check_draws(enemy_pieces, king)


    def _check_checkmate(self, color, pieces, king):
        """ Check if the king is in checkmate """
        for piece in pieces:
            if piece.possible_movements(self.board.white_pieces, self.board.black_pieces, king):
                return None

        if king.check(self.board.white_pieces, self.board.black_pieces):
            winner = "black" if color=="w" else "white"
            self.results.prep(f"The {winner} player is the winner")
            self.board.game_active = False

    def _check_draws(self, pieces, king):
        """ Check if the game is draws """
        # Check stalemate
        movements = []
        for piece in pieces:
            movements.extend(piece.possible_movements(self.board.white_pieces, self.board.black_pieces, king))
        if not movements and not king.check(self.board.white_pieces, self.board.black_pieces):
            self.results.prep("The game is draw for stalemate")
            self.board.game_active = False

        # 50 movements rules
        if self.fifty_movements == 100:
            self.results.prep("The game is draw for", "fifty movements rule")
            self.board.game_active = False

        if 3 in self.board.positions.values():
            self.results.prep("The game is draw for repeat", "the same position three times")
            self.board.game_active = False

    def _draw_possible_movements(self):
        """ Draw circles in the possible movements if there are a active piece """
        king = self.board.white_king if self.board.turn == "w" else self.board.black_king

        # Draw a rectangle in the active piece square
        pygame.draw.rect(self.screen, self.settings.active_color, (self.board.active_piece.square[0]*self.settings.square_size,
                         self.board.active_piece.square[1]*self.settings.square_size, self.settings.square_size, 
                         self.settings.square_size), 5, 1)       

        for movement in self.board.active_piece.possible_movements(self.board.white_pieces, self.board.black_pieces, king):
            pygame.draw.circle(self.screen, self.settings.movement_color, ((movement[0]+0.5)*self.settings.square_size, 
                              (movement[1]+0.5)*self.settings.square_size), self.settings.square_size//3)


    def _update_screen(self):
        """ Show the screen """
        self.screen.fill((0,0,0))

        if self.board.game_active:
            self.board.update()

            if self.board.active_piece:
                self._draw_possible_movements()

            self.board.white_pieces.draw(self.screen)
            self.board.black_pieces.draw(self.screen)
        else:
            self.results.update()

        pygame.display.update()

if __name__ == "__main__":
    ai_game = ChessGame()
    ai_game.run_game()