import re

INT_PATTERN = re.compile(r"^-?\d+$")

FIELD_INDENT = "<25"
VALUE_INDENT = "<25"

proc_pid_stat_fields = [
    "pid",                      # 1
    "comm",                     # 2
    "state",                    # 3
    "ppid",                     # 4
    "pgrp",                     # 5
    "session",                  # 6
    "tty_nr",                   # 7
    "tpgid",                    # 8
    "flags",                    # 9
    "minflt",                   # 10
    "cminflt",                  # 11
    "majflt",                   # 12
    "cmajflt",                  # 13
    "utime",                    # 14
    "stime",                    # 15
    "cutime",                   # 16
    "cstime",                   # 17
    "priority",                 # 18
    "nice",                     # 19
    "num_threads",              # 20
    "itrealvalue",              # 21 (obsolete, always 0)
    "starttime",                # 22
    "vsize",                    # 23
    "rss",                      # 24
    "rsslim",                   # 25
    "startcode",                # 26
    "endcode",                  # 27
    "startstack",               # 28
    "kstkesp",                  # 29
    "kstkeip",                  # 30
    "signal",                   # 31
    "blocked",                  # 32
    "sigignore",                # 33
    "sigcatch",                 # 34
    "wchan",                    # 35
    "nswap",                    # 36 (not maintained)
    "cnswap",                   # 37 (not maintained)
    "exit_signal",              # 38
    "processor",                # 39
    "rt_priority",              # 40
    "policy",                   # 41
    "delayacct_blkio_ticks",    # 42
    "guest_time",               # 43
    "cguest_time",              # 44
    "start_data",               # 45
    "end_data",                 # 46
    "start_brk",                # 47
    "arg_start",                # 48
    "arg_end",                  # 49
    "env_start",                # 50
    "env_end",                  # 51
    "exit_code"                 # 52
]