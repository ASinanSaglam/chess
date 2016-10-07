# Title: Chess Board Class and its methods
# Author: Vedat Sinan Ural, Ali Sinan Saglam
# Contact: vsural@gmail.com, asinansaglam@gmail.com
# Created on Sat Jun 13 23:53:13 2015

class MoveParser(object):
    def __init__(self):
        # First module related business
        self.name = "MoveParser"
        # Also important to ensure the board handler knows where everything is
        self.a1, self.h1, self.a8, self.h8 = 101, 108, 31, 38
        # directions 
        self.N, self.S, self.E, self.W = -10, 10, 1, -1
        N, S, E, W = -10, 10, 1, -1
        # Directions for pieces
        # always do .lower() on the piece
        self.directions = {'p': [N,N+N,N+E,N+W],
                           'o': [S,S+S,S+E,S+W],
                           'n': [N+N+E,N+N+W,S+S+E,S+S+W,E+E+N,E+E+S,W+W+N,W+W+S],
                           'b': [N+E,N+W,S+E,S+W],
                           'r': [N,S,E,W],
                           'q': [N,S,E,W,N+W,N+E,S+W,S+E],
                           'k': [N,S,E,W,N+W,N+E,S+W,S+E]}
        # I think I'll also just keep a dictionary of all possible squares instead of generating later on
        self.sq_to_ind = {'a1': 101,'a2': 91,'a3': 81,'a4': 71, 'a5': 61,'a6': 51,'a7': 41,'a8': 31,
                          'b1': 102,'b2': 92,'b3': 82,'b4': 72, 'b5': 62,'b6': 52,'b7': 42,'b8': 32,
                          'c1': 103,'c2': 93,'c3': 83,'c4': 73, 'c5': 63,'c6': 53,'c7': 43,'c8': 33,
                          'd1': 104,'d2': 94,'d3': 84,'d4': 74, 'd5': 64,'d6': 54,'d7': 44,'d8': 34,
                          'e1': 105,'e2': 95,'e3': 85,'e4': 75, 'e5': 65,'e6': 55,'e7': 45,'e8': 35,
                          'f1': 106,'f2': 96,'f3': 86,'f4': 76, 'f5': 66,'f6': 56,'f7': 46,'f8': 36,
                          'g1': 107,'g2': 97,'g3': 87,'g4': 77, 'g5': 67,'g6': 57,'g7': 47,'g8': 37,
                          'h1': 108,'h2': 98,'h3': 88,'h4': 78, 'h5': 68,'h6': 58,'h7': 48,'h8': 38}
        # and reverse
        self.ind_to_sq = {}
        for key in self.sq_to_ind.keys():
            self.ind_to_sq[self.sq_to_ind[key]] = key

    def move_to_str(self, move):
        mstr = self.ind_to_sq[move[0]] + self.ind_to_sq[move[1]]
        return mstr

    def str_to_move(self, mstr):
        move = (self.sq_to_ind[mstr[0:2]], self.sq_to_ind[mstr[2:4]])
        return move 
        
    def movePiece(self, move, board):
        """
        Method to move the piece
   
        Arguments:
          MoveIndices: 
            Indices for the move in the format 
            ( (start tuple), (end tuple) )

        Returns:
          Board state
        """
        board = list(board)
        board[move[1]] = board[move[0]]
        board[move[0]] = "."
        board[0] = str((int(board[0])+1)%2)
        return "".join(board)
