# datoteka koja se izvrsava lokalno, iz razloga sto matplotlib ne radi na lxplus8

import matplotlib.pyplot as plt
import os

os.chdir("Plot")
out = [[[],[],[]],[[],[],[]]] #za svaku dimeziju(E i H) - u prvi element spremamo sume, s u druga dva koordinate
files = [["out_sum_E.txt","out_eta_E.txt","out_phi_E.txt"],["out_sum_H.txt","out_eta_H.txt","out_phi_H.txt"]]
imena = ["E","H"]

for i in range(2):
    j = 0
    for file in files[i]:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                out[i][j].append(float(line.strip("\n")))
        j += 1 

                
    plt.scatter(out[i][1], out[i][2], c=out[i][0], cmap='cividis', s=100, alpha=0.5)
    cbar = plt.colorbar()
    cbar.set_label('Vrijednosti sume')
    plt.xlim(-5,25)
    plt.ylim(-5,25)
    plt.title(f"Suma outputa 14 Stage-1 FPG --- {imena[i]} data")
    plt.xlabel('Eta')
    plt.ylabel('Phi')
    plt.grid()
    plt.savefig(f"Suma_outputa_14_Stage-1_FPG-{imena[i]}_data.png")
    plt.show()

