import csv
import datetime

import math

def storeCSVasDict(readFile):
    dic = {}
    filePtr = open(readFile)
    reader = csv.reader(filePtr)
    header = next(reader)
    itemIndex = 0
    BorderIndex = 0 
    DateIndex = 0 
    MeasureIndex = 0
    ValueIndex = 0
    for item in header:
        if item == 'Border':
            BorderIndex = itemIndex
        if item == 'Date':
            DateIndex = itemIndex
        if item == 'Measure':
            MeasureIndex = itemIndex
        if item == 'Value':
            ValueIndex = itemIndex
        itemIndex += 1

    for row in reader:
        if row:
            dt = datetime.datetime.strptime(row[DateIndex], '%m/%d/%Y %I:%M:%S %p')
            key = tuple([row[BorderIndex], dt.year, dt.month, row[MeasureIndex]])
            if key not in dic:
                dic[key] = [int(row[ValueIndex]),0]
            else:
                dic[key][0] += int(row[ValueIndex])
    filePtr.close()
    return dic

def stringToTime(date_string):
    dt = datetime.datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p')
    return dt.timestamp()

def roundToWhole(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)



def storeTotalCrossing(dic):
    for i in dic:
        for j in dic:
            if (i[0] == j[0] and i[3]==j[3] and i[1]>=j[1] and i[2]>j[2]):
                dic[i][1] += (dic[j][0])
    return dic




    
def outputReport(dic):
    with open('report.csv','w') as outfile:
        writer=csv.writer(outfile, delimiter=',',lineterminator='\n',)
        writer.writerow(["Border","Date","Measure","Value","Average"])
        for i in sorted(dic, key=lambda x: (x[1],x[2],dic[x],x[3],x[0]), reverse=True):
            if i[2] > 10:
                monthStr = '0' + str(i[2])
            else:
                monthStr = '0' + str(i[2])
            yearStr = str(i[1])

            Date = monthStr + '/01/' + yearStr + ' 12:00:00 AM'
            if i[2] != 1:
                Average = roundToWhole(dic[i][1]/float(i[2]-1))
            else: 
                Average = 0
            row = [i[0], Date, i[3], str(dic[i][0]),str(Average) ]
    
            writer.writerow(row)

def main():
    dic = storeCSVasDict('Border_Crossing_Entry_Data.csv')
    aggregatedDic = storeTotalCrossing(dic)
    outputReport(aggregatedDic)

if __name__ == '__main__':
    main()

    