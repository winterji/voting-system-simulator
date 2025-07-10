import random
import copy
from .abstract_voting_system import AbstractVotingSystem

class InstantRunoffVotingSystem(AbstractVotingSystem):

    def __init__(self, candidates, options):
        super().__init__(candidates, options)
        self.votes_for_candidates = {candidate: 0 for candidate in candidates}
        self.eliminated_candidates = []
        self.round = 0
        # print(self.candidates)
        self.not_voted = []
        self.votes_per_round = []
        self.winner = None

    def vote(self, voter, ranked_candidates):
        if not voter.has_voted:
            # willingess to vote
            if random.random() < voter.willingness_to_vote:
                self.votes.append({'voter': voter, 'ranked_candidates': ranked_candidates})
                voter.has_voted = True
            else:
                # print(f"Voter {voter.id} did not vote due to low willingness.")
                voter.has_voted = False
                self.not_voted.append(voter)
        else:
            raise ValueError("Voter has already voted.")
        
    def process_round(self):
        self.round += 1
        # Count votes for this round
        current_votes = {candidate: 0 for candidate in self.candidates}
        for vote in self.votes:
            ranked_candidates = vote['ranked_candidates']
            if ranked_candidates:
                # Vote for the first candidate in the ranked list if wasnt eliminated yet
                for candidate_info in ranked_candidates:
                    candidate = candidate_info['candidate']
                    if candidate not in self.eliminated_candidates:
                        current_votes[candidate] += 1
                        break
        
        self.votes_per_round.append(current_votes)
        self.votes_for_candidates = copy.deepcopy(current_votes)
        
        # Check for a winner - at least one candidate has more than half of the votes
        total_votes = sum(current_votes.values())
        print(f"Round {self.round}: Total votes: {total_votes}, Current votes: {current_votes}")
        if total_votes == 0:
            return None
        for candidate, votes in current_votes.items():
            if votes > total_votes / 2:
                self.winner = candidate
                return candidate
        # No winner, find the candidate with the least votes to eliminate
        min_votes = min(current_votes.values())
        # TODO - only one to eliminate - eliminate all candidates with the least votes for now
        candidates_to_eliminate = [candidate for candidate, votes in current_votes.items() if votes == min_votes]
        # Eliminate the first candidate in the list of candidates to eliminate
        candidate_to_eliminate = candidates_to_eliminate[0]
        self.eliminated_candidates.append(candidate_to_eliminate)
        self.candidates.remove(candidate_to_eliminate)
        print(f"Eliminating candidate {candidate_to_eliminate} with {min_votes} votes.")
        # end round - in the next round votes will be counted again, but only for the remaining candidates

    def get_winner(self):
        return self.winner

    def get_results(self):
        winner = None
        while winner is None:
            winner = self.process_round()
        print(f"Winner after round {self.round}: {winner}")

        return self.votes_per_round