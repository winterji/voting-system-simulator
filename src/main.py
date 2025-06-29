from simulator.simulator import Simulator
from citizens import Candidate, SimpleVoter
from voting_systems import PluralityVotingSystem
from graphPlotter import plot_results
from citizensGenerators import UniformSimpleVoterGenerator, UniformSimpleAdvancedVoterGenerator

COLORS = ['blue', 'red', 'green', 'purple', 'white', 'black', 'orange']
LEFT_BOUND = -50
RIGHT_BOUND = 50

# load voters and candidates

generator = UniformSimpleAdvancedVoterGenerator(LEFT_BOUND, RIGHT_BOUND)
voters = generator.generate(1000)

candidates = [
    Candidate("candidate1", 13, LEFT_BOUND, RIGHT_BOUND),
    Candidate("candidate2", -31, LEFT_BOUND, RIGHT_BOUND),
    Candidate("candidate3", 5, LEFT_BOUND, RIGHT_BOUND),
    Candidate("candidate4", 20, LEFT_BOUND, RIGHT_BOUND),
]

candidates_colors = {candidate: None for candidate in candidates}

# Create a simulator instance and supply it with a voting system and voters
sim = Simulator(PluralityVotingSystem, voters, candidates)
results, winner = sim.run()

plot_results(voters, candidates, results, winner)
