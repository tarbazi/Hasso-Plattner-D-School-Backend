import {getHour, getDaily, getWeekly, getMonthly, getYearly, switchDay, switchWeek, switchMonth} from "./AdaptorClass.js"

console.log(await getHour("2023-09-20", "12", "0"))
console.log(await getDaily("2023-09-20", "0"))
console.log(await getWeekly("2023-09-17", "0"))
console.log(await getMonthly("2023-09-01", "0"))
console.log(await getYearly("2023", "0"))

console.log(await getHourDummy("2023-09-20", "12", "0"))
console.log(await getDailyDummy("2023-09-20", "0"))
console.log(await getWeeklyDummy("2023-09-17", "0"))
console.log(await getMonthlyDummy("2023-09-01", "0"))
console.log(await getYearlyDummy("2023", "0"))

console.log(await switchDay("2023-09-17", "0"))
console.log(await switchWeek("2023-09-10", "1"))
console.log(await switchMonth("2023-08-10", "1"))