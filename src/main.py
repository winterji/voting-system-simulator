import sys

from simulator.simulator import Simulator
from citizens import *
from voting_systems import *
from graphPlotter import *
from citizensGenerators import *

LEFT_BOUND = -10
RIGHT_BOUND = 10

# load voters and candidates

clusters_v1 = [
    ClusterDefinition((0, 0), 2.5, 0.2),
    ClusterDefinition((1, -5), 2, 0.3),
    ClusterDefinition((-1, 6), 1.5, 0.15),
    ClusterDefinition((6, 0), 1.5, 0.1),
    ClusterDefinition((-8, -5), 1, 0.08),
    ClusterDefinition((3, -4), 1, 0.07),
    ClusterDefinition((0, 0), 5, 0.1),
]

clusters_v2 = [
    ClusterDefinition((0, -8), 1.5, 0.12, willingness_to_vote=0.85),
    ClusterDefinition((1, -5), 2, 0.23, willingness_to_vote=0.8),
    ClusterDefinition((-7, -6), 1, 0.04, willingness_to_vote=0.88),
    ClusterDefinition((3, -4), 1.2, 0.06, willingness_to_vote=0.85),
    ClusterDefinition((6, -1), 1.5, 0.09, willingness_to_vote=0.9),
    ClusterDefinition((2, 3), 1.5, 0.08, willingness_to_vote=0.85),
    ClusterDefinition((-1, 7), 2, 0.17, willingness_to_vote=0.7),
    ClusterDefinition((-1, -1), 3, 0.2, willingness_to_vote=0.10),
]

generator = ClusteredVoterGenerator(LEFT_BOUND, RIGHT_BOUND, clusters=clusters_v2)
voters = generator.generate(1500, AdvancedVoter2D)

# candidates = [
#     Candidate("candidate1", 13, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate2", -31, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate3", 5, LEFT_BOUND, RIGHT_BOUND),
#     Candidate("candidate4", 20, LEFT_BOUND, RIGHT_BOUND),
# ]

candidates = [
    Candidate("Spolu", [6, -2.2], LEFT_BOUND, RIGHT_BOUND, popularity=0.85),
    # Candidate("ODS", [6, -3], LEFT_BOUND, RIGHT_BOUND, popularity=0.75),
    # Candidate("TOP 09", [7, 2], LEFT_BOUND, RIGHT_BOUND, popularity=0.45),
    # Candidate("KDU-ČSL", [3, -5], LEFT_BOUND, RIGHT_BOUND, popularity=0.4),
    Candidate("ANO 2011", [2, -6], LEFT_BOUND, RIGHT_BOUND, popularity=0.9),
    Candidate("SPD", [3, -8], LEFT_BOUND, RIGHT_BOUND, popularity=0.9),
    Candidate("Piráti", [-2, 8], LEFT_BOUND, RIGHT_BOUND, popularity=0.6),
    Candidate("STAN", [1, 4], LEFT_BOUND, RIGHT_BOUND, popularity=0.55),
    Candidate("KSČM", [-9, -7], LEFT_BOUND, RIGHT_BOUND, popularity=0.25),
    Candidate("SOCDEM", [-5, -3], LEFT_BOUND, RIGHT_BOUND, popularity=0.2),
    Candidate("Zelení", [-6, 9], LEFT_BOUND, RIGHT_BOUND, popularity=0.35),
    Candidate("Stačilo!", [-4, -5], LEFT_BOUND, RIGHT_BOUND, popularity=0.45),
    Candidate("Motoristé", [7, -7], LEFT_BOUND, RIGHT_BOUND, popularity=0.35),
]

# select voting system according to parameter
voting_system = PluralityVotingSystem
options = {}
if len(sys.argv) > 1:
    voting_system_name = sys.argv[1]
    if voting_system_name == "condorcet":
        voting_system = CondorcetVotingSystem
    elif voting_system_name == "approval":
        voting_system = ApprovalVotingSystem
        if len(sys.argv) <= 2:
            print("No approval distance provided, using default 3")
            options = {"approval_distance": 3}
        else:
            options = {"approval_distance": float(sys.argv[2])}
    elif voting_system_name == "instant_runoff" or voting_system_name == "irv" or voting_system_name == "runoff":
        voting_system = InstantRunoffVotingSystem
    elif voting_system_name == "score" or voting_system_name == "scoring":
        voting_system = ScoringVotingSystem
        if len(sys.argv) <= 3:
            print("No max_score or score_limits provided, using default max_score 3 and score_limits 1,3")
            options = {
                "max_score": 3,
                "score_limits": [1, 3]
            }
        else:
            options = {
                "max_score": int(sys.argv[2]),
                "score_limits": [int(x) for x in sys.argv[3].split(",")]
            }

    elif voting_system_name == "plurality":
        voting_system = PluralityVotingSystem
    else:
        print("Voting system not recognised")
else:
    print("No voting system set - using default: PluralityVotingSystem")

# Create a simulator instance and supply it with a voting system and voters
sim = Simulator(voting_system, voters, candidates, options=options)
results, winner = sim.run()

if voting_system == ApprovalVotingSystem:
    plot_approvals_2D(voters, candidates, results, winner, sim.voting_system.approval_distance)
elif voting_system == ScoringVotingSystem:
    plot_scores_2D(voters, candidates, results, winner, sim.voting_system.score_limits)
elif voting_system == InstantRunoffVotingSystem:
    plot_results_per_rounds_2D(voters, candidates, results, winner)
elif voting_system == PluralityVotingSystem:
    print_percantage_results(results)
    plot_results_2D(voters, candidates, results, winner)

