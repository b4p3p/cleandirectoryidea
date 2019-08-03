#!/usr/bin/env python3
import os
import glob
import shutil
import platform

from pathlib import Path

print("Clean Idea Folders")
print("==================")

def convert_bytes(num):
	"""
	this function will convert bytes to MB.... GB... etc
	"""
	for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
	    if num < 1024.0:
	        return "%3.1f %s" % (num, x)
	    num /= 1024.0

def folder_size(path='.'):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total

def annotate_size(arr):
	ris = list()
	for f in arr:
		size = folder_size(f)
		ris.append( (f, convert_bytes(size), size) ) 
	return ris

def check_folder(root):
	ris=list()
	for app in APPS:
		risapps = []
		for f in os.listdir(root):
			if app in f:
				f = "{}/{}".format(root, f)
				risapps.append(f)
		risapps.sort()
		if len(risapps) > 1:
			print("Current: {} - {}".format(risapps[-1], convert_bytes(folder_size(risapps[-1]))))
			risapps = risapps[:-1]
			ris += risapps
		elif len(risapps) == 1:
			print("Current: {} - {}".format(risapps[0], convert_bytes(folder_size(risapps[0]))))
		else:
			print("Current nothing")

	ris.sort()
	ris = annotate_size(ris)
	return ris

def get_folder(name):
	# https://intellij-support.jetbrains.com/hc/en-us/articles/206544519-Directories-used-by-the-IDE-to-store-settings-caches-plugins-and-logs
	sys = platform.system()
	if sys == "Darwin" and name == "CONF":
		return "{}/Library/Preferences".format(HOME)
	if sys == "Darwin" and name == "CACHE":
		return "{}/Library/Caches".format(HOME)
	if sys == "Darwin" and name == "PLUGINS":
		"{}/Library/Application Support".format(HOME)
	if sys == "Darwin" and name == "LOGS":
		return "{}/Library/Logs".format(HOME)
	return None

HOME = str(Path.home())
APPS=["PyCharm2", "IntelliJIdea2", "PhpStorm2", "WebStorm2"]
ris = list()

print(get_folder("CONF"))

print("Configuration...")
ris = check_folder(get_folder("CONF"))

print("Cache...")
ris += check_folder(get_folder("CACHE"))

print("Plugins...")
ris += check_folder(get_folder("PLUGINS"))

print("Logs...")
ris += check_folder(get_folder("LOGS"))

total = 0
for f in ris:
	total += f[2]
	print(f)
	
print("Total: {}".format(convert_bytes(total)))

if total > 0:
	res = input("Clean? (Y/N) : ").lower()

	if res == "y":
		for f in ris:
			print("Delete: {}".format(f[0]))
			shutil.rmtree(f[0])
else:
	print("Nothing to do")
	
print("OK")


