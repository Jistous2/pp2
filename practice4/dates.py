from datetime import datetime, timedelta

# 1) Вычитаем 5 дней из текущей даты и времени
# datetime.now() -> текущий момент
# timedelta(days=5) -> временной промежуток в 5 суток
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print("Current date:", current_date)
print("Five days ago:", five_days_ago)

# 2) Получаем вчера, сегодня и завтра
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday.date())
print("Today:", today.date())
print("Tomorrow:", tomorrow.date())

# 3) Убираем микросекунды из объекта datetime
# replace(microsecond=0) оставляет дату и время, но обнуляет микросекунды
current_with_microseconds = datetime.now()
without_microseconds = current_with_microseconds.replace(microsecond=0)

print("With microseconds:", current_with_microseconds)
print("Without microseconds:", without_microseconds)

# 4) Считаем разницу между двумя датами в секундах
# date2 - date1 дает timedelta, total_seconds() переводит разницу в секунды
date1 = datetime(2025, 3, 1, 12, 0, 0)
date2 = datetime(2025, 3, 2, 14, 30, 0)

difference = date2 - date1
print("Difference in seconds:", int(difference.total_seconds()))
