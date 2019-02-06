class CommandTrigger :
    commands = {}

    def add_domain(self, name, trigger):
        self.commands[name] = trigger
        pass
    def get_domain(self, name):
        return self.commands[name]

    def trigger(self, domain, intent = "", object = ""):
        self.commands[domain] (intent, object)


if __name__ == '__main__':
    res = {"domain": "telephone",
               "intent": "call",
               "object": {
                   "name": "李四"
                   }
           }

    def cell_callback( intent, value ):
        print("cellphone intent: %s  ojbct:%s" % (intent, value))


    ct = CommandTrigger()
    ct.add_domain("cell", cell_callback)
    ct.trigger("cell")
