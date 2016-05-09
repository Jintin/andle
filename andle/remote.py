#!/usr/bin/python

import andle.http
from xml.dom import minidom

JCENTER_URL = "https://jcenter.bintray.com/"
# MAVEN_URL = "https://repo1.maven.org/maven2/"


def load(name, url=JCENTER_URL):
	request = andle.http.request(url + name.replace(".", "/").replace(":", "/") + "/maven-metadata.xml")
	try:
		DOMTree = minidom.parse(request)

		collection = DOMTree.documentElement
		versioning = collection.getElementsByTagName("versioning")[0]
		latest = versioning.getElementsByTagName("release")[0]
		version = latest.childNodes[0].data
		return version
	except BaseException:
		print("fail to get version : " + name)
		return None
