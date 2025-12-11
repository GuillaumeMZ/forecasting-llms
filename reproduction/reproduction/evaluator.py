import itertools
import json
from pathlib import Path
from typing import TypedDict

from openrouter import OpenRouter
import polars as pl

from .answer import parse_answer
from .property import Property

class Question(TypedDict):
    id: str
    questions: list[str]

class Input(TypedDict):
    models: list[str]
    temperatures: list[float]
    context: str
    questions: list[Question]

def evaluate_property(client: OpenRouter, property: Property, input_directory: Path) -> pl.DataFrame:
    """
    Evaluate a given property using the provided OpenRouter client.
    
    :param client: An instance of OpenRouter to interact with the language model.
    :param property: An instance of a Property subclass to evaluate
    :return: A list of Result objects containing the evaluation results.
    """
    input: Input = json.load((input_directory / f"{property.name()}.json").open())

    df = pl.DataFrame({
        "model": pl.Series(dtype=pl.Utf8),
        "temperature": pl.Series(dtype=pl.Float64),
        "question_id": pl.Series(dtype=pl.Utf8),
        "answers": pl.Series(dtype=pl.List(pl.Float64)),
    })

    for model, temperature, questions, _ in itertools.product(
        input["models"],
        temperature_:=input["temperatures"],
        input["questions"],
        range(6) if temperature_ == 0.5 else range(3)
    ):
        current_answers: list[float] = []

        for subquestion in questions["questions"]:
            response = client.chat.send(
                model=model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": input["context"]},
                    {"role": "user", "content": subquestion}
                ]
            )

            unparsed_answer = response.choices[0].message.content

            if unparsed_answer is None or not isinstance(unparsed_answer, str):
                # print(f"[WARNING]: could not parse answer for question {subquestion} (answer is None or not a string)")
                break

            maybe_answer = parse_answer(unparsed_answer)

            if maybe_answer is None:
                # print(f"[WARNING]: could not parse answer for question {subquestion} (answer: {unparsed_answer})")
                break

            current_answers.append(maybe_answer)

        if len(current_answers) == len(questions["questions"]):
            df = df.vstack(
                pl.DataFrame({
                    "model": [model],
                    "temperature": [temperature],
                    "question_id": [questions["id"]],
                    "answers": [current_answers],
                })
            )

        current_answers = []

    return df