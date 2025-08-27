import random

from .citizen import Citizen
from .candidate import Candidate

class AdvancedVoterND(Citizen):
    """
    Represents an advanced voter in the voting system, inheriting from Citizen.
    Advanced voter takes into account the candidate's popularity when ranking candidates.
    A voter has an ID, political affiliation, age, and a flag indicating whether they have
    voted or not. The voter can rank candidates based on their political affiliation.
    Adds random diviation to each candidate's score.

    The NDVoter has political affiliation as a N integers. He ranks candidates per distance in N dimensional space.
    Political affiliation space is N dimensional hypercube with min and max values for all axes - political_min and political_max.
    """
    def __init__(self, id: str, political_affiliation: list[int], political_min, political_max, age: int = -1, willingness_to_vote: float = 1.0):
        """"
        id: str
        political_affiliation
        age (optional)
        """
        super().__init__(id, political_affiliation, political_min, political_max, age, willingness_to_vote)
        self.num_possible_answers = self.political_max - self.political_min + 1
        self.neutral_answer = (self.political_max + self.political_min) / 2
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
            # Calculate Euclidean distance in N dimensional space
            total = len(political_affiliation)
            agreed_on = 0
            for i, question in enumerate(political_affiliation):
                if question == self.neutral_answer or self.political_affiliation[i] == self.neutral_answer:
                    continue
                if question > self.neutral_answer and self.political_affiliation[i] > self.neutral_answer:
                    if question == self.political_affiliation[i]:
                        agreed_on += 2
                    else:
                        agreed_on += 1
                elif question < self.neutral_answer and self.political_affiliation[i] < self.neutral_answer:
                    if question == self.political_affiliation[i]:
                        agreed_on += 2
                    else:
                        agreed_on += 1
                else:
                    max_possible_distance = self.num_possible_answers - 1
                    dist = abs(question - self.political_affiliation[i]) / max_possible_distance
                    # calc_disagreement = dist * 2 # scale to 0-2
                    calc_disagreement = round(dist * 2)  # scale to 0-2 and round it
                    agreed_on -= calc_disagreement
            # score is a precentage of questions agreed on
            score = agreed_on / total
            # score = (res * (1-candidate.get_popularity()/2))
            candidate_distances.append({"candidate": candidate, "distance": score, "score": score})
        ranked_candidates = sorted(candidate_distances, key=lambda x: x["score"], reverse=True)
        # print(f"Preffered candidate is {ranked_candidates[0]['candidate'].id} with score {ranked_candidates[0]['score']}")
        self.ranked_candidates = ranked_candidates
        # self.willingness_to_vote = self.willingness_to_vote * (1.0 - ranked_candidates[0]["score"]/(self.political_max*2))
        # print("ranked candidates for " + self.get_id())
        # print(ranked_candidates)
        return ranked_candidates

class AdvancedVoterNDBool(Citizen):
    """
    Represents an advanced voter in the voting system, inheriting from Citizen.
    Advanced voter takes into account the candidate's popularity when ranking candidates.
    A voter has an ID, political affiliation, age, and a flag indicating whether they have
    voted or not. The voter can rank candidates based on their political affiliation.
    Adds random diviation to each candidate's score.
    
    The 2DVoter has political affiliation as a two integers. He ranks candidates per distance in two dimensional space.
    Political affiliation space is 2D square with min and max values for both axes - political_min and political_max.
    """
    def __init__(self, id: str, political_affiliation: list[bool], political_min, political_max, age: int = -1, willingness_to_vote: float = 1.0):
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
            # Calculate Euclidean distance in N dimensional space
            total = len(political_affiliation)
            agreed_on = 0
            for i, question in enumerate(political_affiliation):
                # only 2 possible answers, so +1 for agree, -1 for disagree
                if question == self.political_affiliation[i]:
                    agreed_on += 1
                else:
                    agreed_on -= 1
            # random_diviation = random.random() * candidate.get_popularity()
            # if random.random() >= 0.5:
            #     random_diviation = random_diviation * (-1)
            # score is a precentage of questions agreed on
            score = agreed_on / total
            # score = (res * (1-candidate.get_popularity()/2))
            candidate_distances.append({"candidate": candidate, "distance": score, "score": score})
        ranked_candidates = sorted(candidate_distances, key=lambda x: x["score"], reverse=True)
        # print(f"Preffered candidate is {ranked_candidates[0]['candidate'].id} with score {ranked_candidates[0]['score']}")
        self.ranked_candidates = ranked_candidates
        # self.willingness_to_vote = self.willingness_to_vote * (1.0 - ranked_candidates[0]["score"]/(self.political_max*2))
        # print("ranked candidates for " + self.get_id())
        # print(ranked_candidates)
        return ranked_candidates
