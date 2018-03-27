from problem_source.base import base_contest_manager


class UsacoContestManager(base_contest_manager.BaseContestManager):
    def params_must_be_set(self, contest_description):
        params = []
        for param in ['year', 'month', 'lang']:
            if contest_description[param] is None:
                params.append(param)
        return params

    @property
    def short_name(self):
        return "usaco"

    @property
    def long_name(self):
        return "USA Computing Olympiad"

    @property
    def main_link(self):
        return "http://usaco.org/"
