#!/usr/bin/env python

from unittest import TestCase

import os
import andle
import andle.sdk
import andle.project


class TestAndle(TestCase):
	CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
	SDK_PATH = CURRENT_PATH + "/sdk"

	def test_sdk(self):
		"""
		sdk load data test
		"""
		data = andle.sdk.load(self.SDK_PATH)
		print data

		self.assertEqual(data['build-tools'], '23.0.1', "build-tools not correct")
		self.assertEqual(data['platforms'], '23', "platforms not correct")
		self.assertEqual(data['dependency']['com.google.android.gms:play-services'], '8.1.0', "depedency not correct")
		self.assertEqual(data['dependency']['com.android.support:appcompat-v7'], '23.0.1', "depedency not correct")

	def test_project(self):
		"""
		update project test
		"""
		data = andle.sdk.load(self.SDK_PATH)
		old = open(self.CURRENT_PATH + "/src/old.gradle").read()
		f = open(self.CURRENT_PATH + "/dist/build.gradle", 'w')
		f.write(old)
		f.close()
		andle.project.update(self.CURRENT_PATH + "/dist", data)

		txt1 = open(self.CURRENT_PATH + "/dist/build.gradle").read()
		txt2 = open(self.CURRENT_PATH + "/src/new.gradle").read()

		self.assertNotEqual(old, txt1, "same compare data")
		self.assertEqual(txt1, txt2, "update not correct")
