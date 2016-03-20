import settings


class Problem:
    def __init__(self):
        self.tests = []
        self.sample_tests = []
        self.statement = "problem.pdf"
        self.checker = None
        self.id = ""
        self.name = ""
        self.time_limit = settings.TIME_LIMIT_BY_DEFAULT
        self.memory_limit = settings.MEMORY_LIMIT_BY_DEFAULT
        self.source = ""
        self.stdin = None
        self.stdout = None
