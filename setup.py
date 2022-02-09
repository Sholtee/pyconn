# pylint: disable=missing-module-docstring
if __name__ == '__main__':
    from setuptools import setup

    setup(
        name='pyconn',
        version='0.0.0',
        description='RPC.NET Python Connector',
        author='Denes Solti',
        author_email='sodnaatx@gmail.com',
        license='MIT',
        url='https://github.com/Sholtee/pyconn',
        package_dir={'': 'src'},
        packages=['pyconn'],
        python_requires='>=3.9'
    )
