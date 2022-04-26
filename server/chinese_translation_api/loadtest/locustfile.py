import random
import json
from chinese_translation_api.evaluation.evaluation_pipeline import EvaluationPipeline
from chinese_translation_api.models.base import ChineseToEnglishTranslator
from locust import HttpUser, task, between
import pip


def load_dset():
    translator = ChineseToEnglishTranslator()
    pipeline = EvaluationPipeline(predictor=translator)
    pipeline.load_dset("./test_data/opus-2020-07-17.test.txt")
    global chinese_dset
    chinese_dset = pipeline.test_ch

    return chinese_dset


load_dset()


class TranslateUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def translate_chineseToEng(self):

        # chinese_words = ["你好", "爱", "幸福", "微笑", "中国人", "是的", "再见", "谢谢你"]
        req = {"text": random.choice(chinese_dset)}
        response = self.client.post("api/translate/chinese", json.dumps(req))

        print(response.text)
