import requests

class DingtalkRobot:
    BaseUrl = 'https://oapi.dingtalk.com/robot/send?access_token='

    def __init__(self, token):
        self.token = token
        self.access_url = self.BaseUrl + token

    def send_text(self, content):
        print('Sending message to DingTalk Channel...')
        message = {
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }

        response = requests.post(url=self.access_url, json=message)
        status = response.json()
        if status['errcode'] != 0:
            raise DingtalkRobot.Error('Error Code: {}, {}'.format(
                status['errcode'],
                status['errmsg']
            ))

        return True

    class Error(ValueError):
        pass