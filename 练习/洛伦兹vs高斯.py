import numpy as np
import matplotlib.pyplot as plt

center = 500      #峰的中心位置
sigma = 20        #峰宽度（不对）
ampltude = 1      #峰高度
x = np.linspace(400, 600, 1000)  #波长范围


#生成高斯峰
y = ampltude * np.exp(-(x - center)**2 / (2 * sigma**2))


def lorentzian(x, center, gamma, amplitude):#这里的gamma就是γ，也就是对应于σ的东西
    return ampltude * gamma**2 * (1 / ((x - center)**2 + gamma**2))    #这里第一次写错了在于这个分母没有用阔靠括起来导致运算顺序错了

y_lorentz = lorentzian(x, center, sigma, ampltude)

plt.plot(x, y, label= 'Gaussian')
plt.plot(x, y_lorentz,label='Lorentzian')
plt.legend()
plt.title('Gaussian vs Lorentzian')
plt.show()     #结果上能看出来，高斯更集中更加胖，而洛伦兹中间瘦分散到两边尾巴了