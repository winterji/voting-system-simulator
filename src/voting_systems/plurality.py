import random
from .abstract_voting_system import AbstractVotingSystem

class PluralityVotingSystem(AbstractVotingSystem):

    def __init__(self, candidates):
        super().__init__(candidates)
        self.votes_for_candidates = {candidate: 0 for candidate in candidates}
        # print(self.candidates)
        self.not_voted = []

    def vote(self, voter, ranked_candidates):
        candidate = ranked_candidates[0]["candidate"]
        if not voter.has_voted:
            # willingess to vote
            if random.random() < voter.willingness_to_vote:
                # print(f"Voter {voter.id} is voting for {candidate}")
                if candidate in self.candidates:
                    self.votes.append({'voter': voter, 'candidate': candidate})
                    self.votes_for_candidates[candidate] += 1
                    voter.vote(candidate)
                else:
                    raise ValueError("Candidate not found in the voting system.")
            else:
                # print(f"Voter {voter.id} did not vote due to low willingness.")
                voter.has_voted = False
                self.not_voted.append(voter)
        else:
            raise ValueError("Voter has already voted.")

    def get_winner(self):
        return max(self.votes_for_candidates, key=lambda k: self.votes_for_candidates[k])

    def get_results(self):
        res = {candidate: self.votes_for_candidates[candidate] for candidate in self.candidates}
        res["not_voted"] = len(self.not_voted)
        return res