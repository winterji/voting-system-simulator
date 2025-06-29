from simulator.simulator import Simulator
from citizens import *
from voting_systems import PluralityVotingSystem
from graphPlotter import plot_results_1D, plot_results_2D
from citizensGenerators import *

COLORS = ['blue', 'red', 'green', 'purple', 'white', 'black', 'orange']
LEFT_BOUND = -10
RIGHT_BOUND = 10

# load voters and candidates

generator = Uniform2DVoterGenerator(LEFT_BOUND, RIGHT_BOUND)
voters = generator.generate(1000, SimpleAdvancedVoter2D)

# candidates = [
#     Candidate("candidate1", 13, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate2", -31, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate3", 5, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate4", 20, LEFT_BOUND, RIGHT_BOUND),
# ]

candidates = [
    Candidate("candidate1", [3, 5], LEFT_BOUND, RIGHT_BOUND),
    Candidate("candidate2", [7, 0], LEFT_BOUND, RIGHT_BOUND),
    Candidate("candidate3", [-8, -8], LEFT_BOUND, RIGHT_BOUND),
    Candidate("candidate4", [-1, -4], LEFT_BOUND, RIGHT_BOUND),
]

candidates_colors = {candidate: None for candidate in candidates}

# Create a simulator instance and supply it with a voting system and voters
sim = Simulator(PluralityVotingSystem, voters, candidates)
results, winner = sim.run()

plot_results_2D(voters, candidates, results, winner)
