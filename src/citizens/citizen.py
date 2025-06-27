

class Citizen:
    def __init__(self, id: str, political_affiliation, age: int = -1):
        self.id: str = id
        self.political_affiliation = political_affiliation
        self.age: int = age
        self.voted_for = None
        self.has_voted: bool = False

    def __repr__(self):
        return f"Citizen(id={self.id}, age={self.age}, political affiliation={self.political_affiliation})"
    
    def __str__(self):
        return f"Citizen {self.id} (political affiliation: {self.political_affiliation}, age: {self.age})"

    def get_political_affiliation(self):
        return self.political_affiliation
    
    def get_id(self) -> str:
        return self.id
    
    def get_age(self) -> int:
        return self.age
    
    def rank_candidates(self, candidates):
        """
        Ranks the candidates based on the citizen's preferences.
        This method should be overridden in subclasses if needed.
        """
        raise NotImplementedError("This method should be overridden in subclasses.")
    
    def vote(self, candidate):
        """
        Marks the citizen as having voted for a candidate.
        """
        if not self.has_voted:
            self.voted_for = candidate
            self.has_voted = True
        else:
            raise ValueError("Citizen has already voted.")