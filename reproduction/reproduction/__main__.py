import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from openrouter import OpenRouter

from .bayes import Bayes
from .evaluator import evaluate_property
from .monotonicity import Monotonicity
from .negation import Negation
from .paraphrasing import Paraphrasing
from .property import Property
from .result import serialize_results

if len(sys.argv) != 3:
    print("Usage: python3 -m reproduction <input_directory> <output_directory>")
    sys.exit(1)

input_directory, output_directory = Path(sys.argv[1]), Path(sys.argv[2])

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("No OpenRouter API key set!")

# create output directory if it does not exist
output_directory.mkdir(parents=True, exist_ok=True)

with OpenRouter(api_key) as client:
    steps: list[Property] = [
        Bayes(),
        Monotonicity(),
        Negation(),
        Paraphrasing(),
    ]

    for step in steps:
        results = evaluate_property(client, step, input_directory)
        serialize_results(step, results, output_directory)