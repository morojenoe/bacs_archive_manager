from base_problem_extractor import BaseProblemExtractor
import path
import logging
import problem


class KTHChallengeProblemExtractor(BaseProblemExtractor):
    def extract(self, path_to_contest, contest_description):
        tests_mask = "*.[ia]*"
        path_to_contest = path.Path(path_to_contest)
        dirs = path_to_contest.dirs()
        if len(dirs) != 1:
            logging.warning(
                "Expected number of directories 1, found {0}".format(
                    len(dirs)))
        problem_dirs = dirs[0].dirs()

        if contest_description["year"] >= 2013:
            return self._extract_new(problem_dirs, tests_mask)
        return self._extract_old(problem_dirs, tests_mask)

    def _extract_new(self, problem_dirs, tests_mask):
        problems = []
        for problem_dir in problem_dirs:
            task = problem.Problem()
            samples_dir = problem_dir.joinpath("data", "sample")
            tests_dir = problem_dir.joinpath("data", "secret")
            if samples_dir.exists():
                task.sample_tests = samples_dir.files(tests_mask)
            if tests_dir.exists():
                task.tests = tests_dir.files(tests_mask)
            task.id = self._get_problem_id(
                "{0}_{1}".format(self.contest_short_name, problem_dir.name))
            problems.append(task)

        return problems

    def _extract_old(self, problem_dirs, tests_mask):
        problems = []
        for problem_dir in problem_dirs:
            task = problem.Problem()
            task.tests = problem_dir.files(tests_mask)
            task.id = self._get_problem_id(
                "{0}_{1}".format(self.contest_short_name, problem_dir.name))
            problems.append(task)

        return problems
