import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from spectra_utils import gaussian
from scipy.signal import find_peaks

x = np.linspace(400, 700, 1000)

peak1 = gaussian(x, center=520, sigma=10, amplitude=10)
peak2 = gaussian(x, center=560, sigma=15, amplitude=6)
peak3 = gaussian(x, center=610, sigma=8, amplitude=8)

y_multi = peak1 + peak2 +peak3

plt.plot(x, y_multi)
plt.title('多峰叠加光谱')
plt.xlabel('Wavenumber (cm⁻¹)')
plt.ylabel('Intensity')
plt.grid(True)

plt.show()
        #尝试调整这个中心位置了，近到一种程度就会吞并，也就是分辨率的概念
dy = np.diff(y_multi)   #这个函数是对列表俩俩做差的
# for i in range(len(dy)):  这里不用for。直接用np.where就能寻找
n = np.where((dy[:-1] > 0 ) & (dy[1:] < 0 ))  #这里是利用了判断结果为布尔型，结果为一串布尔型数据，两组数据比对，发现前一个和后一个异号则取出对应的序号，这个序号就是再x中的索引
print(n)     #并且这里面还有错位的思路就是这个第一组去掉尾，第二组去掉头；从而错位对齐判断
print(x[n])      #这里这个得到的索引是x的索引不是具体的x值，所以要用这个x[n]输出一下 
   
peaks, properties = find_peaks(y_multi, height=1, distance=20)  #这个height限制的是峰的高度，高于他的才计入
                                                  #第二个distance是限制峰的间隔，高于这个间距才能识别
print(f'找到{len(peaks)}个峰,位置在x = {x[peaks]}')

plt.plot(x, y_multi)
plt.plot(x[peaks], y_multi[peaks], 'ro')
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
print(calculate_fwhm(x, y_multi, peaks[0]))#当这里是叠加峰的时候，这个算法可能会失效，因为叠加峰半高位置被叠掉了