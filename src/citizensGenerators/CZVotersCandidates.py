from citizens.candidate import Candidate
from citizensGenerators.clustersGenerator import ClusterDefinition

LEFT_BOUND = -10
RIGHT_BOUND = 10

# clusters_v1 = [
#     ClusterDefinition((0, 0), 2.5, 0.2),
#     ClusterDefinition((1, -5), 2, 0.3),
#     ClusterDefinition((-1, 6), 1.5, 0.15),
#     ClusterDefinition((6, 0), 1.5, 0.1),
#     ClusterDefinition((-8, -5), 1, 0.08),
#     ClusterDefinition((3, -4), 1, 0.07),
#     ClusterDefinition((0, 0), 5, 0.1),
# ]

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