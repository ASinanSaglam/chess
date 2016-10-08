from base_modules import BaseMsg

# A description of all msgs we have
# A null msg
class NullMsg(BaseMsg):
    '''
    Absolutely nothing
    '''
    def __init__(self, content=None, mtype='NULL', player=None):
        self.content = content
        self.mtype = mtype
        self.player = player

# Input related messages
class ReadInput(BaseMsg):
    '''
    This is the msg from the input reader, passing the input entered by the player
    to the main bus. Text is the content 
    '''
    def __init__(self, content=None, mtype='READ_INPUT', player=None, inptype=None):
        self.content = content
        self.mtype = mtype
        self.player = player
        self.inptype = inptype 

class GetInput(BaseMsg):
    '''
    This is the msg for the input reader, signaling the reader to take input 
    Inptype is the type of input, player is the object requesting the input
    '''
    def __init__(self, content=None, mtype='GET_INPUT', player=None, inptype=None, Menus=None):
        self.content = content
        self.mtype = mtype
        self.player = player
        self.inptype = inptype 
        self.Menus = Menus 

# Move/command related msges
class ParsedMove(BaseMsg):
    '''
    Msg from the input parser, confirming it's a move. At this stage the board is not 
    involved
    '''
    def __init__(self, content=None, mtype='PARSED_MOVE', raw_text='', player=None):
        self.content = content
        self.raw_text = raw_text
        self.mtype = mtype
        self.player = player

class ValidMove(BaseMsg):
    '''
    Msg from referee, validating a particular move. Content is move, rest is obv
    '''
    def __init__(self, content=None, mtype='VALID_MOVE', raw_text='', player=None, board=None):
        self.content = content
        self.raw_text = raw_text
        self.mtype = mtype
        self.player = player
        self.board = board

class InvalidMove(BaseMsg):
    '''
    Invalid move move
    '''
    def __init__(self, content=None, mtype='INVALID_MOVE', raw_text='', player=None, board=None):
        self.content = content
        self.raw_text = raw_text
        self.mtype = mtype
        self.player = player
        self.board = board

class ProcessedMove(BaseMsg):
    '''
    From board handler, confirming that the move is made on the current board
    '''
    def __init__(self, content=None, mtype='PROCESSED_MOVE', raw_text='', player=None, board=None):
        self.content = content
        self.raw_text = raw_text
        self.mtype = mtype
        self.player = player
        self.board = board

class InvalidCommand(BaseMsg):
    '''
    Invalid command 
    '''
    def __init__(self, content=None, mtype='INVALID_COMMAND', raw_text='', player=None):
        self.content = content
        self.mtype = mtype
        self.raw_text = raw_text
        self.player = player

# Game state related msges
class QuitGame(BaseMsg):
    '''
    Command to quit the game
    '''
    def __init__(self, content=None, mtype='QUIT_GAME', tmodule="GameState"):
        self.content = content
        self.mtype = mtype
        
class StartGame(BaseMsg):
    '''
    Command to quit the game
    '''
    def __init__(self, content=None, mtype='START_GAME', tmodule="GameState", game_type="normal", players=None):
        self.content = content
        self.mtype = mtype
        self.game_type = game_type 
        self.players = players
        self.tmodule = tmodule 

class InitGame(BaseMsg):
    '''
    Msg that can be used to display the board, it's read by board class to signal the need to show the 
    board to the player, w/o making a move
    '''
    def __init__(self, content=None, mtype='INIT_GAME', tmodule="GameState"):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule

class GameStarted(BaseMsg):
    '''
    Signal to all modules that the game started
    '''
    def __init__(self, content=None, mtype='GAME_STARTED', tmodule=None, game_type="normal", players=None, board=None):
        self.content = content
        self.mtype = mtype
        self.game_type = game_type 
        self.players = players
        self.tmodule = tmodule 
        self.board = board

class GotoMenu(BaseMsg):
    '''
    Msg to signal GameState to head to a particular menu
    '''
    def __init__(self, content=None, mtype='GOTO_MENU', tmodule="GameState", Menus=None):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule
        self.Menus = Menus

# Msges to board handler
class ShowBoard(BaseMsg):
    '''
    Msg that can be used to display the board, it's read by board class to signal the need to show the 
    board to the player, w/o making a move
    '''
    def __init__(self, content=None, mtype='SHOW_BOARD', tmodule="BoardHandler"):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule

class ShowHistory(BaseMsg):
    '''
    Msg that can be used to display the history, it's read by board handler class to signal the need to show the 
    history to the player
    '''
    def __init__(self, content=None, mtype='SHOW_HISTORY', tmodule="BoardHandler"):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule

class CurrentBoard(BaseMsg):
    '''
    Board handler msg that shows the current state of the board
    '''
    def __init__(self, content=None, mtype='CURRENT_BOARD', board=None):
        self.content = content
        self.mtype = mtype
        self.board = board 

# Msges to display driver
class RenderBoard(BaseMsg):
    '''
    '''
    def __init__(self, content=None, mtype='RENDER_BOARD', tmodule="DisplayDriver", board=None, player=None):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule
        self.board = board
        self.player = player

class RenderHistory(BaseMsg):
    '''
    '''
    def __init__(self, content=None, mtype='RENDER_HISTORY', tmodule="DisplayDriver", history=None):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule
        self.history = history

class RenderMenu(BaseMsg):
    '''
    Msg to display the menu. Contains the dictionary of menus and the information about the previous menu 
    we are coming from, incase we have to return to it
    '''
    def __init__(self, content=None, mtype='RENDER_MENU', tmodule="DisplayDriver", Menus=None):
        self.content = content
        self.mtype = mtype
        self.tmodule = tmodule
        self.Menus = Menus
