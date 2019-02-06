import requests
import json

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
    appid = '15534301'
    appkey = '3gqBI5oIGTdxjNizhCjBHsXC'
    secretkey = 'HOK2DY4ggXvVnZOmaIGwrufvAdlraXOd'
    headers = {'Content-Type': 'application/json'}

    session_id = ''

    def __init__(self):
        self.token = self.get_token()
        print(self.token)

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
        # print(fdata)
        if fdata['error_code'] == 0:
            self.last_dialog = fdata['result']
            self.session_id = self.last_dialog['session_id']

            first_action = fdata['result']['response_list'][0]['action_list'][0]
            return first_action['say']
        return ""

if __name__ == '__main__':
    bi = BaiduInteraction()
    bi.parse("往右走10米")
