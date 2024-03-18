from datetime import datetime

date_str1 = "9/11/2024"
date_str2 = "9/15/2024"

date1 = datetime.strptime(date_str1, "%m/%d/%Y")
date2 = datetime.strptime(date_str2, "%m/%d/%Y")

if date1 < date2:
    print(f"{date_str1} is earlier than {date_str2}")
elif date1 > date2:
    print(f"{date_str2} is earlier than {date_str1}")
else:
    print("Both dates are the same")
