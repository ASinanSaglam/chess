# Title: Chess Board Class and its methods
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

from base_modules import BaseModule
from MoveParser import MoveParser
from msgs import ProcessedMove, RenderBoard, RenderHistory, GameStarted

class BoardHandler(BaseModule):
    def __init__(self, board=None):
        # First module related business
        super(BoardHandler, self).__init__()
        self.name = "BoardHandler"
        self.MParser = MoveParser()
        # Now board specific attributes
        self.board = board
        # this stores all previous board states visited
        self.move_history = []
        # this is the move input history
        self.inp_history = []
   
    ## sof Module level
    def handle_msg(self, msg):
        if msg.mtype == "VALID_MOVE":
            self.processMove(msg)
            self.add_move_to_history(msg)
        elif msg.mtype == "SHOW_BOARD":
            self.showBoard()
        elif msg.mtype == "START_GAME":
            self.initBoard(game_type=msg.game_type)
            self.add_players(msg.players)
            self.send_to_bus(GameStarted(board=self.board, players=self.players))
        elif msg.mtype == "SHOW_HISTORY":
            self.showBoard()
            pass
        else:
            pass
    ## eof Module level 

    ## sof Msg level
    def add_move_to_history(self, msg):
        self.move_history.append(self.board)
        self.inp_history.append(msg.inp_str)

    def processMove(self, msg):
        self.board = self.MParser.movePiece(msg.content, msg.board)
        ProM = ProcessedMove(content=msg.content, player=self.in_turn(), board=self.board)
        self.send_to_bus(ProM)

    def showBoard(self):
        RB = RenderBoard(board=self.board, player=self.in_turn())
        self.send_to_bus(RB)

    def showHistory(self):
        RH = RenderHistory(history=self.inp_history, player=self.in_turn())
        self.send_to_bus(RH)
    ## eof msg level

    ## sof Lower level
    def in_turn(self):
        turn = int(self.board[0])
        return filter(lambda x: x.turn == turn, self.players)[0]

    def add_players(self, players):
        self.players = players
        for player in players:
            player.board = self
 
    def initBoard(self, game_type="normal"):
        """
        Method to initialize the board.
        """
        self.initRep()
        if game_type == "normal":
            # for now I'll just initalize normally in my
            # representation initialization
            pass
        else: 
            raise NotImplementedError
            
    def initRep(self):
        '''
        Method that initializes the representation of the board
        '''
        # note most of this is straight out of
        # https://github.com/thomasahle/sunfish/ 

        # Now let's talk board represantation
        # A board is a string and a 130-char string, contains 
        # every thing related to a board state, except for 3-fold rep rule
        board  = "0000000000" # 0-9
        board += "          " # 10-19
        board += "          " # 20-29
        board += " rnbqkbnr " # 30-39
        board += " oooooooo " # 40-49
        board += " ........ " # 50-59
        board += " ........ " # 60-69
        board += " ........ " # 70-79
        board += " ........ " # 80-89
        board += " pppppppp " # 90-99
        board += " RNBQKBNR " # 100-109
        board += "          " # 110-119
        board += "          " # 120-129
        # Board states info is stored in the first 10 characters
        # 0 = turn (0 for white 1 for black), 1-2 = castle kingside/queenside for white (0 mean ok, 1 means not)
        # 3-4 = castle kinside, queenside for black, 5-6 = white/black in check (0 means not in check, 1 means it is)
        # 7 = en passant (0 means not available, 1 means available), 8-10 = 50 move draw (chars 8-10 combined shows the 
        # number of half moves passed without a pawn move or capture)
        # 
        # note that when comparing board positions you have to clean the last 3 character, the 50 move draw ones 
        # since they will muck things up if you are checking for 3-fold rep rule
        self.board = board
    ## eof Lower level
