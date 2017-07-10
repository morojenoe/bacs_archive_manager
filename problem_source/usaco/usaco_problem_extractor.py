import pathlib

from problem_source.base import base_problem_extractor
from src import problem


class UsacoProblemExtractor(base_problem_extractor.BaseProblemExtractor):
    def extract(self, path_to_contest, contest_description):
        tests_mask = "*.[io]*"
        problems = []
        path_to_contest = pathlib.Path(path_to_contest)
        dirs = [d for d in path_to_contest.iterdir() if d.is_dir()]

        for p_dir in dirs:
            p = problem.Problem()
            p.tests = list(p_dir.glob(tests_mask))
            p.statement = path_to_contest.joinpath(p_dir.name + ".html")
            p.id = self._get_problem_id(
                "usaco_{}_{}_{}".format(contest_description["year"],
                                        contest_description["month"],
                                        p_dir.name))
            p.source = "USACO {} {}".format(contest_description["year"],
                                            contest_description["month"])
            problems.append(p)

        return problems
