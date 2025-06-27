from simulator.simulator import Simulator
from citizens import Candidate, SimpleVoter
from voting_systems import PluralityVotingSystem
from graphPlotter import plot_results

COLORS = ['blue', 'red', 'green', 'purple', 'white', 'black', 'orange']

# load voters and candidates
voters = [
    SimpleVoter("pepa", 5),
    SimpleVoter("karel", -5),
    SimpleVoter("lisa", 3),
]
candidates = [
    Candidate("candidate1", 13),
    Candidate("candidate2", -1)
]

candidates_colors = {candidate: None for candidate in candidates}

# Create a simulator instance and supply it with a voting system and voters
sim = Simulator(PluralityVotingSystem, voters, candidates)
results = sim.run()

plot_results(voters, candidates, results)
