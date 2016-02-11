#!/usr/bin/python

try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen


def request(url):
	try:
		return urlopen(url)
	except Exception:
		return None
