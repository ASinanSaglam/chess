from InputReader import InputReader
from InputParser import InputParser
from BoardHandler import BoardHandler
from DisplayDriver import DisplayDriver
from GameState import GameState
from Referee import Referee
from MainBus import MainBus

# temporary for testing
from msgs import InitGame

class GameInit(object):
    def __init__(self):
        self.MB = MainBus()
        self.Inp = InputReader()
        self.IParse = InputParser()
        self.BHandler = BoardHandler()
        self.Ref = Referee()
        self.GState = GameState()
        self.DDisp = DisplayDriver()
        self.MB.connect_module(self.Inp)
        self.MB.connect_module(self.IParse)
        self.MB.connect_module(self.BHandler)
        self.MB.connect_module(self.GState)
        self.MB.connect_module(self.Ref)
        self.MB.connect_module(self.DDisp)

    def run(self):
        import os, yaml, sys
        term_opt = 'True'
        filename = '.cmasher_opts.yaml'
        if os.path.isfile(filename):
            opts_f = open('.cmasher_opts.yaml', 'r')
            opts = yaml.load(opts_f)
            try:
                if not (opts['blessed_term'] == 'True'):
                    term_opt = 'False'
            except: 
                pass

        if term_opt == 'True':
            try:
                from blessings import Terminal
                t = Terminal()
                self.MB.msg_q.append(InitGame())
                self.DDisp.term = t
                with self.DDisp.term.fullscreen():
                    while self.GState.running:
                        self.MB.run()
                        self.Inp.run()
                        self.IParse.run()
                        self.Ref.run()
                        self.BHandler.run()
                        self.GState.run()
                        self.DDisp.run()
                    sys.exit()
                sys.exit()
            except:
                self.run_without_term()
        else:
            self.run_without_term()

    def run_without_term(self):
        import sys
        self.MB.msg_q.append(InitGame())
        while self.GState.running:
                self.MB.run()
                self.Inp.run()
                self.IParse.run()
                self.Ref.run()
                self.BHandler.run()
                self.GState.run()
                self.DDisp.run()
        sys.exit()
