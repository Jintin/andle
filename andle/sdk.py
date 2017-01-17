#!/usr/bin/env python

import os
import sys
import andle.version
from os.path import expanduser

DATA_PATH = expanduser("~") + "/.andle"


def setpath(path):
	if not os.path.exists(path):
		print("not exist path")
		sys.exit(0)
	with open(DATA_PATH, "w+") as file_:
		file_.write(os.path.abspath(path))
	print("setsdk:" + getpath())


def getpath():
	if not os.path.exists(DATA_PATH):
		print("set sdk path first")  # TODO prompt input
		sys.exit(0)
	file = open(DATA_PATH)
	return file.read().rstrip('\n')


def load(path=""):
	data = {}
	if path == "":
		path = getpath()
	# find build tool
	find_config(data, "build-tools", path)

	# find sdk version
	find_config(data, "platforms", path)
	data["platforms"] = data["platforms"].replace("android-", "")

	# find dependencies
	data["dependency"] = {}
	find_dependency(data["dependency"], "", path + "/extras/android/m2repository")
	find_dependency(data["dependency"], "", path + "/extras/google/m2repository")

	return data


def find_config(data, name, path):
	for f in os.listdir(path + "/" + name + "/"):
		if os.path.isdir(path + "/" + name + "/" + f):
			update_value(f, data, name)


def find_dependency(data, tag, path):
	if os.path.exists(path):
		no_dir = True
		for f in os.listdir(path):
			if (os.path.isdir(path + "/" + f)):
				no_dir = False
				find_dependency(data, tag + "/" + f, path + "/" + f)
		if no_dir:
			list = tag[1:].split("/")
			if len(list) < 2:
				return
			version = list.pop(len(list) - 1)
			name = list.pop(len(list) - 1)
			package = ".".join(list)

			update_value(version, data, package + ":" + name)


def update_value(var, obj, key):
	if key in obj:
		if andle.version.newer(obj[key], var) > 0:
			obj[key] = var
	else:
		obj[key] = var
