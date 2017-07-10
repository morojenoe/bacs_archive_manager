import re
import logging


class TestRenamer:
    def __init__(self, input_test_re, output_test_re):
        self.in_re = re.compile(input_test_re)
        self.out_re = re.compile(output_test_re)
        self.new_name = {}
        self.test_number = 1

    def _add_test(self, test_in, test_out):
        self.new_name[test_in] = "{0}.in".format(self.test_number)
        self.new_name[test_out] = "{0}.out".format(self.test_number)
        self.test_number += 1

    def _add_tests(self, path_to_tests):
        tests_in, tests_out = self._split(path_to_tests)
        tests_in.sort()
        tests_out.sort()
        if len(tests_in) != len(tests_out):
            logging.error('{} input tests found, {} output tests found, '
                          'the number of tests must match.'
                          .format(len(tests_in), len(tests_out)))
            return False
        for test_in, test_out in zip(tests_in, tests_out):
            self._add_test(test_in, test_out)
        return True

    def fit(self, sample_tests, main_tests):
        self.new_name.clear()
        self.test_number = 1
        if sample_tests is not None:
            if not self._add_tests(sample_tests):
                return False
        if main_tests is not None:
            if not self._add_tests(main_tests):
                return False
        return True

    def _split(self, path_to_tests):
        tests_in = [test for test in path_to_tests if self.in_re.match(test)]
        tests_out = [test for test in path_to_tests if self.out_re.match(test)]
        return tests_in, tests_out

    def __getitem__(self, test_name):
        if test_name not in self.new_name:
            logging.error('There is no test with name "{0}" in {1}.'.format(
                test_name,
                self.new_name))
            raise KeyError()
        return self.new_name[test_name]
