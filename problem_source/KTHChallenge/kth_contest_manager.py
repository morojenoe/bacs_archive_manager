from problem_source.base import base_contest_manager


class KTHChallengeContestManager(base_contest_manager.BaseContestManager):
    def params_must_be_set(self, contest_description):
        params = []
        if contest_description['year'] is None:
            params.append('year')
        return params

    @property
    def short_name(self):
        return "kth_challenge"

    @property
    def long_name(self):
        return "KTH Challenge"

    @property
    def main_link(self):
        return "http://challenge.csc.kth.se/"
