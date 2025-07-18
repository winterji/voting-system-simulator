import random
from .abstract_voting_system import AbstractVotingSystem

class PluralityVotingSystem(AbstractVotingSystem):

    def __init__(self, candidates, options):
        super().__init__(candidates, options)
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
    
class PluralityRunoff(AbstractVotingSystem):
    def __init__(self, candidates, options):
        super().__init__(candidates, options)
        self.votes_for_candidates_round_1 = {candidate: 0 for candidate in candidates}
        self.votes_for_candidates_round_2 = {}
        self.candidates_round_2 = []
        # print(self.candidates)
        self.not_voted = []

    def vote(self, voter, ranked_candidates):
        candidate = ranked_candidates[0]["candidate"]
        if not voter.has_voted:
            # willingess to vote
            if random.random() < voter.willingness_to_vote:
                # print(f"Voter {voter.id} is voting for {candidate}")
                if candidate in self.candidates:
                    self.votes.append({'voter': voter, 'ranked_candidates': ranked_candidates})
                    self.votes_for_candidates_round_1[candidate] += 1
                    voter.vote(candidate)
                else:
                    raise ValueError("Candidate not found in the voting system.")
            else:
                # print(f"Voter {voter.id} did not vote due to low willingness.")
                voter.has_voted = False
                self.not_voted.append(voter)
        else:
            raise ValueError("Voter has already voted.")
        
    def process_round_2(self):
        pass
        # for vote in self.votes:
        #     if random.random() < voter.willingness_to_vote:
        #         pass
    def get_winner(self):
        return max(self.votes_for_candidates_round_1, key=lambda k: self.votes_for_candidates_round_1[k])

    def get_results(self):
        sorted_candidates = sorted(self.votes_for_candidates_round_1, key=lambda k: self.votes_for_candidates_round_1[k], reverse=True)
        self.candidates_round_2.append(sorted_candidates[0], sorted_candidates[1])
        self.process_round_2()
        res = {candidate: self.votes_for_candidates_round_1[candidate] for candidate in self.candidates}
        res["not_voted"] = len(self.not_voted)
        return res