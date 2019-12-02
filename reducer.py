import csv
import sys
import json

empty_str = ''
for line in sys.stdin:
    empty_str += line
print(empty_str)
dictionary = json.loads(empty_str)
print(dictionary)

if dictionary['type'] == "project":
    print(dictionary['value'])

if dictionary['type'] == "where_only_or":
    print(dictionary['value'])

if dictionary['type'] == "where_only_and":
    print(dictionary['value'])

if dictionary['type'] == "aggregate_only" or dictionary['type'] == "where_agg_and" or dictionary['type'] == "where_agg_or":
    dictionary['value'] = [int(i) for i in dictionary['value']]
    if dictionary['key'] == 'avg':
        print(sum(dictionary['value'])/len(dictionary['value']))
    if dictionary['key'] == 'count':
        print(len(dictionary['value']))
    if dictionary['key'] == 'sum':
        print(sum(dictionary['value']))

