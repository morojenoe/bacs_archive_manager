import base_problem_extractor
import path
import problem


class UsacoProblemExtractor(base_problem_extractor.BaseProblemExtractor):
    def extract(self, path_to_contest, contest_description):
        problems = []
        path_to_contest = path.Path(path_to_contest)
        dirs = path_to_contest.dirs()

        for p_dir in dirs:
            p = problem.Problem()
            p.tests = p_dir.files()
            p.statement = path_to_contest.joinpath(p_dir.name + ".html")
            p.id = self._get_problem_id(
                "usaco_{}_{}_{}".format(contest_description["year"],
                                        contest_description["month"],
                                        p_dir.name))
            p.source = "USACO {} {}".format(contest_description["year"],
                                            contest_description["month"])
            problems.append(p)

        return problems
