import requests
import json

from src.command import CommandTrigger


class SpeekRecognizer:
    def regcognize(self, data) :
        pass

class BaiduSpeekRecognizer(SpeekRecognizer) :
    appid = '15534257'
    appkey = 'nblpNvt7OfULKmHqVk7SLdGi'
    secretkey = 'D1FY0kkSmDgl8u1BzxuYAPFEbBXZl0Fl'

    headers = {'Content-Type': 'audio/pcm;rate=16000'}
    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        '''
        Access Token 有效期为一个月
        :return:
        '''
        server = "https://openapi.baidu.com/oauth/2.0/token?"
        grant_type = "client_credentials"
        # API Key
        client_id = self.appkey
        # Secret Key
        client_secret = self.secretkey

        url = "%sgrant_type=%s&client_id=%s&client_secret=%s" % (server, grant_type, client_id, client_secret)
        # 获取token
        res = requests.post(url)
        token = json.loads(res.text)["access_token"]

        return token


    def regcognize(self, data = b''):
        server = 'http://vop.baidu.com/server_api'
        url = '%s?dev_pid=1536&cuid=hypermind&token=%s' % (server, self.token)
        res = requests.post(url, data = data, headers = self.headers)
        fdata = json.loads(res.text)
        if fdata['err_no'] == 0 :
            return(fdata['result'][0])
        return ''

class BaiduInteraction:
    #百度UNIT 理解和交互的配置数据
    appid = '15534301'
    appkey = '3gqBI5oIGTdxjNizhCjBHsXC'
    secretkey = 'HOK2DY4ggXvVnZOmaIGwrufvAdlraXOd'

    #发送数据的头部
    headers = {'Content-Type': 'application/json'}

    #会话ID
    session_id = ''

    def __init__(self):
        '''
        初始化权限Token
        '''
        self.token = self.get_token()

    def get_token(self):
        '''
        Access Token 有效期为一个月
        :return:
        '''
        server = "https://openapi.baidu.com/oauth/2.0/token?"
        grant_type = "client_credentials"
        # API Key
        client_id = self.appkey
        # Secret Key
        client_secret = self.secretkey

        url = "%sgrant_type=%s&client_id=%s&client_secret=%s" % (server, grant_type, client_id, client_secret)
        # 获取token
        res = requests.post(url)
        token = json.loads(res.text)["access_token"]

        return token

    def clear_session(self):
        '''
        清除session对话
        :return:
        '''
        self.session_id = ''

    def parse(self, content):
        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + self.token
        data = {
            'log_id': 'hypermind',
            'version': '2.0',
            'service_id': 'S13423',
            'session_id': self.session_id,
            'request': {
                'query': content,
                'user_id': 'hypermind'
            }
        }
        res = requests.post(url, json = data, headers = self.headers)
        fdata = json.loads(res.text)
        if fdata['error_code'] == 0:
            self.last_dialog = fdata['result']
            self.session_id = self.last_dialog['session_id']
            return True
        return False

    def get_response(self):
        return self.Response(self.last_dialog['response_list'])

    class Response:
        '''
        回复类
        通过这个类可以解析获取机器人要说的话 要做的动作
        解析机器人的意图 并调用命令触发器执行意图
        '''
        class NoResponseException(Exception):
            pass

        def __init__(self, responses):
            if len(responses) > 0 :
                self.response = responses[0] #取得最佳回复
                action_list = self.response['action_list']
                if len(action_list) > 0:
                    #取得最佳action
                    self.action = action_list[0]
            else:
                raise self.NoResponseException #抛出无回复异常

        def get_say(self):
            '''
            :return: 机器人要说的话
            '''
            return self.action['say']

        def get_action(self):
            '''
            :return:  获得要做的动作
            '''
            return self.action['action_id']

        def exe_cmd(self, command_trigger):
            '''
            执行Response 中的命令意图
            :param command_trigger: 命令触发器
            :return: None
            '''
            schema = self.response['schema']

            print(schema)
            if 'slots' in schema:
                slots = schema['slots']
                for slot in slots:
                    command_trigger.trigger(schema['intent'], slot['name'], slot['normalized_word'])
            else:
                command_trigger.trigger(schema['intent'])

if __name__ == '__main__':
    def walk_callback(name, arg):
        print("运动意图 : 名称 : %s 数据 : %s" % (name, arg))
    def default_callback(intent, name, arg):
        print("未知意图 : ", intent, "   名称 : ", name, "  参数 :  - ", arg)

    cmd = CommandTrigger()
    cmd.add_intent("ROBOT_WALK", walk_callback)
    cmd.add_intent("default", default_callback)

    bi = BaiduInteraction()
    bi.parse("向前走")
    res = bi.get_response()

    print(res.get_say())
    res.exe_cmd(cmd)




