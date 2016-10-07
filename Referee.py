# Title: Referee class 
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

from base_modules import BaseModule 
from MoveParser import MoveParser
#from msgs import ValidMove, InvalidMove
 
class Referee(BaseModule):
    """
    A referee class for the chess engine. 
    This class checks the validity of moves and handles
    move generation for any purpose
    """
    def __init__(self):
        super(Referee,self).__init__()
        self.name = "Referee"
        self.MParser = MoveParser()

    # Module level
    def handle_msg(self, msg):
        if msg.mtype == "PARSED_MOVE":
            self.validateInput(msg)
        elif msg.mtype == "GAME_STARTED":
            self.board = msg.board
        elif msg.mtype == "PROCESSED_MOVE":
            self.board = msg.board
        else:
            pass
    # eof Module level

    # sof Msg level
    def validateInput(self, msg):
        inp_move = msg.content
        # Re-writing this section with a different logic
        moves, move_strs = self.gen_moves()
        # Let's test 
        #driver = self.att_modules['MainBus'].att_modules['Display']
        #for move in moves:
        #    test_board = self.board_obj.testMove(move)
        #    driver.BD.displayMove((test_board, self.turn))
        #    if inp_move in moves:
        #        print("PASSED VALIDITY")
        #
        if inp_str in move_strs:
            PM = ValidMove(content=inp_move)
        else:
            PM = InvalidMove(content=True, player=msg.player)
        self.send_to_bus(PM)
    # eof Msg level

    # sof Lower level
    def gen_moves(self):
        self.get_board_state()
        # turn checking
        N, S, E, W = self.MParser.N, self.MParser.S, self.MParser.E, self.MParser.W
        if not self.turn:
            pieces = [1,2,3,4,5,6]
            epieces = [-1,-2,-3,-4,-5,-6]
        else:
            pieces = [-1,-2,-3,-4,-5,-6]
            epieces = [1,2,3,4,5,6]
        # Pieces are the keys to the pieceDict that we want to 
        # generate moves for
        moves = []
        move_strs = []
        for i in range(8):
            for j in range(8):
                piece = self.board_obj.board[i][j]
                pos = np.array([i,j])
                if piece in pieces:
                    dirs = directions[piece]
                    for idir in dirs:
                        # Sort out pawns here
                        if (piece == pieces[0]):
                            # OOB checking
                            npos = pos + np.array(idir)
                            #print(npos, pos, idir)
                            if (npos > 7).any() or (npos < 0).any(): continue
                            npiece = self.board_obj.board[npos[0],npos[1]]
                            if (idir == dirs[1]).all(): 
                                if (pos[0] != 1 or pos[0] != 6): 
                                    move_strs.append(self.board_obj.move_to_str(np.array([pos,npos])))
                                    continue
                            # if (idir == N+E) or (idir == N+W):
                            # Landing piece checking
                            if npiece in pieces: continue
                            # Capture check
                            if ((idir == dirs[2]).all() or (idir == dirs[3]).all()): 
                                if (npiece in epieces):
                                    moves.append(np.array([pos,npos]))
                                    move_strs.append(self.board_obj.move_to_str(np.array([pos,npos])))
                                    continue
                                continue
                            moves.append(np.array([pos,npos]))
                            move_strs.append(self.board_obj.move_to_str(np.array([pos,npos])))
                        elif (piece == pieces[1]) or (piece == pieces[5]):
                            # OOB checking
                            npos = pos + np.array(idir)
                            if (npos > 7).any() or (npos < 0).any(): continue
                            npiece = self.board_obj.board[npos[0],npos[1]]
                            # Landing piece checking
                            if npiece in pieces: continue
                            if npiece in epieces: 
                                moves.append(np.array([pos,npos]))
                                move_strs.append(self.board_obj.move_to_str(np.array([pos,npos])))
                                continue
                            moves.append(np.array([pos,npos]))
                            move_strs.append(self.board_obj.move_to_str(np.array([pos,npos])))
                        else:
                        # Every other piece here
                            for k in range(1,9):
                                npos = pos + np.array(idir) * k
                                # OOB checking
                                if (npos > 7).any() or (npos < 0).any(): break
                                # Landing piece checking
                                npiece = self.board_obj.board[npos[0],npos[1]]
                                if npiece in pieces: break
                                if npiece in epieces: 
                                    moves.append(np.array([pos,npos]))
                                    move_strs.append(self.board_obj.move_to_str(np.array([pos,npos])))
                                    break
                                moves.append(np.array([pos,npos]))
                                move_strs.append(self.board_obj.move_to_str(np.array([pos,npos])))
        return np.array(moves), move_strs

    # eof Lower level    
