import argparse
from backend import GodOfConsole

god = GodOfConsole()
parser = argparse.ArgumentParser('Simple file manager')

subparser = parser.add_subparsers(dest='command', required=True)

#copy
parser_copy = subparser.add_parser('copy', help='Copy file in workdirectory')
parser_copy.add_argument('path', type=str, help='absolute path to file or filename in workdirectory')
parser_copy.set_defaults(func=god.copy_file)

#delete
parser_delete = subparser.add_parser('delete', help='Delete file or all files in directory')
parser_delete.add_argument('path', type=str, help='file value')
parser_delete.set_defaults(func=god.delete_file_or_dir)

#filecount_in_dir
parser_filecount_in_dir = subparser.add_parser('filecount_in_dir', help='Return count files in directory')
parser_filecount_in_dir.add_argument('path', type=str, help='absolute path or dirname in workdirectory')
parser_filecount_in_dir.set_defaults(func=god.filecount_in_dir)

#find_files
parser_find_files = subparser.add_parser('find_files', help='Find files in directory with mask')
parser_find_files.add_argument('path', type=str, help='file value')
parser_find_files.add_argument('mask', type=str, help='file value')
parser_find_files.set_defaults(func=god.find_files)

#rename_file
parser_rename_file = subparser.add_parser('rename_file', help='Renaming a file with the date the file was created')
parser_rename_file.add_argument('path', type=str, help='file value')
parser_rename_file.set_defaults(func=god.rename_file)

#rename_files_in_dir
parser_rename_files_in_dir = subparser.add_parser('rename_files_in_dir', help='Renaming a files in dir with the date the file was created')
parser_rename_files_in_dir.add_argument('path', type=str, help='file value')
parser_rename_files_in_dir.set_defaults(func=god.rename_files_in_dir)


args = parser.parse_args()

args.func(args.path)