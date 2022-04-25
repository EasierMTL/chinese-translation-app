from api.models.base import ChineseToEnglishTranslator
from api.evaluation.evaluation_pipeline import EvaluationPipeline

if __name__ == "__main__":
    translator = ChineseToEnglishTranslator()
    pipeline = EvaluationPipeline(predictor=translator)
    pipeline.load_dset("./test_data/opus-2020-07-17.test.txt")
    pipeline.evaluate(batch_size=16)