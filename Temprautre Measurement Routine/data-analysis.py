import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.offsetbox import AnchoredText
import math
import pandas as pd

# --- Comment the section if it is giving error
import scienceplots # Just for fancy plots
plt.style.use('science') # Comment this for faster and default plot
# --- 


folder = "30-10-2024//" # Directory
dataset = "data01" # File name
file_name = folder + dataset + "sigmaData.xlsx"
df = pd.read_excel(file_name)
# print(df)

# Data is automatically taken from the Excel file. Please make sure
# that you name the key for the respective data correctly in the Excel file.

file_number = np.array(df["File Number"]) # Just entry or index of the measurement
Deviation = np.array(df["Deviation in Y"]) # Sigma of the fit [um]
timeArray = np.array(df["Time of flight"]) # Time of flight [ms]
t = np.array([])


# Numering of the files is similar to that of numbering of arrays

# 0----1----2----3
# |    |    |    |
# 1----2----3----4

# ----- Uncomment if to be used for averaging the data -----
# start = np.array([6, 11, 16, 21, 26]) # Begining of the array
# end = np.array([10, 15, 20, 25, 30]) # End of the array

# In case no averaging is to be done for the sigma values 
# Plug "start" and "end" arrays with the same values. 

# ----- Uncomment if data is not to be averaged -----
start = np.array([0, 1, 2, 3, 4, 5]) # Begining of the array
end = np.array([0, 1, 2, 3, 4, 5]) # End of the array


sigma = np.array([])
ERR = np.array([])


for i,j in zip(start, end):
    sigma_adder = np.array([])
    iter = np.arange(i, (j+1), 1)
    if i == j:
        sigma = np.append(sigma, Deviation[i])
        ERR = np.append(ERR, 0)
        t = np.append(t, timeArray[i])
    else:
        for k in iter: 
            indx = np.where(file_number == k)[0]
            sigma_adder = np.append(sigma_adder, Deviation[indx])
        sigma = np.append(sigma, np.mean(sigma_adder))
        ERR = np.append(ERR, np.std(sigma_adder)/np.sqrt(sigma_adder.size))
        t = np.append(t, timeArray[i])

# print(sigma)
# print(t)

t_sim = np.arange(min(t), max(t) + 0.1, 0.1)
sigma2 = np.square(sigma)
ERR2 = np.square(ERR)

# Curve fitting
def fit_func(x, a, c):
    return a*x**2 + c

[popt, pconv] = curve_fit(fit_func, t, sigma2)

[a, c] = popt

sigmaSim2 = fit_func(t_sim, a, c)
sigmaSim = np.sqrt(sigmaSim2)

fig, ax = plt.subplots(figsize=(5,4))
ax.plot(t_sim, sigmaSim, "b-", label="Fit")
ax.errorbar(t, sigma, yerr = ERR, fmt = 'o',color = 'black', 
            ecolor = 'black', elinewidth = 1.5, capsize=2, label="Raw Data")

ax.set(xlabel='$t\ (ms)$', ylabel='$\sigma_t\ (\mu m)$',
       title='Temprature Measurement')
# ax.grid()
ax.legend(loc='lower right')

# loc works the same as it does with figures (though best doesn't work)
# pad=5 will increase the size of padding between the border and text
# borderpad=5 will increase the distance between the border and the axes
# frameon=False will remove the box around the text

SqrtPconv = np.sqrt(abs(pconv))

# Temprature Calculation
T = 1.409993199E-25*a*1e-6/1.3806503e-23
delT = 1.409993199E-25*SqrtPconv[0,0]*1e-6/1.3806503e-23

# anchored_text1 = AnchoredText("y = (" + str(int(a)) + ")*x + (" + str(int(b)) + ")", loc=4)
# ax.add_artist(anchored_text1)
anchored_text2 = AnchoredText("T = " + str(int(T/1e-6)) + "$\pm$" + str(math.ceil(int(delT/1e-9)*1e-3)) + " $\mu K$", loc='upper left')
ax.add_artist(anchored_text2)
plt.savefig( "fig_" + dataset + ".png", dpi=600) 
plt.show()