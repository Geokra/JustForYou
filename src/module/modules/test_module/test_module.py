from module.module import Module

class TestModule(Module):

    def on_enable(self):
        print("enable")
    
    def on_disable(self):
        print("disable")
