# RPC.NET-Connector tests
# __main__.py
# Author: Denes Solti

from glob import glob
from inspect import getmembers, isclass
from os import getcwd, makedirs, path
from sys import modules
from unittest import defaultTestLoader, TestCase
from xmlrunner import XMLTestRunner

if __name__ == '__main__':
    cwd = getcwd()

    def get_all_cases(dir: str) -> list[tuple]:
        for file in glob(path.join(cwd, 'tests', dir, '*.py')):
            module = '{0}.{1}'.format(
                dir, 
                path.splitext(
                    path.basename(file)
                )[0]
            )
            exec('import {0}'.format(module))

            def istestcase(cls) -> bool:
                return isclass(cls) and issubclass(cls, TestCase) and cls is not TestCase

            return getmembers(modules[module], istestcase)

    def run_tests(name: str):
        for (name, case) in get_all_cases(name):
            output = path.join(cwd, 'artifacts')
            makedirs(output, exist_ok=True)
            with open(path.join(output, '{0}.xml'.format(name)), 'wb') as output:
                runner = XMLTestRunner(output)
                runner.run(defaultTestLoader.loadTestsFromTestCase(case))

    run_tests('unit')