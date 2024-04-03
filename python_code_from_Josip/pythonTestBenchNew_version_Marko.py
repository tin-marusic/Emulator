import scipy.io as scio
import random
import re
import copy
import numpy as np
import sys
import os

def generateInputEnergies(numberOfItems, lengthOfItems, outputLengthNextStep, manLength):
    output = []

    stringForCommand = '0' + str(lengthOfItems) + 'b'

    for i in range(numberOfItems): #ide od 0 do 255 - po defaultu
        output.append(format(random.getrandbits(8),stringForCommand))
        validationExp = int(output[-1][-lengthOfItems:-manLength],2)
 #       if validationExp == 0: #ovo stavljam da bi mi eksponent uvijek bio barem 1 (a ne 0 - provjeriti s Antom)
 #           output[-1] = "00001" + output[-1][-manLength:]
 #       elif validationExp > outputLengthNextStep - manLength: #ovo proizlazi iz uvjeta da na kraju ukupno imamo 25 bitova (stoga eskponent ne moze bit veci od u nasem slucaju 22 - tenutno)
 #           output[-1] = "10110" + output[-1][-manLength:]
        if validationExp > outputLengthNextStep - manLength: #ovo proizlazi iz uvjeta da na kraju ukupno imamo 25 bitova (stoga eskponent ne moze bit veci od u nasem slucaju 22 - tenutno)
            output[-1] = "10110" + output[-1][-manLength:]

    return output

#ovdje generiram slucajne shift ulaze (256 * 2bita)
def generateInputShifts(numberOfItems, noOfBits):
    output = []
    for i in range(numberOfItems):
        output.append(format(random.getrandbits(2),'02b'))
    return output

#prekodiranje float2int (stavljam proizvoljan broj max i ulaza)
def f2int(inputData, inputLength, expLength, outputLength): #inputData je lista stringova
    output = []
    for i in range(len(inputData)):
        dummy0String = format(0,'0'+ str(outputLength)+'b')
        tempString = inputData[i]
        Exp = tempString[-inputLength:-inputLength+expLength]
        Man = tempString[-inputLength+expLength:]
        lenDecodedString = int(Exp, 2)
        #if i == 3:
        #    tempString = '00000000'
        #    Exp = '00001'
        #    Man = '101'
        #    lenDecodedString = outputLength - inputLength + expLength

        if lenDecodedString == (outputLength - inputLength + expLength): 
            output.append("1" + Man + dummy0String[-lenDecodedString+1:])
        elif lenDecodedString == 0:
            output.append(dummy0String[0:(outputLength - inputLength + expLength)] + Man)
        elif lenDecodedString == 1:
            output.append(dummy0String[-25+lenDecodedString+3:] + "1" + Man)
        else:
            output.append(dummy0String[-25+lenDecodedString+3:] + "1" + Man + dummy0String[-lenDecodedString+1:])
    return output

#kalibracija dekodiranih vrijednosti (ustvari shiftanje za odredjeni iznos u lijevo)
def calibration(inputData, shiftData, targetLength):
    output = []
    for i in range(len(inputData)):
        temp = int(inputData[i],2)*2** int(shiftData[i],2)
        #output.append(format(int(inputData[i], 2) << int(shiftData[i],2),'0'+str(targetLength) +'b'))
        output.append(format(temp,'0'+str(targetLength) +'b'))
        
    return output

#ovo je sada matrica sumacije po shemi definiranoj sa MATLAB skriptom (NOVO)
def sumMatrixNew(inputData, matrixArc, outputLength):
    output = []
    izlazZaKontrolu = 711
    for i in range(len(matrixArc)): #trenutno ide do 720 (izlaza) - odnosno 719
        sumTemp = 0
        currentArc = matrixArc[i,:] #vadim jedan redak koji predstavlja način zbrajanja (spajanja vrijednosti) za taj izlaz
        for j in range(len(currentArc)): #trenutno ide do 256 (odnosno 255)
            #ovdje trebam za odabrane primjere (0, 28, 53, 711) staviti if petlje i ispisivati samo njihove međurezultate za provjeru
            if currentArc[j] == 0:
                pass
            elif currentArc[j] == 1:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):-3]),2)
                #ovo je dio samo za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(1))
                  print(int(inputData[j],2))
                  print(inputData[j][-len(inputData[j]):-3], '   ', int((inputData[j][-len(inputData[j]):-3]),2))
            elif currentArc[j] == 2:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):-2]),2)
                #ovo je dio za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(2))
                  print(int(inputData[j],2))
                  print(inputData[j][-len(inputData[j]):-2], '   ', int((inputData[j][-len(inputData[j]):-2]),2))
            elif currentArc[j] == 3:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):-2]),2) + int((inputData[j][-len(inputData[j]):-3]),2)
                #ovo je dio za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(3))
                  print(int(inputData[j],2))
                  print(bin(int((inputData[j][-len(inputData[j]):-2]),2) + int((inputData[j][-len(inputData[j]):-3]),2)), '   ', int((inputData[j][-len(inputData[j]):-2]),2) + int((inputData[j][-len(inputData[j]):-3]),2))
            elif currentArc[j] == 4:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):-1]),2)
                #ovaj dio je samo za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(4))
                  print(int(inputData[j],2))
                  print(bin(int((inputData[j][-len(inputData[j]):-1]),2)), '   ', int((inputData[j][-len(inputData[j]):-1]),2))
            elif currentArc[j] == 5:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-2]),2) - int((inputData[j][-len(inputData[j]):-3]),2)
                #ovaj dio je samo za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(5))
                  print(int(inputData[j],2))
                  print(bin(int((inputData[j][-len(inputData[j]):]),2) - (int((inputData[j][-len(inputData[j]):-2]),2) - int((inputData[j][-len(inputData[j]):-3]),2))), '   ', int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-2]),2) - int((inputData[j][-len(inputData[j]):-3]),2))
            elif currentArc[j] == 6:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-2]),2)
                #ovaj dio je samo za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(6))
                  print(int(inputData[j],2))
                  print(bin(int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-2]),2)), '   ' ,int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-2]),2))
            elif currentArc[j] == 7:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-3]),2)
                #ovaj dio je samo za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(7))
                  print(int(inputData[j],2))
                  print(bin(int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-3]),2)), '   ', int((inputData[j][-len(inputData[j]):]),2) - int((inputData[j][-len(inputData[j]):-3]),2))
            if currentArc[j] == 8:
                sumTemp = sumTemp + int((inputData[j][-len(inputData[j]):]),2)
                #ovaj dio je samo za testiranje
                if i == izlazZaKontrolu:
                  print(j)
                  print('Broj osmina za ovaj ulaz je: ' + str(8))
                  print(int(inputData[j],2))
                  print(inputData[j], '   ', int((inputData[j][-len(inputData[j]):]),2))
        output.append(format(sumTemp,'0' + str(outputLength) + 'b'))
        #ovo je samo za testiranje
        if i == izlazZaKontrolu:
          print('Suma pri danoj arhitekturi je: ' + str(sumTemp))
    return output

#ovo je dio gdje racunam ukupnu sumu (funkcija vracam samo rezultat zbrajanja a ceE dio ce se uzeti iz odgovarajuceg Arraya kada bude trealo)
def totalEnergySums(inputData, outputLength):
    output = []
    duljina = int(len(inputData)/2)
    for i in range(duljina):
        output.append(format(int(inputData[i],2) + int(inputData[i+duljina],2),'0' + str(outputLength) + 'b'))
    return output

#ovo je dio gdje se dobacuje odredjeni broj bitova da bi se dobila trazena duljina bitova (trenutno 19 ali se potencijalno moze promijeniti). Izlaz je takav da ide prvo 360ceE suma pa zatim 360 totalSUM (ocekuje i takav ulaz).
def trimmSummationsNew(inputData, desiredLength):
    output = []
    tempInput = inputData.copy()   
    for i in range(len(tempInput)):
        currentLen = len(tempInput[i])
        diffLen = currentLen - desiredLength
        if diffLen < 0:
            return "Negative length. Check desired length!"
        else:
            output.append(tempInput[i][-len(tempInput[i]):-diffLen])
    return output

#ovo je dio koji radi prekodiranje iz int u float
def int2f(inputData, expLength, outputLength): #inputData je lista stringova
    output = []
    #inputData[1] = '0000000000000010000' #ovo je da testiram prva dva kraka IF petlje jer se bas cesto ne javljaju
    for i in range(len(inputData)):
        tempIndices = [x.start() for x in re.finditer('1', inputData[i])]
        if tempIndices:
            firstNumber = len(inputData[i]) - tempIndices[0] - 1
            if firstNumber<4:
                newExp = '0000'
                newMan = inputData[i][-4:]
                #print('*****POSEBNO1********')
                #print(firstNumber)
                #print(newExp)
                #print(newMan)
            elif firstNumber == 4:
                newExp = '0001'
                newMan = inputData[i][-4:]
                #print('*****POSEBNO2********')
                #print(firstNumber)
                #print(newExp)
                #print(newMan)
            else:
                newExp = format(firstNumber-3,'0' + str(expLength) + 'b') 
                newMan = inputData[i][tempIndices[0]+1:tempIndices[0]+5]
            output.append(newExp + newMan)
        else:
            output.append(format(0,'0' + str(outputLength) + 'b'))
    return output

#ovo je dio koji pretvara *.vh arhitekturu dobivenu iz Matlab skripte u array s kojim se može raditi u Pythonu
def vhArchInputToArray(inputFileName, output_size, input_size): #inputData je lista stringova
    output = np.zeros((output_size, input_size))
    f = open(inputFileName, 'r')
    lines = f.readlines()
    counter = -1 
    counter_preamble = 5 #jer mi ono meni zanimljivo ide od 6 (odnosno 5-og indeksiranog) retka
    for item in lines:
        counter = counter + 1
        if counter >= 5:
            #counter = counter + 1
            start_index = item.find('*/') + 7 #7 zato jer je to konstanta koju se vidi iz datoteka
            tempString = item[start_index:] #prije bilo 20 - ovo bi trebalo u nekom trenutku fiksirati
            tempString_variable = tempString.strip().split(",")
            tempString_variable = list(filter(None, tempString_variable))
            tempFlag = True

            if len(tempString_variable)>1:
                counter1 = 1
                for i in range(0,int(tempString_variable[0])):
                    output[counter-counter_preamble,int(tempString_variable[counter1])] = int(tempString_variable[counter1+1])                          
                    counter1 = counter1 + 2
    return output

def vhArchValidation(inputArchArray, output_size, input_size): #nije najefikasnije napisano ali mi daje bolju kontrolu nad pojedinim dijelovima provjere
    validationArray = np.zeros((1,input_size))
    for i in range(0,input_size):
        tempSum = 0
        for j in range(0,output_size):
            tempSum = tempSum + inputArchArray[j,i]
        
        if tempSum != 8:
            print("Something is wrong with the architecture. Please re-check it and try again!")
            raise SystemExit(0)
        validationArray[0,i] = tempSum
    print("Architecture file verified sucesfully!")

    return


#vadim parametre arhitehture iz *.vh datoteke
def getParametersFromVhFile(inputFileName):
    f = open(inputFileName, 'r')
    lines = f.readlines()
    
    input_line = lines[1]
    output_line = lines[2]

    in_num = ""

    flag_current_digit = False
    flag_current_alpha = False
    flag_last_digit = False
    flag_last_alpha = False

    flag_start_condition = False
    flag_stop_condition = False

    firstTime = False

    for element in input_line:
        if element.isdigit() == True:
            flag_current_digit = True
            flag_current_alpha = False
            if firstTime == False:
                firstTime = True
        else:
            flag_current_digit = False
            flag_current_alpha = True
        
        if flag_current_digit == True and flag_last_alpha == True and firstTime == True:
            flag_start_condition = True
        if flag_current_alpha == True and flag_last_digit == True and firstTime == True:
            firstTime = False
            flag_stop_condition = True
        
        if flag_start_condition == True and flag_stop_condition == False:
            in_num = in_num + element

        flag_last_alpha = flag_current_alpha
        flag_last_digit = flag_current_digit  


    out_num = ""

    flag_current_digit = False
    flag_current_alpha = False
    flag_last_digit = False
    flag_last_alpha = False

    flag_start_condition = False
    flag_stop_condition = False

    firstTime = False

    for element in output_line:
        if element.isdigit() == True:
            flag_current_digit = True
            flag_current_alpha = False
            if firstTime == False:
                firstTime = True
        else:
            flag_current_digit = False
            flag_current_alpha = True
        
        if flag_current_digit == True and flag_last_alpha == True and firstTime == True:
            flag_start_condition = True
        if flag_current_alpha == True and flag_last_digit == True and firstTime == True:
            firstTime = False
            flag_stop_condition = True
        
        if flag_start_condition == True and flag_stop_condition == False:
            out_num = out_num + element

        flag_last_alpha = flag_current_alpha
        flag_last_digit = flag_current_digit
    #print(out_num)  

    return int(in_num), int(out_num)




#********************************************
#***************************************
#****************************
#***************
#GLAVNI DIO KODA GDJE POZIVAM FUNKCIJE
#***************
#****************************
#***************************************
#********************************************
def main(fileName_CE_E,fileName_CE_H):
    os.chdir('../inputs')
    #ucitavam podatke iz Matlaba koji su generirani sa skriptom za Vivado, ali daju i MAT otput za ovaj testbench
    #U DRUGOJ VERZIJI - ucitavam *.vh file koji sadrzi odgovrajuci human redable format (HRF) koji se koristi i za kod zbog neefikasnog binarnog kodiranja kada govorimo o osminama
    #ime je za sada hard-kodirano ali to kada sve istestiram za prvu verziju onda cu promijeniti
    
    #fileName_CE_E = 'CE_E_13_v6.vh'  # matrica arhitekture za CE_E ulaze
    #fileName_CE_H = 'CE_H_13_v6.vh'  # matrica arhitekture za CE_H ulaze

    #Definiram koliko ulaza ima na svakom od CE_E i CE_H "kanala" - za sada polazim od pretpostavke da ih ne može biti više od 256 (u budućnosti će biti i do par tisuća). Ovo je ujedno i broj shift bitova koji će se generirati za svaki kanal
    #ovo trebam napraviti tako da ucitam file i onda iz drugog retka izvucem brojeve (sada sam ih rucno unio temeljem *.vh datoteka koje mi je Ante dao)
    #in_E_num = 70
    #in_H_num = 62

    #out_E_num = 440
    #out_H_num = 49

    in_E_num, out_E_num = getParametersFromVhFile(fileName_CE_E)
    in_H_num, out_H_num = getParametersFromVhFile(fileName_CE_H)

    #ovdje definiram broj bunch crossinga odnosno koliko redaka ce imati izlazne datoteke (sami broj izlaznih datoteka ostaje isit). Sve se radi za istu sumatorsku konfiguraciju, samo se mijenjaju ulazni podaci
    nBunch = 5
    filesCreatedFlag = False #izgleda da postoji + parametar koji ovo izbjegava - provjeriti

    #u ovoj matrici je nacin zbrajanja tj. spajanja ulaza sklopa na ulaze sumatora a i dalje na izlaze - u biti se koristi kod bloka sum_matrix(_v3)
    matVariable_CE_E = vhArchInputToArray(fileName_CE_E, out_E_num, in_E_num)
    matVariable_CE_H = vhArchInputToArray(fileName_CE_H, out_H_num, in_H_num)


    #ovo funkcija nije nužna za ispravan rad sklopa, ali provjerava da li su sve osmine za svaki od 256 ulaza raspojdeljene po izlazima, i ako nisu prekida izvođene i javlja grešku
    #funkcija za dodatnu provjeru ispravnosti arhitekture (prvenstveno MATLAB skripte, ali i funkcije vhArchToArray koja je ovdje napisana)
    #vhArchValidation(matVariable_CE_E, out_E_num, in_E_num)  #ZA SADA IZOSTAVLJAM JER MI SE ARHITEKTURA PROMIJENILA PA MI PRETPOSTAVKE VISE NE VRIJEDE I OVO FAILA
    #vhArchValidation(matVariable_CE_H, out_E_num, in_E_num)

    #generiram ulaze 
    #glavni ulaz je 256 8-bitnih ulaza (5 bitova je eksponent a 3 bita su mantisa) - ove stvari trebam snimiti u datoteku da Ante zna ponoviti test
    inputArray_CE_E = generateInputEnergies(in_E_num,8,25,3)
    inputArray_CE_H = generateInputEnergies(in_H_num,8,25,3)

    #generiram shift bitove
    shiftArray_CE_E = generateInputShifts(in_E_num,2)
    shiftArray_CE_H = generateInputShifts(in_H_num,2)

    #sada radim Float2Int prekodiranje
    decodedInputArray_CE_E = f2int(inputArray_CE_E, 8, 5, 25)
    decodedInputArray_CE_H = f2int(inputArray_CE_H, 8, 5, 25)

    #sada radim kalibraciju odnosno shiftanje
    calibtratedInputArray_CE_E = calibration(decodedInputArray_CE_E, shiftArray_CE_E, 28)
    calibtratedInputArray_CE_H = calibration(decodedInputArray_CE_H, shiftArray_CE_H, 28)

    #sada radim sumaciju 
    summedValues_CE_E = sumMatrixNew(calibtratedInputArray_CE_E, matVariable_CE_E, 32)
    summedValues_CE_H = sumMatrixNew(calibtratedInputArray_CE_H, matVariable_CE_H, 32)

    #sada radim trimming
    trimmedSums_CE_E = trimmSummationsNew(summedValues_CE_E, 19)
    trimmedSums_CE_H = trimmSummationsNew(summedValues_CE_H, 19)

    #sada radim pretvaranje u float
    outputValues_CE_E = int2f(trimmedSums_CE_E, 4, 8)
    outputValues_CE_H = int2f(trimmedSums_CE_H, 4, 8)


    #snimam sve u fileove sa bazom naziva fileName i onda dodajem nastavke ovisno sto snimam
    #konvertiram u dekadski brojevni sustav
    inputArrayDec_CE_E = []
    shiftArrayDec_CE_E = []
    inputArrayDec_CE_H = []
    shiftArrayDec_CE_H = []
    decodedInputArrayDec_CE_E = []
    decodedInputArrayDec_CE_H = []
    calibtratedInputArrayDec_CE_E = []
    calibtratedInputArrayDec_CE_H = []
    for i in range(len(inputArray_CE_E)):
        inputArrayDec_CE_E.append(int(inputArray_CE_E[i],2))
        shiftArrayDec_CE_E.append(int(shiftArray_CE_E[i],2))
        decodedInputArrayDec_CE_E.append(int(decodedInputArray_CE_E[i],2))
        calibtratedInputArrayDec_CE_E.append(int(calibtratedInputArray_CE_E[i],2))
    for i in range(len(inputArray_CE_H)):
        inputArrayDec_CE_H.append(int(inputArray_CE_H[i],2))
        shiftArrayDec_CE_H.append(int(shiftArray_CE_H[i],2))
        decodedInputArrayDec_CE_H.append(int(decodedInputArray_CE_H[i],2))
        calibtratedInputArrayDec_CE_H.append(int(calibtratedInputArray_CE_H[i],2))

    summedValuesDec_CE_E = []
    summedValuesDec_CE_H = []
    trimmedSumsDec_CE_E = []
    outputValuesDec_CE_E = []
    trimmedSumsDec_CE_H = []
    outputValuesDec_CE_H = []
    for i in range(len(summedValues_CE_E)):
        summedValuesDec_CE_E.append(int(summedValues_CE_E[i],2))
        trimmedSumsDec_CE_E.append(int(trimmedSums_CE_E[i],2))
        outputValuesDec_CE_E.append(int(outputValues_CE_E[i],2))
    for i in range(len(summedValues_CE_H)):
        summedValuesDec_CE_H.append(int(summedValues_CE_H[i],2))
        trimmedSumsDec_CE_H.append(int(trimmedSums_CE_H[i],2))
        outputValuesDec_CE_H.append(int(outputValues_CE_H[i],2))


    #***********SNIMAM ZA CE_E*********************
    #with open(fileName_CE_E + '_inputData_CE_E' + '.txt', 'w') as f:
    #    f.writelines("%s" %line for line in inputArrayDec_CE_E)

    #ulazni podaci
    """
    with open(fileName_CE_E + '_inputData_CE_E_1' + '.txt', 'w') as f:
        for i in range (len(inputArrayDec_CE_E)):
            if i == len(inputArrayDec_CE_E)-1:
                f.write(str(inputArrayDec_CE_E[i]))
            else:
                f.write(str(inputArrayDec_CE_E[i]) + ', \n')
                
    #shift bitovi
    with open(fileName_CE_E + '_shiftData_CE_E_1' + '.txt', 'w') as f:
        for i in range (len(shiftArrayDec_CE_E)):
            if i == len(shiftArrayDec_CE_E)-1:
                f.write(str(shiftArrayDec_CE_E[i]))
            else:
                f.write(str(shiftArrayDec_CE_E[i]) + ', \n')

    #dekodirani podaci
    with open(fileName_CE_E + '_decodedData_CE_E_1' + '.txt', 'w') as f:
        for i in range (len(decodedInputArrayDec_CE_E)):
            if i == len(decodedInputArrayDec_CE_E)-1:
                f.write(str(decodedInputArrayDec_CE_E[i]))
            else:
                f.write(str(decodedInputArrayDec_CE_E[i]) + ', \n')

    #kalibrirani podaci
    with open(fileName_CE_E + '_calibratedData_CE_E_1' + '.txt', 'w') as f:
        for i in range (len(calibtratedInputArrayDec_CE_E)):
            if i == len(calibtratedInputArrayDec_CE_E)-1:
                f.write(str(calibtratedInputArrayDec_CE_E[i]))
            else:
                f.write(str(calibtratedInputArrayDec_CE_E[i]) + ', \n')

    #sumirani podaci
    with open(fileName_CE_E + '_sumsData_CE_E_1' + '.txt', 'w') as f:
        for i in range (len(summedValuesDec_CE_E)):
            if i == len(summedValuesDec_CE_E)-1:
                f.write(str(summedValuesDec_CE_E[i]))
            else:
                f.write(str(summedValuesDec_CE_E[i]) + ', \n')


    #podaci s totalnom energijom - trenutno ne snimam
    #with open(fileName + '_totalData' + '.txt', 'w') as f:
    #    for i in range (len(totalSumValuesJointDec)):
    #        if i == len(trimmedSumsDec)-1:
    #            f.write(str(totalSumValuesJointDec[i]))
    #        else:
    #            f.write(str(totalSumValuesJointDec[i]) + ',')

    #trimani podaci
    with open(fileName_CE_E + '_trimData_CE_E_1' + '.txt', 'w') as f:
        for i in range (len(trimmedSumsDec_CE_E)):
            if i == len(trimmedSumsDec_CE_E)-1:
                f.write(str(trimmedSumsDec_CE_E[i]))
                #f.write(str(trimmedSums_CE_E[i]))
            else:
                f.write(str(trimmedSumsDec_CE_E[i]) + ', \n')
                #f.write(str(trimmedSums_CE_E[i]) + ', \n')
    """
    #izlazni podaci -spremamo ih u mapu outputs
    with open('../outputs/' + fileName_CE_E + '_outputData_CE_E_1' + '.txt', 'w') as f: 
        for i in range (len(outputValuesDec_CE_E)):
            if i == len(outputValuesDec_CE_E)-1:
                f.write(str(outputValuesDec_CE_E[i]))
            else:
                f.write(str(outputValuesDec_CE_E[i]) + ', \n')


    #***********SNIMAM ZA CE_H*********************
    #with open(fileName_CE_E + '_inputData_CE_E' + '.txt', 'w') as f:
    #    f.writelines("%s" %line for line in inputArrayDec_CE_E)

    #ulazni podaci
    """
    with open(fileName_CE_H + '_inputData_CE_H_1' + '.txt', 'w') as f:
        for i in range (len(inputArrayDec_CE_H)):
            if i == len(inputArrayDec_CE_H)-1:
                f.write(str(inputArrayDec_CE_H[i]))
            else:
                f.write(str(inputArrayDec_CE_H[i]) + ', \n')

    #shift bitovi
    with open(fileName_CE_H + '_shiftData_CE_H_1' + '.txt', 'w') as f:
        for i in range (len(shiftArrayDec_CE_H)):
            if i == len(shiftArrayDec_CE_H)-1:
                f.write(str(shiftArrayDec_CE_H[i]))
            else:
                f.write(str(shiftArrayDec_CE_H[i]) + ', \n')

    #dekodirani podaci
    with open(fileName_CE_H + '_decodedData_CE_H_1' + '.txt', 'w') as f:
        for i in range (len(decodedInputArrayDec_CE_H)):
            if i == len(decodedInputArrayDec_CE_H)-1:
                f.write(str(decodedInputArrayDec_CE_H[i]))

            else:
                f.write(str(decodedInputArrayDec_CE_H[i]) + ', \n')

    #kalibrirani podaci
    with open(fileName_CE_H + '_calibratedData_CE_H_1' + '.txt', 'w') as f:
        for i in range (len(calibtratedInputArrayDec_CE_H)):
            if i == len(calibtratedInputArrayDec_CE_H)-1:
                f.write(str(calibtratedInputArrayDec_CE_H[i]))
            else:
                f.write(str(calibtratedInputArrayDec_CE_H[i]) + ', \n')

    #sumirani podaci
    with open(fileName_CE_H + '_sumsData_CE_H_1' + '.txt', 'w') as f:
        for i in range (len(summedValuesDec_CE_H)):
            if i == len(summedValuesDec_CE_H)-1:
                f.write(str(summedValuesDec_CE_H[i]))
            else:
                f.write(str(summedValuesDec_CE_H[i]) + ', \n')

    #podaci s totalnom energijom - trenutno ne snimam
    #with open(fileName + '_totalData' + '.txt', 'w') as f:
    #    for i in range (len(totalSumValuesJointDec)):
    #        if i == len(trimmedSumsDec)-1:
    #            f.write(str(totalSumValuesJointDec[i]))
    #            #f.write(str(totalSumValuesJoint[i]))
    #        else:
    #            f.write(str(totalSumValuesJointDec[i]) + ',')
    #            #f.write(str(totalSumValuesJoint[i]) + ', \n')

    #trimani podaci
    with open(fileName_CE_H + '_trimData_CE_H_1' + '.txt', 'w') as f:
        for i in range (len(trimmedSumsDec_CE_H)):
            if i == len(trimmedSumsDec_CE_H)-1:
                f.write(str(trimmedSumsDec_CE_H[i]))
            else:
                f.write(str(trimmedSumsDec_CE_H[i]) + ', \n')
    """
    #izlazni podaci
    with open('../outputs/' + fileName_CE_H + '_outputData_CE_H_1' + '.txt', 'w') as f:
        for i in range (len(outputValuesDec_CE_H)):
            if i == len(outputValuesDec_CE_H)-1:
                f.write(str(outputValuesDec_CE_H[i]))
            else:
                f.write(str(outputValuesDec_CE_H[i]) + ', \n')