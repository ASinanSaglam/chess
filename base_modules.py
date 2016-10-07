# A decorator for the classes
#def in_history(f):
#    def new_f(*args, **kwargs):
#        args[0].msg_history.append(args[1])
#        f(*args, **kwargs)
#    return new_f

# Module classes
class BaseModule(object):
    '''
    Every module will have a history, types of msges they know
    and a list of attached modules. At the moment sending basically
    just calls the target modules receive function
    '''
    def __init__(self):
        self.msg_q = []
        self.msg_q_n = []
        self.att_modules = {}
        self.msg_types = {}
        self.msg_history = []
        self.name = "Base"

    def send(self, msg, tmodule):
        #print("me: %s"%self.name)
        #print("Sending msg to module")
        #print(msg, tmodule)
        tmodule.msg_q.append(msg)

    def send_now(self, msg):
        if self.name != "MainBus":
            MB = self.att_modules["MainBus"]
            modules = MB.att_modules
        else: 
            modules = self.att_modules
        modules[msg.tmodule].handle_msg(msg)

    def send_to_bus(self, msg):
        self.send(msg, self.att_modules["MainBus"])

    def attach_module(self, module):
        self.att_modules[module.name] = module

    def connect_module(self, module):
        self.att_modules[module.name] = module
        module.att_modules[self.name] = self

    def run(self):
        #print("me: %s"%self.name)
        #print("Processing queue")
        #print(self.msg_q)
        if len(self.msg_q_n) > 0:
            self.msg_q = self.msg_q_n + self.msg_q
        self.msg_q_n = []
        while len(self.msg_q) > 0:
            curr_msg = self.msg_q.pop(0)
            self.handle_msg(curr_msg)
            #print("current_msg")
            #print(curr_msg.content)
            #try:
            #    print("handling")
            #    print(curr_msg)
            #    print("by:")
            #    print(self)
            #    self.handle_msg(curr_msg)
            #except:
            #    print("couldn't handle msg")
            #    self.msg_q_n.append(curr_msg)
            #print("after handling")
            #print(self.msg_q)

class BaseMsg(object):
    '''
    A message class is only an object with a specific message type 
    and some attributes so that the target module knows what to do 
    with the module. All types are in all caps
    '''
    def __init__(self, content=None, mtype='BASE'):
        self.mtype = mtype
        self.content = content

class BasePlayer(object):
    '''
    A player class, also will allow for future AI hooks
    '''
    def __init__(self, ptype='BASE', turn=False):
        self.ptype = ptype
        self.turn = turn
