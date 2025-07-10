import random
from .abstract_voting_system import AbstractVotingSystem

class ApprovalVotingSystem(AbstractVotingSystem):
    """
    Approval Voting System implementation. Needs "approval_distance" in options.
    """

    def __init__(self, candidates, options):
        super().__init__(candidates, options)
        if "approval_distance" not in options:
            raise ValueError("Approval distance must be provided in options for Approval voting system.")
        self.approval_distance = options["approval_distance"]
        self.approvals_for_candidates = {candidate: 0 for candidate in candidates}
        # print(self.candidates)
        self.not_voted = []

    def vote(self, voter, ranked_candidates):
        if not voter.has_voted:
            # willingess to vote
            if random.random() < voter.willingness_to_vote:
                # print(f"Voter {voter.id} is voting for {candidate}")
                approvesOne = False
                for candidate in ranked_candidates:
                    # Check if the candidate is in the list of candidates
                    if candidate['candidate'] in self.candidates:
                        # if distance enough, approve the candidate
                        if candidate['distance'] <= self.approval_distance:
                            approvesOne = True
                            # print(f"Voter {voter.id} approves candidate {candidate['candidate'].id}")
                            self.votes.append({'voter': voter, 'candidate': candidate['candidate']})
                            self.approvals_for_candidates[candidate['candidate']] += 1
                            voter.approve(candidate['candidate'])
                        # self.votes.append({'voter': voter, 'candidate': candidate})
                        # self.votes_for_candidates[candidate] += 1
                        # voter.vote(candidate)
                    else:
                        raise ValueError("Candidate not found in the voting system.")
                if approvesOne:
                    voter.has_voted = True
                else:
                    voter.has_voted = False
                    self.not_voted.append(voter)
            else:
                # print(f"Voter {voter.id} did not vote due to low willingness.")
                voter.has_voted = False
                self.not_voted.append(voter)
        else:
            raise ValueError("Voter has already voted.")

    def get_winner(self):
        return max(self.approvals_for_candidates, key=lambda k: self.approvals_for_candidates[k])

    def get_results(self):
        res = {candidate: self.approvals_for_candidates[candidate] for candidate in self.candidates}
        res["not_voted"] = len(self.not_voted)
        return res