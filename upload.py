#!/usr/bin/env python

import os
import andle
os.system("sudo rm -rf dist")
os.system("sudo python setup.py sdist")
os.system("twine upload dist/andle-" + andle.__version__ + ".tar.gz")
