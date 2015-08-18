import argparse
import logging
from KTHChallenge.kth_problem_extractor import KTHChallengeProblemExtractor
from KTHChallenge.kth_link_maker import KTHChallengeLinkMaker
from KTHChallenge.kth_contest_manager import KTHChallengeContestManager
from data_downloader import BaseDownloader
from package_manager import PackageManager
import settings
from tests_renamer import TestRenamer

contest_managers = [KTHChallengeContestManager(
    KTHChallengeLinkMaker(),
    KTHChallengeProblemExtractor('kth_challenge'),
    BaseDownloader(),
    PackageManager(TestRenamer('.*\.in$', '.*\.ans$')),
    settings.PATH_TO_PROBLEMS)]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', )
    parser.add_argument('--source', help='')
    parser.add_argument('--year', help='', type=int)
    return vars(parser.parse_args())


def process_get_command(contest_description):
    for cm in contest_managers:
        if cm.short_name() == contest_description['source']:
            cm.download_contest(contest_description)


def main():
    if settings.MAINTAINERS is None:
        logging.error('Please set the MAINTAINERS field in settings.py')
        return
    contest_description = parse_args()
    if contest_description['command'] == 'get':
        del contest_description['command']
        process_get_command(contest_description)
    elif contest_description['command'] == 'list':
        raise NotImplementedError()


if __name__ == '__main__':
    main()
