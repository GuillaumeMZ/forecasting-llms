from scipy.stats import spearmanr

from .property import Property

def _is_increasing(answers: list[float]) -> bool:
    return all(x < y for x, y in zip(answers, answers[1:]))

class Monotonicity(Property):
    def subquestions_count(self) -> int:
        return 5

    def violation(self, answers: list[float]) -> float:
        # From the paper:
        # "Let p be the Spearman correlation between the predictions f(qi) and the set {2040, 2036, 2032, 2028, 2025}."
        # "Our violation metric is then e := (1 - p) / 2 € [0, 1]. In case of increasing monotonicity, we use the Spearman correlation"
        # "with the set {2025, 2028, 2032, 2036, 2040}."

        if len(answers) != 5:
            raise RuntimeError("Monotonicity property expects exactly 5 answers.")
        
        target = [2025, 2028, 2032, 2036, 2040] if _is_increasing(answers) else [2040, 2036, 2032, 2028, 2025]
        (rho, _) = spearmanr(answers, target)
        violation = (1 - rho) / 2 # type: ignore

        return violation
    
    def name(self) -> str:
        return "monotonicity"