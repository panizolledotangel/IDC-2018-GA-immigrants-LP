class GaConfiguration:

    def __init__(self, crossover_rate=0.8, mutation_rate=0.2, number_generations=300, elitism=0.1, population_size=300,
                 offspring_size=300, generations_to_converge=10, threshold_converge=0.01):

        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.number_generations = number_generations
        self.offspring_size = offspring_size
        self.elitism = elitism
        self.population_size = population_size
        self.generations_to_converge = generations_to_converge
        self.threshold_converge = threshold_converge

    def make_dict(self):
        d = {
            "crossover_rate": self.crossover_rate,
            "elitism": self.elitism,
            "mutation_rate": self.mutation_rate,
            "population_size": self.population_size,
            "max_num_generations": self.number_generations,
            "offspring_size": self.offspring_size,
            "generations_to_converge": self.generations_to_converge,
            "threshold_converge": self.threshold_converge
        }
        return d
