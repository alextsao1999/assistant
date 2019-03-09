import time

from src.command import CommandTrigger
from src.recognizer import BaiduSpeekRecognizer, BaiduInteraction
from src.trigger import SoundTrigger

class SoundAssistant :
    #创建识别器
    recognaizer = BaiduSpeekRecognizer()

    #创建交互器
    interation = BaiduInteraction()

    def __init__(self, command_trigger):
        #开始进入声音监控
        self.sound_trigger = SoundTrigger(200, self.sound_callback, rate=16000)
        self.sound_trigger.start()
        self.command_trigger = command_trigger

    def get_command_trigger(self):
        return self.command_trigger

    def sound_callback(self, data):
        if len(data) > 10 :
            text = self.recognaizer.regcognize(b''.join(data))
            if text != '':
                print("你说 : ", text)
                if self.interation.parse(text):
                    response = self.interation.get_response()
                    print("机器人说 : ", response.get_say())
                    response.exe_cmd(self.command_trigger)
                else:
                    print("错误 : 没有回复")


    def stop(self):
        self.sound_trigger.stop()
        self.sound_trigger.close()

    def is_active(self):
        return self.sound_trigger.is_active()

if __name__ == '__main__':
    def default_callback(intent, name, value):
        print("默认(未知)回调   意图:", intent, "   名称 : ", name, "  value : " , value)
        pass
    def robot_walk_callback(name, value):
        print("机器人运动回调被调用了  名称: ", name, "   value : ", value)
        pass

    #创建命令触发器
    ct = CommandTrigger()

    #添加意图触发回调 default 为默认触发
    ct.add_intent("default", default_callback)
    ct.add_intent("ROBOT_WALK", robot_walk_callback)

    #在后台启动声音监测线程
    sa = SoundAssistant(ct)

    #因为是监测非阻塞的 主线程要阻塞一下 防止退出
    while sa.is_active():
        time.sleep(0.1)

    sa.stop()


