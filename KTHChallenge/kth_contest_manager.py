import base_contest_manager


class KTHChallengeContestManager(base_contest_manager.BaseContestManager):
    @property
    def short_name(self):
        return "kth_challenge"

    @property
    def long_name(self):
        return "KTH Challenge"

    @property
    def main_link(self):
        return "http://challenge.csc.kth.se/"
