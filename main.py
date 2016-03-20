import argparse
import logging

from problem_source.KTHChallenge.kth_link_maker import KTHChallengeLinkMaker
from problem_source.KTHChallenge.kth_problem_extractor import KTHChallengeProblemExtractor
from problem_source.usaco.usaco_contest_manager import UsacoContestManager
from problem_source.usaco.usaco_downloader import UsacoDownloader
from problem_source.usaco.usaco_problem_extractor import UsacoProblemExtractor

import settings
from problem_source.KTHChallenge.kth_contest_manager import KTHChallengeContestManager
from problem_source.base.data_downloader import BaseDownloader
from problem_source.usaco.usaco_link_maker import UsacoLinkMaker
from src.package_manager import PackageManager
from tools.tests_renamer import TestRenamer

contest_managers = [
    KTHChallengeContestManager(
        KTHChallengeLinkMaker(),
        KTHChallengeProblemExtractor(),
        BaseDownloader(),
        PackageManager(TestRenamer("^.*\.in$", "^.*\.ans$")),
        settings.PATH_TO_PROBLEMS),

    UsacoContestManager(UsacoLinkMaker(),
                        UsacoProblemExtractor(),
                        UsacoDownloader(),
                        PackageManager(TestRenamer("(^.*\.in$)|(^I\..*$)",
                                                   "(^.*\.out$)|(^O\..*)$")),
                        settings.PATH_TO_PROBLEMS)]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', )
    parser.add_argument('--source', help='')
    parser.add_argument('--year', help='', type=int)
    parser.add_argument('--month', help='')
    parser.add_argument('--division', help='')
    parser.add_argument('--lang', help='')
    return vars(parser.parse_args())


def process_get_command(contest_description):
    for cm in contest_managers:
        if cm.short_name == contest_description['source']:
            cm.download_contest(contest_description)


def process_list_command():
    for (index, cm) in enumerate(contest_managers, start=1):
        print("{0}) {1} - {2} ({3})".format(index,
                                            cm.short_name,
                                            cm.long_name,
                                            cm.main_link))


def main():
    if settings.MAINTAINERS is None:
        logging.error('Please set the MAINTAINERS field in settings.py')
        return
    contest_description = parse_args()
    if contest_description['command'] == 'get':
        del contest_description['command']
        process_get_command(contest_description)
    elif contest_description['command'] == 'list':
        process_list_command()


if __name__ == '__main__':
    main()
