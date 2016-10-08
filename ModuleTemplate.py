from base_modules import BaseModule

class TemplateModule(BaseModule):
    '''
    This is a template module to follow for the future modules 
    ''' 
    def __init__(self):
        super(TemplateModule, self).__init__()
        self.name = "TemplateModule"

    ## sof Module level
    def handle_msg(self, msg):
        if msg.mtype == "SAMPLE_MSG":
            self.sampleMsgFunc(msg)
        else:
            pass
    ## eof Module level 

    ## sof Msg level
    def sampleMsgFunc(self, msg):
        stuff = msg.content
        SampleMsg = sampleLowerFunc(stuff)
        self.send_to_bus(SampleMsg)
        return
    ## eof Msg level

    ## sof Lower level
    def sampleLowerFunc(self, msg):
        pass
    ## eof Lower level
