import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def dft2(im):
    freq = cv2.dft(np.float32(im), flags=cv2.DFT_COMPLEX_OUTPUT)
    freq_shift = np.fft.fftshift(freq)
    mag, phase = freq_shift[:, :, 0], freq_shift[:, :, 1]
    return mag + 1j * phase


def idft2(freq):
    real, imag = freq.real, freq.imag
    back = cv2.merge([real, imag])
    back_ishift = np.fft.ifftshift(back)
    im = cv2.idft(back_ishift, flags=cv2.DFT_SCALE)
    im = cv2.magnitude(im[:, :, 0], im[:, :, 1])
    return im


def ideal(sz, D0):
    h, w = sz
    u, v = np.meshgrid(range(-w // 2, w // 2), range(-h // 2, h // 2))  # , sparse=True)
    return np.sqrt(u ** 2 + v ** 2) > D0


def gaussian(sz, D0):
    h, w = sz
    u, v = np.meshgrid(range(-w // 2, w // 2), range(-h // 2, h // 2))  # , sparse=True)
    return 1 - np.exp(-(u ** 2 + v ** 2) / (2 * D0 ** 2))


def butterworth(sz, D0, n=1):
    h, w = sz
    u, v = np.meshgrid(range(-w // 2, w // 2), range(-h // 2, h // 2))  # , sparse=True)
    return 1 / (1 + (D0 / (0.01 + np.sqrt(u ** 2 + v ** 2))) ** (2 * n))


def plot_HPF(im, f, D0s):
    freq = dft2(im)
    fig = plt.figure(figsize=(20, 20))
    plt.subplots_adjust(0, 0, 1, 0.95, 0.05, 0.05)
    i = 1
    for D0 in D0s:
        freq_kernel = f(im.shape, D0)
        convolved = freq * freq_kernel  # by the Convolution theorem
        im_convolved = idft2(convolved).real
        im_convolved = (255 * im_convolved / np.max(im_convolved)).astype(np.uint8)
        plt.subplot(2, 2, i)
        last_axes = plt.gca()
        img = plt.imshow((20 * np.log10(0.01 + freq_kernel)).astype(int), cmap=plt.cm.viridis)

        divider = make_axes_locatable(img.axes)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(img, cax=cax)
        plt.sca(last_axes), plt.title('{} HPF Kernel (freq)'.format(f.__name__), size=10)
        plt.subplot(2, 2, i + 2), plt.imshow(im_convolved), plt.axis('off')
        plt.title(r'output with {} HPF ($D_0$={})'.format(f.__name__, D0), size=10)
        i += 1
    plt.show()


def plot_HPF_3d(im, f, D0s):
    freq = dft2(im)
    fig = plt.figure(figsize=(20, 10))
    plt.subplots_adjust(0, 0, 1, 0.95, 0.05, 0.05)
    i = 1
    for D0 in D0s:
        freq_kernel = f(im.shape, D0)
        convolved = freq * freq_kernel  # by the Convolution theorem
        Y = np.arange(freq_kernel.shape[0])
        X = np.arange(freq_kernel.shape[1])
        X, Y = np.meshgrid(X, Y)
        Z = (20 * np.log10(0.01 + convolved)).real
        ax = fig.add_subplot(1, 2, i, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.viridis, linewidth=0, antialiased=False)
        ax.zaxis.set_major_locator(LinearLocator(10)), ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        ax.set_xlabel('F1', size=15), ax.set_ylabel('F2', size=15)
        plt.title(r'output with {} HPF (freq)'.format(f.__name__, D0), size=10)
        fig.colorbar(surf, shrink=0.5, aspect=10)
        i += 1
    plt.show()


def plot_filter_3d(sz, f, D0s, cmap=plt.cm.viridis):
    fig = plt.figure(figsize=(20, 10))
    plt.subplots_adjust(0, 0, 1, 0.95, 0.05, 0.05)
    i = 1
    for D0 in D0s:
        freq_kernel = f(sz, D0)
        Y = np.arange(freq_kernel.shape[0])
        X = np.arange(freq_kernel.shape[1])
        X, Y = np.meshgrid(X, Y)
        Z = (20 * np.log10(0.01 + freq_kernel)).real
        ax = fig.add_subplot(1, 2, i, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=False)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        ax.set_xlabel('F1', size=15)
        ax.set_ylabel('F2', size=15)
        ax.set_title('{} HPF Kernel (freq)'.format(f.__name__), size=10)
        fig.colorbar(surf, shrink=0.5, aspect=10)
        i += 1
    plt.show()


im = plt.imread('10726.png')
im = rgb2gray(im)
plt.figure(figsize=(50, 55))
plt.imshow(im, cmap='gray'), plt.axis('off'), plt.title('original image')
plt.show()
D0 = [2,9]

# ideal
plot_HPF(im, ideal, D0)
plot_filter_3d(im.shape, ideal, D0)

# gaussian
plot_HPF(im, gaussian, D0)
plot_HPF_3d(im, gaussian, D0)
plot_filter_3d(im.shape, gaussian, D0)
# butterworth
plot_HPF(im, butterworth, D0)
plot_HPF_3d(im, butterworth, D0)
plot_filter_3d(im.shape, butterworth, D0)


# def guassHighfillter(im):
#     freq = cv2.dft(np.float32(im), flags=cv2.DFT_COMPLEX_OUTPUT)
#     freq_shift = np.fft.fftshift(freq)
#     mag, phase = freq_shift[:, :, 0], freq_shift[:, :, 1]
#     dft = mag + 1j * phase
#     freq_kernel = 2
#     convolved = dft * freq_kernel
#     im_convolved = idft2(convolved).real
#     im_convolved = (255 * im_convolved / np.max(im_convolved)).astype(np.uint8)
#     plt.imshow(im_convolved)
#     plt.show()
#     print("1")
# im = plt.imread('pre-crop11687.jpg')
# guassHighfillter(im)
