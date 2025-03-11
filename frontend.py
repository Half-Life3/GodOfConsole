import argparse
from backend import GodOfConsole

parser = argparse.ArgumentParser('Simple file manager. Require to use abs path')

subparser = parser.add_subparsers(dest='command', required=True)

#copy
parser_copy = subparser.add_parser('copy', help='Copy file in workdirectory')
parser_copy.add_argument('userdata', type=str, help='absolute path to file or local filename.format')
parser_copy.add_argument('--destination', type=str, help='destination path for files copy or local', default=None, required=False)
parser_copy.set_defaults(func=GodOfConsole.copy_file)

#delete
parser_delete = subparser.add_parser('delete', help='Delete file or all files in directory')
parser_delete.add_argument('userdata', type=str, help='file name or directory')
parser_delete.set_defaults(func=GodOfConsole.delete_file_or_dir)

#filecount_in_dir
parser_filecount_in_dir = subparser.add_parser('filecount', help='Return count files in directory')
parser_filecount_in_dir.add_argument('path', type=str, help='absolute path or dirname in workdirectory')
parser_filecount_in_dir.set_defaults(func=GodOfConsole.filecount_in_dir)

#find_files
parser_find_files = subparser.add_parser('find', help='Find files in directory with mask')
parser_find_files.add_argument('path', type=str, help='abs file path')
parser_find_files.add_argument('mask', type=str, help='mask value')
parser_find_files.set_defaults(func=GodOfConsole.find_files)

#rename_file
parser_rename_file = subparser.add_parser('rename', help='Renaming a file with the date the file was created')
parser_rename_file.add_argument('path', type=str, help='abs file path')
parser_rename_file.add_argument('--recursive', help='recursive flag', type=str, required=False, default=False)
parser_rename_file.set_defaults(func=GodOfConsole.rename)

#analyse_workdir
parser_rename_file = subparser.add_parser('analyse', help='Analysis of all subfolders and files')
parser_rename_file.add_argument('path', type=str, help='abs path')
parser_rename_file.add_argument('size_limit', help='Size in bytes for filtering large files', type=int)
parser_rename_file.set_defaults(func=GodOfConsole.analyse_workdir)

args = parser.parse_args()

if args.command == 'copy':
    args.func(args.userdata, args.destination)
if args.command == 'delete':
    args.func(args.userdata)
if args.command == 'filecount':
    args.func(args.path)
if args.command == 'find':
    args.func(args.path, args.mask)
if args.command == 'rename':
    args.func(args.path, args.recursive)
if args.command == 'analyse':
    args.func(args.path, args.size_limit)
