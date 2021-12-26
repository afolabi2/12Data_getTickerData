from datetime import datetime
ts = int('1284101485')
pm = datetime.utcfromtimestamp(ts)
# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
print(pm.strftime('%Y-%m-%d %H:%M:%S'))
print(type(pm))