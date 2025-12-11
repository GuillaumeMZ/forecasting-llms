import math

from .property import Property

class Bayes(Property):
    def subquestions_count(self) -> int:
        return 4
    
    def violation(self, answers: list[float]) -> float:
        if len(answers) != 4:
            raise RuntimeError("Bayes property expects exactly 4 answers.")
        
        return math.sqrt(math.fabs(answers[0] * answers[2] - answers[1] * answers[3]))
    
    def name(self) -> str:
        return "bayes"