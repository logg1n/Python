from datetime import datetime, timedelta

time = datetime.now() + timedelta(seconds=10)

while datetime.now() < time:
    pass
