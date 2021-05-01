import datetime
import pickle
from collections import namedtuple
from typing import List

Log = namedtuple('Log', ['name', 'time', 'size'])
Log.__doc__ = '''\
Log from compiling an image.

- name (str): Name of the compiled file.
- time (float): Time it took to compile the file.
- size (int): Size of the compiled file (in bytes).'''

def write_works(path:str, logs:List[Log], src_works:List[str] = []):
    """Write a works file enumerating the works in a series.

    Args:
        path (str): Path to write the file to.
        logs (List[Log]): List of logs from compiling generated works.
        src_works (List[str]): List of files which are not generated.
    """
    works = src_works + [i.name for i in logs]
    with open("%s/works.txt" % path, "w") as f:
        f.write("\n".join(works))

def write_log(path:str, logs:List[Log]):
    """Write the log file at the given path.

    Args:
        path (str): Path to write the log file to.
        logs (List[Log]): List of logs to include in the file.
    """
    names, times, sizes = zip(*logs)

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

    pickle_path = '/'.join(path.split('/')[:-1]) + '/log.pickle'
    with open(pickle_path, 'wb') as handle:
        pickle.dump(logs, handle, protocol=pickle.HIGHEST_PROTOCOL)


def collapse_log(name:str, logs:List[Log]) -> Log:
    """Collapse the list of logs into a single log with the given name.

    Args:
        name (str): Name of the collapsed log.
        logs (List[Log]): List of logs to be collapsed.

    Returns:
        Log: Collapsed log.
    """
    time = sum(log.time for log in logs)
    size = sum(log.size for log in logs)
    return Log(name=name, time=time, size=size)
