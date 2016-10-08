from base_modules import BaseModule
from Players import HumanPlayer, AIPlayer
from Menus import Menus
from msgs import GetInput, RenderMenu, InvalidCommand, ShowBoard, StartGame, \
                 ShowHistory, ShowBoardNow, ShowHistoryNow
# SetOptions
class GameState(BaseModule):
    def __init__(self):
        super(GameState, self).__init__()
        self.name = "GameState"
        self.in_game = False
        self.running = True
        self.paused = False
        self.players = []
        self.Menus = Menus(menu_state="main menu")

    ## sof Module level
    def handle_msg(self, msg):
        # Handle quitting
        if msg.mtype == "QUIT_GAME":
            self.quit_game()
        # Handle invalid stuff
        elif msg.mtype == "INVALID_COMMAND":
            self.invalid_command(msg)
        elif msg.mtype == "INVALID_MOVE":
            self.invalid_move(msg)
        # Handle menus
        elif msg.mtype == "GOTO_MENU":
            self.goto_menu(msg)
        elif msg.mtype == "START_GAME":
            self.start_game(msg)
        elif msg.mtype == "INIT_GAME":
            self.init_game(msg)
        else:
            pass
    ## eof Module level

    ## sof Msg level
    def quit_game(self):
        print("Quitting game!")
        self.save_opts()
        print("Final board position: ")
        self.send_now(ShowBoardNow())
        if self.Menus.opts_dict['print_hist_on_quit'] == 'True' and self.in_game:
            self.send_now(ShowHistoryNow())
        self.running = False

    def invalid_command(self, msg):
        print("Invalid command, try again.")
        if msg.player:
            msg.player.read_input()
        else:
            self.send_to_bus(GetInput(inptype="COMMAND", Menus=self.Menus))

    def invalid_move(self, msg):
        print("Invalid move, try again.")
        msg.player.read_input()

    def goto_menu(self, msg):
        MM = self.set_menu(msg)
        self.send_to_bus(MM)

    def start_game(self, msg):
        self.players = msg.players
        self.in_game = True
        self.send_to_bus(ShowBoard())

    def init_game(self, msg):
        self.load_opts()
        # Initialize game, we are in menus now
        if self.Menus.menu_state != "main menu":
            self.Menus.menu_state = "main menu"
        self.send_now(RenderMenu(Menus=self.Menus))
    ## eof Msg level

    ## sof Lower level
    def load_opts(self, filename='.cmasher_opts.yaml'):
        import os, yaml
        if os.path.isfile(filename):
            opts = open('.cmasher_opts.yaml', 'r')
            self.Menus.opts_dict = yaml.load(opts)
        else:
            # Defaults here
            self.Menus.opts_dict = {'ai_diff': '1',
                         'ai_type': 'random',
                         'print_hist_on_quit': 'True', 
                         'blessed_term': 'True'}
            self.save_opts()
        #self.send_to_bus(SetOptions(content=self.opts_dict))


    def save_opts(self, filename='.cmasher_opts.yaml'):
        import os, yaml
        if os.path.isfile(filename):
            os.remove(filename)
        with open(filename, 'w') as ofile:
            yaml.dump(self.Menus.opts_dict, ofile, default_flow_style=True)
        #self.send_to_bus(SetOptions(content=self.opts_dict))
        

    def set_menu(self, msg):
        # some logic here
        if not msg.content:
            return RenderMenu(Menus=self.Menus)

        if self.Menus.menu_dict[msg.content] == ["new_lmulti"]:
            import random
            t1 = random.randint(0,100)%2 
            t2 = (t1+1)%2
            Player1 = HumanPlayer(turn=t1)
            Player2 = HumanPlayer(turn=t2)
            return StartGame(players=[Player1, Player2])
        elif self.Menus.menu_dict[msg.content] == ["new_single"]:
            import random
            t1 = random.randint(0,100)%2 
            t2 = (t1+1)%2
            Player1 = HumanPlayer(turn=t1)
            #Player2 = AIPlayer(turn=t2)
            Player2 = AIPlayer(turn=t2, aitype='basic')
            return StartGame(players=[Player1, Player2])
        elif self.Menus.menu_dict[msg.content] == ["set_hist_on_quit"]:
            self.switch_option('print_hist_on_quit')
            return RenderMenu(Menus=self.Menus)
        elif self.Menus.menu_dict[msg.content] == ["set_blessing"]:
            self.switch_option('blessed_term')
            return RenderMenu(Menus=self.Menus)
        elif self.Menus.menu_dict[msg.content] == ["not_implemented"]:
            return RenderMenu(Menus=self.Menus)

        if (not self.in_game) or self.paused:
            if not self.Menus.goto_menu(msg.content):
                return InvalidCommand()
        # Now we can handle the rendering
        return RenderMenu(Menus=self.Menus)

    def switch_option(self, option):
        try:
            val = self.Menus.opts_dict[option] 
            if self.Menus.opts_dict[option] == 'True':
                self.Menus.opts_dict[option] = 'False'
            else:
               self.Menus.opts_dict[option] = 'True'
        except:
            self.Menus.opts_dict[option] = 'True'
        self.save_opts()

    def add_player(self, player):
        self.players.append(add_player)
    ## eof Lower level
