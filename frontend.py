import os
import sys
import argparse
from backend import copy, delete

parser = argparse.ArgumentParser('Simple file manager')

subparser = parser.add_subparsers(dest='command', required=True)

parser_add = subparser.add_parser('copy', help='Copy files')
parser_add.add_argument('file_name', type=str, help='file value')
parser_add.add_argument('file_format', type=str, help='file format')
parser_add.set_defaults(func=copy)

parser_delete = subparser.add_parser('delete', help='Delete files')
parser_delete.add_argument('file_name', type=str, help='file value')
parser_delete.add_argument('file_format', type=str, help='file format')
parser_delete.set_defaults(func=delete)


args = parser.parse_args()
#print(args)
args.func(args.file_name, args.file_format)


