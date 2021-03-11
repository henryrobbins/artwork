import numpy as np

def read(file_name:str) -> np.ndarray:
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


def enlarge(M:np.ndarray, k:int) -> np.ndarray:
    """Enlarge the netpbm image M by the multiplier k.

    Args:
        M (np.ndarray): NumPy array representing a netpbm image.
        k (int): Multiplier by which to enlarge the image.

    Returns:
        np.ndarray: NumyPy array representing the enlarged image.
    """
    n,m = M.shape
    expanded_rows = np.zeros((n*k,m))
    for i in range(n*k):
        expanded_rows[i] = M[i // k]
    expanded = np.zeros((n*k, m*k))
    for j in range(m*k):
        expanded[:,j] = expanded_rows[:,j // k]
    return expanded.astype(int)


def change_gradient(M:np.ndarray, n_old:int, n_new:int) -> np.ndarray:
    """Change the max gradient value of the netpbm image M to n.

    Args:
        M (np.ndarray): NumPy array representing a netpbm image.
        n_old (int): Old max gradient value.
        n_new (int): New max gradient value.

    Returns:
        np.ndarray: NumyPy array representing the adjusted image.
    """
    return np.array(list(map(lambda x: x // int(n_old / n_new), M)))
