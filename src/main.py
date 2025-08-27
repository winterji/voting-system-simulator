import sys

from simulator.simulator import Simulator
from citizens import *
from voting_systems import *
from graphPlotter import *
from citizensGenerators import *
from citizensGenerators.CZVotersCandidates import candidates, clusters_v2

LEFT_BOUND = 1
RIGHT_BOUND = 5

# load voters and candidates

# generator = ClusteredVoterGenerator(LEFT_BOUND, RIGHT_BOUND, clusters=clusters_v2)
# voters = generator.generate(1500, AdvancedVoter2D)

voterModel = SimpleVoter
generator = ClusteredVoterGenerator(-10, 10, clusters=clusters_v2)

# voters = generator.generate(1500, voterModel, size_of_questions=15)
voters = generator.generate(1500, voterModel)
print(f"Average voters answer to questions: {sum([sum(v.political_affiliation) for v in voters]) / len(voters)}")

all_true = [RIGHT_BOUND for _ in range(15)]
all_false = [LEFT_BOUND for _ in range(15)]
# mid = [True for _ in range(8)] + [False for _ in range(7)]

# candidates = [
#     Candidate("All-TRUE", all_true, LEFT_BOUND, RIGHT_BOUND, popularity=1),
#     Candidate("All-FALSE", all_false, LEFT_BOUND, RIGHT_BOUND, popularity=1),
#     # Candidate("Mid", mid, 0, 1, popularity=1)
# ]


# select voting system according to parameter
voting_system = PluralityVotingSystem
options = {}
if len(sys.argv) > 1:
    voting_system_name = sys.argv[1]
    if voting_system_name == "condorcet":
        voting_system = CondorcetVotingSystem
    elif voting_system_name == "approval" or voting_system_name == "approve":
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

if voterModel == AdvancedVoterNDBool or voterModel == AdvancedVoterND:
    print("AdvancedVoterND or AdvancedVoterNDBool model used - not plotting results")
    if voting_system == PluralityVotingSystem:
        print_percantage_results(results)
else:
    if voting_system == ApprovalVotingSystem:
        plot_approvals_2D(voters, candidates, results, winner, sim.voting_system.approval_distance)
    elif voting_system == ScoringVotingSystem:
        plot_scores_2D(voters, candidates, results, winner, sim.voting_system.score_limits)
    elif voting_system == InstantRunoffVotingSystem:
        plot_results_per_rounds_2D(voters, candidates, results, winner)
    elif voting_system == PluralityVotingSystem:
        print_percantage_results(results)
        plot_results_2D(voters, candidates, results, winner)

