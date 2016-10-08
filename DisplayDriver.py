#!/usr/bin/env python
# -*- coding: utf8 -*-

import numpy as np

from base_modules import BaseModule
from msgs import GetInput, QuitGame, GotoMenu, ShowBoard

class DisplayDriver(BaseModule):
    def __init__(self, term=None):
        super(DisplayDriver, self).__init__()
        self.name = "DisplayDriver"
        self.BD = BoardDisplay(driver=self)
        self.term = term

    ## sof Module level
    def handle_msg(self, msg):
        # Pass moves to board displayer
        if msg.mtype == "PROCESSED_MOVE":
            self.BD.handle_msg(msg)
            msg.player.read_input()
        elif msg.mtype == "RENDER_BOARD":
            self.BD.handle_msg(msg)
            msg.player.read_input()
        elif "RENDER_MENU" in msg.mtype:
            self.menu_display(msg)
            self.send_to_bus(GetInput(inptype="COMMAND", Menus=msg.Menus))
        elif msg.mtype == "RENDER_HISTORY":
            self.render_history(msg)
        elif msg.mtype == "CURRENT_BOARD":
            self.board = msg.board
        else:
            pass
    ## eof Module level

    ## sof Msg level
    def menu_display(self, msg):
        if self.term:
            self._menu_display_term(msg)
        else:
            self._menu_display_noterm(msg)

    def render_history(self, msg):
        if self.term:
            self._render_hist_term(msg.history)
        else:
            self._render_hist_noterm(msg.history)
    ## eof Msg level

    ## sof Lower level
    def _menu_display_term(self, msg):
        menu_name = msg.Menus.menu_state
        menu_content = msg.Menus.menu_choices
        if menu_content[0] == "NOT_IMPLEMENTED":
            return GotoMenu(Menus=msg.Menus)
        elif menu_content[0] == "QUIT_GAME":
            return QuitGame()
        # We have blessings, let's improve the view
        print(self.term.clear())
        h, w = self.term.height, self.term.width
        print(self.term.move(h/2-(h/4), 0) + "{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("{0:{fill}{align}{width}}".format(" Welcome to Chessmasher5000 ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("")
        # Print menu name here
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("{0:{fill}{align}{width}}".format(" "+menu_name+" ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format(" Type to navigate menus ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("")
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        for elem in menu_content:
            if menu_name == 'settings':
                opts = msg.Menus.opts_dict
                set_keys = msg.Menus.setting_dict
                print("{0:{fill}{align}{width}}".format(" "+elem+": "+opts[set_keys[elem]]+" ", fill="#", align="^", width=w) )
            else:
                print("{0:{fill}{align}{width}}".format(" "+elem+" ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))

    def _menu_display_noterm(self, msg):
        menu_name = msg.Menus.menu_state
        menu_content = msg.Menus.menu_choices
        if menu_content[0] == "NOT_IMPLEMENTED":
            return GotoMenu(content=msg.Menus.prev_menu, Menus=msg.Menus)
        elif menu_content[0] == "QUIT_GAME":
            return QuitGame()
        print("###################################")
        print("### Welcome to Chessmasher5000 ####")        
        print("###################################")        
        # Print menu name here
        print("{0:{fill}{align}{width}}".format("# "+menu_name+" ", fill="#", align="<", width=35))
        print("## Type to navigate menus #########")        
        print("###################################")        
        for elem in menu_content:
            if menu_name == 'settings':
                opts = msg.Menus.opts_dict
                set_keys = msg.Menus.setting_dict
                print("# {0}".format(elem) + ": " + opts[set_keys[elem]]+ " ")
            else:
                print("# {0}".format(elem))
        print("###################################")        


    def _render_hist_term(self, hist):
        print(self.term.clear())
        h, w = self.term.height, self.term.width
        print(self.term.move(h/2-(h/4), 0) + "{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print("{0:{fill}{align}{width}}".format(" Game History ", fill="#", align="^", width=w) )
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        print(", ".join(hist))
        print("")
        raw_input("Press enter to continue!")

    def _render_hist_noterm(self, hist):
        print("Game history: ")
        print(", ".join(hist))
    ## eof Lower level


class BoardDisplay(BaseModule):
    def __init__(self, driver=None):
        super(BoardDisplay, self).__init__()
        self.name = "BoardDisplay"
        self.DisplayDriver = driver

        #try:
        self.pieceDict = {
              ".": ".", "p": u'\u2659', "N": u'\u2658', 
              "B": u'\u2657', "R": u'\u2656', "Q": u'\u2655',
              "K": u'\u2654', "o": u'\u265F', "n": u'\u265E', 
              "b": u'\u265D', "r": u'\u265C', "q": u'\u265B',
              "k": u'\u265A'}
        #except:
        #    self.pieceDict = {
        #          0: ".", 1: "P", 2: "N", 
        #          3: "B", 4: "R", 5: "Q",
        #          6: "K", -1: "o", -2: "n", 
        #          -3: "b", -4: "r", -5: "q",
        #          -6: "k" }

    def handle_msg(self, msg):
        if msg.mtype == "PROCESSED_MOVE":
            self.displayMove(msg)
        elif msg.mtype == "RENDER_BOARD":
            self.displayMove(msg)
        else:
            pass

    def displayMove(self, msg):
        if self.DisplayDriver.term:
            self._displayMoveTerm(msg)
        else:
            self._displayMoveNoTerm(msg)

    def displayBoard(self, board):
        if self.DisplayDriver.term:
            self._displayMoveTerm(None,board=board)
        else:
            self._displayMoveNoTerm(None,board=board)

    def get_turn(self):
        board = self.board
        return int(board[0])

    def _displayMoveNoTerm(self,msg,board=None):
        if not board:
            self.board = msg.board
            turn = self.get_turn()
        else:
            turn = int(board[0])

        if not turn:
            print("###################################")        
            print("#####   Whites turn to play   #####")
        else:
            print("###################################")        
            print("#####   Blacks turn to play   #####")
        if not board:
            self._printBoardNoTerm()
        else:
            self._printBoardNoTerm(board=board)

    def _displayMoveTerm(self,msg,board=None):
        if not board:
            self.board = msg.board
            turn = self.get_turn()
        else:
            turn = int(board[0])

        t = self.DisplayDriver.term
        h, w = t.height, t.width
        print(t.clear())
        if not turn:
            print(t.move(h/2-(h/4),0) + "{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
            print("{0:{fill}{align}{width}}".format(" Whites turn to play ", fill="#", align="^", width=w) )
            print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        else:
            print(t.move(h/2-(h/4),0) + "{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
            print("{0:{fill}{align}{width}}".format(" Blacks turn to play ", fill="#", align="^", width=w) )
            print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
        if not board:
            self._printBoardTerm()
        else:
            self._printBoardTerm(board=board)


    def trPiece(self, piece):
        """
        Helper function for translating the chess pieces. Meant to be 
        used for function "map" in order to convert from index to piece.

        """
        return self.pieceDict[piece]

    def _printBoardNoTerm(self, board=None):
        """
        A way to print the board to the output. For now it only uses
        print but later we should implement stuff to deal with commandlines
        so that this works in bash/zsh etc. 

        Returns:
          Nothing, just prints the board. 
        """

        if not board:
            board = self.board[31:109]
        else:
            board = board[31:109]
        board = u"".join(board.split())
        board = map(self.trPiece, board)
        board = u"".join(board)
        #print("Current Board State")
        print("###################################")        
        print("   --------------------------")
        print( u" 8 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[0:8])) 
        print( u" 7 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[8:16])) 
        print( u" 6 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[16:24])) 
        print( u" 5 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[24:32])) 
        print( u" 4 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[32:40])) 
        print( u" 3 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[40:48])) 
        print( u" 2 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[48:56])) 
        print( u" 1 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[56:64])) 
        print("   --------------------------")
        print( "     {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  "\
                     .format(*['A','B','C','D','E','F','G','H',]))
        print("###################################")        

    def _printBoardTerm(self, board=None):
        """
        A way to print the board to the output. For now it only uses
        print but later we should implement stuff to deal with commandlines
        so that this works in bash/zsh etc. 

        Returns:
          Nothing, just prints the board. 
        """

        t = self.DisplayDriver.term
        h, w = t.height, t.width

        if not board:
            board = self.board[31:109]
        else:
            board = board[31:109]
        board = u"".join(board.split())
        board = map(self.trPiece, board)
        board = u"".join(board)
        print("")
        print("{0:{align}{width}}".format("   --------------------------", align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 8 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[0:8]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 7 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[8:16]), align="^", width=w)) 
        print(u'{0:{align}{width}}'.format(u" 6 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[16:24]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 5 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[24:32]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 4 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[32:40]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 3 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[40:48]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 2 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[48:56]), align="^", width=w))
        print(u'{0:{align}{width}}'.format(u" 1 | {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7} |".format(*board[56:64]), align="^", width=w))
        print("{0:{align}{width}}".format("   --------------------------", align="^", width=w))
        print("{0:{align}{width}}".format( "     {0}  {1}  {2}  {3}  {4}  {5}  {6}  {7}  "\
                     .format(*['A','B','C','D','E','F','G','H',]), align="^", width=w))
        print("")
        print("{0:{fill}{align}{width}}".format("", fill="#", align="<", width=w))
