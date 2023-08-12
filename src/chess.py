import pygame, sys

from pygame.locals import *
from stockfish import Stockfish
from settings import Settings
from results import Results
from Board.board import Board
from Piece.pawn import Pawn
from Piece.king import King
from AI.ai import Ai

class ChessGame:
    """ A class to manage the game """

    def __init__(self):
        """ Create a new game instance """
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(self.settings.screen_size)

        self.square_size = self.settings.square_size
        self.board = Board(self)
        self.array = []
        for i in range(8):
            if i%2:
                self.array.append([1 if j%2 else 0 for j in range(8)])
            else:
                self.array.append([0 if j%2 else 1 for j in range(8)])

        self.results = Results(self)
        self.clock = pygame.time.Clock()

        self.board._reset_all()
        self.sound = pygame.mixer.Sound("Assets/chessmove.wav")

        self.active_piece = None
        self.chess_ai = Ai(self, depth=3)
        self.stockfish = Stockfish(path= self.settings.StockFish_Path, depth=1)
        self.board.test()

    def run_game(self, mode):
        """ Init the game loop """
        while True:
            self._check_events()
            self._update_screen()
            self._auto_move(mode)
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

        if self.active_piece: 
            if checked_square in self.active_piece.possible_captures(self.board.white_pieces, self.board.black_pieces, king):
                self._move(friendly_pieces, enemy_pieces, checked_square)
            else:
                active_piece = None
                for piece in friendly_pieces:
                    if piece.square == checked_square:
                        # Desactive the piece if press it two times
                        if piece == self.active_piece:
                            active_piece = None
                        # If press other piece, change the active piece
                        else:
                            active_piece = piece
                        break
                self.active_piece = active_piece
        else:
            for piece in friendly_pieces:
                if piece.square == checked_square:
                    self.active_piece = piece
                    break

    def _move(self, friendly_pieces, enemy_pieces, square):
        """ Move the active piece, realize the captures and change of turn """
        has_capture = self.board.square[square]
        old_pos = self.active_piece.square
        # The next lines is for the en passant capture 

        # Capture the piece en passant
        if type(self.active_piece) is Pawn and square in self.active_piece.move_en_passant(enemy_pieces):
            self.active_piece.movement((square[0], self.active_piece.square[1]))
            pygame.sprite.groupcollide(friendly_pieces, enemy_pieces, False, True)

        # The en passant capture only be made on the movement inmediately after of the enemy pawn 
        # makes the double-step move
        for piece in enemy_pieces:
            if type(piece) is Pawn:
                piece.en_passant = False

        if type(self.active_piece) is Pawn:
            if square[1] == self.active_piece.square[1] + 2*self.active_piece.direction:
                self.active_piece.en_passant = True

        # The next lines is for castle
        if type(self.active_piece) is King: 
            # Short castle
            movement, rook = self.active_piece.short_castle(self.board.white_pieces, self.board.black_pieces)
            if square in movement:
                rook.movement((rook.square[0]-2, rook.square[1]))
                rook.already_moved = True
            # Large castle
            movement, rook = self.active_piece.large_castle(self.board.white_pieces, self.board.black_pieces)
            if square in movement:
                rook.movement((rook.square[0]+3, rook.square[1]))
                rook.already_moved = True


        self.active_piece.movement(square)
        self.sound.play()
        self.active_piece.already_moved = True

        # Check the captures
        capture = pygame.sprite.groupcollide(friendly_pieces, enemy_pieces, False, True)

        if capture or type(self.active_piece) is Pawn:
            self.board.fifty_movements = 0
        else:
            self.board.fifty_movements += 1

        if type(self.active_piece) is Pawn:
            # The pawn is turned into a queen
            self.active_piece.promotion(friendly_pieces)

        if (self.board.turn == 'w'):
            self.board.total_turns += 1
        self.board.last_move = (self.active_piece, square, has_capture)
        self.board.update_PGN(old_pos)
        print(self.board._get_FEN_position())
        print(self.board.PGN)
        actual_position = self.board._get_position()
        if actual_position in self.board.positions.keys():
            self.board.positions[actual_position] += 1
        else:
            self.board.positions[actual_position] = 1
        self.board.turn = "b" if self.board.turn == "w" else "w"
        self.active_piece = None

        king = self.board.white_king if self.board.turn == "w" else self.board.black_king
        self._check_checkmate(self.board.turn, enemy_pieces, king)
        self._check_draws(enemy_pieces, king)

    def _check_checkmate(self, color, pieces, king):
        """ Check if the king is in checkmate """
        for piece in pieces:
            if piece.possible_captures(self.board.white_pieces, self.board.black_pieces, king):
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
            movements.extend(piece.possible_captures(self.board.white_pieces, self.board.black_pieces, king))
        if not movements and not king.check(self.board.white_pieces, self.board.black_pieces):
            self.results.prep("The game is draw for stalemate")
            self.board.game_active = False

        # 50 movements rules
        if self.board.fifty_movements == 100:
            self.results.prep("The game is draw for", "fifty movements rule")
            self.board.game_active = False

        if 3 in self.board.positions.values():
            self.results.prep("The game is draw for repeat", "the same position three times")
            self.board.game_active = False

    def _draw_possible_movements(self):
        """ Draw circles in the possible movements if there are a active piece """
        king = self.board.white_king if self.board.turn == "w" else self.board.black_king

        # Draw a rectangle in the active piece square
        pygame.draw.rect(self.screen, self.settings.active_color, (self.active_piece.square[0]*self.settings.square_size,
                         self.active_piece.square[1]*self.settings.square_size, self.settings.square_size, 
                         self.settings.square_size), 5, 1)       

        for movement in self.active_piece.possible_captures(self.board.white_pieces, self.board.black_pieces, king):
            pygame.draw.circle(self.screen, self.settings.movement_color, ((movement[0]+0.5)*self.settings.square_size, 
                              (movement[1]+0.5)*self.settings.square_size), self.settings.square_size//3)

    def update(self):
        """ Draw the board on the screen """
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.screen, 
                                 self.settings.light_color if self.array[i][j] else self.settings.dark_color, 
                                 (i*self.square_size, j*self.square_size, self.square_size, self.square_size))

    def _update_screen(self):
        """ Show the screen """
        self.screen.fill((0,0,0))

        if self.board.game_active:
            self.update()

            if self.active_piece:
                self._draw_possible_movements()

            self.board.white_pieces.draw(self.screen)
            self.board.black_pieces.draw(self.screen)
        else:
            self.results.update()

        pygame.display.update()

    def _auto_move(self, mode):
        if self.board.game_active == False:
            return
        if mode == "human":
            if self.board.turn == 'b':
                friendly_pieces = self.board.white_pieces if self.board.turn == "w" else self.board.black_pieces 
                enemy_pieces = self.board.white_pieces if self.board.turn == "b" else self.board.black_pieces
                initial_pos, move = self.chess_ai.get_best_move(self.board._get_FEN_position(), 'b')
                piece_to_move = self.board.get_piece_at_square(initial_pos)
                self.active_piece = piece_to_move
                self._move(friendly_pieces, enemy_pieces, move)
        elif mode == "AI":
            if self.board.turn == 'b':
                friendly_pieces = self.board.white_pieces if self.board.turn == "w" else self.board.black_pieces 
                enemy_pieces = self.board.white_pieces if self.board.turn == "b" else self.board.black_pieces
                initial_pos, move = self.chess_ai.get_best_move(self.board._get_FEN_position(), 'b')
                piece_to_move = self.board.get_piece_at_square(initial_pos)
                self.active_piece = piece_to_move
                self._move(friendly_pieces, enemy_pieces, move)
            else:
                friendly_pieces = self.board.white_pieces if self.board.turn == "w" else self.board.black_pieces 
                enemy_pieces = self.board.white_pieces if self.board.turn == "b" else self.board.black_pieces
                self.stockfish.set_fen_position(self.board._get_FEN_position())
                move = self.stockfish.get_best_move()
                if move:
                    piece_to_move = self.board.get_piece_at_square(self.board.pos_to_movement(move[0:2]))
                    self.active_piece = piece_to_move
                    self._move(friendly_pieces, enemy_pieces, self.board.pos_to_movement(move[2:4]))
