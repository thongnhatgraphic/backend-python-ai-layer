from datetime import datetime, timezone, timedelta


now = datetime.now(timezone.utc)
print(now)

expire = now + timedelta(minutes=10)
print(expire)

if datetime.now(timezone.utc) > expire:
    print("Expired")
else:
    print("Not yet expired")

# 2 convert datetime -> string
now_to_string = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
print(now_to_string)

time_string_to_datetime = datetime.strptime(
    now_to_string, "%Y-%m-%d %H:%M:%S"
)

print(time_string_to_datetime)

# 3: UTC time and VietNam time

# time local in PC not only time in VietNam
# now_to_string = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def get_timezone(offset_hours: int):
    return timezone(timedelta(hours=offset_hours))

def local_to_utc(local_dt: datetime, offset_hours: int):
    tz = get_timezone(offset_hours)
    
    # gắn timezone vào datetime
    local_dt = local_dt.replace(tzinfo=tz)
    
    # convert sang UTC
    return local_dt.astimezone(timezone.utc)

local_time = datetime.now()

print(local_time)