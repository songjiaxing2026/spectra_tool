# spectra_tool —— 拉曼光谱参数提取工具

输入拉曼光谱数据，输出峰位置、峰高、FWHM、信噪比。

## 能做什么

- 生成高斯函数、洛伦兹函数，并给它们增添噪声
- 滑动窗口平均、高斯平均
- 画图
- 寻峰，计算指定峰位置的半高宽（FWHM）
- 计算信噪比
- 输出表格

## 安装

需要先装好 Python，再安装依赖：

```
pip install -r requirements.txt
```

## 用法

1. 把输入数据放到项目文件夹的 `data` 子文件夹中。

2. 在该文件夹下打开终端，运行：

   ```
   python spectra_utils.py
   ```

3. 结果输出到项目文件夹的 `results` 子文件夹下。

## 输出结果

产出结果用表格形式呈现：在屏幕上打出表格，并在 `results` 文件夹下生成 csv 格式表格数据。

例如输入 4 档噪声的数据，输出参数如下：

| 文件 | 峰位置 | 峰高 | FWHM | 信噪比 |
| --- | --- | --- | --- | --- |
| raman_silicon_clean.csv | 519.9199 | 1049.6438 | 7.4074 | 3385.118621 |
| raman_silicon_noisy_0.5pct.csv | 519.9199 | 1053.4638 | 7.4074 | 197.7845416 |
| raman_silicon_noisy_2pct.csv | 520.1201 | 1089.6854 | 7.4074 | 52.43107915 |
| raman_silicon_noisy_5pct.csv | 520.3203 | 1152.1265 | 6.6066 | 21.72079243 |

## 目录结构

```
spectra_tool/
├─ spectra_utils.py      主程序
├─ requirements.txt      依赖清单
├─ README.md             本说明
├─ data/                 输入数据（CSV）
├─ results/              输出结果
└─ 练习/                 学习过程脚本，不保证能直接运行
```
