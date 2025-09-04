# This is a script for analyzing a single file !!!
# The data from it will be written to sql database

import sqlite3
from constants import *
import argparse
import json

import nltk
from nltk.probability import FreqDist

parser = argparse.ArgumentParser(description="Script for analyzing transcribed data")
parser.add_argument("input_file", help="Your input_file")

args = parser.parse_args()

print(args.input_file)

conn = sqlite3.connect(TRANSCRIBED_DB_PATH)
cur = conn.cursor()

lines = "".join(open(args.input_file, "r").readlines())
tokens = nltk.word_tokenize(lines)
fdist = FreqDist(tokens)

freq_data = {
    "metadata": {
        "filename": args.input_file,
        "total_tokens": len(tokens),
        "unique_tokens": len(fdist.keys())
    },
    "frequency_distribution": dict(fdist.most_common(50))
}

output_json =  args.input_file.replace(".transcribed", ".json").replace(TRANSCRIBED_PATH, TRANSCRIBED_TF_PATH)
with open(output_json, "w") as f:
    json.dump(freq_data, f, ensure_ascii=False, indent=4)


