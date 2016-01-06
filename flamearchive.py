#!/usr/bin/env python

###############################################################
#            flamearchive.py v2.1                             #
#                                                             #
# By: Kyle Obley (kyle.obley@gmail.com)                       #
#                                                             #
# Crawls through batch setups to find any gateway imported    #
# clips and add them to the specified tar archive.            #
#                                                             #
###############################################################

import os
import sys
import re
import glob
import tarfile
import tempfile
from xml.dom import minidom

if len(sys.argv) < 3:
    sys.exit('\nUsage: python %s /path/to/batch /path/to/archive.tar\n' % sys.argv[0])

sourceDir = sys.argv[1]
destFile = sys.argv[2]

dumpfile = tempfile.NamedTemporaryFile(delete=False)

# Check to see if archive already exists and dump the contents to our temp file
# so we don't duplicate any data.
if os.path.exists(destFile):
    print '\nERROR: Archive already exists, please specify a different file.\n'
    sys.exit(1)

print('\nCreating file list...')

# Get a list of all the files within the batch setups and add them to the temp file
for r,d,f in os.walk(sourceDir):
    for files in f:
        if files.endswith(".mio"):
             currentFile = os.path.join(r,files)
             # Hack to skip bunk mio files Flame has greated
             if os.path.getsize(currentFile) > 500:
                 sourceMIO = minidom.parse(currentFile)

                 # Get the current version used in the batch setup
                 versions = sourceMIO.getElementsByTagName('versions')
                 for node in versions:
                    currentVersion = node.getAttribute('currentVersion')

                 # Get file path for the current version
                 feeds = sourceMIO.getElementsByTagName('feed')
                 for feed in feeds:
                     if feed.getAttribute('vuid') == currentVersion:
                         sequence = feed.getElementsByTagName('path')[0].childNodes[0].nodeValue
                         sequence = re.sub('\[\d*\-\d*\]', '*', sequence)

                         # Write each file path out to the temp file
                         for name in glob.glob(sequence):
                            dumpfile.write(name + '\n')

dumpfile.close()

print('Creating archive...')

# Create archive
tar = tarfile.open(destFile, "a")

# Go through the file list and only add unique files
prev = None
for line in sorted(open(dumpfile.name)):
      line = line.strip()
      if prev is not None and not line.startswith(prev):
            print('\tAdding: ' + prev)
            tar.add(prev)
      prev = line
if prev is not None:
      tar.add(prev)
      print('\tAdding: ' + prev)

# Close archive
tar.close()

# Remove temp file
os.unlink(dumpfile.name)

print('Archive successfully created.')
