#!/usr/bin/env python

import os
import sys
from os.path import expanduser

DATA_PATH = expanduser("~") + "/.andle"


def setpath(path):
	"""
	set android sdk path
	:param path: sdk path
	:return: error path or none
	"""
	if not os.path.exists(path):
		print("not exist path")
		sys.exit(0)
	with open(DATA_PATH, "w+") as file_:
		file_.write(os.path.abspath(path))
	print("setsdk:" + getpath())


def getpath():
	"""
	get sdk path
	:return: path
	"""
	if not os.path.exists(DATA_PATH):
		print("set sdk path first")  # TODO prompt input
		sys.exit(0)
	file = open(DATA_PATH)
	return file.read()


def load(path=getpath()):
	"""
	load sdk config and dependency data
	:return: sdk data
	"""
	data = {}

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
	"""
	find config in sdk folder
	:param data: sdk data
	:param name: which folder
	:param path: sdk path
	"""
	for f in os.listdir(path + "/" + name + "/"):
		if os.path.isdir(path + "/" + name + "/" + f):
			update_value(f, data, name)


def find_dependency(data, tag, path):
	"""
	find dependency in sdk folder
	:param data: sdk data
	:param tag: current tag
	:param path: current path
	"""
	no_dir = True
	for f in os.listdir(path):
		if (os.path.isdir(path + "/" + f)):
			no_dir = False
			find_dependency(data, tag + "/" + f, path + "/" + f)
	if no_dir:
		list = tag[1:].split("/")
		version = list.pop(len(list) - 1)
		name = list.pop(len(list) - 1)
		package = ".".join(list)

		update_value(version, data, package + ":" + name)


def update_value(var, obj, key):
	"""
	update obj value if newer
	:param var: new value
	:param obj: dic obj
	:param key: dic key
	"""
	if not key in obj:
		obj[key] = var
		return
	list1 = obj[key].split(".")
	list2 = var.split(".")
	index = 0

	while list1[index] == list2[index]:
		if list1.__len__() <= index + 1 or list2.__len__() <= index + 1:
			return list1.__len__() < list2.__len__()
		index += 1
	if list1[index] < list2[index]:
		obj[key] = var
