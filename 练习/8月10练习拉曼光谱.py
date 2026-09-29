import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/raman_silicon_clean.csv')
#print(df)
plt.plot(df['wavenumber_cm-1'], df['intensity'])
plt.xlabel('Raman shift (cm⁻¹)')
plt.ylabel('Intensity')
plt.title('硅的拉曼光谱')
plt.show()
