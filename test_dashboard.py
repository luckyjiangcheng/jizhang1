#!/usr/bin/env python3
import datetime

# 测试日期范围计算
def build_period_range(period, today_start):
    start, end, prevStart, prevEnd = None, None, None, None
    granularity = 'day'
    if period == 'today':
        start = today_start
        end = today_start
        end = end.replace(hour=23, minute=59, second=59, microsecond=999)
        prevStart = today_start - datetime.timedelta(days=1)
        prevEnd = prevStart.replace(hour=23, minute=59, second=59, microsecond=999)
        granularity = 'hour'
    elif period == 'week':
        day = today_start.weekday() or 7  # 0-6, 0 is Monday
        start = today_start - datetime.timedelta(days=day-1)
        end = start + datetime.timedelta(days=6)
        end = end.replace(hour=23, minute=59, second=59, microsecond=999)
        prevStart = start - datetime.timedelta(days=7)
        prevEnd = end - datetime.timedelta(days=7)
        granularity = 'day'
    elif period == 'month':
        start = today_start.replace(day=1)
        next_month = today_start.replace(day=28) + datetime.timedelta(days=4)
        end = next_month - datetime.timedelta(days=next_month.day)
        end = end.replace(hour=23, minute=59, second=59, microsecond=999)
        # Previous month
        prev_month = start - datetime.timedelta(days=1)
        prevStart = prev_month.replace(day=1)
        prevEnd = start - datetime.timedelta(seconds=1)
        granularity = 'day'
    elif period == 'year':
        start = today_start.replace(month=1, day=1)
        end = today_start.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999)
        prevStart = start.replace(year=start.year-1)
        prevEnd = end.replace(year=end.year-1)
        granularity = 'month'
    return start, end, granularity

# 测试当前日期
today = datetime.datetime.now()
today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
print(f"Current date: {today}")
print(f"Today start: {today_start}")

# 测试不同时间段
periods = ['today', 'week', 'month', 'year']
for period in periods:
    start, end, granularity = build_period_range(period, today_start)
    print(f"\n{period.capitalize()}:")
    print(f"  Start: {start}")
    print(f"  End: {end}")
    print(f"  Granularity: {granularity}")

# 测试示例数据日期范围
sample_dates = [
    "2023-10-01", "2023-10-02", "2023-10-03", "2023-10-05", "2023-10-08",
    "2023-10-12", "2023-10-15", "2023-11-01", "2023-11-05", "2023-12-10"
]
print("\nSample data dates:")
for date_str in sample_dates:
    print(f"  {date_str}")

# 检查示例数据是否在当前月份范围内
current_month_start, current_month_end, _ = build_period_range('month', today_start)
print(f"\nCurrent month range: {current_month_start} to {current_month_end}")
print("Sample data in current month:")
for date_str in sample_dates:
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    in_range = current_month_start <= date <= current_month_end
    print(f"  {date_str}: {'✓' if in_range else '✗'}")
