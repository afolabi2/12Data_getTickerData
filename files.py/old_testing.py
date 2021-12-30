from datetime import datetime
# ts = int('1284101485')
# pm = datetime.utcfromtimestamp(ts)
# # if you encounter a "year is out of range" error the timestamp
# # may be in milliseconds, try `ts /= 1000` in that case
# print(pm.strftime('%Y-%m-%d %H:%M:%S'))
# print(type(pm))
p1_str = '2021-12-25 20:40:00'
p2_str = '2022-01-12 05:20:00'
p1 = datetime.strptime(f'{p1_str}', '%Y-%m-%d %H:%M:%S')
p2 = datetime.strptime(f'{p2_str}', '%Y-%m-%d %H:%M:%S')
p3 = p2 - p1
p4 = p3.total_seconds()/(5000 * 5 * 60)
print(p4)
