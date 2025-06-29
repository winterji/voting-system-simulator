from .citizen import Citizen
from .candidate import Candidate

class SimpleVoter(Citizen):
    """
    Represents a simple voter in the voting system, inheriting from Citizen.
    A voter has an ID, political affiliation, age, and a flag indicating whether they have
    voted or not. The voter can rank candidates based on their political affiliation.
    
    The SimpleVoter has political affiliation as a single integer. He ranks candidates per distance in one dimensional space.
    """
    def __init__(self, id: str, political_affiliation, political_min, political_max, age: int = -1):
        """"
        id: str
        political_affiliation
        age (optional)
        """
        super().__init__(id, political_affiliation, political_min, political_max, age)

    def __repr__(self):
        return f"Voter(id={self.id}, age={self.age}, political affiliation={self.political_affiliation}, voted={self.voted})"
    
    def __str__(self):
        return f"Voter {self.id} (political affiliation: {self.political_affiliation}, age: {self.age}, voted: {self.voted})"
    
    def has_voted(self) -> bool:
        return self.voted
    
    def rank_candidates(self, candidates: list[Candidate]) -> list[Candidate]:
        candidate_distances = []
        for candidate in candidates:
            political_affiliation = candidate.get_political_affiliation()
            res = abs(political_affiliation - self.political_affiliation)
            candidate_distances.append({"candidate": candidate, "distance": res})
        ranked_candidates = sorted(candidate_distances, key=lambda x: x["distance"])
        # print("ranked candidates for " + self.get_id())
        # print(ranked_candidates)
        return ranked_candidates

class SimpleAdvancedVoter(SimpleVoter):
    """
    The SimpleAdvancedVoter has political affiliation as a single integer. He ranks candidates per distance in one dimensional space.
    If the closest candidate is too far away, the voter does not vote.
    """
    def __init__(self, id: str, political_affiliation, political_min, political_max, age: int = -1):
        super().__init__(id, political_affiliation, political_min, political_max, age)

    def rank_candidates(self, candidates: list[Candidate]) -> list[Candidate]:
        candidate_distances = []
        for candidate in candidates:
            political_affiliation = candidate.get_political_affiliation()
            res = abs(political_affiliation - self.political_affiliation)
            candidate_distances.append({"candidate": candidate, "distance": res})
        ranked_candidates = sorted(candidate_distances, key=lambda x: x["distance"])
        if ranked_candidates and ranked_candidates[0]["distance"] > 10:
            # If the closest candidate is too far away, the voter does not vote
            self.willingness_to_vote = 1.0 - ranked_candidates[0]["distance"]/self.political_max
        # print("ranked candidates for " + self.get_id())
        # print(ranked_candidates)
        return ranked_candidates