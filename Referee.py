# Title: Referee class 
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

from base_modules import BaseModule 
from MoveParser import MoveParser
from msgs import ValidMove, InvalidMove
 
class Referee(BaseModule):
    """
    A referee class for the chess engine. 
    This class checks the validity of moves and handles
    move generation for any purpose
    """
    def __init__(self):
        super(Referee,self).__init__()
        self.name = "Referee"
        self.board = None
        self.MParser = MoveParser()

    # Module level
    def handle_msg(self, msg):
        if msg.mtype == "PARSED_MOVE":
            self.validateInput(msg)
        elif msg.mtype == "GAME_STARTED":
            self.board = msg.board
        elif msg.mtype == "CURRENT_BOARD":
            self.board = msg.board
        #elif msg.mtype == "PROCESSED_MOVE":
        #    self.board = msg.board
        else:
            pass
    # eof Module level

    # sof Msg level
    def validateInput(self, msg):
        inp_move = msg.content
        # Re-writing this section with a different logic
        moves = self.gen_moves(self.board)
        # Let's test 
        #driver = self.att_modules['MainBus'].att_modules['DisplayDriver']
        #for move in moves:
        #    test_board = self.MParser.movePiece(move, self.board)
        #    driver.BD.displayBoard(board=test_board)
        #    if inp_move in moves:
        #        print("PASSED VALIDITY")
        #
        if inp_move in moves:
            PM = ValidMove(content=inp_move, raw_text=self.MParser.move_to_str(inp_move), \
                           player=msg.player, board=self.board)
        else:
            PM = InvalidMove(content=True, player=msg.player)
        self.send_to_bus(PM)
    # eof Msg level

    # sof Lower level
    def gen_moves(self, board):
        # turn checking
        turn = self.MParser.check_turn(board)
        # directions
        N, S, E, W = self.MParser.N, self.MParser.S, self.MParser.E, self.MParser.W
        if not turn:
            pieces = ['p','N','B','R','Q','K']
            epieces = ['o','n','b','r','q','k']
        else:
            epieces = ['p','N','B','R','Q','K']
            pieces = ['o','n','b','r','q','k']
        # Pieces are the keys to the pieceDict that we want to 
        # generate moves for
        moves = []
        for pos, ch in enumerate(board):
            if ch in pieces:
                dirs = self.MParser.directions[ch.lower()]
                for idir in dirs:
                    # Sort out pawns, knights and king here
                    if (ch.lower() in 'pokn'):
                        # OOB checking
                        npos = pos + idir
                        # landing piece friendly check
                        npiece = board[npos]
                        if (npiece == " "): continue
                        if npiece in pieces: continue
                        # pawn checks
                        if ch.lower() in 'po':
                            # double move check, need to be at the starting pos.
                            front = board[pos + dirs[0]]
                            if idir == dirs[0] and (front == "."): moves.append((pos,npos))
                            if (idir == dirs[1]):
                                if ch == 'p':
                                    if ((pos-90) >= 0 and (pos-90) < 10) and (front == "."):
                                        moves.append((pos,npos))
                                        continue
                                if ch == 'o':
                                    if ((pos-40) >= 0 and (pos-40) < 10) and (front == "."):
                                        moves.append((pos,npos))
                                        continue
                            # check en passant here
                            # if (idir == N+E) or (idir == N+W):
                            # Capture check
                            if (idir == dirs[2]) or (idir == dirs[3]):
                                if (npiece in epieces):
                                    moves.append((pos,npos))
                                    continue
                                continue
                        else:
                            if npiece in epieces or npiece == ".": 
                                moves.append((pos,npos))
                                continue
                    else:
                    # Every other piece here
                        for k in range(1,9):
                            npos = pos + idir * k
                            # OOB checking
                            # Landing piece checking
                            npiece = board[npos]
                            if (npiece == " "): break
                            if npiece in pieces: break
                            if npiece in epieces: 
                                moves.append((pos,npos))
                                break
                            moves.append((pos,npos))
        return moves
    # eof Lower level    
