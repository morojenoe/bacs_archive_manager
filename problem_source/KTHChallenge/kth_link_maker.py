from problem_source.base import base_link_maker


class KTHChallengeLinkMaker(base_link_maker.BaseLinkMaker):
    def __init__(self):
        self.main_link = "http://challenge.csc.kth.se"

    def get_links(self, contest_description):
        links = []
        url = self.main_link
        if contest_description["year"] != 2015:
            url += str(contest_description["year"])

        links.append("{0}/problems.pdf".format(url))
        links.append(
            "{0}/{1}".format(url, self.test_data_name(contest_description)))

        return links

    @staticmethod
    def test_data_name(contest_description):
        year = contest_description["year"]
        if year <= 2012:
            return "testdata.tar.bz2"
        if year == 2013:
            return "challenge-2013.tar.bz2"
        return "packaged-problems.tar.bz2"
