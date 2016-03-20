from problem_source.base import base_contest_manager


class UsacoContestManager(base_contest_manager.BaseContestManager):
    @property
    def short_name(self):
        return "usaco"

    @property
    def long_name(self):
        return "USA Computing Olympiad"

    @property
    def main_link(self):
        return "http://usaco.org/"
