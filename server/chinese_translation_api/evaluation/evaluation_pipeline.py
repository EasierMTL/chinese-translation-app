from multiprocessing.pool import ThreadPool
from datasets import load_metric
from chinese_translation_api.models.base import Predictor
from chinese_translation_api.evaluation.debug_memory import track


def chunks(lst, n):
    """Yield a list of n-sized chunks from lst."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]


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
    def evaluate(self, max_samples=10000, num_workers=1):
        """Runs prediction on entire dataset and calculates the corpus BLEU.
        """
        num_samples = len(self.test_ch)
        if (num_samples < max_samples):
            raise IndexError(f"max_samples must be <= {num_samples}")

        bleu = load_metric("bleu")
        combined_data = zip(self.test_ch[:max_samples],
                            self.test_labels[:max_samples])

        def process_data(args):
            pred = self.predictor.predict(args[0]).split(" ")
            label = args[1]
            processed_labels = [label[0].split(" "), label[1].split(" ")]
            bleu.add(predictions=pred, references=processed_labels)

        t = ThreadPool(num_workers)
        t.map(process_data, combined_data)
        t.close()

        # calculate BLEU
        results = bleu.compute()
        print("Results:\n", results)
