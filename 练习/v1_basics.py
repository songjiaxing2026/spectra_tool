import numpy as np
import matplotlib.pyplot as plt

#目标：生成一个单高斯峰，并画出来
center = 500      #峰的中心位置
sigma = 20        #峰宽度
ampltude = 1      #峰高度
x = np.linspace(400, 600, 1000)  #波长范围


#生成高斯峰
y = ampltude * np.exp(-(x - center)**2 / (2 * sigma**2))

#画图

# y2 = np.ones(1000) * 0.5
# plt.plot(x, y2)
# a = np.where( y >= 0.5)
# plt.scatter(x[a[0][0]], y[a[0][0]], c='r')
# plt.scatter(x[a[0][-1]], y[a[0][-1]], c='r')
# plt.text(x[a[0][0]], y[a[0][0]], s=round(x[a[0][0]],1))
# plt.text(x[a[0][-1]], y[a[0][-1]], s=round(x[a[0][-1]],1))
# plt.text((x[a[0][0]]+x[a[0][-1]]) / 2, (y[a[0][0]] + y[a[0][-1]]) / 2, s=round((x[a[0][-1]] - x[a[0][0]]), 1))   

#  这里的 σ（sigma） 叫标准差，它和半高宽（FWHM） 的关系是：

#   FWHM = 2√(2·ln2) · σ  ≈  2.355 · σ

#第二天加噪声（模拟真实光谱仪的测量噪声）
noise_level = 0.05
noise = np.random.normal(0, noise_level, size=x.shape)
y_noise = y + noise

#滑动平均去噪  其实就是每个点和周围几个取平均值，不断滑动
def moving_average(y, window=5):
    return np.convolve(y, np.ones(window)/window, mode='same')    #这个函数是离散卷积，把窗口倒数作为其加权就可以实现窗口平均了；学会了

y_denoised = moving_average(y_noise, window=10)  #这个window小了去噪不足，大了容易抹平山峰



#画对比图
plt.plot(x, y_noise, label='Noisy', alpha=0.5)
plt.plot(x, y, label='Clean')
plt.plot(x, y_denoised, label='Denoised', linestyle='--')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')      #强度
plt.title('Moving Average Denoising') #移动平均去噪
#plt.title('Single Gaussian Peak')  #单高斯峰
plt.grid(True)
plt.legend()
plt.show()

#小循环，对比不容噪声水平下的去噪效果

noise_levels = [0.02, 0.05, 0.10, 0.20]
fig, axes = plt.subplots(2, 2, figsize=(10, 8))  #这个是把格子分配出来，返回出来两个量，第一个是画布，第二个是坐标系；我猜测第一个都一样，第二个分别是axes[0/1, 0/1]四个
                #这里要加subplots!!
for i, nl in enumerate(noise_levels):  #这个enumerate函数是把列表标上了序号，同时得到索引和元素两个东西
    noise = np.random.normal(0, nl, size=x.shape)
    y_noise = y + noise
    y_denoised = moving_average(y_noise, window=10)

    ax = axes[i // 2, i % 2]
    ax.plot(x, y, label='Clean', alpha=0.5)
    ax.plot(x, y_denoised, label=f'Noise={nl}', alpha=0.5)
    ax.legend()
    ax.set_title(f'Noise level = {nl}')

plt.tight_layout()
plt.show()