from .abstract_voting_system import AbstractVotingSystem

class PluralityVotingSystem(AbstractVotingSystem):

    def __init__(self, candidates):
        super().__init__(candidates)
        self.votes_for_candidates = {candidate: 0 for candidate in candidates}
        # print(self.candidates)

    def vote(self, voter, ranked_candidates):
        candidate = ranked_candidates[0]["candidate"]
        if not voter.has_voted:
            # print(f"Voter {voter.id} is voting for {candidate}")
            if candidate in self.candidates:
                self.votes.append({'voter': voter, 'candidate': candidate})
                self.votes_for_candidates[candidate] += 1
                voter.vote(candidate)
            else:
                raise ValueError("Candidate not found in the voting system.")
        else:
            raise ValueError("Voter has already voted.")

    def get_winner(self):
        return max(self.votes_for_candidates, key=lambda k: self.votes_for_candidates[k])

    def get_results(self):
        return self.votes_for_candidates