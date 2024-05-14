import requests
from requests.auth import HTTPBasicAuth
import datetime 
import calendar
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def getVals(numArr): #Extracts data in the format of the Meteo API and return an array of the values
    a = 0
    outputData = [None]*len(numArr)
    
    for i in numArr:
        outputData[a] = i[1]
        a += 1

    return outputData

def sumNums(numArr): 
    sumNum = 0
    n = len(numArr)
    
    for i in numArr:
        if (i != None):
            sumNum += i
        else:
            n -= 1
            
    if n != 0:
        return round(sumNum, 2)
    else:
        return None
    
@app.route("/hourlyData/<day>/<hourNum>/<powerUnits>", methods=["GET"])
def hourlyData(day, hourNum, powerUnits):
    apiPath = "https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=day&date="
    day = str(day)
    hourNum = int(hourNum)
    myAPI = requests.get(apiPath+day)
    myData = myAPI.json()["chartData"]["data"]
    outputData = getVals(myData[12*hourNum:12*hourNum + 12])
    
    a = 0
    for i in outputData:
        outputData[a] = {"Minute": str(a*5), "value": str(i)}
        a += 1
    
    return jsonify({
        "PowerGeneration": outputData
    })
    
@app.route("/dailyData/<day>/<powerUnits>", methods=["GET"])
def dailyData(day, powerUnits):
    apiPath = "https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=day&date="
    myAPI = requests.get(apiPath+day)
    myData = myAPI.json()["chartData"]["data"]
    
    a = 0
    outputData = [None]*24
      
    for i in range(0, 288, 12):
        outputData[a] = {"Hour": str(a), "value": str(sumNums(getVals(myData[i: i+12])))}
        a += 1
    
    return jsonify({
        "PowerGeneration": outputData
    })

@app.route("/weeklyData/<weeksSunday>/<powerUnits>", methods=["GET"])
def weeklyData(weeksSunday, powerUnits):
    apiPath = "https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=month&date="
    weeksSunday = getSunday(weeksSunday)
    myAPI = requests.get(apiPath+weeksSunday)
    day = int(myAPI.json()["chartData"]["date"].split("-")[2])
    myData = myAPI.json()["chartData"]["data"]
    if (len(myData[day-1:]) < 7):
        tempArr = weeksSunday.split("-")
        
        nextMonth = tempArr[0]+"-"+str(int(tempArr[1])+1)+"-"+tempArr[2]
        myData += requests.get(apiPath+nextMonth).json()["chartData"]["data"]
    
    weeksData = getVals(myData[day-1: day+6])   
    a = 0
    daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
    outputData = [None]*7
    
    
    for i in range(0, 7):
        myData = myAPI.json()["chartData"]["data"]
        outputData[a] = {"Day": daysOfWeek[i], "value": str(weeksData[i])}
        a += 1
        
    return  jsonify({
        "PowerGeneration": outputData
    })
    
@app.route("/monthlyData/<month>/<powerUnits>", methods=["GET"])
def monthlyData(month, powerUnits):
    apiPath = "https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=month&date="
    myAPI = requests.get(apiPath + month + "-01")
    outputData = ["-"]
    dayNum = 1
    monthsData = getVals(myAPI.json()["chartData"]["data"])

    for i in monthsData:
        outputData += [{"Day": str(dayNum), "value": str(i)}]
        dayNum += 1
    
    return jsonify({
        "PowerGeneration": outputData[1:]
    })

@app.route("/yearlyData/<year>/<powerUnits>", methods=["GET"])
def yearlyData(year, powerUnits):
    apiPath = "https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=month&date="
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    outputData = ["-"]*12

    yearTotal = 0
    for i in range(0, 12):
        monthsSum = sumNums(getVals(requests.get(apiPath+year+"-"+str(i+1)+"-01").json()["chartData"]["data"]))
        if monthsSum != None:
            yearTotal += monthsSum
        outputData[i] = {"Month": months[i], "value": str(monthsSum)}

    return  jsonify({
        "Total": yearTotal, "PowerGeneration": outputData
    })

@app.route("/nextDay/<day>/<dir>", methods=["GET"])
def nextDay(day, dir):
    if dir == "1":
        return jsonify({
            "Day" : requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=day&date="+day).json()["chartData"]["next"]
        })
    else:
        return jsonify({
            "Day" : requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=day&date="+day).json()["chartData"]["prev"]
        })

def nextDay1(day, dir):
    if dir == "1":
        return requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=day&date="+day).json()["chartData"]["next"]
    else:
        return requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=day&date="+day).json()["chartData"]["prev"]

@app.route("/nextWeek/<weeksSunday>/<dir>", methods=["GET"])
def nextWeek(weeksSunday, dir):
    if dir == "1":
        weeksSunday = requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=week&date="+weeksSunday).json()["chartData"]["next"]
    else:
        weeksSunday = requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=week&date="+weeksSunday).json()["chartData"]["prev"]
    arr = weeksSunday.split("-")
    if datetime.date(int(arr[0]), int(arr[1]), int(arr[2])).weekday() != 6:
        weeksSunday = None
    return jsonify({
        "Sunday" : weeksSunday
    })

def getSunday(day):
    arr = day.split("-")
    while (datetime.date(int(arr[0]), int(arr[1]), int(arr[2])).weekday() != 6):
        day = str(datetime.date(int(arr[0]), int(arr[1]), int(arr[2]))-datetime.timedelta(days=1))
        arr = day.split("-")
    return day

@app.route("/nextMonth/<month>/<dir>", methods=["GET"])
def nextMonth(month, dir):
    if dir == "1":
        month = requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=month&date="+month).json()["chartData"]["next"]
    else:
        month = requests.get("https://ws.meteocontrol.de/api/sites/C36EM/data/energygeneration?apiKey=gpbgpSav1s&type=month&date="+month).json()["chartData"]["prev"]
    return jsonify({
        "Month" : month
    })

def fileLookup(year, month):
    fileName = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return fileName[int(month)-1]+year[2:]

def makeHourly(fileName, day, hourNum, data):
    file = open(fileName, "r")
    day = int(day.split("-")[2])
    if day < 10:
        fileData = file.readlines()[day-1][13:-4].split("], [")
    else:
        fileData = file.readlines()[day-1][14:-4].split("], [")
    file.close()
    fileData = fileData[int(hourNum)].split(", ")
    
    a = 0
    for i in fileData:
        fileData[a] = {"Minute": str(a*5), "value": i}
        a += 1
    return fileData

@app.route("/dummyHourlyData/<day>/<hourNum>/<powerUnits>")
def dummyHourlyData(day, hourNum, powerUnits):
    year = day.split("-")[0]
    month = day.split("-")[1]
    fileName = fileLookup(year, month)
    SolarFileName = "SolarHourlyData"+fileName+".csv"
    ConsumptionFileName = "ConsumptionHourlyData"+fileName+".csv"
    WaterFileName = "WaterHourlyData"+fileName+".csv"
    solar = makeHourly("./Dummy/"+SolarFileName, day, hourNum, "DummySolarData")
    consumption = makeHourly("./Dummy/"+ConsumptionFileName, day, hourNum, "DummyConsumptionData")
    water = makeHourly("./Dummy/"+WaterFileName, day, hourNum, "DummyWaterData")
    return jsonify({
        "DummyData": { "SolarData": solar, "ConsumptionData": consumption, "WaterData": water}
    })

@app.route("/liveHourlyData/<day>/<hourNum>/<powerUnits>")
def liveHourlyData(day, hourNum, powerUnits):
    year = day.split("-")[0]
    month = day.split("-")[1]
    fileName = fileLookup(year, month)
    ConsumptionFileName = "ConsumptionHourlyData"+fileName+".csv"
    WaterFileName = "WaterHourlyData"+fileName+".csv"
    consumption = makeHourly("./Live/"+ConsumptionFileName, day, hourNum, "DummyConsumptionData")
    water = makeHourly("./Live/"+WaterFileName, day, hourNum, "DummyWaterData")
    return jsonify({
        "LiveData": { "ConsumptionData": consumption, "WaterData": water}
    })

def makeDaily(fileName, day):
    file = open(fileName, "r")
    day = int(day.split("-")[2])
    if day < 10:
        fileData = file.readlines()[day-1][12:-3].split(", ")
    else:
        fileData = file.readlines()[day-1][13:-3].split(", ")
    file.close()
    a = 0
      
    for i in fileData:
        fileData[a] = {"Hour": str(a), "value": i}
        a += 1
    return fileData

@app.route("/dummyDailyData/<day>/<powerUnits>")
def dummyDailyData(day, powerUnits):
    year = day.split("-")[0]
    month = day.split("-")[1]
    fileName = fileLookup(year, month)
    SolarFileName = "SolarDailyData"+fileName+".csv"
    ConsumptionFileName = "ConsumptionDailyData"+fileName+".csv"
    WaterFileName = "WaterDailyData"+fileName+".csv"
    solar = makeDaily("./Dummy/"+SolarFileName, day)
    consumption = makeDaily("./Dummy/"+ConsumptionFileName, day)
    water = makeDaily("./Dummy/"+WaterFileName, day)
    return jsonify({
        "DummyData": { "SolarData": solar, "ConsumptionData": consumption, "WaterData": water}
    })

@app.route("/liveDailyData/<day>/<powerUnits>")
def liveDailyData(day, powerUnits):
    year = day.split("-")[0]
    month = day.split("-")[1]
    fileName = fileLookup(year, month)
    ConsumptionFileName = "ConsumptionDailyData"+fileName+".csv"
    WaterFileName = "WaterDailyData"+fileName+".csv"
    consumption = makeDaily("./Live/"+ConsumptionFileName, day)
    water = makeDaily("./Live/"+WaterFileName, day)
    return jsonify({
        "LiveData": { "ConsumptionData": consumption, "WaterData": water}
    })

def getDays(weeksSunday):
    days = [None]*7
    days[0] = weeksSunday
    for i in range(1, 7):
        days[i] = nextDay1(days[i-1], "1")
        if days[i] == None:
            break

    return days

def forDay(fileName, day):
    file = open(fileName+".csv", "r")
    daysData = file.readline()[15:-3].split(", ")[int(day)-1]
    return daysData

def toJson(arr):
    daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
    outputData = [None]*7
    for i in range(0, 7):
        outputData[i] = {"Day": daysOfWeek[i], "value": arr[i]}
    return outputData

@app.route("/dummyWeeklyData/<weeksSunday>/<powerUnits>")
def dummyWeeklyData(weeksSunday, powerUnits):
    weeksSunday = getSunday(weeksSunday)
    days = getDays(weeksSunday)
    solar = [None]*7
    consumption = [None]*7
    water = [None]*7
    a = 0
    for day in days:
        if day != None:
            year = day.split("-")[0]
            month = day.split("-")[1]
            fileName = fileLookup(year, month)
            solar[a] = forDay("./Dummy/SolarMonthlyData"+fileName, day.split("-")[2])
            consumption[a] = forDay("./Dummy/ConsumptionMonthlyData"+fileName, day.split("-")[2])
            water[a] = forDay("./Dummy/WaterMonthlyData"+fileName, day.split("-")[2])
            a += 1
        else:
            break
    solar = toJson(solar)
    consumption = toJson(consumption)
    water = toJson(water)
    return jsonify({
        "DummyData": { "SolarData": solar, "ConsumptionData": consumption, "WaterData": water}
    })

@app.route("/liveWeeklyData/<weeksSunday>/<powerUnits>")
def liveWeeklyData(weeksSunday, powerUnits):
    weeksSunday = getSunday(weeksSunday)
    days = getDays(weeksSunday)
    consumption = [None]*7
    water = [None]*7
    a = 0
    for day in days:
        year = day.split("-")[0]
        month = day.split("-")[1]
        fileName = fileLookup(year, month)
        consumption[a] = forDay("./Live/ConsumptionMonthlyData"+fileName, day.split("-")[2])
        water[a] = forDay("./Live/WaterMonthlyData"+fileName, day.split("-")[2])
        a += 1
    consumption = toJson(consumption)
    water = toJson(water)
    return jsonify({
        "DummyData": {"ConsumptionData": consumption, "WaterData": water}
    })

def makeMonthly(fileName):
    file = open(fileName, "r")
    fileData = file.readline()[15:-3].split(", ")
    outputData = [None]*len(fileData)
    dayNum = 1

    for i in fileData:
        outputData[dayNum-1]= {"Day": str(dayNum), "value": i}
        dayNum += 1
    return outputData

@app.route("/dummyMonthlyData/<day>/<powerUnits>")
def dummyMonthlyData(day, powerUnits):
    year = day.split("-")[0]
    month = day.split("-")[1]
    fileName = fileLookup(year, month)
    SolarFileName = "./Dummy/SolarMonthlyData"+fileName+".csv"
    ConsumptionFileName = "./Dummy/ConsumptionMonthlyData"+fileName+".csv"
    WaterFileName = "./Dummy/WaterMonthlyData"+fileName+".csv"
    solar = makeMonthly(SolarFileName)
    consumption = makeMonthly(ConsumptionFileName)
    water = makeMonthly(WaterFileName)
    return jsonify({
        "DummyData": { "SolarData": solar, "ConsumptionData": consumption, "WaterData": water}
    })

@app.route("/liveMonthlyData/<day>/<powerUnits>")
def liveMonthlyData(day, powerUnits):
    year = day.split("-")[0]
    month = day.split("-")[1]
    fileName = fileLookup(year, month)
    ConsumptionFileName = "./Live/ConsumptionMonthlyData"+fileName+".csv"
    WaterFileName = "./Live/WaterMonthlyData"+fileName+".csv"
    consumption = makeMonthly(ConsumptionFileName)
    water = makeMonthly(WaterFileName)
    return jsonify({
        "DummyData": { "ConsumptionData": consumption, "WaterData": water}
    })

def makeYearly(fileName, year):
    file = open(fileName, "r")
    fileData = file.readline()[:-2].split(",")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    outputData = [None]*12
    if year[:4] == "2022":
        a = 5
        for i in range(7):
            outputData[a] = fileData[i]
            a += 1
    elif year[:4] == "2023":
        a = 0
        for i in range(7, 17):
            outputData[a] = fileData[i]
            a += 1
    for i in range(0, 12):
        outputData[i] = {"Month": months[i], "value": outputData[i]}

    return outputData

@app.route("/dummyYearlyData/<year>/<powerUnits>")
def dummyYearlyData(year, powerUnits):
    solar = makeYearly("./Dummy/SolarYearlyData.csv", year)
    consumption = makeYearly("./Dummy/ConsumptionYearlyData.csv", year)
    water = makeYearly("./Dummy/WaterYearlyData.csv", year)
    return jsonify({
        "DummyData": { "SolarData": solar, "ConsumptionData": consumption, "WaterData": water}
    })

@app.route("/getPastMonthsWater/<month>")
def getPastMonthsWater(month):
    file = open("./Dummy/WaterYearlyData.csv", "r")
    fileData = file.readline()[:-2].split(",")
    month = int(month.split("-")[1])
    outputData = [None]*2
    outputData[0] = fileData[6+month-1]
    outputData[1] = fileData[6+month]
    cost = float(outputData[1])*44.97/1000
    return jsonify({
        "Cost": cost, "CurrentMonth": outputData[1], "PastMonth": outputData[0]
    })

@app.route("/liveYearlyData/<year>/<powerUnits>")
def liveYearlyData(year, powerUnits):
    consumption = makeYearly("./Live/ConsumptionYearlyData.csv", year)
    water = makeYearly("./Live/WaterYearlyData.csv", year)
    return jsonify({
        "DummyData": { "ConsumptionData": consumption, "WaterData": water}
    })

@app.route("/extraData/<month>")
def getExtras(month):
    months =[31,28,31,30,31,30,31,31,30,31,30,31]
    response = requests.get("https://dashboard.terrafirma-software.com/Clientapi/getG21Data?data_id=14509&costSavings=false&from_date="+month[:7]+"-01"+"%2000:00&to_date="+month[:7]+"-"+str(months[int(month.split("-")[1])-1])+"%2023:59", auth = HTTPBasicAuth("wanda.majikijela@dschool.org.za", "Wanda#123"))
    waste = response.json()["data_json"][1]["total_waste_kwh"]
    cost = response.json()["data_json"][1]["cost_of_power_consumed"]
    
    return({
        "Waste": waste, "Cost": cost
    })

if __name__ == "__main__":
    app.run(debug=True, port=8081)