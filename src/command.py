class CommandTrigger :
    commands = {}

    def add_intent(self, intent, trigger):
        self.commands[intent] = trigger
        pass
    def get_intent(self, intent):
        return self.commands[intent]

    def trigger(self, intent, name = '', args = None):
        if not intent in self.commands:
            self.commands['default'] (intent, name, args)
        else:
            self.commands[intent] (name, args)

if __name__ == '__main__':
    res = {"domain": "telephone",
               "intent": "call",
               "object": {
                   "name": "李四"
                   }
           }

    def cell_callback( name, args ):
        print("telephone name:%s kwargs:%s" % (name, args))
    def default_callback( intent, name, args):
        print("intent: %s  name: %s  args: %s" % (intent, name, args))
        pass


    ct = CommandTrigger()
    ct.add_intent("default", default_callback)
    ct.add_intent("cell", cell_callback)


    ct.trigger("celldddd", "call", {'number': 1234})
