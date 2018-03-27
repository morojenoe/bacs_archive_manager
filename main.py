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
    parser.add_argument('command', help='get or list')
    parser.add_argument('--source', help='')
    parser.add_argument('--year', help='you may use one digit year(0 for 2000, 1 for 2001, etc), \n you may use'
                                       ' two digit year(00 for 2000, 11 for 2011, etc), and of course you may use '
                                       ' four digit year(1992, 2014, etc)', type=int)
    parser.add_argument('--month', help='you may use digits(1 - for january, 2 for february, 12 - for december), also '
                                        'you may use short(jan, feb, mar, apr, map, june, july, aug, '
                                        'sep or sept, oct, nov, dec) or long names in addition you may use '
                                        'unambiguous prefix of long name of the month(janu, decem, nove, etc.)')
    parser.add_argument('--division', help='not for all contests')
    parser.add_argument('--lang', help='')
    contest_description = vars(parser.parse_args())

    return contest_description


def process_get_command(contest_description):
    for cm in contest_managers:
        if cm.short_name == contest_description['source']:
            params = cm.params_must_be_set(contest_description)
            if len(params) == 0:
                cm.download_contest(contest_description)
            else:
                logging.error('Please, set next params: {0}'.format(', '.join(params)))


def process_list_command(contest_description):
    if contest_description['source'] is None:
        for (index, cm) in enumerate(contest_managers, start=1):
            print("{0}) {1} - {2} ({3})".format(index,
                                                cm.short_name,
                                                cm.long_name,
                                                cm.main_link))
    else:
        source = contest_description['source']
        cm = next((c for c in contest_managers if c.short_name == source), None)
        if cm is None:
            logging.error('The source "{0}" is not supported '.format(source))
            return
        print(cm.is_exists(contest_description))


def _check_settings():
    if settings.MAINTAINERS is None:
        logging.error('Please set the MAINTAINERS field in settings.py')
        return False
    if settings.PATH_TO_PROBLEMS is None:
        logging.error('Please set the PATH_TO_PROBLEMS in setting.py')
        return False
    return True


def _check_contest_description_year(contest_description):
    if len(str(contest_description['year'])) <= 2:
        contest_description['year'] += 2000
    return True


def _check_contest_description_month(contest_description):
    if contest_description['month'] is None:
        return True

    check_result = True
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december']
    if str(contest_description['month']).isdigit():
        if 1 <= int(contest_description['month']) <= 12:
            contest_description['month'] = int(contest_description['month']) - 1
        else:
            logging.error('The month value is not recognizable.')
            check_result = False
    else:
        input_month = str(contest_description['month']).lower()
        found_months = []
        for m in months:
            if m.startswith(input_month):
                found_months.append(m)
        if len(found_months) == 0:
            logging.error('month name is not known {0}'.format(input_month))
            check_result = False
        elif len(found_months) == 1:
            contest_description['month'] = months.index(found_months[0])
        else:
            logging.error('ambiguous month name {0}: {1}'.format(input_month, ', '.join(found_months)))
            check_result = False
    return check_result


def _check_contest_description(contest_description):
    check_result = _check_contest_description_year(contest_description)
    check_result = check_result and _check_contest_description_month(contest_description)
    return check_result


def main():
    if not _check_settings():
        return
    contest_description = parse_args()
    if not _check_contest_description(contest_description):
        return
    if contest_description['command'] == 'get':
        del contest_description['command']
        process_get_command(contest_description)
    elif contest_description['command'] == 'list':
        process_list_command(contest_description)


if __name__ == '__main__':
    main()
