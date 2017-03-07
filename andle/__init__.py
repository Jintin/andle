#!/usr/bin/env python

import andle.android
import andle.sdk

__version__ = "1.8.0"


def update(path, dryrun, remote, gradle, interact):
	data = sdk.load()
	android.update(path, data, dryrun, remote, gradle, interact)


def setsdk(path):
	sdk.setpath(path)
