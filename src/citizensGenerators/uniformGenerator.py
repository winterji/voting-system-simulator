import random
from citizens import SimpleVoter, SimpleAdvancedVoter

class UniformGenerator:
    def __init__(self, left_bound: int = -50, right_bound: int = 50):
        self.population_size = 0
        self.citizens = []
        self.left_bound = left_bound
        self.right_bound = right_bound

class UniformSimpleVoterGenerator(UniformGenerator):
    def generate(self, population_size: int):
        """
        Generates a uniform distribution of citizens.
        Each citizen has a unique ID and a political affiliation.
        Political affiliations are evenly distributed across the population.
        """
        self.population_size = population_size
        for i in range(self.population_size):
            political_affiliation = random.uniform(self.left_bound, self.right_bound)  # Political affiliation in the range [0, 1]
            voter = SimpleVoter(id="voter-" + str(i), political_affiliation=political_affiliation, political_min=self.left_bound, political_max=self.right_bound)
            self.citizens.append(voter)
        return self.citizens
    

class UniformSimpleAdvancedVoterGenerator(UniformGenerator):
    def generate(self, population_size: int):
        """
        Generates a uniform distribution of citizens.
        Each citizen has a unique ID and a political affiliation.
        Political affiliations are evenly distributed across the population.
        """
        self.population_size = population_size
        for i in range(self.population_size):
            political_affiliation = random.uniform(self.left_bound, self.right_bound)  # Political affiliation in the range [0, 1]
            voter = SimpleAdvancedVoter(id="SimpleADVvoter-" + str(i), political_affiliation=political_affiliation, political_min=self.left_bound, political_max=self.right_bound)
            self.citizens.append(voter)
        return self.citizens
    
