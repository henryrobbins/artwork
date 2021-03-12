import datetime
from collections import namedtuple
from typing import List, Dict

Log = namedtuple('Log', ['name', 'time', 'size'])
Log.__doc__ = '''\
Log from compiling an image.

- name (str): Name of the compiled file.
- time (float): Time it took to compile the file.
- size (int): Size of the compiled file (in bytes).'''


def write_log(path:str, log:List[Dict]):
    """Write the log file at the given path.

    Args:
        path (str): Path where the log file should be written.
        log (List[Dict]): Dictionary for each item in the log.
    """

    names, times, sizes = zip(*log)

    def size_string(size):
        s = size
        i = 0
        units = ['B','KB','MB','GB','TB']
        while s >= 1000:
            s = round(s / 1000)
            i += 1
        return '%d%s' % (s, units[i])

    times = ['%.3f' % time for time in times]
    sizes = [size_string(size) for size in sizes]

    # compute needed width for each field
    name_w = max(max(len(i) for i in names) + 1, len('file_name'))
    time_w = max(max(len(i) for i in times) + 1, len('time (s)'))
    size_w = max(max(len(i) for i in sizes) + 1, len('size'))

    f = open(path, 'w')
    f.write('%s\n' % str(datetime.datetime.now()))
    f.write('%s | %s | %s \n' % ('file_name'.ljust(name_w),
                                 'time (s)'.ljust(time_w),
                                 'size'.ljust(size_w)))
    f.write('-'*(name_w + time_w + size_w + 6) + '\n')
    for log in zip(names, times, sizes):
        f.write('%s | %s | %s \n' % (log[0].ljust(name_w),
                                     log[1].ljust(time_w),
                                     log[2].ljust(size_w)))
    f.close()