import random

from .citizen import Citizen
from .candidate import Candidate

class SimpleVoter2D(Citizen):
    """
    Represents a simple voter in the voting system, inheriting from Citizen.
    A voter has an ID, political affiliation, age, and a flag indicating whether they have
    voted or not. The voter can rank candidates based on their political affiliation.
    
    The 2DVoter has political affiliation as a two integers. He ranks candidates per distance in two dimensional space.
    Political affiliation space is 2D square with min and max values for both axes - political_min and political_max.
    """
    def __init__(self, id: str, political_affiliation, political_min, political_max, age: int = -1, willingness_to_vote: float = 1.0):
        """"
        id: str
        political_affiliation
        age (optional)
        """
        super().__init__(id, political_affiliation, political_min, political_max, age, willingness_to_vote)

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
            # Assuming political_affiliation is a tuple (x, y) for 2D space - calculate distance
            # Calculate Euclidean distance in 2D space
            res = ((political_affiliation[0] - self.political_affiliation[0]) ** 2 + 
                    (political_affiliation[1] - self.political_affiliation[1]) ** 2) ** 0.5
            candidate_distances.append({"candidate": candidate, "distance": res})
        ranked_candidates = sorted(candidate_distances, key=lambda x: x["distance"])
        self.ranked_candidates = ranked_candidates
        # print("ranked candidates for " + self.get_id())
        # print(ranked_candidates)
        return ranked_candidates
    
class SimpleAdvancedVoter2D(Citizen):
    """
    Represents a simple voter in the voting system, inheriting from Citizen.
    A voter has an ID, political affiliation, age, and a flag indicating whether they have
    voted or not. The voter can rank candidates based on their political affiliation.
    
    The 2DVoter has political affiliation as a two integers. He ranks candidates per distance in two dimensional space.
    Political affiliation space is 2D square with min and max values for both axes - political_min and political_max.
    """
    def __init__(self, id: str, political_affiliation, political_min, political_max, age: int = -1, willingness_to_vote: float = 1.0):
        """"
        id: str
        political_affiliation
        age (optional)
        """
        super().__init__(id, political_affiliation, political_min, political_max, age, willingness_to_vote)
        # self.willingness_to_vote = 1.0 set in citizen

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
            # Assuming political_affiliation is a tuple (x, y) for 2D space - calculate distance
            # Calculate Euclidean distance in 2D space
            res = ((political_affiliation[0] - self.political_affiliation[0]) ** 2 + 
                    (political_affiliation[1] - self.political_affiliation[1]) ** 2) ** 0.5
            candidate_distances.append({"candidate": candidate, "distance": res})
        ranked_candidates = sorted(candidate_distances, key=lambda x: x["distance"])
        self.ranked_candidates = ranked_candidates
        self.willingness_to_vote = self.willingness_to_vote * (1.0 - ranked_candidates[0]["distance"]/(self.political_max*2))
        # print("ranked candidates for " + self.get_id())
        # print(ranked_candidates)
        return ranked_candidates
    
class AdvancedVoter2D(Citizen):
    """
    Represents an advanced voter in the voting system, inheriting from Citizen.
    Advanced voter takes into account the candidate's popularity when ranking candidates.
    A voter has an ID, political affiliation, age, and a flag indicating whether they have
    voted or not. The voter can rank candidates based on their political affiliation.
    Adds random to each candidate's score.
    
    The 2DVoter has political affiliation as a two integers. He ranks candidates per distance in two dimensional space.
    Political affiliation space is 2D square with min and max values for both axes - political_min and political_max.
    """
    def __init__(self, id: str, political_affiliation, political_min, political_max, age: int = -1, willingness_to_vote: float = 1.0):
        """"
        id: str
        political_affiliation
        age (optional)
        """
        super().__init__(id, political_affiliation, political_min, political_max, age, willingness_to_vote)
        # self.willingness_to_vote = 1.0

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
            # Assuming political_affiliation is a tuple (x, y) for 2D space - calculate distance
            # Calculate Euclidean distance in 2D space
            res = ((political_affiliation[0] - self.political_affiliation[0]) ** 2 + 
                    (political_affiliation[1] - self.political_affiliation[1]) ** 2) ** 0.5
            random_divergance = random.random() * candidate.get_popularity()
            if random.random() >= 0.5:
                random_divergance = random_divergance * (-1)
            candidate_distances.append({"candidate": candidate, "distance": res, "score": (res * (1-candidate.get_popularity()/2)) + random_divergance})
        ranked_candidates = sorted(candidate_distances, key=lambda x: x["score"])
        self.ranked_candidates = ranked_candidates
        # self.willingness_to_vote = self.willingness_to_vote * (1.0 - ranked_candidates[0]["score"]/(self.political_max*2))
        # print("ranked candidates for " + self.get_id())
        # print(ranked_candidates)
        return ranked_candidates