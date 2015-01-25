class ScribeEmpty(object):

    def __init__(self, period=10):
        """
        :param period: every evaluation divisible by period will be saved
        """
        if period < 1:
            period = 1
        self.period = period
        self.evaluation = 0

    def reset(self):
        self.evaluation = 0

    def increment_evaluation(self):
        self.evaluation += 1

    def is_enough_evaluations(self):
        return self.evaluation % self.period == 1

    def set_period(self, period):
        if period < 1:
            period = 1
        self.period = period


class ScribeInMemory(ScribeEmpty):

    def __init__(self, eng=None, period=10):
        super(ScribeInMemory, self).__init__(period)
        self.best_fitness = []
        self.engine = eng

    def set_engine(self, eng):
        """
        Set engine for the scribe
        """
        self.engine = eng

    def reset(self):
        super(ScribeInMemory, self).reset()
        self.best_fitness = []

    def get_best_fitness(self):
        return self.best_fitness

    def increment_evaluation(self):
        if self.is_enough_evaluations():
            self.best_fitness.append(self.engine.get_best_fitness())
        super(ScribeInMemory, self).increment_evaluation()


class ScribeInMemoryFitness(ScribeInMemory):
    """
    Stores fitness apart from best fitness - useful only for simulated annealing
    """

    def __init__(self, eng=None, period=10):
        super(ScribeInMemoryFitness, self).__init__(eng, period)
        self.fitness = []

    def reset(self):
        super(ScribeInMemoryFitness, self).reset()
        self.fitness = []

    def get_fitness(self):
        return self.fitness

    def increment_evaluation(self):
        if self.is_enough_evaluations():
            self.fitness.append(self.engine.get_fitness())
        super(ScribeInMemoryFitness, self).increment_evaluation()