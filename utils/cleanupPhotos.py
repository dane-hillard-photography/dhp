#!/usr/bin/env python

import os
import re
import sys
import shutil
import pprint
import MySQLdb

from collections import defaultdict

sys.path.append(os.path.abspath('..'))

from dhp import settings

print 'Gathering info...'

db = MySQLdb.connect(host='localhost',
					 user='root',
					 passwd='l1ttl3l3v14th4n',
					 db='django')

cur = db.cursor()

cur.execute('SELECT image, thumbnail_large, thumbnail_medium, thumbnail_small, thumbnail_square FROM photography_photograph')

mediaDir = settings.MEDIA_ROOT
unusedDir = 'unused'

sizes = ['uncropped', 'large', 'medium', 'small', 'square']

dbFiles = defaultdict(set)
fsFiles = defaultdict(set)

for row in cur.fetchall():
	sizedList = zip(sizes, row)
	for size, file in sizedList:
		dbFiles[size].add(os.path.join(mediaDir, file))

for root, dirs, files in os.walk(os.path.join(mediaDir, 'images')):
	size = root.split('/')[-1]
	if size == 'images':
		continue

	for file in files:
		if re.match('.*\.(jpg|JPG)$', file):
			fsFiles[size].add(os.path.join(root, file))

unusedFiles = defaultdict(set)
missingFiles = defaultdict(set)

for size in sizes:
	unusedFiles[size].update(fsFiles[size].difference(dbFiles[size]))
	missingFiles[size].update(dbFiles[size].difference(fsFiles[size]))

try:
	os.mkdir(unusedDir)
except OSError:
	pass

for size in sizes:
	try:
		os.mkdir(os.path.join(unusedDir, size))
	except OSError:
		pass

print 'Cleaning up...'

for size in sizes:
	for file in missingFiles[size]:
		print '{0} does not exist but is referenced in the database!'.format(file)
	
	for file in unusedFiles[size]:
		shutil.move(file, os.path.join(unusedDir, size))
