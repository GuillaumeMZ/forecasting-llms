from .property import Property

class Paraphrasing(Property):
    def subquestions_count(self) -> int:
        return 4
    
    def violation(self, answers: list[float]) -> float:
        if len(answers) != 4:
            raise RuntimeError("Paraphrasing property expects exactly 4 answers.")
        
        return max(answers) - min(answers)
    
    def name(self) -> str:
        return "paraphrasing"