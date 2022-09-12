import json

from sellers_data import sellers_data

sellers_data = sellers_data("ball", 5)
print(json.dumps(sellers_data, indent=4))
