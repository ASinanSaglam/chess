from CBoard import CBoard
from MainBus import MainBus
from DisplayDriver import DisplayDriver
from InputParser import InputParser
from InputReader import InputReader
from GameState import GameState
from Referee import CRef
from msgs import InitGame
import sys

class GameInit(object):
    def __init__(self):
        self.MB = MainBus()
        self.GState = GameState()
        self.DDisp = DisplayDriver()
        self.IParse = InputParser()
        self.Inp = InputReader()
        self.CB = CBoard()
        self.Ref = CRef()
        self.MB.connect_module(self.GState)
        self.MB.connect_module(self.IParse)
        self.MB.connect_module(self.DDisp)
        self.MB.connect_module(self.Inp)
        self.MB.connect_module(self.CB)
        self.MB.connect_module(self.Ref)

    def run(self):
        import os, yaml
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
                        self.CB.run()
                        self.DDisp.run()
                        self.GState.run()
                sys.exit()
            except:
                pass
        self.MB.msg_q.append(InitGame())
        while self.GState.running:
            self.MB.run()
            self.Inp.run()
            self.IParse.run()
            self.Ref.run()
            self.CB.run()
            self.DDisp.run()
            self.GState.run()
        sys.exit()
