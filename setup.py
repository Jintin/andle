#!/usr/bin/env python

import andle
from setuptools import setup

setup(name='andle',
	  version=andle.__version__,
	  description='android dependency sync tool',
	  long_description='andle is a command line tool to help you sync dependencies, sdk or build tool version in gradle base Android projects.',
	  keywords='android gradle config build version dependency sync',
	  scripts=['bin/andle'],
	  test_suite='nose.collector',
	  tests_require=['nose'],
	  url='http://github.com/Jintin/andle',
	  author='Jintin',
	  author_email='jintinapps@gmail.com',
	  license='MIT',
	  packages=['andle'],
	  zip_safe=False)
