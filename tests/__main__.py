# RPC.NET-Connector tests
# __main__.py
# Author: Denes Solti

from os import path
from pathlib import Path
from typing import Iterable
from unittest import TestCase, TestSuite, TextTestRunner, defaultTestLoader
from inspect import getmembers, isclass
from glob import glob
import sys

if __name__ == '__main__':
    cwd = Path().resolve()

    sys.path.append(
        path.join(cwd, 'src')
    )

    def get_all_cases(dir: str) -> Iterable[object]:
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

            for (_, cls) in getmembers(sys.modules[module], istestcase):
                yield cls
        
    runner = TextTestRunner()

    for case in get_all_cases('unit'):
        runner.run(
            defaultTestLoader.loadTestsFromTestCase(case)
        )