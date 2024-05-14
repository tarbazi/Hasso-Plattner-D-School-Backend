import csv
import random

months = ["June22.csv","July22.csv","August22.csv","September22.csv","October22.csv","November22.csv","December22.csv","January23.csv","February23.csv","March23.csv","April23.csv","May23.csv","June23.csv","July23.csv","August23.csv","September23.csv","October23.csv"]
numDays = [30,31,31,30,31,30,31,31,28,31,30,31,30,31,31,30,31]

calender = ["2022-06-", "2022-07-", "2022-08-", "2022-09-", "2022-10-", "2022-11-", "2022-12-", "2023-01-", "2023-02-", "2023-03-", "2023-04-","2023-05-","2023-06-","2023-07-","2023-08-","2023-09-","2023-10-"]
index = -1

def solarProduction(hourArr):
    temp = [100, 150, 300, 300, 400, 400, 400, 300, 300, 150, 100]
    temp1 = [50, 100, 200, 200, 250, 250, 250, 200, 200, 100, 50]
    for i in range(6, 17):
        for j in range(12):
            val = random.randint(temp1[i-6], temp[i-6])
            hourArr[i][j] = val/12
            
    return hourArr

def energyConsumption(hourArr):
    temp0 = [150, 400, 400, 400, 400, 400, 400, 400, 400, 550, 550, 550, 550, 400, 400, 400, 400, 400, 400, 200, 50]
    temp1 = [200, 500, 500, 600, 600, 600, 600, 600, 600, 800, 800, 800, 800, 600, 600, 600, 600, 600, 600, 400, 100]
    for i in range(21):
        for j in range(12):
            val = random.randint(temp0[i], temp1[i])
            hourArr[i][j] = val/120
            
    return hourArr

def waterUsage(hourArr):
    for i in range(24):
        for j in range(12):
            val = random.randint(0, 100)
            hourArr[i][j] = val/12
            
    return hourArr

def makeDaily(dailyArr):
    dailyData = [0]*24
    index = 0
    for i in dailyArr:
        dailyData[index] = sum(i)
        index += 1
    return dailyData
    
s3 = open("./Dummy/SolarYearlyData.csv","a",newline="")

c3 = open("./Dummy/ConsumptionYearlyData.csv","a",newline="")
w3 = open("./Dummy/WaterYearlyData.csv","a",newline="")

rc3 = open("./Live/RealConsumptionYearlyData.csv","a",newline="")
rw3 = open("./Live/RealWaterYearlyData.csv","a",newline="")

solarData3 = [0]*17

consumptionData3 = [0]*17
waterData3 = [0]*17

rconsumptionData3 = [0]*17
rwaterData3 = [0]*17

writerS3 = csv.writer(s3)

writerC3 = csv.writer(c3)
writerW3 = csv.writer(w3) 

writerRC3 = csv.writer(rc3)
writerRW3 = csv.writer(rw3) 

for i in months:
    index += 1
    
    s = open("./Dummy/SolarHourlyData"+i,"a",newline="")
    
    c = open("./Dummy/ConsumptionHourlyData"+i,"a",newline="")
    w = open("./Dummy/WaterHourlyData"+i,"a",newline="")
    
    rc = open("./Live/ConsumptionHourlyData"+i,"a",newline="")
    rw = open("./Live/WaterHourlyData"+i,"a",newline="")    
    
    s1 = open("./Dummy/SolarDailyData"+i,"a",newline="")
    
    c1 = open("./Dummy/ConsumptionDailyData"+i,"a",newline="")
    w1 = open("./Dummy/WaterDailyData"+i,"a",newline="")
    
    rc1 = open("./Live/ConsumptionDailyData"+i,"a",newline="")
    rw1 = open("./Live/WaterDailyData"+i,"a",newline="")    
    
    s2 = open("./Dummy/SolarMonthlyData"+i,"a",newline="")
    
    c2 = open("./Dummy/ConsumptionMonthlyData"+i,"a",newline="")
    w2 = open("./Dummy/WaterMonthlyData"+i,"a",newline="")    
    
    rc2 = open("./Live/ConsumptionMonthlyData"+i,"a",newline="")
    rw2 = open("./Live/WaterMonthlyData"+i,"a",newline="")        
    
    writerS = csv.writer(s)
    
    writerC = csv.writer(c)
    writerW = csv.writer(w)
    
    writerRC = csv.writer(rc)
    writerRW = csv.writer(rw)    
    
    writerS1 = csv.writer(s1)
    
    writerC1 = csv.writer(c1)
    writerW1 = csv.writer(w1)
    
    writerRC1 = csv.writer(rc1)
    writerRW1 = csv.writer(rw1)    
    
    writerS2 = csv.writer(s2)
    
    writerC2 = csv.writer(c2)
    writerW2 = csv.writer(w2)
    
    writerRC2 = csv.writer(rc2)
    writerRW2 = csv.writer(rw2)    
    
    solarData2 = [0]*numDays[index]
    
    consumptionData2 = [0]*numDays[index]
    waterData2 = [0]*numDays[index]
    
    rconsumptionData2 = [0]*numDays[index]
    rwaterData2 = [0]*numDays[index]    
       
    for j in range(1, numDays[index]+1):
        date = calender[index]+str(j)
        hoursData = [[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12,[0]*12]
        
        solarData = str(solarProduction(hoursData))
        
        consumptionData = str(energyConsumption(hoursData))
        waterData = str(waterUsage(hoursData))
        
        rconsumptionData = str(energyConsumption(hoursData))
        rwaterData = str(waterUsage(hoursData))        
        
        solarData1 = str(makeDaily(eval(solarData)))
        
        consumptionData1 = str(makeDaily(eval(consumptionData)))
        waterData1 = str(makeDaily(eval(waterData)))
        
        rconsumptionData1 = str(makeDaily(eval(consumptionData)))
        rwaterData1 = str(makeDaily(eval(waterData)))        
        
        solarData2[j-1] = sum(eval(solarData1))
        
        consumptionData2[j-1] = sum(eval(consumptionData1))
        waterData2[j-1] = sum(eval(waterData1))
        
        rconsumptionData2[j-1] = sum(eval(rconsumptionData1))
        rwaterData2[j-1] = sum(eval(rwaterData1))        
        
        solarData3[index] += sum(eval(solarData1))
        consumptionData3[index] += sum(eval(consumptionData1))
        waterData3[index] += sum(eval(waterData1))       
        
        rowS = (calender[index]+str(j), solarData)
        
        rowC = (calender[index]+str(j), consumptionData)
        rowW = (calender[index]+str(j), waterData)
        
        rowRC = (calender[index]+str(j), rconsumptionData)
        rowRW = (calender[index]+str(j), rwaterData)        
        
        rowS1 = (calender[index]+str(j), solarData1)
        
        rowC1 = (calender[index]+str(j), consumptionData1)
        rowW1 = (calender[index]+str(j), waterData1) 
        
        rowRC1 = (calender[index]+str(j), rconsumptionData1)
        rowRW1 = (calender[index]+str(j), rwaterData1)         
        
        writerS.writerow(rowS)
        
        writerC.writerow(rowC)
        writerW.writerow(rowW)
        
        writerRC.writerow(rowRC)
        writerRW.writerow(rowRW)        
        
        writerS1.writerow(rowS1)
        
        writerC1.writerow(rowC1)
        writerW1.writerow(rowW1)
        
        writerRC1.writerow(rowRC1)
        writerRW1.writerow(rowRW1)        
        
    rowS2 = (calender[index]+".csv", solarData2)
    
    rowC2 = (calender[index]+".csv", consumptionData2)
    rowW2 = (calender[index]+".csv", waterData2)
    
    rowRC2 = (calender[index]+".csv", rconsumptionData2)
    rowRW2 = (calender[index]+".csv", rwaterData2)    
    
    writerS2.writerow(rowS2)
    
    writerC2.writerow(rowC2)
    writerW2.writerow(rowC2)
    
    writerRC2.writerow(rowRC2)
    writerRW2.writerow(rowRC2)    
        
rowS3 = (solarData3)

rowC3 = (consumptionData3)
rowW3 = (waterData3)

rowRC3 = (rconsumptionData3)
rowRW3 = (rwaterData3)

writerS1.writerow(rowS1)

writerC1.writerow(rowC1)
writerW1.writerow(rowW1)

writerRC1.writerow(rowRC1)
writerRW1.writerow(rowRW1)

writerS3.writerow(rowS3)

writerC3.writerow(rowC3)
writerW3.writerow(rowW3)

writerRC3.writerow(rowRC3)
writerRW3.writerow(rowRW3)

s.close()
c.close()
w.close()
rc.close()
rw.close()

s1.close()
c1.close()
w1.close()
rc1.close()
rw1.close()

s2.close()
c2.close()
w2.close()
rc2.close()
rw2.close()

s3.close()
c3.close()
w3.close()
rc3.close()
rw3.close()