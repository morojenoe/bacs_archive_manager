import unittest

import problem_source.KTHChallenge.kth_link_maker as link_maker


class SymbolTableVariablesTestCase(unittest.TestCase):
    def test_simple_variable(self):
        kth_link_maker = link_maker.KTHChallengeLinkMaker()

        real_links = {
            2011: ["http://challenge.csc.kth.se/2011/problems.pdf",
                   "http://challenge.csc.kth.se/2011/testdata.tar.bz2"],
            2012: ["http://challenge.csc.kth.se/2012/problems.pdf",
                   "http://challenge.csc.kth.se/2012/testdata.tar.bz2"],
            2013: ["http://challenge.csc.kth.se/2013/problems.pdf",
                   "http://challenge.csc.kth.se/2013/challenge-2013.tar.bz2"],
            2014: ["http://challenge.csc.kth.se/2014/problems.pdf",
                   "http://challenge.csc.kth.se/2014/packaged-problems.tar.bz2"],
            2015: ["http://challenge.csc.kth.se/2015/problems.pdf",
                   "http://challenge.csc.kth.se/2015/packaged-problems.tar.bz2"],
            2016: ["http://challenge.csc.kth.se/2016/problems.pdf",
                   "http://challenge.csc.kth.se/2016/problems.tar.xz"],
            2017: ["http://challenge.csc.kth.se/problems.pdf",
                   "http://challenge.csc.kth.se/problems.tar.xz"],
        }

        for year in range(2011, 2018):
            contest_description = {
                'year': year
            }
            links = kth_link_maker.get_links(contest_description)
            self.assertEqual(links[0], real_links[year][0])
            self.assertEqual(links[1], real_links[year][1])


if __name__ == '__main__':
    unittest.main()
