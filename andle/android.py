#!/usr/bin/env python

import os
import fnmatch
import andle.remote
import andle.gradle

COMPILE_TAGS = ["compile", "Compile"]


def update(path, data, dryrun=False, remote=False, gradle=False):
	global is_dryrun
	is_dryrun = dryrun
	global check_remote
	check_remote = remote
	global check_gradle
	check_gradle = gradle

	for file in filter(path, "build.gradle"):
		parse_dependency(file, data)

	if check_gradle:
		gradle_version = andle.gradle.load()
		for file in filter(path, "gradle-wrapper.properties"):
			parse_gradle(file, gradle_version)


def filter(path, name):
	result = []
	for root, dir, files in os.walk(path):
		for file in fnmatch.filter(files, name):
			result.append(root + "/" + file)
	return result


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
	global modify
	modify = False

	global line
	for line in io:
		word = line.split()
		if word.__len__() >= 2:
			check_dependency(word, data)
			check_classpath(word, data)
		new_data += line

	# save back
	save(path, new_data)


def check_dependency(word, data):
	first = word[0]
	# find compileSdkVersion tag
	if first == "compileSdkVersion":
		platforms = word[1]
		if data["platforms"] == "N":
			update_value("compileSdkVersion", platforms, "android-N")
		else:
			update_value("compileSdkVersion", platforms, data["platforms"])
		return True
	# find buildToolsVersion tag
	elif first == "buildToolsVersion":
		buildToolsVersion = word[1].replace("\"", "")
		update_value("buildToolsVersion", buildToolsVersion, data["build-tools"])
		return True
	# find compile tag
	elif any(first.endswith(compile) for compile in COMPILE_TAGS):
		check_version(word, data["dependency"], check_remote)
		return True
	else:
		return False


def check_classpath(word, data):
	if check_gradle and word[0].startswith("classpath"):
		check_version(word, data["dependency"], check_gradle)
		return True
	else:
		return False


def check_version(word, deps, check_online):
	string = word[1]
	if string.startswith("'") or string.startswith("\""):
		dep = string.split(string[0])[1]
		tag = dep[:dep.rfind(":")]
		version = get_version(dep)

		if tag in deps:
			update_value(tag, version, deps[tag])
		elif check_online:
			online_version = andle.remote.load(tag)
			update_value(tag, version, online_version)
			deps[tag] = online_version


def get_version(dep):
	version = dep[dep.rfind(":") + 1:]

	if "@" in version:
		version = version[:version.find("@")]
	return version


def update_value(name, old, new):
	if old == new or new == None:
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
