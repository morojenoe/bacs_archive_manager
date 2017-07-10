import logging

import pathlib

from problem_source.base.base_problem_extractor import BaseProblemExtractor
from src import problem


class KTHChallengeProblemExtractor(BaseProblemExtractor):
    def extract(self, path_to_contest, contest_description):
        tests_mask = "*.[ia]*"
        path_to_contest = pathlib.Path(path_to_contest)
        dirs = [d for d in path_to_contest.iterdir() if d.is_dir()][0]
        if contest_description["year"] >= 2016:
            problem_dirs = [d for d in dirs.iterdir() if d.is_dir()]
        else:
            problem_dirs = [d for d in dirs.iterdir() if d.is_dir()][0]
            problem_dirs = [d for d in problem_dirs.iterdir() if d.is_dir()]

        if contest_description["year"] >= 2013:
            return self._extract_new(problem_dirs,
                                     tests_mask,
                                     contest_description)
        return self._extract_old(problem_dirs, tests_mask, contest_description)

    def _extract_new(self, problem_dirs, tests_mask, contest_description):
        problems = []
        for problem_dir in problem_dirs:
            task = problem.Problem()
            samples_dir = problem_dir.joinpath("data", "sample")
            tests_dir = problem_dir.joinpath("data", "secret")
            if samples_dir.exists():
                task.sample_tests = list(samples_dir.glob(tests_mask))
            if tests_dir.exists():
                task.tests = list(tests_dir.glob(tests_mask))
            task.statement = problem_dir.parent.parent.joinpath("problems.pdf")
            task.id = self._problem_id(contest_description, problem_dir.name)
            task.source = "KTH Challenge {0}".format(
                contest_description["year"])
            problems.append(task)

        return problems

    def _extract_old(self, problem_dirs, tests_mask, contest_description):
        problems = []
        for problem_dir in problem_dirs:
            task = problem.Problem()
            task.statement = problem_dir.parent.parent.parent.joinpath(
                "problems.pdf")
            task.tests = list(problem_dir.glob(tests_mask))
            task.id = self._problem_id(contest_description, problem_dir.name)
            problems.append(task)

        return problems

    def _problem_id(self, contest_description, problem_dir_name):
        return self._get_problem_id(
            "kth_challenge_{0}_{1}".format(contest_description["year"],
                                           problem_dir_name))
