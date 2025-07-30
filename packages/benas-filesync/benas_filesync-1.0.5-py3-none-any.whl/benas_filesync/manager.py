'''
@author: Benas Untulis
@description:
- FileSyncManager class for managing file synchronization between source, backup, and versioning directories.
'''

import os
import shutil
import logging
from datetime import datetime
import hashlib

class FileSyncManager:
    '''
    **Purpose:** 
    - A class to manage file synchronization between a source directory, a backup directory, and a versioning directory.
    This class provides methods to retrieve .txt files, compute file hashes, check if files should be synchronized,
    and perform the synchronization process.

    **Attributes:**
    - ``source (str)``: Path to the source directory containing .txt files.
    - ``backup (str)``: Path to the backup directory where files will be copied.
    - ``versioning (str)``: Path to the versioning directory where old versions will be stored.
    - ``dry_run (bool)``: If True, preview actions without making changes.
    - ``modified_within (int)``: If specified, only sync files modified within the last N minutes.
    - ``logger (logging.Logger)``: Logger instance for logging actions and errors.

    **Example:**
    ```python
    >>> manager = FileSyncManager('/path/to/source', '/path/to/backup', '/path/to/versioning', dry_run=True, modified_within=60)
    >>> manager.sync()
    ```

    Example Output:
    - logging: Copying new file: example.txt
    - logging: Versioning: example.txt → example_20231001T123456.txt
    - logging: Skipped (unchanged): unchanged_file.txt

    ```python
    >>> print(manager.get_txt_files())
    ```
    Example Output:
    - ['file1.txt', 'file2.txt', 'file3.txt']

    ```python
    >>> print(manager.hash_file('/path/to/file.txt'))
    ```
    Example Output:
    - 'abc123def456...'

    ```python
    >>> print(manager.should_sync('/path/to/source/file.txt', '/path/to/backup/file.txt'))
    ```
    Example Output:
    - ``True``  # If the files differ or backup does not exist
    - ``False`` # If the files are identical
    '''

    def __init__(self, source, backup, versioning, dry_run=False, modified_within=None):
        '''
        **Purpose:** 
        - Initialize the FileSyncManager with source, backup, and versioning directories.

        **Args:**
        - ``source (str)``: Path to the source directory containing .txt files.
        - ``backup (str)``: Path to the backup directory where files will be copied.
        - ``versioning (str)``: Path to the versioning directory where old versions will be stored.
        - ``dry_run (bool)``: If True, preview actions without making changes.
        - ``modified_within (int)``: If specified, only sync files modified within the last N minutes.
        '''

        self.source = source
        self.backup = backup
        self.versioning = versioning
        self.dry_run = dry_run
        self.modified_within = modified_within
        self.logger = logging.getLogger(__name__)

    def get_txt_files(self):
        '''
        **Purpose:** 
        - Retrieve all .txt files from the specified directory.

        **Args:**
        - ``self``: Instance of the FileSyncManager class.
            
            - **Used Parameters:**
                - The following parameters can be set when creating an instance of the FileSyncManager class:
                
                - ``source (str)``: The directory path to search for .txt files.

        **Returns:**
        - ``list``: A list of .txt filenames in the specified directory.
        
        **Example:**
        ```python
        >>> get_txt_files('/path/to/directory')
        ```
        Example Output:
        - ['file1.txt', 'file2.txt']

        **Raises:**
         - ``FileNotFoundError``: If the specified path does not exist.
        - ``ValueError``: If the specified path is not a directory.
        - ``RuntimeError``: If there is an error reading the directory.
        '''

        try:
            if not os.path.isdir(self.source):
                raise ValueError(f"Provided source path is not a directory: {self.source}")
            return [f for f in os.listdir(self.source)
                    if f.endswith('.txt') and os.path.isfile(os.path.join(self.source, f))]
        except Exception as e:
            raise RuntimeError(f"Error reading .txt files from {self.source}: {e}")


    @staticmethod
    def hash_file(filepath):
        '''
        **Purpose:** 
        - Compute the SHA-256 hash of a file to determine if it has changed.

        **Args:**
        - ``self``: Instance of the FileSyncManager class.
        - ``filepath (str)``: The path to the file to be hashed.

        **Returns:**
         - ``str``: The SHA-256 hash of the file as a hexadecimal string.

        **Example:**
        ```python
        >>> hash_file('/path/to/file.txt')
        ```
        Example Output:
        - '3a1f4b2c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8a9b0c1d2'
        
        **Raises:**
        - ``FileNotFoundError``: If the specified file does not exist.
        - ``ValueError``: If the specified path is not a file.
        - ``RuntimeError``: If there is an error reading the file.
        '''

        try:
            if not os.path.isfile(filepath):
                raise ValueError(f"Path is not a file: {filepath}")
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                hasher.update(f.read())
            return hasher.hexdigest()
        except Exception as e:
            raise RuntimeError(f"Error hashing file {filepath}: {e}")


    def should_sync(self, source_path, backup_path):
        '''
        **Purpose:** 
        - Determine if a file should be synchronized between source and backup locations.

        **Args:**
        - ``self``: Instance of the FileSyncManager class.
        - ``source_path (str)``: The path to the source file.
        - ``backup_path (str)``: The path to the backup file.

        **Returns:**
        - ``bool``: True if the file should be synchronized, False otherwise.

        **Example:**
        ```python
        >>> should_sync('/path/to/source/file.txt', '/path/to/backup/file.txt')
        ```
        Example Output:
        - ``True``  # If the files differ or backup does not exist
        - ``False`` # If the files are identical
                
        **Raises:**
            - ``FileNotFoundError``: If the source file does not exist.
            - ``ValueError``: If the source or backup path is not a file.
            - ``RuntimeError``: If there is an error comparing the files.
        '''

        try:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source file not found: {source_path}")
            if not os.path.isfile(source_path):
                raise ValueError(f"Source path is not a file: {source_path}")
            if not os.path.exists(backup_path):
                return True
            return self.hash_file(source_path) != self.hash_file(backup_path)
        except Exception as e:
            raise RuntimeError(f"Error comparing files:\n  {source_path}\n  {backup_path}\nDetails: {e}")

    def sync(self):
        '''
        **Purpose:** 
        - Synchronize .txt files from the source directory to the backup directory and manage versioning.

        **Args:**
        - ``self``: Instance of the FileSyncManager class.

            - **Used Parameters:**
                - The following parameters can be set when creating an instance of the FileSyncManager class:

                - ``source (str)``: Path to the source directory containing .txt files.
                - ``backup (str)``: Path to the backup directory where files will be copied.
                - ``versioning (str)``: Path to the versioning directory where old versions will be stored.
                - ``dry_run (bool)``: If True, preview actions without making changes.
                - ``modified_within (int)``: If specified, only sync files modified within the last N minutes.

       **Returns:**
        - ``None``

        **Example:**
        ```python
        >>> sync_files('/path/to/source', '/path/to/backup', '/path/to/versioning', dry_run=True, modified_within=60)
        ```
        Example Output:
        - ``logging``: Copying new file: example.txt
        - ``logging``: Versioning: example.txt → example_20231001T123456.txt
        - ``logging``: Skipped (unchanged): unchanged_file.txt

        **Raises:**
        - ``RuntimeError``: If there are issues with file operations (e.g., copying, moving, hashing).
        - ``PermissionError``: If there are insufficient permissions to read/write files.
        - ``FileNotFoundError``: If the source directory does not exist.
        - ``ValueError``: If the source or backup path is not a directory.
        - ``OSError``: If there are issues with file operations (e.g., permission denied, disk full).
        '''

        try:
            os.makedirs(self.backup, exist_ok=True)
            os.makedirs(self.versioning, exist_ok=True)

            for filename in self.get_txt_files():
                source_path = os.path.join(self.source, filename)
                backup_path = os.path.join(self.backup, filename)

                if self.modified_within:
                    try:
                        mtime = os.path.getmtime(source_path)
                    except Exception as e:
                        raise RuntimeError(f"Error getting modification time for {source_path}: {e}")
                    minutes_ago = (datetime.now().timestamp() - mtime) / 60
                    if minutes_ago > self.modified_within:
                        continue

                if not os.path.exists(backup_path):
                    self.logger.info(f"Copying new file: {filename}")
                    if not self.dry_run:
                        try:
                            shutil.copy2(source_path, backup_path)
                        except Exception as e:
                            raise RuntimeError(f"Error copying file {source_path} to {backup_path}: {e}")
                elif self.should_sync(source_path, backup_path):
                    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
                    versioned_name = f"{os.path.splitext(filename)[0]}_{timestamp}.txt"
                    versioned_path = os.path.join(self.versioning, versioned_name)
                    self.logger.info(f"Versioning: {filename} → {versioned_name}")
                    if not self.dry_run:
                        try:
                            shutil.move(backup_path, versioned_path)
                            shutil.copy2(source_path, backup_path)
                        except Exception as e:
                            raise RuntimeError(f"Error during versioning of {filename}: {e}")
                else:
                    self.logger.info(f"Skipped (unchanged): {filename}")
        except Exception as e:
            raise RuntimeError(f"Synchronization failed: {e}")