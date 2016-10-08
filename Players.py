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
    def __init__(self, ptype='AI', turn=None):
        super(AIPlayer, self).__init__()
        self.ptype = ptype
        self.turn = turn

    def read_input(self):
        from msgs import ValidMove
        import random
        # This should only be a temporary hack
        ref = self.handler.att_modules["MainBus"].att_modules["Referee"]
        moves = ref.gen_moves(ref.board)
        rand_i = random.randint(0, len(moves)-1)
        rand_move = moves[rand_i]
        self.handler.send_to_bus(ValidMove(content=rand_move, \
                raw_text=self.handler.MParser.move_to_str(rand_move)))
