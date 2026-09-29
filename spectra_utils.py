import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd


def gaussian(x, center, sigma, amplitude=1):
    return amplitude * np.exp(-(x - center)**2 / (2 * sigma**2))

def lorentzien(x, center, gamma, ampltude=1):
    return ampltude * gamma**2 / ((x - center)**2 + gamma**2)

def add_noise(y, noise_level=0.05):
    return y + np.random.normal(0, noise_level, size=y.shape)

def moving_average(y, winow=10):
    return np.convolve(y, np.ones(winow) / winow, mode='same')

#自己在网上搜的高斯去噪是指对窗口里面做加权平均，而权重用e^(-距离² / (2σ²))除总权重得到权重和为1的权重分布，用这个替代平均分布就行了
def gaussian_filter1d(y, sigma=0.3, winow=9):
    b = []
    c = 0
    for i in range(winow):                    #winow-1):这里写错了，range（2）包含的是0和1没有2   
        b.append(np.exp(-(winow//2 - i)**2 / (2 * sigma**2)))
        c = c + b[i]
    #return np.convolve(y, b/c, mode='same')   这里列表不能直接除一个数，但np.array数组可以这样操作
    b_array = np.array(b) / c
    return np.convolve(y, b_array, mode='same')



def plot_spectra(x, *ys, labels=None, title='Spectra'):    #疑惑1在于这个ys是可变参数，但这个咋用还挺疑惑的，其次这个label怎么和这个ys对应上也疑惑
    # fig, axes = plt.subplots()                       #这里疑惑了  ;哦哦，这里不是想要他画一个图里面，而是画好几个线在一个图里面
    for i, nl in enumerate(ys):   #使用这个可变参数时候，不用加*
        label = labels[i] if labels else None    #这是啥，什么用法  ；这叫条件赋值
        plt.plot(x, nl, label=label, alpha=0.7)
    plt.legend()
    plt.xlabel('Wavelength(nm)')
    plt.ylabel('Intensity')
    plt.title(title)
    plt.grid(True)    #画格子
    plt.show()

def calculate_fwhm(x, y, peak_index):
    """计算指定峰位置的半高宽"""    #这样的一个字符串可以在用函数时出现作为函数说明
    peak_height = y[peak_index]
    half_height = peak_height / 2
    half_index1 = peak_index
    half_index2 = peak_index
    #while y[half_index1] <= half_height:  #while写反了！他是条件满足则循环
    while y[half_index1] >= half_height:
        half_index1 -= 1
    while y[half_index2] >= half_height:
        half_index2 += 1
    fwhm = x[half_index2] - x[half_index1]
    return fwhm

def find_peak(y_multi, height=1, distance=20):
    peaks, properties = find_peaks(y_multi, height=height, distance=distance)  #这个height限制的是峰的高度，高于他的才计入
                                                  #第二个distance是限制峰的间隔，高于这个间距才能识别
    return peaks

def calculate_SNR(x, y, peak_index):
    baseline_mask = (x < x[peak_index] - 10) | (x > x[peak_index] + 10)
    noise_std = np.std(y[baseline_mask])
    baseline = np.mean(y[baseline_mask])  #索引用的都是中括号！！
    signal = y[peak_index] - baseline
    snr = signal / noise_std
    return snr

def to_dataframe(filenames):
    """输出表格的，列表分别为文件，峰位置，峰高， fwhm，信噪比"""

    # peak_index = find_peak(x, y_multi, height=1, distance=20)
    # a = x[peak_index]
    # b = y_multi[peak_index]
    # fwhm = calculate_fwhm(x, y_multi, peak_index)
    # baseline_mask = (x < x[peak_index] - 10) | (x > x[peak_index] + 10)   #这里得到的时一系列的布尔类型吧，为啥能作为索引？
    # noise_std = np.std(y_multi(baseline_mask))  #这是求标准差的函数
    # baseline = np.mean(y_multi(baseline_mask))  #背景水平
    # signal = y_multi(peak_index) - baseline  #信号 = 峰比背景高多少
    # snr = signal / noise_std
    rows = []
    for fn in filenames:
        df = pd.read_csv('data/' + fn)   ##在这里加就高效多了
        x1 = df['wavenumber_cm-1'].values
        y = df['intensity'].values    #歇会，不要影响积极性！同时把CSV 数据处理回顾8月1日的内容也先跳过，
        #这个添加values是取出里面的数据作为一个numpy数组，直接出来的是带着标签的数
        peaks = find_peak(y, height=1, distance=20)  #这里有个问题可能有好几个峰所以要选一个，
        peak_index = peaks[np.argmax(y[peaks])]  #用这个取最大值索引的函数，这个出来的是索引吗？是的
        a = x1[peak_index]
        b = y[peak_index]
        fwhm = calculate_fwhm(x1, y, peak_index)
        snr = calculate_SNR(x1, y, peak_index)
        rows.append({'文件':fn, '峰位置':a, '峰高':b, 'FWHM':fwhm, '信噪比':snr})
    return pd.DataFrame(rows)    #这里学了一个dataframe，出来时很漂亮的表格数据


if __name__ == '__main__':   #保护一下防止import调用时自动输出了；这只是一个测试
    bg = to_dataframe(['raman_silicon_noisy_5pct.csv',
                       'raman_silicon_clean.csv',
                       'raman_silicon_noisy_0.5pct.csv',
                       'raman_silicon_noisy_2pct.csv'])  #filenames要用列表装哦
    print(bg)
    bg.to_csv('results/输入数据信息.csv', index=False, encoding='utf-8-sig')

