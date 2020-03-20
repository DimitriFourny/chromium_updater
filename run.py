#!/usr/bin/env python3
import requests
import os
import sys
import glob 
import subprocess 

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def chromium_dir():
  local_dir = os.getenv("LOCALAPPDATA")
  chromium_dir = os.path.join(local_dir, "Chromium\\Application")
  return chromium_dir

def chromium_installed_versions():
  directories = glob.glob(chromium_dir() + '/[0-9]*')
  versions = [os.path.basename(d) for d in directories]
  return versions

def get_last_chromium_info(channel):
  '''Possible channels: stable, beta, canary, canary_asan, dev'''
  data = []
  with requests.get("http://omahaproxy.appspot.com/all.json") as r:
    data = r.json()

  for obj in data:
    if obj["os"] == "win64":
      versions = obj["versions"]
      for version in versions:
        if version["channel"] == channel:
          return version
  
  return None

def get_last_revision():
  url = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2FLAST_CHANGE?&alt=media"
  with requests.get(url) as r:
    r.raise_for_status()
    return r.text
  return None


installed_versions = chromium_installed_versions()
print("Installed version(s): %s" % ", ".join(installed_versions))

channel = "canary"
last_chromium = get_last_chromium_info(channel)
version = last_chromium["version"]
revision = last_chromium["branch_base_position"]
print("Last '%s' version: %s (r%s)" % (channel, version, revision))

last_revision = get_last_revision()
print("It's possible to update to r%s" % last_revision)

update_it = None
while update_it == None:
  choice = input("Do you want to update it? [y/n]: ").lower().strip()
  if choice == 'y':
    update_it = True
  elif choice == 'n':
    update_it = False

if not update_it:
  sys.exit(1)

filename = "chromium_installer.exe"
url = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2F" + \
      last_revision + "%2Fmini_installer.exe?&alt=media"

with requests.get(url) as r:
  r.raise_for_status()
  filesize = int(r.headers["Content-length"])
  print("Downloading %s..." % sizeof_fmt(filesize))

  with open(filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192): 
      if chunk: 
        f.write(chunk)

print("Saved in %s" % filename)
print("Update chromium")

subprocess.call([filename], stdin=None, stdout=None, 
    stderr=None, shell=False)
  
print("Delete %s" % filename)
os.remove(filename)