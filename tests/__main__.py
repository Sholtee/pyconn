""" The main entry point of the `tests` module """

# RPC.NET-Connector tests
# __main__.py
# Author: Denes Solti

from glob import glob
from inspect import getmembers, isclass
from os import getcwd, makedirs, path
from sys import modules
from typing import Iterable
from unittest import defaultTestLoader, TestCase
from xmlrunner import XMLTestRunner

if __name__ == '__main__':
    cwd = getcwd()

    def get_all_cases(parent_dir: str) -> Iterable[tuple]:
        """ Reads all the test cases found under the given directory """

        for file in glob(path.join(cwd, 'tests', parent_dir, '*.py')):
            module = f'{parent_dir}.{path.splitext(path.basename(file))[0]}'

            # pylint: disable=exec-used
            exec(f'import {module}')

            def istestcase(cls) -> bool:
                return isclass(cls) and issubclass(cls, TestCase) and cls is not TestCase

            for (name, case) in getmembers(modules[module], istestcase):
                yield (name, case)

    def run_tests(test_type: str):
        """ Runs test cases identified by their type. The result is saved in the `artifacts` folder """

        for (name, case) in get_all_cases(test_type):
            output = path.join(cwd, 'artifacts')
            makedirs(output, exist_ok=True)
            with open(path.join(output, f'{name}.xml'), 'wb') as output:
                runner = XMLTestRunner(output)
                runner.run(defaultTestLoader.loadTestsFromTestCase(case))

    run_tests('unit')
    run_tests('integration')
