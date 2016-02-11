#!/usr/bin/python

import json
import andle.http
import codecs

URL = "http://services.gradle.org/versions/current"


def load(url=URL):
	try:
		reader = codecs.getreader("utf-8")
		data = json.load(reader(andle.http.request(url)))
		return data["version"]
	except Exception:
		print("fail to connect url: " + url)
		return None
