import logging
import pathlib
import settings
import configparser
import shutil


class PackageManager:
    def __init__(self, tests_renamer):
        self.tests_renamer = tests_renamer

    def build_package(self, problem, dir_path):
        dir_path = pathlib.Path(dir_path).joinpath(problem.id)
        self._make_skeleton(dir_path)
        self._build_checker(dir_path, problem)
        self._build_statement(dir_path, problem)
        self._build_tests(dir_path, problem)
        self._build_config(dir_path, problem)

    def build_packages(self, problems, dir_path):
        for problem in problems:
            self.build_package(problem, dir_path)

    def _build_checker(self, dir_path, problem):
        dir_path = dir_path.joinpath('checker')
        checker_config = configparser.ConfigParser()

        checker_config.add_section('build')
        checker_config.add_section('utility')

        if problem.checker is None:
            checker_config.set('build', 'builder', 'none')
            checker_config.set('utility', 'call', 'std/strict/out_stdout')
            try:
                with dir_path.joinpath('config.ini').open('w') as config_file:
                    checker_config.write(config_file)
            except OSError:
                logging.error('Cannot write to checker/config.ini')
        else:
            raise NotImplementedError()

    @staticmethod
    def _build_statement(dir_path, problem):
        dir_path = dir_path.joinpath('statement')
        dest_file_name = dir_path.joinpath(
            'problem{}'.format(pathlib.Path(problem.statement).suffix))
        config_path = dir_path.joinpath(
            "{0}.ini".format(pathlib.Path(problem.statement).suffix[1:]))

        statement_config = configparser.ConfigParser()

        statement_config.add_section('info')
        statement_config.add_section('build')

        statement_config.set('info', 'lang', 'C')

        statement_config.set('build', 'builder', 'copy')
        statement_config.set('build', 'source', dest_file_name.name)

        try:
            with config_path.open('w') as config_file:
                statement_config.write(config_file)
        except OSError as error:
            logging.error(
                'Cannot write to statement/{0}'.format(dir_path.name))
            logging.exception(error)

        try:
            shutil.copyfile(str(problem.statement), str(dest_file_name))
        except OSError as error:
            logging.error('Cannot copy problem statement')
            logging.exception(error)

    def _build_tests(self, dir_path, problem):
        if not self.tests_renamer.fit([str(t) for t in problem.sample_tests],
                                      [str(t) for t in problem.tests]):
            logging.error('Please manage test for {} manually.'.format(
                problem.name))
            return

        dir_path = pathlib.Path(dir_path.joinpath('tests'))
        for test in problem.sample_tests + problem.tests:
            shutil.copyfile(str(test),
                            str(dir_path.joinpath(
                                self.tests_renamer[str(test)])))

    @staticmethod
    def _build_config(dir_path, problem):
        config = configparser.ConfigParser()

        config.add_section('info')
        config.add_section('resource_limits')

        config.set('info', 'name', problem.name)
        config.set('info', 'maintainers', settings.MAINTAINERS)
        config.set('info', 'source', problem.source)

        config.set('resource_limits', 'time', problem.time_limit)
        config.set('resource_limits', 'memory', problem.memory_limit)

        if (problem.stdin is not None) or (problem.stdout is not None):
            config.add_section('files')
            if problem.stdin is not None:
                config.set('files', 'stdin', problem.stdin)
            if problem.stdout is not None:
                config.set('files', 'stdout', problem.stdout)

        try:
            with dir_path.joinpath('config.ini').open('w') as config_file:
                config.write(config_file)
        except OSError:
            logging.error('Cannot write to config.ini')

    @staticmethod
    def _make_skeleton(dir_path):
        content_of_format_file = 'bacs/problem/single#simple0'

        if dir_path.exists():
            logging.warning('{0} already exists'.format(dir_path))

        try:
            dir_path.joinpath('checker').mkdir(exist_ok=True, parents=True)
            dir_path.joinpath('misc').mkdir(exist_ok=True, parents=True)
            dir_path.joinpath('statement').mkdir(exist_ok=True, parents=True)
            dir_path.joinpath('tests').mkdir(exist_ok=True, parents=True)
            with dir_path.joinpath('format').open('w') as format_file:
                format_file.write(content_of_format_file)
        except (OSError, IOError) as error:
            logging.error('Cannot write to {0}'.format(dir_path))
            logging.exception(error)
            return False

        return True
