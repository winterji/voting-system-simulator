import random
from .abstract_voting_system import AbstractVotingSystem

class CondorcetVotingSystem(AbstractVotingSystem):
    """
    Approval Voting System implementation. Needs "approval_distance" in options.
    """

    def __init__(self, candidates, options):
        super().__init__(candidates, options)
        self.approvals_for_candidates = {candidate: 0 for candidate in candidates}
        # print(self.candidates)
        self.not_voted = []
        self.setup()

    def setup(self):
        # Initialize pairwise comparison matrix
        self.pairwise_matrix = {candidate: {c: 0 for c in self.candidates} for candidate in self.candidates}

    def vote(self, voter, ranked_candidates):
        if not voter.has_voted:
            # willingess to vote
            if random.random() < voter.willingness_to_vote:
                self.votes.append({'voter': voter, 'ranked_candidates': ranked_candidates})
                for i in range(len(ranked_candidates)):
                    for j in range(i + 1, len(ranked_candidates)):
                        candidate_a = ranked_candidates[i]["candidate"]
                        candidate_b = ranked_candidates[j]["candidate"]
                        if candidate_a in self.candidates and candidate_b in self.candidates:
                            # Update pairwise comparison - only add the vote for the upper candidate
                            self.pairwise_matrix[candidate_a][candidate_b] += 1
                            # self.pairwise_matrix[candidate_b][candidate_a] -= 1
                voter.has_voted = True
            else:
                # print(f"Voter {voter.id} did not vote due to low willingness.")
                voter.has_voted = False
                self.not_voted.append(voter)
        else:
            raise ValueError("Voter has already voted.")

    def get_winner(self):
        return max(self.candidate_wins, key=lambda k: len(self.candidate_wins[k]))

    def get_results(self):
        self.candidate_wins = {candidate: [] for candidate in self.candidates}
        # find if someone is Condorcet winner
        for candidate, comparisons in self.pairwise_matrix.items():
            # print(f"Candidate {candidate.id} comparisons: {comparisons}")
            # print(self.pairwise_matrix[self.candidates[1]][candidate])
            for other in self.candidates:
                if other != candidate:
                    print(f"Comparing {candidate.id} with {other.id}: {comparisons[other]} vs {self.pairwise_matrix[other][candidate]}")
                    if comparisons[other] > self.pairwise_matrix[other][candidate]:
                        self.candidate_wins[candidate].append(other)
            # Check if candidate is a Condorcet winner
        if len(self.candidate_wins[candidate]) >= len(self.candidates) - 1:
            return {"winner": candidate, "pairwise_matrix": self.pairwise_matrix}
        return {"winner": None, "pairwise_matrix": self.pairwise_matrix}