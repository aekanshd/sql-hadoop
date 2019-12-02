import csv
import sys
import json

empty_str = ''
for line in sys.stdin:
    empty_str += line
dictionary = json.loads(empty_str)
print(dictionary)

if dictionary['type'] == "project":
    print(dictionary['value'])