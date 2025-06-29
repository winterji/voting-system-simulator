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
voters = generator.generate(10000, SimpleAdvancedVoter2D)

# candidates = [
#     Candidate("candidate1", 13, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate2", -31, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate3", 5, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate4", 20, LEFT_BOUND, RIGHT_BOUND),
# ]

candidates = [
    Candidate("ODS", [6, -3], LEFT_BOUND, RIGHT_BOUND),
    Candidate("TOP 09", [7, 2], LEFT_BOUND, RIGHT_BOUND),
    Candidate("KDU-ČSL", [3, -5], LEFT_BOUND, RIGHT_BOUND),
    Candidate("ANO 2011", [2, -6], LEFT_BOUND, RIGHT_BOUND),
    Candidate("SPD", [6, -9], LEFT_BOUND, RIGHT_BOUND),
    Candidate("Piráti", [-2, 8], LEFT_BOUND, RIGHT_BOUND),
    Candidate("STAN", [1, 4], LEFT_BOUND, RIGHT_BOUND),
    Candidate("KSČM", [-9, -7], LEFT_BOUND, RIGHT_BOUND),
    Candidate("SOCDEM", [-5, -3], LEFT_BOUND, RIGHT_BOUND),
    Candidate("Zelení", [-6, 9], LEFT_BOUND, RIGHT_BOUND),
]


candidates_colors = {candidate: None for candidate in candidates}

# Create a simulator instance and supply it with a voting system and voters
sim = Simulator(PluralityVotingSystem, voters, candidates)
results, winner = sim.run()

plot_results_2D(voters, candidates, results, winner)
