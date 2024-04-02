# datoteka koja se izvrsava lokalno, iz razloga sto matplotlib ne radi na lxplus8

import matplotlib.pyplot as plt
import os

os.chdir("outputs")
out = [[],[],[]] #u prvi element spremamo sume, s u druga dva koordinate
files = ["out_sum_E.txt","out_eta_E.txt","out_phi_E.txt"]

i = 0
for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            out[i].append(float(line.strip("\n")))
    i += 1 

            
plt.scatter(out[1], out[2], c=out[0], cmap='cividis', s=100, alpha=0.5)
cbar = plt.colorbar()
cbar.set_label('Vrijednosti sume')
plt.xlim(-5,25)
plt.ylim(-5,25)
plt.title("Suma outputa 14 Stage-1 FPG --- E data")
plt.xlabel('Eta')
plt.ylabel('Phi')
plt.grid()
plt.savefig("Suma_outputa_14_Stage-1_FPG-E_data.png")
plt.show()

