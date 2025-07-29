import random
from citizens import *
from .uniformGenerator import UniformGenerator

class ClusterDefinition:
    def __init__(self, center: tuple[float, float], spread: float, relative_size: float, willingness_to_vote: float = 1.0):
        self.center: tuple[float, float] = center
        self.spread: float = spread
        self.relative_size: float = relative_size
        self.willingness_to_vote = willingness_to_vote
    
    def __repr__(self):
        return f"ClusterDefinition(center={self.center}, spread={self.spread}, relative_size={self.relative_size})"
    
    def __str__(self):
        return f"Cluster at {self.center} with spread {self.spread} and relative size {self.relative_size}"

class ClusteredVoterGenerator(UniformGenerator):
    """
    Generates citizens grouped into clusters based on a normal distribution.
    Each cluster originates around a random center within [left_bound, right_bound],
    and voters' affiliations are drawn from a Gaussian distribution around each center.

    Parameters:
    - left_bound (float): minimum possible affiliation value.
    - right_bound (float): maximum possible affiliation value.
    - num_clusters (int): number of clusters to generate.
    - cluster_std (float): standard deviation for each cluster's normal distribution.
    """
    def __init__(self, left_bound: float = -50, right_bound: float = 50,
                 num_clusters: int = 3, cluster_std: float = 3.0, clusters: list[ClusterDefinition] = None):
        super().__init__(left_bound, right_bound)
        self.num_clusters = num_clusters
        self.cluster_std = cluster_std
        self.set_clusters = None
        if clusters:
            self.set_clusters = clusters
            self.num_clusters = len(clusters)

    def generate(self, population_size: int, voterClass):
        """
        Generate a population of voters divided into clusters.

        Args:
            population_size (int): total number of voters to generate.
            voterClass (class): class for creating voter instances (e.g., SimpleVoter, SimpleAdvancedVoter),
                                 must accept id, political_affiliation, political_min, political_max.

        Returns:
            List of voterClass instances with clustered affiliations.
        """
        self.population_size = population_size
        self.citizens = []

        # 1. Generate random cluster centers
        if not self.set_clusters:
            left_for_center = self.left_bound + self.cluster_std
            right_for_center = self.right_bound - self.cluster_std
            # cluster_centers = [(random.uniform(left_for_center, right_for_center), random.uniform(left_for_center, right_for_center))
            #                 for _ in range(self.num_clusters)]
            clusters = [
                ClusterDefinition((random.uniform(left_for_center, right_for_center), random.uniform(left_for_center, right_for_center)), self.cluster_std, 1 / self.num_clusters)
                for _ in range(self.num_clusters)
            ]
        else:
            # cluster_centers = self.cluster_centers
            clusters = self.set_clusters

        # 2. Distribute population sizes across clusters (according to cluster relative sizes)
        # base_count = population_size // self.num_clusters
        # extras = population_size % self.num_clusters
        # cluster_sizes = [base_count + (1 if i < extras else 0)
        #                  for i in range(self.num_clusters)]
        cluster_sizes = [int(population_size * cluster.relative_size) for cluster in clusters]
        for i in range(population_size - sum(cluster_sizes)):
            cluster_sizes[i % self.num_clusters] += 1

        # 3. Generate voters for each cluster
        uid = 0
        for cluster_idx, cluster in enumerate(clusters):
            for _ in range(cluster_sizes[cluster_idx]):
                # Sample from Gaussian around the cluster center
                affiliation_x = random.gauss(cluster.center[0], cluster.spread)
                affiliation_y = random.gauss(cluster.center[1], cluster.spread)
                # Clamp to bounds
                affiliation_x = max(self.left_bound, min(self.right_bound, affiliation_x))
                affiliation_y = max(self.left_bound, min(self.right_bound, affiliation_y))

                if cluster.willingness_to_vote:
                    willingness_to_vote = cluster.willingness_to_vote
                else:
                    willingness_to_vote = 1.0
                voter = voterClass(
                    id=f"voter-c{cluster_idx}-{uid}",
                    political_affiliation=[affiliation_x, affiliation_y],
                    political_min=self.left_bound,
                    political_max=self.right_bound,
                    willingness_to_vote=willingness_to_vote
                )
                self.citizens.append(voter)
                uid += 1

        return self.citizens

# Example usage:
# generator = ClusteredVoterGenerator(num_clusters=4, cluster_std=10)\# voters = generator.generate(200, SimpleVoter)
