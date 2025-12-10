from abc import ABC, abstractmethod

class Property(ABC):
    @abstractmethod
    def subquestions_count(self) -> int:
        """
        :return: The number of subquestions.
        """
        pass

    @abstractmethod
    def violation(self, answers: list[float]) -> float:
        """
        Compute the violation given a list of answers.
        Answers list length should match the number of subquestions.
        Answers must be already averaged.
        :param answers: List of answers corresponding to the subquestions.
        :return: A float representing the violation.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """
        :return: The name of the property.
        """
        pass