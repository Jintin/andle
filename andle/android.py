#!/usr/bin/env python

import os
import fnmatch


def update(path, data, dryrun=False):
	"""
	update your android projects config
	:param path: path to android projects
	:param data: newest config data
	:param dryrun: dryrun or not
	"""
	for root, dir, files in os.walk(path):
		for file in fnmatch.filter(files, "build.gradle"):
			parse(root + "/" + file, data, dryrun)


def parse(path, data, dryrun=False):
	"""
	analyze gradle file to update
	:param path: gradle file path
	:param data: newest config data
	:param dryrun: dryrun or not
	"""
	print("check " + path)

	global modify
	modify = False
	new_data = ""
	find_sdk = False
	find_tools = False
	deps = data["dependency"]

	with open(path) as f:
		io = f.read()
		print(io)
	global line
	for line in io:
		word = line.split()
		# find compileSdkVersion tag
		if not find_sdk and line.__contains__("compileSdkVersion"):
			find_sdk = True
			platforms = word[1]
			update_value("compileSdkVersion", platforms, data["platforms"])
		# find buildToolsVersion tag
		elif not find_tools and line.__contains__("buildToolsVersion"):
			find_tools = True
			buildToolsVersion = word[1].replace("\"", "")
			update_value("buildToolsVersion", buildToolsVersion, data["build-tools"])
		# find compile tag
		elif line.__contains__("compile"):
			string = word[1]
			if string.startswith("'") or string.startswith("\""):
				dep = string.split(string[0])[1]
				tag = dep[:dep.rfind(":")]
				if deps.__contains__(tag):
					version = dep[dep.rfind(":") + 1:]
					if version.__contains__("@"):
						version = version[:version.find("@")]
					update_value(tag, version, deps[tag])

		new_data += line

	# is modify save back
	if modify:
		save(path, new_data, dryrun)
	else:
		print("OK")


def update_value(name, old, new):
	"""
	check if value is different then update
	:param name: tag name
	:param old: old value
	:param new: new value
	"""
	if old == new:
		return
	global line
	global modify
	print(name + ": " + old + " -> " + new)
	modify = True
	line = line.replace(old, new)


def save(path, new_data, dryrun):
	"""
	save gradle file back or print(dryrun)
	:param path: gradle file path
	:param new_data: gradle data
	:param dryrun: dryrun or not
	"""
	if dryrun:
		print(new_data)
	else:
		f = open(path, 'w')
		f.write(new_data)
		f.close()
