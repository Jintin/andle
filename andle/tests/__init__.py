#!/usr/bin/env python

from unittest import TestCase

import os
import andle
import andle.sdk
import andle.android
import andle.maven


class TestAndle(TestCase):
	CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
	SDK_PATH = CURRENT_PATH + "/sdk"

	def test_sdk(self):
		"""
		sdk load data test
		"""
		data = andle.sdk.load(self.SDK_PATH)
		print(data)

		self.assertEqual(data['build-tools'], '23.0.1', "build-tools not correct")
		self.assertEqual(data['platforms'], '23', "platforms not correct")
		self.assertEqual(data['dependency']['com.google.android.gms:play-services'], '8.1.0', "depedency not correct")
		self.assertEqual(data['dependency']['com.android.support:appcompat-v7'], '23.0.1', "depedency not correct")

	def test_android(self):
		"""
		update project test
		"""
		data = andle.sdk.load(self.SDK_PATH)
		old = open(self.CURRENT_PATH + "/src/old.gradle").read()
		f = open(self.CURRENT_PATH + "/dist/build.gradle", 'w')
		f.write(old)
		f.close()
		andle.android.update(self.CURRENT_PATH + "/dist", data)

		dist = open(self.CURRENT_PATH + "/dist/build.gradle").read()
		new = open(self.CURRENT_PATH + "/src/new.gradle").read()

		self.assertNotEqual(old, dist, "same compare data")
		self.assertEqual(dist, new, "update not correct")

		andle.android.update(self.CURRENT_PATH + "/dist", data, False, True)
		dist = open(self.CURRENT_PATH + "/dist/build.gradle").read()
		self.assertNotEqual(dist, new, "remote not work")

	def test_remote(self):
		"""
		remote maven test
		"""
		value = andle.maven.load(andle.android.JCENTER_URL, "com.facebook.android:facebook-android-sdk")
		self.assertTrue(value != None)
