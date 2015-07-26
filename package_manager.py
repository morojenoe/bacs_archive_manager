import logging
import path.Path
import settings
import configparser.ConfigParser


class PackageManager:
    def __init__(self, tests_renamer):
        self.tests_renamer = tests_renamer

    def build_package(self, problem, path_to_directory):
        path_to_directory = path.Path(path_to_directory).joinpath(problem.ID)
        self.make_skeleton(path_to_directory)
        self.build_checker(path_to_directory, problem)
        self.build_statement(path_to_directory, problem)
        self.build_tests(path_to_directory, problem)
        self.build_config(path_to_directory, problem)

    def build_packages(self, problems, path_to_directory):
        for problem in problems:
            self.build_package(problem, path_to_directory)

    def build_checker(self, path_to_directory, problem):
        path_to_directory = path_to_directory.joinpath('checker')
        checker_config = configparser.ConfigParser()

        checker_config.add_section('build')
        checker_config.add_section('utility')

        if problem.checker is None:
            checker_config.set('build', 'builder', 'none')
            checker_config.set('utility', 'call', 'std/strict/out_stdout')
            try:
                with path_to_directory.joinpath('config.ini').open('w') as config_file:
                    checker_config.write(config_file)
            except OSError:
                logging.error('Cannot write to checker/config.ini')
        else:
            raise NotImplementedError()

    @staticmethod
    def build_statement(path_to_directory, problem):
        statement_config = configparser.ConfigParser()

        statement_config.add_section('info')
        statement_config.add_section('build')

        statement_config.set('info', 'lang', 'C')

        statement_config.set('build', 'builder', 'copy')
        statement_config.set('source', 'source', problem.statement)

        if problem.statement is not None:
            path_to_directory = path_to_directory.joinpath('statement',
                                                           "{0}.ini".format(path.Path(problem.statement).ext))
        else:
            path_to_directory = path_to_directory.joinpath('statement', 'pdf.ini')

        try:
            with path_to_directory.open('w') as config_file:
                statement_config.write(config_file)
        except OSError:
            logging.error('Cannot write to statement/{0}'.format(path_to_directory.name))

    def build_tests(self, path_to_directory, problem):
        self.tests_renamer.fit(problem.sample_tests, problem.tests)

        path_to_directory = path.Path(path_to_directory.joinpath('tests'))
        for test in problem.sample_tests + problem.tests:
            path_to_directory.copyfile(test, path_to_directory.joinpath(self.tests_renamer[test]))

    @staticmethod
    def build_config(path_to_directory, problem):
        config = configparser.ConfigParser()

        config.add_section('info')
        config.add_section('resource_limits')
        config.add_section('files')

        config.set('info', 'name', problem.name)
        config.set('info', 'maintainers', settings.MAINTAINERS)
        config.set('info', 'source', problem.source)

        config.set('resource_limits', 'time',
                   problem.time_limit if problem.time_limit is not None else settings.TIME_LIMIT_BY_DEFAULT)
        config.set('resource_limits', 'memory',
                   problem.memory_limit if problem.time_limit is not None else settings.MEMORY_LIMIT_BY_DEFAULT)

        config.set('files', 'stdin', problem.stdin)
        config.set('files', 'stdout', problem.stdout)

        try:
            with path_to_directory.joinpath('config.ini').open('w') as config_file:
                config.write(config_file)
        except OSError:
            logging.error('Cannot write to config.ini')

    @staticmethod
    def make_skeleton(path_to_directory):
        content_of_format_file = 'bacs/problem/single#simple0'

        if path_to_directory.exists():
            logging.warning('{path} already exists'.format(path=path_to_directory))

        try:
            path_to_directory.joinpath('checker').makedirs_p()
            path_to_directory.joinpath('misc').makedirs_p()
            path_to_directory.joinpath('statement').makedirs_p()
            path_to_directory.joinpath('tests').makedirs_p()
            with path_to_directory.joinpath('format').open() as format_file:
                format_file.write(content_of_format_file)
        except (OSError, IOError):
            logging.error('Cannot write to {path}'.format(path_to_directory))
            return False

        return True
