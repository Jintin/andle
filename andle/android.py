#!/usr/bin/env python

import os
import fnmatch
import andle.remote
import andle.gradle

COMPILE_TAGS = ["compile", "Compile"]
GRADLE_TAGS = ["classpath"]

is_dryrun = False
check_remote = False
check_gradle = False


def update(path, data, dryrun=False, remote=False, gradle=False):
	global is_dryrun
	is_dryrun = dryrun
	global check_remote
	check_remote = remote
	global check_gradle
	check_gradle = gradle

	global is_modify
	is_modify = False

	gradle_version = andle.gradle.load()
	for root, dir, files in os.walk(path):
		for file in fnmatch.filter(files, "build.gradle"):
			parse_dependency(root + "/" + file, data)
		if check_gradle and gradle_version:
			for file in fnmatch.filter(files, "gradle-wrapper.properties"):
				parse_gradle(root + "/" + file, gradle_version)


def parse_gradle(path, version):
	print("check " + path)
	with open(path) as f:
		io = f.readlines()

	global modify
	modify = False
	new_data = ""

	global line
	for line in io:
		if line.startswith("distributionUrl"):
			update_value("distributionUrl", line[16:].strip(),
						 "https\://services.gradle.org/distributions/gradle-" + version + "-all.zip")
		new_data += line

	# save back
	save(path, new_data)


def parse_dependency(path, data):
	print("check " + path)
	with open(path) as f:
		io = f.readlines()

	new_data = ""
	find_sdk = False
	find_tools = False
	global modify
	modify = False
	deps = data["dependency"]

	global line
	for line in io:
		compare = line.strip()
		word = line.split()
		if word.__len__() == 0:
			continue
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
		elif any(word[0].endswith(compile) for compile in COMPILE_TAGS):
			check_version(word, deps, check_remote)
		# find gradle tag
		elif check_gradle and any(compare.startswith(gradle) for gradle in GRADLE_TAGS):
			check_version(word, deps, check_gradle)
		new_data += line

	# save back
	save(path, new_data)


def check_version(word, deps, check_online):
	string = word[1]
	if string.startswith("'") or string.startswith("\""):
		dep = string.split(string[0])[1]
		tag = dep[:dep.rfind(":")]
		version = dep[dep.rfind(":") + 1:]

		if version.__contains__("@"):
			version = version[:version.find("@")]
		if deps.__contains__(tag):
			update_value(tag, version, deps[tag])
		elif check_online:
			online_version = andle.remote.load(tag)
			if online_version != None:
				update_value(tag, version, online_version)
				deps[tag] = online_version


def update_value(name, old, new):
	if old == new:
		return
	print(name + ": " + old + " -> " + new)
	global modify
	modify = True
	global line
	line = line.replace(old, new)


def save(path, new_data):
	if modify:
		if not is_dryrun:
			f = open(path, 'w')
			f.write(new_data)
			f.close()
			print("done")
	else:
		print("ok")
