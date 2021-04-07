import os
import pickle
from log import write_log, collapse_log

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS = []

# =============== Python Works ===============

python_works = ['netpbm/template'
                'netpbm/dissolve',
                'netpbm/mod',
                'netpbm/drunk_walk',
                'netpbm/partition',
                'netpbm/clip',
                'netpbm/channel',
                'netpbm/resolution',
                'netpbm/compile']

for path in python_works:
    name = path.split('/')[-1]
    os.system("python %s/%s.py" % (path, name))
    with open('%s/%s/log.pickle' % (ROOT, path), 'rb') as handle:
        logs = pickle.load(handle)
    LOGS.append(collapse_log(path, logs))
    print('%s was compiled.' % path)

write_log('%s/%s' % (ROOT, 'compile.log'), LOGS)
