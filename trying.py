# from datetime import datetime
# from pytz import timezone
#
#
# def get_time(message):
#     unix_time = int(message.date)
#     date = datetime.fromtimestamp(unix_time , timezone('Israel'))
#     return date
#
#
# # unix = '1544010258'
# # print(get_time(unix))
#
# #
# # fmt = "%Y-%m-%d %H:%M:%S %Z%z"
# #
# # # Current time in UTC
# now_utc = datetime.now(timezone('UTC'))
# # print(now_utc.year)
#
# # print (now_utc.strftime(fmt))
# #
# # # Convert to US/Pacific time zone
# # now_pacific = now_utc.astimezone(timezone('Israel'))
# # print (now_pacific.strftime(fmt))
# # print (now_pacific)
# #
