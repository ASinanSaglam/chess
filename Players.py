from base_modules import BasePlayer
from msgs import GetInput

class HumanPlayer(BasePlayer):
    '''
    Human player class
    '''
    def __init__(self, ptype='HUMAN', turn=None):
        super(HumanPlayer, self).__init__()
        self.ptype = ptype
        self.turn = turn

    def read_input(self):
        self.handler.send_to_bus(GetInput(inptype="MOVE", player=self))

class AIPlayer(BasePlayer):
    '''
    AI player class
    '''
    def __init__(self, ptype='AI', turn=None, aitype='random'):
        super(AIPlayer, self).__init__()
        self.ptype = ptype
        self.turn = turn
        self.aitype = aitype

    def read_input(self):
	if self.aitype == 'random':
            from msgs import ValidMove
            import random
            # This should only be a temporary hack
            ref = self.handler.att_modules["MainBus"].att_modules["Referee"]
            moves = ref.gen_moves(ref.board)
            rand_i = random.randint(0, len(moves)-1)
            rand_move = moves[rand_i]
            self.handler.send_to_bus(ValidMove(content=rand_move, \
                    raw_text=self.handler.MParser.move_to_str(rand_move)))
	elif self.aitype == 'basic':
            from msgs import ValidMove
            # This should only be a temporary hack
	    # Maybe I should move move generation from ref. to somewhere else?
            self.ref = self.handler.att_modules["MainBus"].att_modules["Referee"]
            # Regardless, here we do some scoring and select a high scoring move
            curr_board = self.ref.board
            moves = self.ref.gen_moves(curr_board)
            scores = []
            depth = 3
            for move in moves:
                nboard = self.ref.MParser.movePiece(move, curr_board)
                score = self.evaluate_board(nboard, depth)
                scores.append(score)
	    max_score = max(scores) 
            max_ind = scores.index(max_score)
            ai_move = moves[max_ind]
            print("Found move, with score: ", ai_move, max_score)
            print("Depth was: ", depth)
            print("Scores were: ")
            print(zip(moves,scores))
            # Return our move
            self.handler.send_to_bus(ValidMove(content=ai_move, \
                    raw_text=self.handler.MParser.move_to_str(ai_move)))

    def evaluate_board(self, board, depth=2):
        if depth > 0:
            moves = self.ref.gen_moves(board)
            scores = []
            for move in moves:
                nboard = self.ref.MParser.movePiece(move, board)
                score = self.evaluate_board(nboard, depth=depth-1)
                scores.append(score)
            return max(scores) 
        else:
            return self.score_board(board)

    def score_board(self, board):
        # figure out the side so the func is symettric
        turn = int(board[0]) 
        if not turn:
            side_mult = +1
        else:
            side_mult = -1

        # Material calculation
        # piece weights
        kWt, qWt, rWt, bWt, nWt, pWt = 200, 9, 5, 3, 3, 1
        # count pieces
        wK, bK = board.count('K'), board.count('k')
        wQ, bQ = board.count('Q'), board.count('q')
        wR, bR = board.count('R'), board.count('r')
        wB, bB = board.count('B'), board.count('b')
        wN, bN = board.count('N'), board.count('n')
        wP, bP = board.count('p'), board.count('o')
        # calculate score
        matScore = kWt * (wK - bK) \
                 + qWt * (wQ - bQ) \
                 + rWt * (wR - bR) \
                 + bWt * (wB - bB) \
                 + nWt * (wN - bN) \
                 + pWt * (wP - bP)
       
        # Mobility calculation
        mobWt = 0.3
        wBoard = list(board)
        wBoard[0] = '0'
        wBoard = "".join(wBoard)
        wMob = len(self.ref.gen_moves(wBoard))
        bBoard = list(board)
        bBoard[0] = '1'
        bBoard = "".join(bBoard)
        bMob = len(self.ref.gen_moves(bBoard))
        mobScore = mobWt * (wMob - bMob)
 
        # Final evaluation
        return (matScore + mobScore) * side_mult
