import requests

class Line_module():
    def __init__(self):
        self.api_url = "https://notify-api.line.me/api/notify"
        self.token = "LYy0yPmrqjMc3rmvdQR2WcbCCVZkmFlf6FZBZGEkpYQ"
        self.headers = {'Authorization':'Bearer '+self.token}

    def send_msg(self):
        self.message = {
            "message" : "[낙상감지 알림] : 낙상이 감지되었습니다!"
        }
        requests.post(self.api_url, headers = self.headers, data = self.message)
