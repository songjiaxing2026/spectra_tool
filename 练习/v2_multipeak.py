# v2_multipeak.py —— 多峰 → 加噪 → 寻峰 → FWHM → 标注 → 表格
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from spectra_utils import gaussian, add_noise, find_peak, calculate_fwhm

x = np.linspace(400, 700, 1000)
y = gaussian(x, 520, 10, 10) + gaussian(x, 560, 15, 6) + gaussian(x, 610, 8, 8)   # ① 多峰

noise_levels = [0, 0.1, 0.5, 1.0]                        # ② 不同噪声
rows = []
fig, axes = plt.subplots(2, 2, figsize=(12, 8))          # 2x2 子图，v1 里你用过

for i, noise in enumerate(noise_levels):
    y_noisy = add_noise(y, noise)                        # ② 加噪声
    peaks = find_peak(y_noisy)                           # ③ 寻峰（找所有峰）
    ax = axes[i // 2, i % 2]
    ax.plot(x, y_noisy)
    for p in peaks:                                      # ④ 每个峰
        fwhm = calculate_fwhm(x, y_noisy, p)             #    算 FWHM
        ax.plot(x[p], y_noisy[p], 'ro')                  # ⑤ 峰顶红点
        if y_noisy[p] > 4:                               # 半高线只给"高一点"的峰画，图才不乱
            ax.axhline(y_noisy[p] / 2, ls='--', color='gray', alpha=0.5)
        rows.append({'噪声': noise, '峰位置': round(x[p], 1),
                       '峰高': round(y_noisy[p], 2), 'FWHM': round(fwhm, 2)})   # ⑥ 收集
    ax.set_title(f'noise = {noise}')

plt.tight_layout()
plt.show()
print(pd.DataFrame(rows))                                # ⑥ 输出表格