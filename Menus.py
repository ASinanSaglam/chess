class Menus(object):
    def __init__(self, menu_state="main menu"):
        self.menu_dict = {"main menu": ["new game","load game","settings"],
                          "new game": ["single player", "local multi player"],
                          "load game": ["not_implemented"], 
                          "settings": ["set AI type", "set AI diff", "show hist", "bless term"],
                          "set AI type": ["not_implemented"], 
                          "set AI diff": ["not_implemented"], 
                          "show hist": ["set_hist_on_quit"], 
                          "bless term": ["set_blessing"], 
                          "single player": ["new_single"], 
                          "local multi player": ["new_lmulti"]}
        self.setting_dict = {"set AI type": "ai_type",
                             "set AI diff": "ai_diff",
                             "show hist": "print_hist_on_quit",
                             "bless term": "blessed_term"}
        self.menu_state = menu_state 
        self.menu_choices = self.menu_dict[self.menu_state]
        self.prev_menu = None
        self.opts_dict = None

    def goto_menu(self, menu_str):
        if (menu_str in self.menu_choices) or (menu_str == self.prev_menu):
            self.prev_menu = self.menu_state
            self.menu_state = menu_str
            self.menu_choices = self.menu_dict[menu_str]
            return self.menu_choices
        else:
            return False
