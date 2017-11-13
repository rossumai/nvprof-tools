# NVIDIA Profier (nvprof) utilities

import sqlite3
import sys

table_prefix = 'CUPTI_ACTIVITY_KIND_'

def total_time(conn, table='CUPTI_ACTIVITY_KIND_MEMCPY'):
    c = conn.cursor()
    c.execute('SELECT (1.0 * MAX(end) - 1.0 * MIN(start)) * 1e-9 FROM {}'.format(table))
    total_time = c.fetchone()[0]
    print('Total time: %.03f sec' % total_time)

def list_tables(conn):
    c = conn.cursor()
    c.execute('select name from sqlite_master where type="table" and name like "CUPTI%" order by name')
    return [row[0] for row in c.fetchall()]

def table_sizes(conn):
    table_sizes = {}
    c = conn.cursor()
    for table in list_tables(conn):
        c.execute('select count(*) from %s' % table)
        table_sizes[table] = c.fetchone()[0]
    return table_sizes

def total_event_count(conn):
    ts = table_sizes(conn)
    return sum(ts.values())

def biggest_tables(conn):
    ts = table_sizes(conn)
    return sorted([(n,s) for (n,s) in ts.items() if s > 0],
        key=lambda item: item[1], reverse=True)

def print_info(conn):
    total_time(conn)
    ts = biggest_tables(conn)
    print('Total number of events:', sum(s for (n, s) in ts))
    print('Events by table:')
    for (name, size) in ts:
        print(name, ':', size)

def truncate_tables(conn, tables):
    c = conn.cursor()
    for table in tables:
        c.execute('DELETE FROM %s' % table)
    c.execute('VACUUM')
    conn.commit()

def delete_unnecessary_events(conn):
    tables = ['%s%s' % (table_prefix, table) for table in ['RUNTIME', 'DRIVER']]
    truncate_tables(conn, tables)

def with_conn(db_file, func):
    conn = sqlite3.connect(db_file)
    with conn:
        func(conn)
