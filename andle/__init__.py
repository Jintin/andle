#!/usr/bin/env python

import project
import sdk


def update(path, dryrun=False):
	"""
	update android projects config
	:param path: projects path
	:param dryrun: dryrun or not
	"""
	data = sdk.load()
	project.update(path, data, dryrun)


def setsdk(path):
	"""
	set android sdk path
	:param path: sdk path
	"""
	sdk.setpath(path)
