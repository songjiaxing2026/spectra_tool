import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
from scipy.optimize import curve_fit


def gaussian(x, center, sigma, c, amplitude=1):
    return amplitude * np.exp(-(x - center)**2 / (2 * sigma**2)) + c

def lorentzian(x, center, gamma, c, amplitude=1):
    return amplitude * gamma**2 / ((x - center)**2 + gamma**2) + c

def add_noise(y, noise_level=0.05):
    return y + np.random.normal(0, noise_level, size=y.shape)

def moving_average(y, winow=10):
    return np.convolve(y, np.ones(winow) / winow, mode='same')

def gaussian_filter1d(y, sigma=0.3, winow=9):
    b = []
    c = 0
    for i in range(winow):
        b.append(np.exp(-(winow//2 - i)**2 / (2 * sigma**2)))
        c = c + b[i]
    b_array = np.array(b) / c
    return np.convolve(y, b_array, mode='same')


def plot_spectra(x, *ys, labels=None, title='Spectra'):
    for i, nl in enumerate(ys):
        label = labels[i] if labels else None
        plt.plot(x, nl, label=label, alpha=0.7)
    plt.legend()
    plt.xlabel('Wavelength(nm)')
    plt.ylabel('Intensity')
    plt.title(title)
    plt.grid(True)
    plt.show()

def calculate_fwhm(x, y, peak_index):
    """计算指定峰位置的半高宽"""
    bool_list = (x>x[peak_index-200])&(x<x[peak_index+200])
    x1 = x[bool_list]
    y1 = y[bool_list]
    p0 = [x[peak_index], 3, 0, y[peak_index]]
    popt, pcov = curve_fit(gaussian, x1, y1, p0=p0)
    fwhm = 2.3548*popt[1]
    return fwhm

def find_peak(y, height=1, distance=20):
    peaks, properties = find_peaks(y, height=height, distance=distance)  #这个height限制的是峰的高度，高于他的才计入
                                                  #第二个distance是限制峰的间隔，高于这个间距才能识别
    return peaks

def calculate_SNR(x, y, peak_index):
    baseline_mask = (x < x[peak_index] - 10) | (x > x[peak_index] + 10)
    noise_std = np.std(y[baseline_mask])
    baseline = np.mean(y[baseline_mask])
    signal = y[peak_index] - baseline
    snr = signal / noise_std
    return snr

def to_dataframe(filenames):
    """输出表格的，列表分别为文件，峰位置，峰高， fwhm, 信噪比"""
    rows = []
    for fn in filenames:
        df = pd.read_csv('data/' + fn)
        x1 = df['wavenumber_cm-1'].values
        y = df['intensity'].values
        peaks = find_peak(y, height=1, distance=20)  #这里有个问题可能有好几个峰所以要选一个，
        peak_index = peaks[np.argmax(y[peaks])]
        a = x1[peak_index]
        b = y[peak_index]
        fwhm = calculate_fwhm(x1, y, peak_index)
        snr = calculate_SNR(x1, y, peak_index)
        rows.append({'文件':fn, '峰位置':a, '峰高':b, 'FWHM':fwhm, '信噪比':snr})
    return pd.DataFrame(rows)


if __name__ == '__main__':   #保护一下防止import调用时自动输出了
    bg = to_dataframe(['raman_silicon_clean.csv',
                       'raman_silicon_noisy_0.5pct.csv',
                       'raman_silicon_noisy_2pct.csv',
                       'raman_silicon_noisy_5pct.csv'])
    print(bg)
    bg.to_csv('results/输入数据信息.csv', index=False, encoding='utf-8-sig')
