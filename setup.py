#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Sterling Swygert",
    author_email='sterling.swygert@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A project for ingesting and modeling sports stats with the intent of using it to build ML models",
    entry_points={
        'console_scripts': [
            'sports_stats=sports_stats.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sports_stats',
    name='sports_stats',
    packages=find_packages(include=['sports_stats', 'sports_stats.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sterling-swygert/sports_stats',
    version='0.1.0',
    zip_safe=False,
)
