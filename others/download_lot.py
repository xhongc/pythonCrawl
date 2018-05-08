from datetime import datetime,timedelta

one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
print(one_mintes_ago)
