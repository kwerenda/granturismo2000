import abc

class Engine(object):

    def __init__(self, model):
        self._model = model
        self._dims = model.n_turns


    @abc.abstractmethod
    def solve(self, iterations):
        """Perform all steps"""
        return

    @abc.abstractmethod
    def step(self):
        """Make one step"""
        return




