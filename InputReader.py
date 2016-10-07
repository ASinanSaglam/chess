from base_modules import BaseModule
from msgs import ReadInput
from Menus import Menus

class Completer(object):
    def __init__(self, opts):
        self.opts = opts
        return
    
    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s for s in self.opts if s and s.startswith(text)]
            else:
                self.matches = self.opts[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

class InputReader(BaseModule):
    def __init__(self):
        super(InputReader, self).__init__()
        self.name = "InputReader"
        self.rl_setup = False

    ## Module related
    def handle_msg(self, msg):
        # Now handle input requests
        if msg.mtype == "GET_INPUT":
            self.get_input(msg)
        else:
            pass
    ## eof Module related

    ## sof Msg level
    def get_input(self, msg):
        # Make sure parser is setup
        if not self.rl_setup:
            self.setup_parser()
        if msg.inptype == "MOVE" and msg.player:
            inp = self.input_loop("move", comp_check=False)
            inp = self.clean_inp(inp)
            IM = ReadInput(content=inp, inptype=msg.inptype, player=self.reading_for)
            self.reading = False
            self.send_to_bus(IM)
        elif msg.inptype == "COMMAND":
            if msg.Menus:
                self.Menus = msg.Menus
            inp = self.input_loop("command", comp_keys=self.Menus.menu_choices)
            inp = self.clean_inp(inp)
            IM = ReadInput(content=inp, inptype=msg.inptype)
            self.reading = False
            self.send_to_bus(IM)
    ## eof Msg level

    ## sof Lower level
    def input_loop(self, inp, comp_check=True, comp_keys=None):
        if comp_check and comp_keys:
            mkeys = comp_keys
            mkeys += ['exit', 'quit']
            self.Completer = Completer(mkeys)
            self.rl.set_completer(self.Completer.complete)
        print("Please enter a %s:"%inp)
        if comp_check:
            while True:
                line = raw_input('$ ')
                if line in comp_keys:
                    break
                print('Incorrect input: %s'%line)
        else:
            line = raw_input("$ ")
        return line

    def clean_inp(self, inp):
        return inp.strip().lower()

    def setup_parser(self):
        # Parser related
        import readline as rl
        import os
        # We need to setup tab completion
        menu = Menus()
        self.Menus = menu
        mkeys = menu.menu_dict[menu.menu_state]
        mkeys += ['exit', 'quit']
        self.mkeys = mkeys
        self.Completer = Completer(mkeys)
        rl.set_completer(self.Completer.complete)
        self.rl = rl
        # Read some options
        if os.path.isfile('.rl.rc'):
            rl.read_init_file('.rl.rc')
        else:
            f = open('.rl.rc', 'w')
            f.writelines(['tab: complete\n','set editing-mode vi'])
            f.close()
            rl.read_init_file('.rl.rc')
    ## eof Lower level
