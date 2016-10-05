from base_modules import BaseModule
from msgs import ReadInput, QuitGame
import sys

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
        self.name = "InpReader"
        self.reading = False
        self.reading_for = None

    def setup_parser(self):
        # Parser related
        import readline as rl
        import os
        # We need to setup tab completion
        mkeys = self.att_modules['MainBus'].att_modules['GameState'].menu_dict.keys()
        mkeys += ['exit', 'quit']
        self.mkeys = mkeys
        rl.set_completer(Completer(mkeys).complete)
        # Read some options
        if os.path.isfile('.rl.rc'):
            rl.read_init_file('.rl.rc')
        else:
            f = open('.rl.rc', 'w')
            f.writelines(['tab: complete\n','set editing-mode vi'])
            f.close()
            rl.read_init_file('.rl.rc')

    def handle_msg(self, msg):
        if msg.mtype == "READING_STATUS":
            if msg.player:
                self.set_status(msg.content, player=msg.player)
            else:
                self.set_status(msg.content)
        else:
            pass

    def set_status(self, status, player=None):
        self.reading = status
        if player:
            self.reading_for = player
        else:
            self.reading_for = None

    def input_loop(self, inp, comp_check=True):
        #line = ''
        #while line != 'stop':
        #    line = raw_input("Please enter a %s: "%inp)
        #return line.replace("\n","")
        print("Please enter a %s:"%inp)
        if comp_check:
            while True:
                line = raw_input('$ ')
                if line in self.mkeys:
                    break
                print('ENTERED %s'%line)
        else:
            line = raw_input("$ ")
        return line

    def run(self):
        self.setup_parser()
        while len(self.msg_q) > 0:
            curr_msg = self.msg_q.pop(0)
            self.handle_msg(curr_msg)
        if self.reading == "MOVE" and self.reading_for:
            inp = self.input_loop("move", comp_check=False)
            inp = self.clean_inp(inp)
            #print(inp)
            IM = ReadInput(content=inp, player=self.reading_for)
            self.reading = False
            self.send_to_bus(IM)
        elif self.reading == "COMMAND":
            inp = self.input_loop("command")
            inp = self.clean_inp(inp)
            #print(inp)
            IM = ReadInput(content=inp)
            self.reading = False
            self.send_to_bus(IM)
        else:
          pass

    def clean_inp(self, inp):
        return inp.strip().lower()
