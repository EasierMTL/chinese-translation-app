from chinese_translation_api.models.base import ChineseToEnglishTranslator
from chinese_translation_api.evaluation.evaluation_pipeline import EvaluationPipeline

if __name__ == "__main__":
    from datetime import datetime, timedelta

    translator = ChineseToEnglishTranslator()
    pipeline = EvaluationPipeline(predictor=translator)
    pipeline.load_dset("./test_data/opus-2020-07-17.test.txt")

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    pipeline.evaluate(num_workers=4, sentence_bleu=False, print_bleu_every=2000)

    after = datetime.now()
    after_time = after.strftime("%H:%M:%S")
    print("After Evaluation =", after_time)
    duration = (after - now).total_seconds()
    print("Duration: ", str(timedelta(seconds=duration)))