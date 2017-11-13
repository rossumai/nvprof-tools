# NVIDIA Profier (nvprof) utilities

import sys

import sqlite3

table_prefix = 'CUPTI_ACTIVITY_KIND_'

def total_time(conn, table='CUPTI_ACTIVITY_KIND_MEMCPY'):
    c = conn.cursor()
    c.execute('SELECT (1.0 * MAX(end) - 1.0 * MIN(start)) * 1e-9 FROM {}'.format(table))
    total_time = c.fetchone()[0]
    print('total time: %.03f sec' % total_time)

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
    return sorted([(s, n) for (n, s) in ts.items() if s > 0], reverse=True)

def truncate_tables(conn, tables):
    c = conn.cursor()
    for table in ['RUNTIME', 'DRIVER']:
        c.execute('DELETE FROM %s%s' % table_prefix)
    c.execute('VACUUM')
    conn.commit()

def delete_unnecessary_events(conn):
    tables = ['%s%s' % (table, table_prefix) for table in ['RUNTIME', 'DRIVER']]
    truncate_tables(conn, tables)

if __name__ == '__main__':
    db_name = sys.argv[1]
    conn = sqlite3.connect(db_name)
    total_time(conn)
    conn.close()
