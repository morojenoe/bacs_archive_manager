import base_contest_manager


class KTHChallengeContestManager(base_contest_manager.BaseContestManager):
    def short_name(self):
        return "kth_challenge"

    def long_name(self):
        return "KTH Challenge"

    def main_link(self):
        return "http://challenge.csc.kth.se/"
