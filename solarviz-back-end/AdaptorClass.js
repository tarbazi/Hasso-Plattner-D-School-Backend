export async function getHour(day, hourNum, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/hourlyData/"+day+"/"+hourNum+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getHourDummy(day, hourNum, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/dummHourlyData/"+day+"/"+hourNum+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getDaily(day, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/dailyData/"+day+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getDailyDummy(day, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/dummyDailyData/"+day+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getWeekly(weeksSunday, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/weeklyData/"+weeksSunday+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getWeeklyDummy(weeksSunday, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/dummyWeeklyData/"+weeksSunday+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getMonthly(month, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/monthlyData/"+month+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getMonthlyDummy(month, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/dummyMonthlyData/"+month+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getYearly(year, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/yearlyData/"+year+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function getDummyYearly(year, powerUnits){
    const response = await fetch("http://127.0.0.1:8081/dummyYearlyData/"+year+"/"+powerUnits)
    const data = await response.json()
    return data
}

export async function switchDay(day, dir){
    const response = await fetch("http://127.0.0.1:8081/nextDay/"+day+"/"+dir)
    const data = await response.json()
    return data
}

export async function switchWeek(weeksSunday, dir){
    const response = await fetch("http://127.0.0.1:8081/nextWeek/"+weeksSunday+"/"+dir)
    const data = await response.json()
    return data
}

export async function switchMonth(month, dir){
    const response = await fetch("http://127.0.0.1:8081/nextMonth/"+month+"/"+dir)
    const data = await response.json()
    return data
}