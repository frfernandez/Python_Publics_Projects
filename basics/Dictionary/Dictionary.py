MonthConvertions = {"Jan" : "January",
                    "Feb" : "February",
                    "Mar" : "March",
                    "Apr" : "April",
                    "May" : "May",
                    "Jun" : "June",
                    "Jul" : "July",
                    "Aug" : "August",
                    "Sep" : "September",
                    "Oct" : "October",
                    "Nov" : "November",
                    "Dec" : "December"};

print(MonthConvertions["Nov"]);
print(MonthConvertions["Mar"]);
print(MonthConvertions.get("Dec"));
print(MonthConvertions.get("Luv"));
print(MonthConvertions.get("Luv", "Not a valid key."));