import numpy as np
import re
import os

os.chdir('../outputs')
files = [[], []]
for file_name in os.listdir():  # load names of all files from the 'outputs' folder into two separate arrays
    if file_name.startswith("CE_E"):
        files[0].append(file_name)
    elif file_name.startswith("CE_H"):
        files[1].append(file_name)

for i in range(2):
    line_count = 0  # number of lines needed for sum, equal to the number of input coordinates
    with open(files[i][0], 'r') as file:
        for line in file:
            line_count += 1
    sum_values = np.zeros(line_count)

    for file in files[i]:
        j = 0
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                sum_values[j] += int(line.strip(", \n"))
                j += 1

    if i == 0:  # filename depending on the data we are looking at
        name = 'out_sum_E.txt'
    elif i == 1:
        name = 'out_sum_H.txt'
    with open('../Plot/' + name, 'w') as f:  # write sums for each coordinate
        for j in range(len(sum_values)):
            f.write(str(sum_values[j]) + '\n')

    # code part for reading coordinates
    eta_coordinates = []
    phi_coordinates = []

    if i == 0:  # two input files from which we will extract coordinates
        name = 'coord_E.txt'
    elif i == 1:
        name = 'coord_H.txt'
    with open('../Plot/' + name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Finding eta and phi coordinates in the line using regular expression
            if i == 0:
                match = re.match(r'/\* out\d+_em-eta(-?\d+)-phi(-?\d+) \*/\s+(.*)', line)  # change if input files change
            else:
                match = re.match(r'/\* out\d+_had-eta(-?\d+)-phi(-?\d+) \*/\s+(.*)', line)  # All input files have the same coordinates at the same positions
            if match:
                eta = int(match.group(1))
                phi = int(match.group(2))
                eta_coordinates.append(eta)
                phi_coordinates.append(phi)
            else:
                print(line)
                print("Error occurred, not all coordinates were loaded - exiting the program")
                exit()

    if i == 0:  # filename depending on the data we are looking at
        name_eta = 'out_eta_E.txt'
        name_phi = 'out_phi_E.txt'
    elif i == 1:
        name_eta = 'out_eta_H.txt'
        name_phi = 'out_phi_H.txt'
    with open('../Plot/' + name_phi, 'w') as f:
        for i in range(len(phi_coordinates)):
            f.write(str(phi_coordinates[i]) + '\n')

    with open('../Plot/' + name_eta, 'w') as f:
        for i in range(len(eta_coordinates)):
            f.write(str(eta_coordinates[i]) + '\n')
