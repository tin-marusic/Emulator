#skripta za pokretanje svih input filova odjednom

from pythonTestBenchNew_version_Marko import main
import os

os.chdir('../inputs') #vazno je da se datoteke nalaze u mapi inputs, prema tome je prilagoden i kod 'pythonTestBenchNew_version_Marko.py'
filenames = os.listdir() #učitavamo imena svih datoteka u mapi 'inputs'
h_files = []
e_files = []

# Razdvajanje datoteka na temelju trećeg slova
for file_name in filenames:
    if file_name[3] == 'H':
        h_files.append(file_name)
    elif file_name[3] == 'E':
        e_files.append(file_name)

for i in range(len(h_files)): #Pretpostavka da je broj fileova jednak
    main(e_files[i],h_files[i])