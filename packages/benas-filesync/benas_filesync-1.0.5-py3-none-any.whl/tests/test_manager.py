'''
@author: Benas Untulis
@description:
- Unit tests for the FileSyncManager class, covering various scenarios such as copying new files,
    skipping unchanged files, versioning on changes, and filtering by modification time.
'''

import unittest
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from benas_filesync.manager import FileSyncManager


class TestFileSyncManager(unittest.TestCase):
    '''
    Test suite for ``FileSyncManager`` class.
    '''

    def setUp(self):
        '''
        **Purpose:**
        - Setup temporary directories for source, backup, and versioning before each test.
        
        **Functionality:**
        - Creates temporary directories and initializes a FileSyncManager instance with dry_run=False.
        '''
        self.source_dir = tempfile.mkdtemp()
        self.backup_dir = tempfile.mkdtemp()
        self.versioning_dir = tempfile.mkdtemp()

        self.manager = FileSyncManager(
            source=self.source_dir,
            backup=self.backup_dir,
            versioning=self.versioning_dir,
            dry_run=False,
            modified_within=None
        )

    def tearDown(self):
        '''
        **Purpose:** 
        - Cleanup temporary directories after each test.

        **Functionality:**
        - Removes all temporary directories created in setUp.
        '''
        shutil.rmtree(self.source_dir)
        shutil.rmtree(self.backup_dir)
        shutil.rmtree(self.versioning_dir)

    def create_file(self, dir_path, filename, content):
        '''
        **Purpose:** 
        - Helper method to create a file with specified content.

        **Args:**
        - ``dir_path (str)``: Directory path to create the file in.
        - ``filename (str)``: Name of the file to create.
        - ``content (str)``: Text content to write into the file.

        **Returns:**
        - ``str``: Full path to the created file.
        '''
        path = os.path.join(dir_path, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def test_copy_new_file(self):
        '''
        **Purpose:** 
        - Test that a new file in source is copied to backup if it doesn't exist there.

        **Functionality steps:**
        - Create a new file in the source directory.
        - Run sync.
        - Assert the file exists in backup.
        '''
        self.create_file(self.source_dir, 'test1.txt', 'hello world')

        self.manager.sync()

        backup_files = os.listdir(self.backup_dir)
        self.assertIn('test1.txt', backup_files)

    def test_skip_unchanged_file(self):
        '''
        **Purpose:** 
        - Test that unchanged files are skipped (not copied or versioned).

        **Functionality steps:**
        - Create identical files in source and backup.
        - Run sync.
        - Assert file remains in backup.
        - Assert versioning directory is empty.
        '''
        self.create_file(self.source_dir, 'test2.txt', 'same content')
        self.create_file(self.backup_dir, 'test2.txt', 'same content')

        self.manager.sync()

        backup_files = os.listdir(self.backup_dir)
        self.assertIn('test2.txt', backup_files)

        versioning_files = os.listdir(self.versioning_dir)
        self.assertEqual(len(versioning_files), 0)

    def test_versioning_on_change(self):
        '''
        **Purpose:** 
        - Test that when a file is changed, the old backup is moved to versioning and source is copied to backup.

        **Functionality steps:**
        - Create a file in source with new content.
        - Create a file in backup with old content.
        - Run sync.
        - Assert backup file updated with new content.
        - Assert versioning contains the old version with timestamp.
        '''
        self.create_file(self.source_dir, 'test3.txt', 'new content')
        self.create_file(self.backup_dir, 'test3.txt', 'old content')

        self.manager.sync()

        with open(os.path.join(self.backup_dir, 'test3.txt'), 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, 'new content')

        versioning_files = os.listdir(self.versioning_dir)
        self.assertEqual(len(versioning_files), 1)
        self.assertTrue(versioning_files[0].startswith('test3_') and versioning_files[0].endswith('.txt'))

    def test_modified_within_filter(self):
        '''
        **Purpose:** 
        - Test that files modified outside the 'modified_within' window are skipped.

        **Functionality steps:**
        - Create a file in source with an old modification time.
        - Set modified_within to less than the file's age.
        - Run sync.
        - Assert file is not copied to backup.
        '''
        file_path = self.create_file(self.source_dir, 'test4.txt', 'content')
        old_time = datetime.now() - timedelta(minutes=10)
        os.utime(file_path, (old_time.timestamp(), old_time.timestamp()))

        self.manager.modified_within = 5

        self.manager.sync()

        backup_files = os.listdir(self.backup_dir)
        self.assertNotIn('test4.txt', backup_files)


if __name__ == '__main__':
    unittest.main()
