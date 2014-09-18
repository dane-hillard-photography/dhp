#!/usr/bin/env python

import os
import re
import sys
import shutil
import MySQLdb

from collections import defaultdict

sys.path.append(os.path.abspath('..'))

from dhp import settings

def main():
    print 'Gathering info...'

    db = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='l1ttl3l3v14th4n',
        db='django'
    )

    cur = db.cursor()

    cur.execute(
        'SELECT image, thumbnail_large, thumbnail_medium, thumbnail_small, thumbnail_square FROM photography_photograph')

    media_dir = settings.MEDIA_ROOT
    unused_dir = 'unused'

    sizes = ['uncropped', 'large', 'medium', 'small', 'square']

    db_files = defaultdict(set)
    fs_files = defaultdict(set)

    for row in cur.fetchall():
        sized_list = zip(sizes, row)
        for size, unused_file in sized_list:
            db_files[size].add(os.path.join(media_dir, unused_file))

    for root, dirs, files in os.walk(os.path.join(media_dir, 'images')):
        size = root.split('/')[-1]
        if size == 'images':
            continue

        for fs_file in files:
            if re.match('.*\.(jpg|JPG)$', fs_file):
                fs_files[size].add(os.path.join(root, fs_file))

    unused_files = defaultdict(set)
    missing_files = defaultdict(set)

    for size in sizes:
        unused_files[size].update(fs_files[size].difference(db_files[size]))
        missing_files[size].update(db_files[size].difference(fs_files[size]))

    try:
        os.mkdir(unused_dir)
    except OSError:
        pass

    for size in sizes:
        try:
            os.mkdir(os.path.join(unused_dir, size))
        except OSError:
            pass

    print 'Cleaning up...'

    for size in sizes:
        for missing_file in missing_files[size]:
            print '{0} does not exist but is referenced in the database!'.format(missing_file)

        for unused_file in unused_files[size]:
            shutil.move(unused_file, os.path.join(unused_dir, size))

if __name__ == '__main__':
    main()
