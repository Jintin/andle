#!/usr/bin/python

import urllib2
from xml.dom import minidom


def load(url, name):
	request = urllib2.urlopen(url + name.replace(".", "/").replace(":", "/") + "/maven-metadata.xml")
	DOMTree = minidom.parse(request)
	collection = DOMTree.documentElement
	versioning = collection.getElementsByTagName("versioning")[0]
	latest = versioning.getElementsByTagName("latest")[0]
	version = latest.childNodes[0].data
	return version
