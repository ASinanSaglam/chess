from base_modules import BaseModule
from MoveParser import MoveParser
from Menus import Menus
from msgs import ParsedMove, InvalidCommand, QuitGame, GotoMenu, ShowBoard

class InputParser(BaseModule):
    def __init__(self):
        super(InputParser, self).__init__()
        self.name = "InputParser"
        self.MParser = MoveParser()
        self.Menus = Menus()

    ## sof Module level
    def handle_msg(self, msg):
        self.try_update_menu(msg)
        if msg.mtype == "READ_INPUT":
            self.processInput(msg)
        else:
            pass
    ## eof Module level

    ## sof Msg level
    def processInput(self, msg):
        if msg.inptype == "MOVE":
            MM = self.parseMove(msg)
        elif msg.inptype == "COMMAND":
            MM = self.parseCommand(msg)
        self.send_to_bus(MM)
        return

    def try_update_menu(self, msg):
        try:
            if msg.Menus:
                self.Menus = msg.Menus
        except:
            pass
    ## eof Msg level

    ## sof Lower level
    def parseCommand(self, msg):
        cmd = msg.content
        if cmd.lower() == "exit" or cmd.lower() =="quit":
            MM = QuitGame()
        elif cmd.lower() == "back":
            MM = GotoMenu(content=self.Menus.prev_menu)
        else:
            try:
                self.Menus.menu_dict[cmd]
                MM = GotoMenu(content=cmd)
            except KeyError:
                MM = InvalidCommand(content="Command not understood!")
        return MM

    def parseMove(self, msg):
        cmd = msg.content
        # MOVE just means we are expecting a move
        # but there are a few other options we can have
        if cmd.lower() == "exit" or cmd.lower() =="quit":
            MM = QuitGame(content=True)
        elif cmd.lower() == 'display':
            MM = ShowBoard()
        else:
            try:
                # Now we test for a move
                pMove = self.MParser.str_to_move(cmd)
                MM = ParsedMove(content=pMove, raw_text=cmd, player=msg.player)
            except:
                # if all else fails it's wrong
                MM = InvalidCommand(content="Move not understood!", player=msg.player)
        return MM
    ## eof Lower level
