import random
import json
from locust import HttpUser, task, between


class TranslateUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def translate_engToChinese(self):
        eng_words = [
            "ability",
            "able",
            "about",
            "above",
            "accept",
            "according",
            "account",
            "across",
        ]

        req = {"text": random.choice(eng_words)}
        response = self.client.post("api/translate/english", json.dumps(req))

        print(response.text)

    @task
    def translate_chineseToEng(self):

        chinese_words = ["你好", "爱", "幸福", "微笑", "中国人", "是的", "再见", "谢谢你"]

        req = {"text": random.choice(chinese_words)}
        response = self.client.post("api/translate/chinese", json.dumps(req))

        print(response.text)
