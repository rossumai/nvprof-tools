# NVIDIA Profier (nvprof) utilities

import sqlite3
import sys

table_prefix = 'CUPTI_ACTIVITY_KIND_'
interval_tables = [
    'CDP_KERNEL',
    'CONCURRENT_KERNEL',
    'DRIVER',
    'KERNEL',
    'MEMCPY',
    'MEMCPY2',
    'MEMSET',
    'OPENACC_DATA',
    'OPENACC_LAUNCH',
    'OPENACC_OTHER',
    'OVERHEAD',
    'RUNTIME',
    'SYNCHRONIZATION',
    'UNIFIED_MEMORY_COUNTER']
unnecessary_tables = ['RUNTIME', 'DRIVER']

def tables_with_prefix(short_tables):
    return ['%s%s' % (table_prefix, table) for table in short_tables]

def time_range(conn):
    """
    Time range of events in nanoseconds.
    """
    # tables with start/end times
    tables = tables_with_prefix([
        t for t in interval_tables
        if t not in unnecessary_tables])

    times = []
    c = conn.cursor()
    for table in tables:
        c.execute('SELECT MIN(start), MAX(end) FROM {}'.format(table))
        start, end = c.fetchone()
        if start is not None and end is not None:
            times.append((start, end))
    if len(times) > 0:
        starts, ends = zip(*times)
        # times in nanoseconds
        start_ns, end_ns = min(starts), max(ends)
        return start_ns, end_ns
    else:
        return 0, 0

def total_time(conn):
    start_ns, end_ns = time_range(conn)
    total_time_sec = (end_ns - start_ns) * 1e-9
    return total_time_sec

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

def compute_utilization(conn):
    # TODO: do not count time in overlapping kernels twice
    # It would be better to compute utitlization on small intervals and then
    # aggregate with median. That would remove the effect of long initialization
    # times.
    c = conn.cursor()
    c.execute("SELECT deviceId, 100. * SUM(1.0 * end - 1.0 * start) / (MAX(end) - MIN(start)) FROM CUPTI_ACTIVITY_KIND_CONCURRENT_KERNEL GROUP BY deviceId")
    return dict(c.fetchall())

def gpu_count(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM CUPTI_ACTIVITY_KIND_DEVICE")
    return c.fetchone()[0]

def print_info(conn):
    print("Number of GPUs: %d" % gpu_count(conn))
    utilization_per_device = compute_utilization(conn)
    mean_utilization = sum(utilization_per_device.values()) / len(utilization_per_device)
    print("Compute utilization (mean): %0.2f %%" % mean_utilization)
    for dev, util in utilization_per_device.items():
        print('  GPU %d: %0.2f %%' % (dev, util))
    print('Total time: %.03f sec' % total_time(conn))
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
    tables = ['%s%s' % (table_prefix, table) for table in unnecessary_tables]
    truncate_tables(conn, tables)

def slice_events(conn, start_ns, end_ns):
    """
    Delete events outside the given range, keep events inside and overlapping.
    """
    base_time, _ = time_range(conn)
    # absolute time of the window
    abs_start_ns, abs_end_ns = base_time + start_ns, base_time + end_ns
    c = conn.cursor()
    for table in tables_with_prefix(interval_tables):
        c.execute('DELETE FROM {} WHERE end < {} OR start > {}'.format(table, abs_start_ns, abs_end_ns))
    c.execute('VACUUM')
    conn.commit()

def with_conn(db_file, func):
    conn = sqlite3.connect(db_file)
    with conn:
        func(conn)
