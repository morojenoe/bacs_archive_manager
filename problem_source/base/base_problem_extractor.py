import settings
from abc import abstractmethod, ABCMeta


class BaseProblemExtractor(metaclass=ABCMeta):
    @abstractmethod
    def extract(self, path_to_contest, contest_description):
        pass

    @staticmethod
    def _get_problem_id(name):
        if settings.START_ID is not None:
            settings.START_ID += 1
            return str(settings.START_ID - 1)
        return name
