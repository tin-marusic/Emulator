import numpy as np
import re
import os

os.chdir('../outputs')
files = [[], []]
for file_name in os.listdir():  #učitavamo imena svih datoteke iz mape 'outputs' u dva zasebna niza
    if file_name.startswith("CE_E"):
        files[0].append(file_name)
    elif file_name.startswith("CE_H"):
        files[1].append(file_name)

for i in range(2):
    line_count = 0 #broj linija potrebnih za sumu, jednak broju ulaznih koordinata
    with open(files[i][0], 'r') as file: 
        for line in file:
            line_count += 1
    sum = np.zeros(line_count)

    for file in files[i]: 
        j = 0
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                sum[j] += int(line.strip(", \n")) 
                j += 1    
    
    if i == 0: #ime filea ovisno koje podatke gledamo
        name = 'out_sum_E.txt'
    elif i == 1:
        name = 'out_sum_H.txt'
    with open('../Plot/' + name, 'w') as f: #zapisujemo sume za svaku koord
        for j in range (len(sum)):
            f.write(str(sum[j]) + '\n')

    #dio koda za citanje koordinata        
    eta_coordinates = []
    phi_coordinates = []
    
    if i == 0: #dva input file iz kojih cemo isčitati koordinate
        name = 'coord_E.txt'
    elif i == 1:
        name = 'coord_H.txt'
    with open('../Plot/' + name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Pronalazak koordinata eta i fi u liniji pomoću regularnog izraza
            if i == 0:
                match = re.match(r'/\* out\d+_em-eta(-?\d+)-phi(-?\d+) \*/\s+(.*)', line)
            else:
                match = re.match(r'/\* out\d+_had-eta(-?\d+)-phi(-?\d+) \*/\s+(.*)', line)
            if match:
                eta = int(match.group(1))
                phi = int(match.group(2))
                eta_coordinates.append(eta)
                phi_coordinates.append(phi)
            else:
                print(line)
                print("Dogodila se greška, sve koordinate nisu ucitane - prekidam program")
                exit()                           
                
    if i == 0: #ime filea ovisno koje podatke gledamo
        name_eta = 'out_eta_E.txt'
        name_phi = 'out_phi_E.txt'
    elif i == 1:
        name_eta = 'out_eta_H.txt'
        name_phi = 'out_phi_H.txt'
    with open('../Plot/' + name_phi, 'w') as f:
        for i in range (len(phi_coordinates)):
            f.write(str(phi_coordinates[i]) + '\n')
            
    with open('../Plot/' + name_eta, 'w') as f:
        for i in range (len(eta_coordinates)):
            f.write(str(eta_coordinates[i]) + '\n')
            