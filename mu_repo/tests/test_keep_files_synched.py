'''
Created on 20/05/2012

@author: Fabio Zadrozny
'''
from __future__ import with_statement

import os.path
import shutil

from mu_repo import keep_files_synched


def read(file2):
    with open(file2, 'r') as f:
        return f.read()


def test_keep_files_synched_struct():
    os.makedirs('.test_temp_dir')
    file1 = os.path.join('.test_temp_dir', 'f1')
    file2 = os.path.join('.test_temp_dir', 'f2')
    with open(file1, 'w') as f:
        f.write('initial')
    shutil.copyfile(file1, file2)
    s = keep_files_synched._KeepInSyncStruct(file1, file2)
    assert 'initial' == read(file2)

    with open(file1, 'w') as f:
        f.write('second')
    s.Sync()
    assert 'second' == read(file2)

    with open(file2, 'w') as f:
        f.write('third')
    s.Sync()
    assert 'third' == read(file1)


def test_keep_files_synched():
    os.makedirs('.test_temp_dir')
    file1 = os.path.join('.test_temp_dir', 'f1')
    file2 = os.path.join('.test_temp_dir', 'f2')
    with open(file1, 'w') as f:
        f.write('initial')
    shutil.copyfile(file1, file2)
    keep_files_synched.KeepInSync(file1, file2)

    assert 'initial' == read(file2)
    with open(file1, 'w') as f:
        f.write('second')
    keep_files_synched.StopSyncs()
    assert 'second' == read(file2)


def test_keep_files_synched_dir():
    os.makedirs('.test_temp_dir/d1')
    os.makedirs('.test_temp_dir/d2')
    file1 = os.path.join('.test_temp_dir', 'd1', 'f1')
    file2 = os.path.join('.test_temp_dir', 'd2', 'f1')
    with open(file1, 'w') as f:
        f.write('initial')
    shutil.copyfile(file1, file2)
    keep_files_synched.KeepInSync('.test_temp_dir/d1', '.test_temp_dir/d2')  # Keep dir in sync

    assert 'initial' == read(file2)
    with open(file1, 'w') as f:
        f.write('second')
    keep_files_synched.StopSyncs()
    assert 'second' == read(file2)

