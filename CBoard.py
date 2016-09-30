# Title: Chess Board Class and its methods
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

import numpy as np
import copy 
from base_modules import BaseModule
from msgs import ProcessedMove, RenderBoard, ReadingStatus
 
class CBoard(BaseModule):
    """
    A Chess board class written for our
    Chess engine program.
 
    Contains the current state of the board
    as well as methods for move generation.
 
    board is the representation of the chess board.
    Uses an 8x8 numpy array.
 
    turn indicates whether it's white's or black's turn;
    turn = 0 -> White's turn.
    turn = 1 -> Black's turn.
 
    cw, cb are castling status for white and black
    respectively. 0 means castling is allowed 1 means
    it is not allowed.
 
    threp is the status of the threefold repetition move
    threp = 0 means the rule isn't invoked.
 
    move50 is the status of the 50 move rule. If it is 0
    the rule isn't invoked.

    check shows if a king is in check currently in the board state
    """
    def __init__(self, board=None, turn=0, cw=0, cb=0, threp=0, move50=0, check=0):
        # First module related business
        super(CBoard, self).__init__()
        self.name = "Board"
        # Now board specific attributes
        self.board = board
        self.temp_board = None
        self.turn = 0
        self.cw = cw
        self.cb = cb
        self.ep = False
        self.threp = threp
        self.move50 = move50
        self.check = check 
        self.move_history = []
        self.inp_history = []
        self.moveDict = { 
             "a": 0, "b": 1, "c": 2, 
             "d": 3, "e": 4, "f": 5, 
             "g": 6, "h": 7, "A": 0, 
             "B": 1, "C": 2, "D": 3, 
             "E": 4, "F": 5, "G": 6, 
             "H": 7, "1": 0, "2": 1, 
             "3": 2, "4": 3, "5": 4, 
             "6": 5, "7": 6, "8": 7 }
        self.invMoveDictLet = { 
             0: "a", 1: "b", 2: "c", 
             3: "d", 4: "e", 5: "f", 
             6: "g", 7: "h"}
        self.invMoveDictNum = { 
             0: "1", 1: "2", 2: "3", 
             3: "4", 4: "5", 5: "6", 
             6: "7", 7: "8"}
        self.pieceDict = {
              0: ".", 1: "P", 2: "N", 
              3: "B", 4: "R", 5: "Q",
              6: "K", -1: "o", -2: "n", 
              -3: "b", -4: "r", -5: "q",
              -6: "k" }
        # At least for now just initialize the board
        self.initBoard()

    def processMove(self, val_move, player):
        self.movePiece(val_move)
        ProM = ProcessedMove(content=(self.board, self.turn), player=self.in_turn())
        return ProM

    def add_to_history(self, move):
        content, inp = move
        if not self.turn:
            self.move_history.append((content, None))
        else:
            prev_move = self.move_history.pop(-1)
            self.move_history.append((prev_move[0], content))
        self.inp_history.append(inp)

    def sendBoard(self):
        ProM = RenderBoard(content=(self.board, self.turn), player=self.in_turn())
        return ProM

    def in_turn(self):
        return filter(lambda x: x.turn == self.turn, self.players)[0]

    def handle_msg(self, msg):
        if msg.mtype == "VALID_MOVE":
            self.add_to_history((msg.content, msg.raw_text))
            ProM = self.processMove(msg.content, msg.player)
            self.send_to_bus(ProM)
        elif msg.mtype == "DISPLAY_BOARD":
            ProM = self.sendBoard()
            self.send_now(ProM)
        elif msg.mtype == "START_GAME":
            self.add_players(msg.players)
        elif msg.mtype == "PRINT_HISTORY":
            print("Printing history")
            print(",".join(self.inp_history))
        else:
            pass

    def add_players(self, players):
        self.players = players
        for player in players:
            player.board = self
 
    def initBoard(self, gameType="normal"):
        """
        Method to initialize the board.
        It sets the board to an 8x8 numpy array with
        all the pieces in the starting position.
        """
        if gameType == "normal":
            self.initNormal()
        else: 
            raise NotImplementedError
            
    def initNormal(self):
        # Sets the board to an empty 8x8 np.array
        self.board = np.zeros((8, 8), int)
         
        # Setting up the pawns in place
        self.board[1][:] = 1
        self.board[6][:] = -1  # minus represents a black piece
 
        # Setting up rest of the white pieces
        self.board[0][0] = self.board[0][7] = 4  # Rooks
        self.board[0][1] = self.board[0][6] = 2  # Knights
        self.board[0][2] = self.board[0][5] = 3  # Bishops
        self.board[0][3] = 5  # Queen
        self.board[0][4] = 6  # King
 
        # Setting up rest of the black pieces
        self.board[7][0] = self.board[7][7] = -4  # Rooks
        self.board[7][1] = self.board[7][6] = -2  # Knights
        self.board[7][2] = self.board[7][5] = -3  # Bishops
        self.board[7][3] = -5  # Queen
        self.board[7][4] = -6  # King
        
        # Make it white's turn
        self.turn = 0

    def move_to_str(self, move):
        ret_str = "".join([self.invMoveDictLet[move[0][1]], self.invMoveDictNum[move[0][0]], \
                        self.invMoveDictLet[move[1][1]], self.invMoveDictNum[move[1][0]]])
        return ret_str
 
    def clearBoard(self):
        """
        Method to clear the board entirely.

        """
        self.board = np.zeros((8, 8), int)
        
    def movePiece(self, moveIndices):
        """
        Method to move the piece
   
        Arguments:
          MoveIndices: 
            Indices for the move in the format 
            ( (start tuple), (end tuple) )

        Returns:
          Nothing, just modifies the board. 
        """
        start, end = moveIndices[0], moveIndices[1]
        assert (start[0] < 8 and start[0] >= 0), "Starting point out of board."
        assert (start[1] < 8 and start[1] >= 0), "Starting point out of board."
        assert (end[0] < 8 and end[0] >= 0), "Ending point out of board."
        assert (end[1] < 8 and end[1] >= 0), "Ending point out of board."
        self.board[end[0],end[1]] = self.board[start[0],start[1]]
        self.board[start[0],start[1]] = 0
        self.turn = (self.turn+1)%2

    def testMove(self, moveIndices):
        """
        Method to test a move, returns temporary copy of the board
   
        Arguments:
          MoveIndices: 
            Indices for the move in the format 
            ( (start tuple), (end tuple) )

        Returns:
          A temporary board with the move in question made
        """
        self.temp_board = copy.deepcopy(self.board)
        start, end = moveIndices[0], moveIndices[1]
        assert (start[0] < 8 and start[0] >= 0), "Starting point out of board."
        assert (start[1] < 8 and start[1] >= 0), "Starting point out of board."
        assert (end[0] < 8 and end[0] >= 0), "Ending point out of board."
        assert (end[1] < 8 and end[1] >= 0), "Ending point out of board."
        self.temp_board[end[0],end[1]] = self.temp_board[start[0],start[1]]
        self.temp_board[start[0],start[1]] = 0
        return self.temp_board
    
    def getSquare(self, coord):
        """
        Returns the piece at square indicated by coordinate given. 

        Arguments: 
          Coord (tuple): Coordinate of the square in tuple (row, column)

        Returns: 
          The contents of the square which can be passed to the piece
          dictionary to find out what piece it is. 
          
        """
        return self.board[coord]
