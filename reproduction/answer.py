import re

ANSWER_REGEX = re.compile(r".*\[Answer\]\s*(\d+\.\d+)", re.DOTALL | re.MULTILINE)

def parse_answer(answer: str) -> float | None:
    matches = ANSWER_REGEX.match(answer)

    if matches is None:
        return None

    return float(matches.group(1))