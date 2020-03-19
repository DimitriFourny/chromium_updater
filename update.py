#!/usr/bin/env python3
import requests
'''
  Just look at
  https://storage.googleapis.com/chromium-browser-snapshots/index.html
  to update this script
'''

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

revision = 0
url = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2FLAST_CHANGE?alt=media"
with requests.get(url) as r:
  revision = r.text
print("Last version: %s" % revision)

filename = "chromium_installer.exe"
url = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2F" + \
      revision + "%2Fmini_installer.exe?&alt=media"
print("Fetching %s" % url)

with requests.get(url) as r:
  r.raise_for_status()
  filesize = int(r.headers["Content-length"])
  print("Downloading %s..." % sizeof_fmt(filesize))

  with open(filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=8192): 
      if chunk: 
        f.write(chunk)

print("Saved in %s" % filename)
