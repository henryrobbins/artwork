from typing import List, Dict

def write_log(path:str, log:List[Dict]):
    """Write the log file at the given path.

    Args:
        path (str): Path where the log file should be written.
        log (List[Dict]): Dictionary for each item in the log.
    """
    f = open(path, 'w')
    f.write('%s | %s | %s \n' % ('file_name'.ljust(25),
                                'time'.ljust(5),
                                'size'.ljust(10)))
    f.write('-'*45 + '\n')
    for entry in log:
        f.write('%s | %s | %s \n' % (entry['name'].ljust(25),
                                    entry['t'].ljust(5),
                                    entry['size'].ljust(10)))
    f.close()