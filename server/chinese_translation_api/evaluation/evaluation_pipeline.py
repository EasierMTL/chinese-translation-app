from multiprocessing import Lock
from multiprocessing.pool import ThreadPool
from datasets import load_metric
from chinese_translation_api.models.base import Predictor
from chinese_translation_api.evaluation.debug_memory import track
from tqdm import tqdm
import json


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
            eng_labels = newLines[i + 1]
            # newLines[i + 2] is just the base model's prediction

            self.test_ch.append(ch_line)
            self.test_labels.append(eng_labels)
            i += 3
        print("Num test samples: ", len(self.test_ch), len(self.test_labels))

        print("Example batch:\n", self.test_ch[0], self.test_labels[0])

    @track
    def evaluate(self,
                 max_samples=10000,
                 num_workers=1,
                 sentence_bleu=True,
                 print_bleu_every: int = 100):
        """Runs prediction on entire dataset and calculates the corpus BLEU.
        """
        num_samples = len(self.test_ch)
        if (num_samples < max_samples):
            raise IndexError(f"max_samples must be <= {num_samples}")

        combined_data = zip(self.test_ch[:max_samples],
                            self.test_labels[:max_samples])
        all_results = []

        predictions = []
        references = []

        if (sentence_bleu):

            def process_data(args):
                bleu = load_metric("bleu")
                pred = self.predictor.predict(args[0]).split(" ")
                # Pretty sure label[1].split(" ") was the base model prediction...
                # processed_labels = [label[0].split(" "), label[1].split(" ")]
                processed_labels = args[1].split(" ")
                results = bleu.compute(predictions=[pred],
                                       references=[[processed_labels]])
                all_results.append(results)
        else:

            bleu = load_metric("bleu")
            lock = Lock()

            def process_data(args):
                pred = self.predictor.predict(args[0]).split(" ")
                # Pretty sure label[1].split(" ") was the base model prediction...
                # processed_labels = [label[0].split(" "), label[1].split(" ")]
                processed_labels = args[1].split(" ")
                lock.acquire()
                # bleu.add_batch(predictions=[pred],
                #                references=[[processed_labels]])
                predictions.append(pred)
                references.append([processed_labels])
                lock.release()

        t = ThreadPool(num_workers)
        counter = 0
        for _ in tqdm(t.imap_unordered(process_data, list(combined_data)),
                      total=len(list(combined_data))):
            counter += 1
            if (counter % print_bleu_every == 0 and counter != max_samples):
                results = bleu.compute(predictions=predictions,
                                       references=references)
                print(f"\nBLEU at {counter}: {results['bleu']}")
            pass
        t.close()
        t.join()

        # calculate BLEU
        if (sentence_bleu):
            avg_bleu = 0
            for result in all_results:
                avg_bleu += result["bleu"]
            avg_bleu = avg_bleu / len(all_results)

            print("Average BLEU:\n", avg_bleu)

            with open('results.json', 'w') as f:
                json.dump(all_results, f)
        else:
            results = bleu.compute(predictions=predictions,
                                   references=references)
            print("Results:\n", results)
