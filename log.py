import datetime
from typing import List, Dict


def write_log(path:str, log:List[Dict]):
    """Write the log file at the given path.

    Args:
        path (str): Path where the log file should be written.
        log (List[Dict]): Dictionary for each item in the log.
    """
    for l in log:
        s = l['size']
        i = 0
        units = ['B','KB','MB','GB','TB']
        while s >= 1000:
            s = round(s / 1000)
            i += 1
        l['size'] = '%d%s' % (s, units[i])

    # compute needed width for each field
    file_name_w = max(max(len(l['name']) for l in log) + 1, len('file_name'))
    time_w = max(max(len(l['t']) for l in log) + 1, len('time (s)'))
    size_w = max(max(len(l['size']) for l in log) + 1, len('size'))

    f = open(path, 'w')
    f.write('%s\n' % str(datetime.datetime.now()))
    f.write('%s | %s | %s \n' % ('file_name'.ljust(file_name_w),
                                'time (s)'.ljust(time_w),
                                'size'.ljust(size_w)))
    f.write('-'*(file_name_w + time_w + size_w + 6) + '\n')
    for entry in log:
        f.write('%s | %s | %s \n' % (entry['name'].ljust(file_name_w),
                                    entry['t'].ljust(time_w),
                                    entry['size'].ljust(size_w)))
    f.close()