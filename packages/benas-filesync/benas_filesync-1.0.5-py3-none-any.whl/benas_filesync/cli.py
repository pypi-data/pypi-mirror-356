'''
@author: Benas Untulis
@description:
- Command-line interface for the file synchronization script.
'''

import argparse

def parse_args():
    '''
    **Purpose:**
    - Parse command-line arguments for the file synchronization script.

    **Returns:**
    - ``argparse.Namespace``: The parsed command-line arguments.

    **Example:**
    ```python
    >>> args = parse_args()
    >>> print(args.source)
    ```
    Example Output:
    - /path/to/source

    ```python
    >>> print(args.backup)
    ```
    Example Output:            
    - /path/to/backup

    ```python
    >>> print(args.versioning)
    ```
    Example Output:
    - /path/to/versioning
    
    **Raises:**
    - ``SystemExit``: If the required arguments are not provided or if the arguments are invalid
    '''

    parser = argparse.ArgumentParser(description="Synchronize .txt files with backup and versioning.")
    parser.add_argument('--source', required=True, help='Path to the source folder (Folder A)')
    parser.add_argument('--backup', required=True, help='Path to the backup folder (Folder B)')
    parser.add_argument('--versioning', required=True, help='Path to the versioning folder (Folder C)')
    parser.add_argument('--dry-run', action='store_true', help='Preview actions without making changes')
    parser.add_argument('--modified-within', type=int, help='Only sync files modified in the last N minutes')
    parser.add_argument(
        '--log-type',
        choices=['none', 'console', 'file', 'both'],
        default='console',
        help='Logging output: none (no logging), console, file, or both'
    )
    parser.add_argument(
        '--log-file',
        default='file_sync.log',
        help='Path to the log file (used if --log-type is file or both). Default: file_sync.log'
    )
    return parser.parse_args()