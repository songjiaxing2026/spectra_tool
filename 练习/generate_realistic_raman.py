"""
生成一个逼真的硅拉曼光谱数据文件 (raman_silicon.csv)
硅的经典拉曼峰在 520 cm⁻¹
"""
import numpy as np

# ===== 参数设置 =====
wavenumber = np.linspace(400, 600, 1000)      # 拉曼位移 (cm⁻¹)
peak_center = 520                               # 硅的一阶拉曼峰
peak_sigma = 3                                  # 峰宽 (~3 cm⁻¹)
peak_amplitude = 1000                           # 峰高
baseline = 50                                   # 基线（背景信号）

# ===== 生成"干净"的拉曼光谱 =====
clean = baseline + peak_amplitude * np.exp(-(wavenumber - peak_center)**2 / (2 * peak_sigma**2))

# ===== 保存为 CSV 文件 =====
data = np.column_stack([wavenumber, clean])
header = "wavenumber_cm-1,intensity"
np.savetxt("raman_silicon_clean.csv", data, delimiter=",", header=header, comments="", fmt="%.4f")

print("OK - 已生成: raman_silicon_clean.csv")
print(f"   波长范围: {wavenumber[0]:.0f} ~ {wavenumber[-1]:.0f} cm-1")
print(f"   数据点数: {len(wavenumber)}")
print(f"   峰位置: {peak_center} cm-1")
print(f"   峰高: {peak_amplitude}")

# 再生成一版带噪声的，更像真实测量数据
for noise_level in [0.5, 2, 5]:
    noisy = clean + np.random.normal(0, noise_level * peak_amplitude / 100, size=clean.shape)
    fn = f"raman_silicon_noisy_{noise_level}pct.csv"
    data_n = np.column_stack([wavenumber, noisy])
    np.savetxt(fn, data_n, delimiter=",", header=header, comments="", fmt="%.4f")
    print(f"OK - 已生成: {fn}  (噪声水平 ~ {noise_level}%)")
