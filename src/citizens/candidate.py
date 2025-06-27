from .citizen import Citizen

class Candidate(Citizen):
    """
    Represents a candidate for office, inheriting from Citizen.
    A candidate has an ID, political affiliation, age, and a popularity score.
    The candidate has popularity.
    """
    def __init__(self, id: str, political_affiliation, age: int = -1, popularity: float = 1.0):
        super().__init__(id, political_affiliation, age)
        self.popularity: int = popularity

    def __repr__(self):
        return f"Candidate id={self.id}"
    
    def __str__(self):
        return f"Candidate {self.id}"

    def get_popularity(self) -> float:
        """
        Returns the popularity score of the candidate.
        """
        return self.popularity