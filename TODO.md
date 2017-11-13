# TODO

- features:
  - [x] total time
  - [x] remove events from not interesting tables
    - [ ] save to new file - copy wanted events to a new db (https://stackoverflow.com/questions/30338054/sqlite3-python-attach-database-copy-table-schema)
  - [x] slice events from a time range
  - [ ] provide some summary information
    - [x] number of GPUs
    - [ ] date
    - [x] stats about events
    - [x] compute utilization
    - [ ] info about memcpy (overlap with compute)
- more nice to have features:
  - [ ] find periodic batches and segment them
    - [ ] compute a stats per batch
- other stuff
  - [x] setup.py
  - [x] command-line interface
  - [ ] object interface
