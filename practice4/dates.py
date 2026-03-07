from datetime import datetime, timedelta

# 1. Subtract five days from current date
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print("Current date:", current_date)
print("Five days ago:", five_days_ago)

# 2. Print yesterday, today, tomorrow
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday.date())
print("Today:", today.date())
print("Tomorrow:", tomorrow.date())

# 3. Drop microseconds from datetime
current_with_microseconds = datetime.now()
without_microseconds = current_with_microseconds.replace(microsecond=0)

print("With microseconds:", current_with_microseconds)
print("Without microseconds:", without_microseconds)

# 4. Calculate two date difference in seconds
date1 = datetime(2025, 3, 1, 12, 0, 0)
date2 = datetime(2025, 3, 2, 14, 30, 0)

difference = date2 - date1
print("Difference in seconds:", int(difference.total_seconds()))