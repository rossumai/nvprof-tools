# nvprof-tools - Python tools for NVIDIA Profiler

Tools to help working with nvprof SQLite files, specifically for profiling
scripts to train deep learning models. The files can be big and thus slow to scp and work with in NVVP. This tool is aimed in extracting the small bits of important information and make profiling in NVVP faster.

You can remove a big number of unimportant events and take a small time slice, so that you can shrink the sqlite database a few MBs.

- Author: Bohumír Zámečník <bohumir.zamecnik@gmail.com>, [Rossum](https://rossum.ai)
- License: MIT

![sliced nvprof in NVVP](https://cdn.pbrd.co/images/GTsUg7h.png)

## Installing

Install package `nvprof` - for just using it:

```
$ pip install nvprof
```

...or for development:

```
$ pip install -e .
```

## Features

```
$ nvprof_tools --help
usage: nvprof_tools [-h] {info,truncate,slice} ...

NVIDIA Profiler tools

positional arguments:
  {info,truncate,slice}

optional arguments:
  -h, --help            show this help message and exit
```

```
$ nvprof_tools slice --help
usage: nvprof_tools slice [-h] [-s START] [-e END] db_file

positional arguments:
  db_file

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        start time (sec)
  -e END, --end END     end time (sec)
```

### Summary about the file

It can show:

- total time (can be used to decide which time slice to take in nvvp)
- number of events in the tables sorted from highest
- compute utilization percentage
- number of GPUs

```
$ nvprof_tools info foo.sqlite
Number of GPUs: 1
Compute utilization: 10.07 %
Total time: 6.659 sec
Total number of events: 516874
Events by table:
CUPTI_ACTIVITY_KIND_RUNTIME : 348080
CUPTI_ACTIVITY_KIND_CONCURRENT_KERNEL : 63792
CUPTI_ACTIVITY_KIND_DRIVER : 48279
CUPTI_ACTIVITY_KIND_SYNCHRONIZATION : 19741
CUPTI_ACTIVITY_KIND_CUDA_EVENT : 17860
CUPTI_ACTIVITY_KIND_MEMCPY : 15974
CUPTI_ACTIVITY_KIND_MEMSET : 2816
CUPTI_ACTIVITY_KIND_OVERHEAD : 309
CUPTI_ACTIVITY_KIND_STREAM : 12
CUPTI_ACTIVITY_KIND_DEVICE_ATTRIBUTE : 8
CUPTI_ACTIVITY_KIND_NAME : 1
CUPTI_ACTIVITY_KIND_CONTEXT : 1
CUPTI_ACTIVITY_KIND_DEVICE : 1
```

In case of multiple GPUs compute utilization is calculated for each device:

```
Number of GPUs: 4
Compute utilization (mean): 43.04 %
  GPU 0: 42.86 %
  GPU 1: 42.34 %
  GPU 2: 43.42 %
  GPU 3: 43.55 %
Total time: 35.041 sec
Total number of events: 5670557
```

### Remove unnecessary events

Typically 80% of the events are runtime/driver CUDA calls, which are not essential for profiling deep learning scripts. Let's remove them.

NOTE: It will overwrite the input file.

```
$ nvprof_tools truncate foo.sqlite
```

Eg. we shrinked a database from 29 MB to 8 MB.

### Slice only a small time range

```
# keep only events between 5 and 6 seconds
$ nvprof_tools slice foo.sqlite -s 5.0 -e 6.0
```

### More information

[More information](docs/info.md)
