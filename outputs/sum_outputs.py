import numpy as np
import re


files = ["CE_E_0_v6.vh_outputData_CE_E_1.txt","CE_E_1_v6.vh_outputData_CE_E_1.txt","CE_E_2_v6.vh_outputData_CE_E_1.txt","CE_E_3_v6.vh_outputData_CE_E_1.txt",
         "CE_E_4_v6.vh_outputData_CE_E_1.txt","CE_E_5_v6.vh_outputData_CE_E_1.txt","CE_E_6_v6.vh_outputData_CE_E_1.txt","CE_E_7_v6.vh_outputData_CE_E_1.txt",
         "CE_E_8_v6.vh_outputData_CE_E_1.txt","CE_E_9_v6.vh_outputData_CE_E_1.txt","CE_E_10_v6.vh_outputData_CE_E_1.txt","CE_E_11_v6.vh_outputData_CE_E_1.txt",
         "CE_E_12_v6.vh_outputData_CE_E_1.txt"]

sum = np.zeros(428)

for file in files:
    i = 0
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            sum[i] += int(line.strip(", \n")) 
            i += 1
            
with open('out_sum.txt', 'w') as f:
    for i in range (len(sum)):
        f.write(str(sum[i]) + '\n')

        
eta_coordinates = []
phi_coordinates = []

with open('CE_E_0_v6.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        # Pronalazak koordinata eta i fi u liniji pomoću regularnog izraza
        match = re.match(r'/\* out\d+_em-eta(-?\d+)-phi(-?\d+) \*/\s+(.*)', line)
        if match:
            eta = int(match.group(1))
            phi = int(match.group(2))
            eta_coordinates.append(eta)
            phi_coordinates.append(phi)
        else:
            print(line)            
            
print(len(eta_coordinates))
with open('out_phi.txt', 'w') as f:
    for i in range (len(phi_coordinates)):
        f.write(str(phi_coordinates[i]) + '\n')
        
with open('out_eta.txt', 'w') as f:
    for i in range (len(eta_coordinates)):
        f.write(str(eta_coordinates[i]) + '\n')