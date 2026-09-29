"""
光谱项目 V1 测试脚本 — 用自己写的工具库
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或者 ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
from spectra_utils import gaussian, add_noise, moving_average, plot_spectra, gaussian_filter1d
import pandas as pd


# 1. 生成模拟光谱（高斯峰）
x = np.linspace(400, 700, 300)
y_clean = gaussian(x, center=520, sigma=15, amplitude=10)

# 2. 加噪声
y_noisy = add_noise(y_clean, noise_level=0.3)

# 3. 去噪（用 np.convolve）
y_smooth = moving_average(y_noisy, winow=10)
y_gaussian_smooth = gaussian_filter1d(y_noisy, sigma=1.8, winow=11)    #之前设置的sigma=0.5,怎么调节winow都不行，原来是权重太集中，几乎都是由中心决定，导致去噪不佳；我以为已经很大了
                                                                     #我还以为sigma是0-1的范围，我错了这个是标准差而已，不限大小，大于0是唯一的要求了
                        #高斯滤波的卖点不是"更平滑"而是"保峰更好"——在同样平滑力度下，高斯滤波对峰的破坏比滑动平均小。
 #哦哦，所以说窗口是根据sigma定的。二者是有联系的，不能说为了平滑设置了sigma=10；结果窗口只有9，远远不够这个3sigma数据，导致整个和直接平均去噪没啥区别了，无法体现这个高斯去噪的特性了
 #这个sigma可以先定，然后定窗口。也就是3*sigma约等于winow/2.这样利用率就高了，就有意义了

# 4. 画在一张图上对比
plot_spectra(x, y_clean, y_noisy, y_smooth, y_gaussian_smooth,
             labels=['原始信号', '含噪声', '10点平滑', '高斯去噪'],
             title='光谱项目 V1 — 信号处理对比')


#用外来数据试试
dp = pd.read_csv('data/raman_silicon_clean.csv')
#print(dp)
wn = dp['wavenumber_cm-1']
ine = dp['intensity']

dp2 = pd.read_csv('data/raman_silicon_noisy_0.5pct.csv')
print(dp2)

ine2 = dp2['intensity']

dp3 = pd.read_csv('data/raman_silicon_noisy_2pct.csv')    #这个读取函数用圆括号不是方括号，用错了
print(dp3)
ine3 = dp3['intensity']

dp4 = pd.read_csv('data/raman_silicon_noisy_5pct.csv')
ine4 = dp4['intensity']

def plotuse(ine2):
    b1 = moving_average(ine, winow=10)
    b2 = gaussian_filter1d(ine, sigma=1.8, winow=11)

    plot_spectra(wn, ine, ine2, b1, b2,
             labels=['原始数据', '加噪信号' ,'10窗口平滑去噪', '11窗口高斯去噪'], 
             title="拉曼光谱去噪对比")

plotuse(ine2)
plotuse(ine3)
plotuse(ine4)