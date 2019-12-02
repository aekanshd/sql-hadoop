import csv
import sys
import json
from prettytable import PrettyTable

x = PrettyTable()

empty_str = ''
for line in sys.stdin:
    empty_str += line
dictionary = json.loads(empty_str)

if dictionary['type'] == "project":

    for i in range(len(dictionary['value'])):
        x.add_column(dictionary['header'][i], dictionary['value'][i])
    print(x)

if dictionary['type'] == "where_only_or":
    for i in range(len(dictionary['value'])):
        x.add_column(dictionary['header'][i], dictionary['value'][i])
    print(x)

if dictionary['type'] == "where_only_and":
    for i in range(len(dictionary['value'])):
        x.add_column(dictionary['header'][i], dictionary['value'][i])
    print(x)

if dictionary['type'] == "aggregate_only" or dictionary['type'] == "where_agg_and" or dictionary['type'] == "where_agg_or":
    dictionary['value'] = [int(i) for i in dictionary['value']]
    if dictionary['key'] == 'avg':
        x.add_column(dictionary['header'][0], [sum(dictionary['value'])/len(dictionary['value'])])
        print(x)
    if dictionary['key'] == 'count':
        x.add_column(dictionary['header'][0], [len(dictionary['value'])])
        print(x)
    if dictionary['key'] == 'sum':
        x.add_column(dictionary['header'][0], [sum(dictionary['value'])])
        print(x)

