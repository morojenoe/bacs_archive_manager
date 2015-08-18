import settings
from abc import abstractmethod, ABCMeta


class BaseProblemExtractor(metaclass=ABCMeta):
    def __init__(self, contest_short_name):
        self.contest_short_name = contest_short_name

    @abstractmethod
    def extract(self, path_to_contest, contest_description):
        pass

    @staticmethod
    def _get_problem_id(name):
        if settings.START_ID is not None:
            settings.START_ID += 1
            return str(settings.START_ID - 1)
        return name
