from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%H:%M:%S")
print("Current Time: ", dt_string)