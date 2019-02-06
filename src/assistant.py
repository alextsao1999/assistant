import time

from src.command import CommandTrigger
from src.recognizer import BaiduSpeekRecognizer, BaiduInteraction
from src.trigger import SoundTrigger

class SoundAssistant :
    recognaizer = BaiduSpeekRecognizer()
    interation = BaiduInteraction()

    def __init__(self, command_trigger):
        #开始进入声音监控
        self.sound_trigger = SoundTrigger(200, self.sound_callback, rate=16000)
        self.sound_trigger.start()
        self.command_trigger = command_trigger

    def sound_callback(self, data):
        if len(data) > 10 :
            text = self.recognaizer.regcognize(b''.join(data))
            if text != '':
                print("你说 : ", text)
                response = self.interation.parse(text)
                print("机器人 : ", response)

    def stop(self):
        self.sound_trigger.stop()
        self.sound_trigger.close()

    def is_active(self):
        return self.sound_trigger.is_active()

if __name__ == '__main__':
    def domain_run(intent, value):
        print("跑步!   意图:", intent, " value : ", value)
        pass

    ct = CommandTrigger()
    ct.add_domain("run", domain_run)

    sa = SoundAssistant(ct)

    while sa.is_active():
        time.sleep(0.1)

    sa.stop()


