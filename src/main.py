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
    ClusterDefinition((0, -8), 1.5, 0.12),
    ClusterDefinition((1, -5), 2, 0.18),
    ClusterDefinition((-7, -6), 1, 0.04),
    ClusterDefinition((3, -4), 1.2, 0.06),
    ClusterDefinition((6, -1), 1.5, 0.09),
    ClusterDefinition((2, 3), 1.5, 0.08),
    ClusterDefinition((-1, 7), 2, 0.13),
    ClusterDefinition((-1, -1), 3, 0.3),
]

generator = ClusteredVoterGenerator(LEFT_BOUND, RIGHT_BOUND, clusters=clusters_v2)
voters = generator.generate(1500, SimpleAdvancedVoter2D)

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
    # Candidate("Zelení", [-6, 9], LEFT_BOUND, RIGHT_BOUND),
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
            options = {"approval_distance": sys.argv[2]}
    elif voting_system_name == "instant_runoff" or voting_system_name == "irv" or voting_system_name == "runoff":
        voting_system = InstantRunoffVotingSystem
    elif voting_system_name == "score" or voting_system_name == "scoring":
        voting_system = ScoringVotingSystem
        if len(sys.argv) <= 3:
            print("No max_score or score_limits provided, using default max_score 3 and score_limits [1, 3]")
            options = {
                "max_score": 3,
                "score_limits": [1, 3]
            }
        else:
            options = {
                "max_score": sys.argv[2],
                "score_limits": [int(x) for x in sys.argv[3].split(",")]
            }

    elif voting_system_name == "plurality":
        voting_system = PluralityVotingSystem
    else:
        print("Voting system not recognised")
else:
    print("No voting system set - using default: PluralityVotingSystem")

# Create a simulator instance and supply it with a voting system and voters
sim = Simulator(voting_system, voters, candidates, options={
    # "approval_distance": 5
    # "max_score": 3,
    # "score_limits": [1, 3]
})
results, winner = sim.run()

if voting_system == ApprovalVotingSystem:
    plot_approvals_2D(voters, candidates, results, winner, sim.voting_system.approval_distance)
elif voting_system == ScoringVotingSystem:
    plot_scores_2D(voters, candidates, results, winner, sim.voting_system.score_limits)
elif voting_system == InstantRunoffVotingSystem:
    plot_results_per_rounds_2D(voters, candidates, results, winner)
elif voting_system == PluralityVotingSystem:
    plot_results_2D(voters, candidates, results, winner)

