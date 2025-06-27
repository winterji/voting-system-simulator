from citizens import *
from voting_systems import *

class Simulator:
    def __init__(self, voting_system, voters, candidates):
        self.voters = voters
        self.candidates = candidates
        self.voting_system = voting_system(candidates)
        self.resutls = []

    def setup(self):
        pass

    def run(self):
        for voter in self.voters:
            if not voter.has_voted:
                # Get the candidate that the voter wants to vote for
                ranked_candidates = voter.rank_candidates(self.candidates)
                # Vote for the candidate
                self.voting_system.vote(voter, ranked_candidates)

        self.resutls = self.voting_system.get_results()
        # Print the results of the voting system
        print("Voting results:")
        print(self.voting_system.get_results())
        print("Winner:", self.voting_system.get_winner())
        return self.voting_system.get_results()
        


