#!/usr/bin/env python

import os
import sys
import andle.version
from os.path import expanduser

DATA_PATH = expanduser("~") + "/.andle"


def setpath(path):
    if not os.path.exists(path):
        print("not exist path")
        sys.exit(0)
    with open(DATA_PATH, "w+") as file_:
        file_.write(os.path.abspath(path))
    print("setsdk:" + getpath())


def getpath():
    if not os.path.exists(DATA_PATH):
        print("set sdk path first")
        sys.exit(0)
    file = open(DATA_PATH)
    return file.read().rstrip('\n')


def load(path=""):
    data = {}
    if path == "":
        path = getpath()
    # find build tool
    find_config(data, "build-tools", path)

    # find sdk version
    find_config(data, "platforms", path)
    data["platforms"] = data["platforms"].replace("android-", "")

    # find dependencies
    data["dependency"] = {}
    
    return data


def find_config(data, name, path):
    for f in os.listdir(path + "/" + name + "/"):
        if os.path.isdir(path + "/" + name + "/" + f):
            update_value(f, data, name)


def update_value(var, obj, key):
    if key in obj:
        if andle.version.newer(obj[key], var) > 0:
            obj[key] = var
    else:
        obj[key] = var
