#!/usr/bin/python

try:
	from urllib.request import urlopen
	from urllib.error import HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError
from xml.dom import minidom


def load(url, name):
	try:
		request = urlopen(url + name.replace(".", "/").replace(":", "/") + "/maven-metadata.xml")
		DOMTree = minidom.parse(request)
		collection = DOMTree.documentElement
		versioning = collection.getElementsByTagName("versioning")[0]
		latest = versioning.getElementsByTagName("latest")[0]
		version = latest.childNodes[0].data
		return version
	except HTTPError:
		return None
