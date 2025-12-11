import math

from .property import Property

class Negation(Property):
    def subquestions_count(self) -> int:
        return 2

    def violation(self, answers: list[float]) -> float:
        if len(answers) != 2:
            raise RuntimeError("Negation property expects exactly 2 answers.")

        return math.fabs(answers[0] + answers[1] - 1.0)
    
    def name(self) -> str:
        return "negation"