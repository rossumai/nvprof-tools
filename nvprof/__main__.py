import argparse
import sqlite3

import nvprof

def cmd_info(db_file):
    nvprof.with_conn(db_file, nvprof.print_info)

def cmd_truncate(db_file):
    nvprof.with_conn(db_file, nvprof.delete_unnecessary_events)

def parse_args():
    parser = argparse.ArgumentParser(description='NVIDIA Profiler tools')
    subparsers = parser.add_subparsers(dest='command')
    parser_info = subparsers.add_parser('info')
    parser_info.add_argument('db_file')
    parser_truncate = subparsers.add_parser('truncate')
    parser_truncate.add_argument('db_file')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == 'info':
        cmd_info(args.db_file)
    if args.command == 'truncate':
        cmd_truncate(args.db_file)

if __name__ == '__main__':
    main()
