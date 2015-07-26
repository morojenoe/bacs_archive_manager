import logging


class TestRenamer:
    def __init__(self, input_test_extension, output_test_extension):
        self.ext_in = input_test_extension
        self.ext_out = output_test_extension
        self.new_name = {}
        self.test_number = 1
        if self.ext_in == self.ext_out:
            logging.error('Input and output extensions must be different.')

    def _add_test(self, test_in, test_out):
        self.new_name[test_in] = "{0}.in".format(self.test_number)
        self.new_name[test_out] = "{0}.out".format(self.test_number)
        self.test_number += 1

    def _add_tests(self, path_to_tests):
        tests_in, tests_out = self._split(path_to_tests)
        tests_in.sort(key=lambda test: int(test))
        tests_out.sort(key=lambda test: int(test))
        for test_in, test_out in zip(tests_in, tests_out):
            self._add_test(test_in, tests_out)

    def fit(self, sample_tests, main_tests):
        self.new_name.clear()
        self.test_number = 1
        self._add_tests(sample_tests)
        self._add_tests(main_tests)

    def _split(self, path_to_tests):
        tests_in = [test.name for test in path_to_tests if test.ext == self.ext_in]
        tests_out = [test.name for test in path_to_tests if test.ext == self.ext_out]
        return tests_in, tests_out

    def __getitem__(self, test_name):
        if test_name not in self.new_name:
            logging.error('There is no test with name "{0}" in {1}.', test_name, self.new_name)
            raise KeyError()
        return self.new_name[test_name]
