#!/usr/bin/python

try:
	from urllib.request import urlopen
	from urllib.error import HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError


def request(url):
	try:
		return urlopen(url)
	except HTTPError:
		return None
