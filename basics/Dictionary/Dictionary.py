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

for key, value in MonthConvertions.items():
    print(key, value)

"""
ini = {"Conection" : "database_type",
       "Conection" : "protocol",
       "Conection" : "database",
       "Conection" : "path",
       "Conection" : "server",
       "Conection" : "port",
       "Conection" : "user",
       "Conection" : "password"};

for key, value in ini.items():
    print(key, value)
"""
