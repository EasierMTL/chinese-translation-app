from datasets import load_metric
from chinese_translation_api.models.base import ChineseToEnglishTranslator, Predictor
from tqdm import tqdm
from chinese_translation_api.evaluation.debug_memory import track


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class EvaluationPipeline:
    """
    Steps:
    1. Read the test data and labels batchwise
    2. Run the model for each input and store the predictions in a list
    3. Run a corpus level BLEU.
    """

    def __init__(self, predictor: Predictor) -> None:
        self.test_ch = []
        self.test_labels = []
        self.predictions = []
        self.predictor = predictor

    @track
    def load_dset(self, dset_path: str):
        """Loads the dataset
        """
        with open(dset_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # print(lines)
        print(len(lines))
        # Get rid of all white space
        newLines = []
        for line in lines:
            if not (line == "\n"):
                newLines.append(line.strip())

        print("Removed whitespace: ", len(newLines))
        # Translation format:
        # - 1 Chinese sentence
        # - 2 reference english translations
        i = 0
        while (i < len(newLines)):
            ch_line = newLines[i]
            eng_labels = [newLines[i + 1], newLines[i + 2]]

            self.test_ch.append(ch_line)
            self.test_labels.append(eng_labels)
            i += 3
        print("Num test samples: ", len(self.test_ch), len(self.test_labels))

        print("Example batch:\n", self.test_ch[0], self.test_labels[0])

    @track
    def evaluate(self, batch_size: int = 8):
        """Runs prediction on entire dataset and calculates the corpus BLEU.
        """
        bleu = load_metric("bleu")
        batched_input = chunks(self.test_ch, batch_size)
        batched_labels = chunks(self.test_labels, batch_size)
        for batch, label_batch in tqdm(zip(batched_input, batched_labels),
                                       len=len(batched_input)):
            pred_batch = self.predictor.predict(batch)
            bleu.add_batch(pred_batch, label_batch)

        # calculate BLEU
        results = bleu.compute()
        print("Results:\n", results)
