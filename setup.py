#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=8.0', 'requests>=2.31.0', 'python-dateutil>=2.8.0', 'pytz>=2023.3','python-dotenv>=1.0.0','pyyaml>=6.0']

test_requirements = [ ]

setup(
    author="Elliot Palmer",
    author_email='elliot@ecoplumbers.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    description="Python Library to make it easier to interact with the ServiceTitan API v2",
    entry_points={
        'console_scripts': [
            'servicepytan=servicepytan.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='servicepytan',
    name='servicepytan',
    packages=find_packages(include=['servicepytan', 'servicepytan.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/elliotpalmer/servicepytan',
    version='0.3.2',
    zip_safe=False,
)
