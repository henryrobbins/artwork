import numpy as np
from typing import Callable

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)


def RGB_to_XYZ(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in RGB color space to XYZ color space.

    Args:
        pixels (np.ndarray): Pixels in the RGB color space.

    Returns:
        np.ndarray: Pixel matrix in the XYZ color space.
    """
    # See the following link for the implemented conversion
    # https://en.wikipedia.org/wiki/CIE_1931_color_space
    b = 0.17697
    A = np.array([[0.49, 0.31, 0.2],
                  [0.17697, 0.81240, 0.01063],
                  [0, 0.01, 0.99]])
    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(lambda x: np.matmul(A,x)/b, 1, p)
    return np.reshape(p, (n,m,k))


def XYZ_to_RGB(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in XYZ color space to RGB color space.

    Args:
        pixels (np.ndarray): Pixels in the XYZ color space.

    Returns:
        np.ndarray: Pixel matrix in the RGB color space.
    """
    # See the following link for the implemented conversion
    # https://en.wikipedia.org/wiki/CIE_1931_color_space
    A = np.array([[0.41847, -0.15866, -0.082835],
                  [-0.091169, 0.25243, 0.015708],
                  [0.00092090, -0.0025498, 0.17860]])
    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(lambda x: np.matmul(A,x), 1, p)
    return np.reshape(p, (n,m,k))


def RGB_to_YUV(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in RGB color space to YUV color space.

    Args:
        pixels (np.ndarray): Pixels in the RGB color space.

    Returns:
        np.ndarray: Pixel matrix in the YUV color space.
    """
    # See the following link for the implemented conversion
    # https://en.wikipedia.org/wiki/YUV
    W_R, W_G, W_B = 0.299, 0.587, 0.114
    U_max = 0.436
    V_max = 0.615

    def to_YUV(x):
        R, G, B = x
        Y = W_R*R + W_G*G + W_B*B
        U = U_max*((B-Y)/(1 - W_B))
        V = V_max*((R-Y)/(1 - W_R))
        return np.array([Y,U,V])

    pixels = normalize(pixels, 'RGB', True)
    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(to_YUV, 1, p)
    return np.reshape(p, (n,m,k))


def YUV_to_RGB(pixels:np.ndarray) -> np.ndarray:
    """Convert a pixel matrix in YUV color space to RGB color space.

    Args:
        pixels (np.ndarray): Pixels in the YUV color space.

    Returns:
        np.ndarray: Pixel matrix in the RGB color space.
    """
    # See the following link for the implemented conversion
    # https://en.wikipedia.org/wiki/YUV
    W_R, W_G, W_B = 0.299, 0.587, 0.114
    U_max = 0.436
    V_max = 0.615

    def to_RGB(x):
        Y, U, V = x
        R = Y + V*((1-W_R)/V_max)
        G = Y - U*((W_B*(1-W_B))/(U_max*W_G)) - V*((W_R*(1-W_R))/(V_max*W_G))
        B = Y + U*((1-W_B)/U_max)
        return np.array([R,G,B])

    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(to_RGB, 1, p)
    p = np.reshape(p, (n,m,k))
    return normalize(p, 'RGB', False)


def XYZ_to_Lab(pixels:np.ndarray,
               standard_illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in XYZ color space to Lab color space.

    Args:
        pixels (np.ndarray): Pixels in the XYZ color space.
        standard_illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the Lab color space.
    """
    # See the following link for the implemented conversion
    # https://en.wikipedia.org/wiki/CIELAB_color_space
    X_n, Y_n, Z_n = {'D50':(96.4212, 100.0, 82.5188),
                     'D65':(95.0489, 100.0, 108.8840)}[standard_illuminant]
    delta = 6 / 29

    def f(t):
        return t**(1/3) if t > delta**3 else (t/(3*delta**2)) + (4/29)

    def to_Lab(x):
        X, Y, Z = x
        L = 116*f(Y/Y_n) - 16
        a = 500*(f(X/X_n) - f(Y/Y_n))
        b = 200*(f(Y/Y_n) - f(Z/Z_n))
        return np.array([L,a,b])

    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(to_Lab, 1, p)
    return np.reshape(p, (n,m,k))


def Lab_to_XYZ(pixels:np.ndarray,
               standard_illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in Lab color space to XYZ color space.

    Args:
        pixels (np.ndarray): Pixels in the Lab color space.
        standard_illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the XYZ color space.
    """
    # See the following link for the implemented conversion
    # https://en.wikipedia.org/wiki/CIELAB_color_space
    X_n, Y_n, Z_n = {'D50':(96.4212, 100.0, 82.5188),
                     'D65':(95.0489, 100.0, 108.8840)}[standard_illuminant]
    delta = 6 / 29

    def f_inv(t):
        return t**3 if t > delta else 3*delta**2*(t-(4/29))

    def to_XYZ(x):
        L, a, b = x
        X = X_n*f_inv(((L + 16)/116) + a/500)
        Y = Y_n*f_inv((L + 16)/116)
        Z = Z_n*f_inv(((L + 16)/116) - b/200)
        return np.array([X,Y,Z])

    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p = np.apply_along_axis(to_XYZ, 1, p)
    return np.reshape(p, (n,m,k))


def RGB_to_Lab(pixels:np.ndarray,
               standard_illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in RGB color space to Lab color space.

    Args:
        pixels (np.ndarray): Pixels in the RGB color space.
        standard_illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the Lab color space.
    """
    return XYZ_to_Lab(RGB_to_XYZ(pixels), standard_illuminant)


def Lab_to_RGB(pixels:np.ndarray,
               standard_illuminant:str = 'D65') -> np.ndarray:
    """Convert a pixel matrix in Lab color space to RGB color space.

    Args:
        pixels (np.ndarray): Pixels in the Lab color space.
        standard_illuminant (str): Standard illuminant {D65, D50}

    Returns:
        np.ndarray: Pixel matrix in the RGB color space.
    """
    return XYZ_to_RGB(Lab_to_XYZ(pixels, standard_illuminant))


def apply_to_channels(pixels:np.ndarray,
                      f_1:Callable,
                      f_2:Callable,
                      f_3:Callable) -> np.ndarray:
    """Return the pixel matrix with the functions applied to each channel.

    Args:
        pixels (np.ndarray): Pixel matrix
        f_1 (Callable): Function to apply to the first channel.
        f_2 (Callable): Function to apply to the second channel.
        f_3 (Callable): Function to apply to the third channel.

    Returns:
        np.ndarray: Pixel matrix with functions applied to each channel.
    """
    n,m,k = pixels.shape
    p = np.reshape(pixels, (n*m,3)).astype(float)
    p[:,0] = f_1(p[:,0])
    p[:,1] = f_2(p[:,1])
    p[:,2] = f_3(p[:,2])
    return np.reshape(p, (n,m,k))


def normalize(pixels:np.ndarray, color_space:str, norm:bool) -> np.ndarray:
    """Normalize / unnormalize the pixel matrix of the given color space.

    Args:
        pixels (np.ndarray): Pixel matrix in the given color space.
        color_space (str): Color space {RGB, Lab, YUV}
        norm (bool): Normalize if true. Otherwise, unnormalize.

    Returns:
        np.ndarray: Pixel matrix in the normalized / unnormalize color space.
    """
    r = {'RGB':[[0,255],[0,255],[0,255]],
         'Lab':[[0,255],[-128,127],[-128,127]],
         'YUV':[[0,1],[-0.436,0.436],[-0.615,0.615]]}[color_space]
    if norm:
        def f(i):
            return lambda x: (x - r[i][0]) / (r[i][1] - r[i][0])
    else:
        def f(i):
            return lambda x: (x * (r[i][1] - r[i][0])) + r[i][0]
    return apply_to_channels(pixels, f(0), f(1), f(2))
