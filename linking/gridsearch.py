import subprocess
import os
import sys

class Scorer:
    def __init__(self, gold_file):
        self.gold_file = gold_file
        self.gold_data = {}

    def Score(self, pred_file):
        if not self.gold_data:
            self.gold_data = self._read(self.gold_file)

        # Load the gold standard
        gold = self.gold_data
        n_gold = len(gold)

        # Load the predictions
        pred = self._read(pred_file)
        n_predicted = len(pred)

        # Evaluate predictions
        n_correct = sum(int(pred[i] == gold[i]) for i in set(gold) & set(pred))
        print('correct: %s' % n_correct)

        # Calculate scores
        precision = float(n_correct) / float(n_predicted)
        print('precision: %s' % precision)
        recall = float(n_correct) / float(n_gold)
        print('recall: %s' % recall)
        f1 = 2 * ((precision * recall) / (precision + recall))
        print('f1: %s' % f1)

        return (f1, precision, recall, n_correct)

    def _read(file):
        data = {}
        for line in open(file):
            record, string, entity = line.strip().split('\t', 2)
            data[(record, string)] = entity
        n_predicted = len(data)
        print('rows: %s' % n_predicted)
        return data

## SETTINGS
#Gridsearch options
cleanOptions = [1, 2]
extractOptions = ["en_core_web_sm","en_core_web_lg"]

#Paths
gold_file = ""
output_file = "gridsearch_outcomes.csv"

scorer = Scorer(gold_file)
results =  {}
for cleanOption in cleanOptions:
    for extractOption in extractOptions:
            outputFileName = "clean-" + str(cleanOption) + "|extract-" + extractOption + ".txt"
            subprocess.call(["python3", "./linking/main.py", "--clean_text", str(cleanOption), "--extract_model", extractOption, "--output_filename", outputFileName])
            f1, precision, recall, n_correct = scorer.Score(outputFileName)
            results[outputFileName] = (f1, precision, recall, n_correct)

results.to_csv(output_file, index=False)

