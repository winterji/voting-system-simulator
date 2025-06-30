from citizens import Citizen, Candidate

class AbstractVotingSystem:
    """
    Abstract base class for voting systems.
    """

    def __init__(self, candidates, options):
        """
        Initialize the voting system with a list of candidates and empty list of votes.
        Votes is a list of dictionaries with keys 'voter' and 'candidate'.
        :param candidates: List of candidates participating in the election.
        """
        self.candidates = candidates
        self.options = options
        self.votes = []

    def get_candidates(self):
        return self.candidates

    def vote(self, voter: Citizen, ranked_candidates: list[Candidate]):
        """
        Record a vote for a candidate by a voter.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def tally_votes(self):
        """
        Tally the votes and return the results.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_winner(self):
        """
        Determine the winner of the election.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")