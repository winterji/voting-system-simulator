import random
from citizens import *

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
            political_affiliation = random.uniform(self.left_bound, self.right_bound)  # Political affiliation in the range [x, y]
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
            political_affiliation = random.uniform(self.left_bound, self.right_bound)  # Political affiliation in the range [x, y]
            voter = SimpleAdvancedVoter(id="SimpleADVvoter-" + str(i), political_affiliation=political_affiliation, political_min=self.left_bound, political_max=self.right_bound)
            self.citizens.append(voter)
        return self.citizens
    
class Uniform2DVoterGenerator(UniformGenerator):
    def generate(self, population_size: int, voterClass):
        """
        Generates a uniform distribution of citizens.
        Each citizen has a unique ID and a political affiliation.
        Political affiliations are evenly distributed across the population.
        """
        self.population_size = population_size
        for i in range(self.population_size):
            political_affiliation = [random.uniform(self.left_bound, self.right_bound), random.uniform(self.left_bound, self.right_bound)]  # Political affiliation in the range [x, y]
            voter = voterClass(id="voter-" + str(i), political_affiliation=political_affiliation, political_min=self.left_bound, political_max=self.right_bound)
            self.citizens.append(voter)
        return self.citizens
    
class UniformNDVoterGenerator(UniformGenerator):

    def __init__(self, num_possible_answers):
        # num_possible_answers has to be odd
        if num_possible_answers % 2 == 0:
            raise ValueError("num_possible_answers must be odd")
        super().__init__(1, num_possible_answers)

    def generate(self, population_size: int, voterClass, size_of_questions: int = 10):
        """
        Generates a uniform distribution of citizens.
        Each citizen has a unique ID and a political affiliation.
        Political affiliations are evenly distributed across the population.
        """
        self.population_size = population_size
        for i in range(self.population_size):
            political_affiliation = []
            for j in range(size_of_questions):
                # append True or False randomly
                num_possible_answers = self.right_bound - self.left_bound + 1
                rnd_answ = random.random()
                one_part = 1 / num_possible_answers
                was_generated = False
                # print(f"rnd_answer: {rnd_answ}, one_part: {one_part}, num_possible_answers: {num_possible_answers}")
                for k in range(self.left_bound, self.right_bound + 1):
                    # print(f"Checking if {rnd_answ} <= {one_part * k}")
                    if rnd_answ <= one_part * k:
                        political_affiliation.append(k)
                        was_generated = True
                        break
                if not was_generated:
                    raise ValueError(f"Answer was not generated for rnd_answer: {rnd_answ} and possible answers: {num_possible_answers}")

            voter = voterClass(id="voter-" + str(i), political_affiliation=political_affiliation, political_min=self.left_bound, political_max=self.right_bound)
            self.citizens.append(voter)
        return self.citizens
    
class UniformNDBoolVoterGenerator(UniformGenerator):

    def __init__(self):
        super().__init__(0, 1)

    def generate(self, population_size: int, voterClass, size_of_questions: int = 10):
        """
        Generates a uniform distribution of citizens.
        Each citizen has a unique ID and a political affiliation.
        Political affiliations are evenly distributed across the population.
        """
        self.population_size = population_size
        for i in range(self.population_size):
            political_affiliation = []
            for j in range(size_of_questions):
                # append True or False randomly
                political_affiliation.append(True if random.random() > 0.5 else False)

            voter = voterClass(id="voter-" + str(i), political_affiliation=political_affiliation, political_min=self.left_bound, political_max=self.right_bound)
            self.citizens.append(voter)
        return self.citizens
