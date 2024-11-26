import datetime


print(datetime.time.tzinfo)
print(datetime.time)
print(datetime.datetime.now())

start_time = datetime.time(hour=8, minute=30)
print(start_time)
print(datetime.datetime.now().time().isoformat(timespec="minutes"))
print(datetime.datetime.now().isoformat(timespec="minutes"))
print(datetime.datetime.now().strftime("%y%m%d-%H%M"))

if datetime.datetime.now().time() > start_time:
    print("past!!!")
else:
    print("not past!!!")