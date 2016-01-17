#!/usr/bin/env python

def newer(version1, version2):

	parts1 = [x for x in version1.split('.')]
	parts2 = [x for x in version2.split('.')]

	# fill up the shorter version with zeros ...
	lendiff = len(parts1) - len(parts2)
	if lendiff > 0:
		parts2.extend([0] * lendiff)
	elif lendiff < 0:
		parts1.extend([0] * (-lendiff))

	return cmp(parts1, parts2)

def cmp(parts1, parts2):
	for i, p in enumerate(parts1):
		ret = (p < parts2[i]) - (p > parts2[i])
		if ret: return ret
	return 0
