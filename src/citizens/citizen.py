

class Citizen:
    def __init__(self, id: str, political_affiliation, political_min, political_max, age: int = -1, willingness_to_vote: float = 1.0):
        self.id: str = id
        self.political_affiliation = political_affiliation
        self.age: int = age
        self.voted_for = None
        self.approved_candidates = []
        self.has_voted: bool = False
        self.willingness_to_vote: float = willingness_to_vote  # Default willingness to vote is 1.0
        self.political_min = political_min
        self.political_max = political_max

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
        
    def vote_again(self, candidate):
        if self.has_voted:
            self.voted_for = candidate
        else:
            raise ValueError("Citizen has not voted yet")
        
    def approve(self, candidate):
        """
        Approves a candidate without marking the citizen as having voted.
        This is useful for voting systems where citizens can approve multiple candidates.
        """
        if not self.has_voted:
            self.approved_candidates.append(candidate)
        else:
            raise ValueError("Citizen has already voted.")