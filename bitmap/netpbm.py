import numpy as np

def read(file_name:str):
    """Read the Netpbm file and return a NumPy matrix.

    Args:
        file_name (str): Name of the Netpbm file.

    Returns:
        np.ndarray: NumPy matrix representing the Netpbm file.
        int: width of the Netpbm file.
        int: height of the Netpbm file.
        int: maximum value of greys between black and white.
    """
    lines = open(file_name).readlines()
    assert lines[0][:-1] == 'P2'
    w,h = [int(i) for i in lines[1][:-1].split(' ')]
    max_val = int(lines[2][:-1])
    M = np.array([line.strip('\n ').split(' ') for line in lines[3:]])
    M = M.astype(int)
    assert (h,w) == M.shape
    return M, w, h, max_val


def write(file_name:str, M:np.ndarray, max_val:int):
    """Write the Netpbm file given the associated matrix of nunbers.

    Args:
        file_name (str): Name of the Netpbm file to be written.
        M (np.ndarray): NumPy array of integers.
    """
    f = open(file_name, "w")
    f.write('P2\n')
    h,w = M.shape
    f.write("%s %s\n" % (w, h))
    f.write("%s\n" % (max_val))
    f.write('\n'.join([' '.join(line) for line in M.astype(str).tolist()]))
    f.write('\n')
    f.close()


def enlarge(M, k):
    """Enlarge some NumPy array by the multiplier k.

    Args:
        M (np.ndarray): NumPy array of integers.
        k (int): Multiplier by which to enlarge the array M.shape

    Returns:
        np.ndarray: The NumyPy array M enlarged by the multiplier k."""
    n,m = M.shape
    expanded_rows = np.zeros((n*k,m))
    for i in range(n*k):
        expanded_rows[i] = M[i // k]
    expanded = np.zeros((n*k, m*k))
    for j in range(m*k):
        expanded[:,j] = expanded_rows[:,j // k]
    return expanded.astype(int)
