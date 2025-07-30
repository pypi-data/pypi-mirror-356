'''
@description: Entry point for the filesync package.
'''

from .manager import FileSyncManager
import benas_filesync.cli as cli
import logging

def setup_logging(log_type, log_file):
    if log_type == 'none':
        logging.disable(logging.CRITICAL)
        return

    handlers = []
    if log_type in ('console', 'both'):
        handlers.append(logging.StreamHandler())
    if log_type in ('file', 'both'):
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=handlers
    )

def main():
    '''
    **Purpose:** 
    - Main function to execute the file synchronization script.
    This function parses command-line arguments, sets up logging, and calls the `sync_files` function
    with the provided arguments. It handles exceptions and logs errors if the script fails.
    
    **Raises:**
    - ``SystemExit``: If the script encounters an error during execution.
    - ``ValueError``: If the provided paths are not valid directories.
    - ``RuntimeError``: If there are issues with file operations (e.g., copying, moving, hashing).
    - ``PermissionError``: If there are insufficient permissions to read/write files.
    '''

    args = cli.parse_args()

    setup_logging(args.log_type, args.log_file)

    try:
        if not all(os.path.isdir(p) for p in [args.source, args.backup, args.versioning]):
            raise ValueError("One or more provided paths are not valid directories.")

        syncer = FileSyncManager(
            source=args.source,
            backup=args.backup,
            versioning=args.versioning,
            dry_run=args.dry_run,
            modified_within=args.modified_within
        )
        syncer.sync()

    except Exception as e:
        logging.error(f"Script execution failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
