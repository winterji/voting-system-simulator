import random
from .abstract_voting_system import AbstractVotingSystem

class ScoringVotingSystem(AbstractVotingSystem):

    def __init__(self, candidates, options):
        super().__init__(candidates, options)
        print(options)
        if ("max_score" or "score_limits") not in options:
            raise ValueError("max_score must be provided in options for Approval voting system.")
        self.max_score = options["max_score"]
        if len(options["score_limits"]) != self.max_score - 1:
            raise ValueError("score_limits must be a list of length max_score - 1 (that is " + str(self.max_score-1) + ") (the lowest score is for everybody else further away), but is " + str(len(options["score_limits"])))
        self.score_limits = options["score_limits"]
        self.votes_for_candidates = {candidate: 0 for candidate in candidates}
        # print(self.candidates)
        self.not_voted = []

    def vote(self, voter, ranked_candidates):
        candidate = ranked_candidates[0]["candidate"]
        if not voter.has_voted:
            # willingess to vote
            if random.random() < voter.willingness_to_vote:
                # print(f"Voter {voter.id} is voting for {candidate}")
                scores = {c: 1 for c in self.candidates}
                for candidate in ranked_candidates:
                    if candidate['candidate'] in self.candidates:
                        # gives score based on distance
                        score = 1
                        for i, limit in enumerate(self.score_limits):
                            if candidate['distance'] <= limit:
                                score = self.max_score - i
                                break
                        scores[candidate['candidate']] = score
                        self.votes_for_candidates[candidate['candidate']] += score
                    else:
                        raise ValueError("Candidate not found in the voting system.")
                self.votes.append({'voter': voter, 'scored_candidates': scores})
                voter.has_voted = True
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

    @staticmethod
    def str_results(results):
        """Convert results dictionary to a string representation."""
        sorted_candidates = sorted(results.items(), key=lambda item: item[1], reverse=True)
        out = "Number of votes per candidate:\n"
        for candidate, votes in sorted_candidates:
            out += f"{candidate}: {votes}\n"
        return out