import json

d1 = {"('Hello',)": 6, "('Hi',)": 5}
s1 = json.dumps(d1)
d2 = json.loads(s1)
print(s1[1])