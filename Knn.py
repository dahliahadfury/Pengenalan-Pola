#author : yurdhafahila

import KMeans as km
import csv
from collections import OrderedDict
import operator

# data training berasal dari data yang telah dilakukan clustering dengan KMeans
# pada data ini yang digunakan sebagai fitur hanya: duration, stepcount, setcount, remcount, c1count, c2count, c3count, c4count, c5count, c6count, uniqcount, errcount
dataTraining = km.bestData
keyFitur = [ "duration", "stepcount", "setcount", "remcount", "c1count", "c2count", "c3count", "c4count", "c5count", "c6count", "uniqcount", "errcount"]

def readMyFile(filecsv):
    data=[]
    with open(filecsv, mode='r', encoding='utf8') as csvFile:

        #delimeter file csv dengan ;
        csvReader = csv.DictReader(csvFile, delimiter=';')
        line_count = 0

        for row in csvReader:
            data.append(row)
            line_count += 1
        print(f'Processed read {line_count} lines.')

    return data

def manualisasi(data):
    tempMax = []
    tempMin = []
    for i in range(len(keyFitur)):
        temp = OrderedDict()
        temp3 = OrderedDict()
        temp2 = []
        for row in data:
            temp2.append(float(row[keyFitur[i]]))        
        temp[keyFitur[i]] = max(temp2)
        temp3[keyFitur[i]] = min(temp2)        
        tempMax.append(temp.copy())
        tempMin.append(temp3.copy())
    for i in range(len(data)): #40 lines
        for j in range(len(keyFitur)):
            data[i][keyFitur[j]] = (float(data[i][keyFitur[j]]) - tempMin[j][keyFitur[j]]) / (tempMax[j][keyFitur[j]] - tempMin[j][keyFitur[j]])
    return(data)


def euclideanDistance(dataTraining, dataTesting):
    result=[]     
    distance =0

    for i in range(len(dataTraining)):
        data= OrderedDict()
        data["id"] =  dataTraining[i]["id"]
        data["Kelompok"] = dataTraining[i]["Kelompok"]

        for j in range(len(keyFitur)):
            distance += (abs(float(dataTesting[keyFitur[j]])-float(dataTraining[i][keyFitur[j]]))**2)
        distance = distance**0.5
        data["distance"] = distance
        result.append(data)

    return result
    
# Function returns N largest elements 
def Nminelements(list1, N): 
    final_list = [] 
  
    for i in range(0, N):  
        min1 = max(list1)
          
        for j in range(len(list1)):      
            if list1[j] < min1: 
                min1 = list1[j]; 
                  
        list1.remove(min1); 
        final_list.append(min1) 
          
    return final_list 
  
def getKelompok(data, N):
    if N > len(data) or N < 0:
        return "jumlah voting tidak sesuai"
        
    result=[]
    distance=[]
    minDis=[]
    temp = OrderedDict()

    for i in range(len(data)):
        distance.append(data[i]["distance"])  

    minDis=Nminelements(distance, N)    

    for i in range(len(minDis)):
        for row in data:
            if minDis[i] == row["distance"]:                
                temp["id"] = row["id"]
                temp["distance"] = row["distance"]
                temp["Kelompok"] = row["Kelompok"]
                result.append(temp.copy())        

    return result

def setKelompok(data):
    Kel={}
    for row in data:
        if row["Kelompok"] in Kel:
            Kel[row["Kelompok"]]+=1
        else:
            Kel[row["Kelompok"]]=1
    return Kel

#DATA TRAINING
print("DATA TRAINING")
print(list(dataTraining[0].keys()))
for data in dataTraining:
	print(list(data.values()))

#open file
#DATA TESTING
print("DATA TESTING")
dataTesting = readMyFile('level1_asg2.csv')
print(list(dataTesting[0].keys()))
for data in dataTesting:
	print(list(data.values()))
dataTesting = manualisasi(dataTesting)


dataTraining = manualisasi(dataTraining)

for i in range(len(dataTesting)):
    eucDisData1 = euclideanDistance(dataTraining, dataTesting[i])
    gk = getKelompok(eucDisData1, 3)
    vote = setKelompok(gk)
    bestVote = max(vote)
    dataTesting[i]["Kelompok"]= bestVote
    # print(bestVote)

# print(dataTesting)
# print(dataTesting["Kelompok"])

#HASIL
print("HASIL DATA TESTING")
print(list(dataTesting[0].keys()))
for data in dataTesting:
	print(list(data.values()))