import argparse
import sqlite3

import nvprof

def cmd_info(db_file):
    nvprof.with_conn(db_file, nvprof.print_info)

def cmd_truncate(db_file):
    nvprof.with_conn(db_file, nvprof.delete_unnecessary_events)

def cmd_slice(db_file, start_sec, end_sec):
    def slice_events(conn):
        nvprof.slice_events(conn, int(start_sec * 1e9), int(end_sec * 1e9))
    nvprof.with_conn(db_file, slice_events)

def parse_args():
    parser = argparse.ArgumentParser(description='NVIDIA Profiler tools')
    subparsers = parser.add_subparsers(dest='command')

    parser_info = subparsers.add_parser('info')
    parser_info.add_argument('db_file')

    parser_truncate = subparsers.add_parser('truncate')
    parser_truncate.add_argument('db_file')

    parser_slice = subparsers.add_parser('slice')
    parser_slice.add_argument('db_file')
    parser_slice.add_argument('-s', '--start', help='start time (sec)', type=float)
    parser_slice.add_argument('-e', '--end', help='end time (sec)', type=float)

    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == 'info':
        cmd_info(args.db_file)
    if args.command == 'truncate':
        cmd_truncate(args.db_file)
    if args.command == 'slice':
        cmd_slice(args.db_file, args.start, args.end)

if __name__ == '__main__':
    main()
