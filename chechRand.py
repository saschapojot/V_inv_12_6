import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fileName="rand.csv"


df=pd.read_csv(fileName)

xVec=np.array(df.iloc[:,0])

xMin=np.min(xVec)
xMax=np.max(xVec)

print("min="+str(xMin))
print(f"max={xMax:.28f}")  # prints the float with 18 decimal places
plt.figure()
plt.hist(xVec, bins=55, density=True, alpha=0.6, color='g', label='Numerical')
plt.savefig("hist.png")
plt.close()