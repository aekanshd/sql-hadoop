import sys
import json

rough_schema = {'type': 'load', 'database': 'bigdata', 'csv_file_name': 'project_list.csv', 'column_types': [{'name': 'batsman', 'datatype': 'string'}, {'name': 'bowler', 'datatype': 'string'}, {'name': 'wickets', 'datatype': 'integer'}, {'name': 'runs', 'datatype': 'integer'}], 'aggregate': 'avg', 'agg_column': 'student_name'}
query = {'type': 'select', 'aggregate': None, 'agg_column': None, 'columns': ['batsman', 'bowler'], 'clauses': {'or': [], 'and': ['wickets = 5', 'runs = 29']}}


#rough_schema = json.loads(sys.argv[1])
#query = json.loads(sys.argv[2])


#'wickets = 5', 'runs = 29'
#Get column names from schema 
schema_cols = [rough_schema['column_types'][i]['name'] for i in range(0,len(rough_schema['column_types']))]
query_cols = query['columns']
query_and = query['clauses']['and']
query_or = query['clauses']['or']
query_agg = query['agg_column']
agg_list = []    
get_col_nums, get_col_nums1, get_col_nums2 = {}, {}, {}
get_col_nums_list, get_col_nums_list1, get_col_nums_list2 = [], [], []
#get_col_nums = [get_col_nums.append(int(schema_cols.index(str(query_cols[i])))) for i in range(len(query_cols))]
#key, value = [], []


def get_column_num(query_cols, schema_cols, aggregate, query_) :    
    if aggregate == 0:
        for i in range(len(query_cols)):
            a = schema_cols.index(str(query_cols[i]))
            get_col_nums.update({query_cols[i] : int(a)})
            get_col_nums_list.append(int(a))
        return get_col_nums
    if aggregate == 1:
        a = int(schema_cols.index(query['agg_column']))
        get_col_nums_list1.append(a)
        get_col_nums1.update({'aggregate' : a})
        return get_col_nums1
    if aggregate == 2:
        for i in range(len(query_)):
            want = [ query_[i].split(' ') for i in range(len(query_)) ]
            a = schema_cols.index(str(want[i][0]))
            get_col_nums2.update({want[i][0] : [int(a), int(want[i][2]), str(want[i][1])]})
            get_col_nums_list2.append([int(a), int(want[i][2])])
        return get_col_nums2





select_columns = [[] for i in range(len(query_cols))]

#Get WHERE column names and list of position with value : [('year', [1, 2]), ('cgpa', [2, 3])]
c = sorted(get_column_num(query_cols, schema_cols, 2, query_and).items(), key = lambda x: x[1])
d = sorted(get_column_num(query_cols, schema_cols, 2, query_or).items(), key = lambda x: x[1])
#print(c)


#Check for PROJECT query. Enter this loop if true.            
if len(query['clauses']['or']) == 0 and len(query['clauses']['and']) == 0 and query['aggregate'] is None: 
    for line in sys.stdin:
        line = line.strip().split(',')
        #print(line)
        
        for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_or).values()))):
            select_columns[i].append(line[int(get_col_nums_list[i])])
    
    key = query['columns']
    value = str(select_columns)[1:-1]           
    print('%s^%s^%s' % ("project",key, value))

    output = dict()
    output['key'] = query['columns']
    #value = select_columns
    output['value'] = select_columns
    output['type'] = "project"
    #value = json.loads(value)
    #key, value = str(key), str(value)          
    print('%s' % (json.dumps(output)))

    

#check for SELECT and WHeRE. Enter loop if true. Where with agg and.
if len(query['clauses']['and']) > 0 and query['aggregate'] is not None:
    agg_column_num = schema_cols.index(query_agg)
    for line in sys.stdin:
        line = line.strip().split(',')

        for i in range(len(list(get_column_num(query_cols, schema_cols, 2, query_and).values()))):
        
            if c[i][1][-1] == '=' and int(line[int(c[i][1][0])]) == c[i][1][1]:
                    agg_list.append(line[agg_column_num])
            if c[i][1][-1] == '>' and int(line[int(c[i][1][0])]) < c[i][1][1]:
                    agg_list.append(line[agg_column_num])
            if c[i][1][-1] == '<' and int(line[int(c[i][1][0])]) > c[i][1][1]:
                    agg_list.append(line[agg_column_num])
    

    output = dict()
    output['key'] = [query['aggregate']]
    #value = select_columns
    output['value'] = agg_list
    output['type'] = "where_agg_and"
    #value = json.loads(value)
    #key, value = str(key), str(value)          
    print('%s' % (json.dumps(output)))

#Where with agg or.   
if len(query['clauses']['or']) > 0 and query['aggregate'] is not None:
    agg_column_num = schema_cols.index(query_agg)
    for line in sys.stdin:
        line = line.strip().split(',')

        for i in range(len(list(get_column_num(query_cols, schema_cols, 2, query_or).values()))):
        
            if d[i][1][-1] == '=' and int(line[int(d[i][1][0])]) == d[i][1][1]:
                    agg_list.append(line[agg_column_num])
            elif d[i][1][-1] == '>' and int(line[int(d[i][1][0])]) < d[i][1][1]:
                    agg_list.append(line[agg_column_num])
            elif d[i][1][-1] == '<' and int(line[int(d[i][1][0])]) > d[i][1][1]:
                    agg_list.append(line[agg_column_num])
    

    output = dict()
    output['key'] = [query['aggregate']]
    #value = select_columns
    output['value'] = agg_list
    output['type'] = "where_only_or"
    #value = json.loads(value)
    #key, value = str(key), str(value)          
    print('%s' % (json.dumps(output)))


#Only aggregate
if len(query['clauses']['or']) == 0 and query['aggregate'] is not None:
    agg_column_num = schema_cols.index(query_agg)
    for line in sys.stdin:
        line = line.strip().split(',')

        agg_list.append(line[agg_column_num])
    

    output = dict()
    output['key'] = [query['aggregate']]
    #value = select_columns
    output['value'] = agg_list
    output['type'] = "aggregate"
    #value = json.loads(value)
    #key, value = str(key), str(value)          
    print('%s' % (json.dumps(output)))


#Only where_or
if len(query['clauses']['or']) > 0 and query['aggregate'] is None:
    for line in sys.stdin:
        line = line.strip().split(',')

        for i in range(len(list(get_column_num(query_cols, schema_cols, 2, query_or).values()))):

            if d[i][1][-1] == '=' and int(line[int(d[i][1][0])]) == d[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_or).values()))):
                        select_columns[i].append(line[int(get_col_nums_list[i])])
            if d[i][1][-1] == '>' and int(line[int(d[i][1][0])]) < d[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_or).values()))):
                    select_columns[i].append(line[int(get_col_nums_list[i])])
            if d[i][1][-1] == '<' and int(line[int(d[i][1][0])]) > d[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_or).values()))):
                    select_columns[i].append(line[int(get_col_nums_list[i])])


    output = dict()
    output['key'] = query['clauses']['or']
    #value = select_columns
    output['value'] = select_columns
    output['type'] = "where_only_or"
    #value = json.loads(value)
    #key, value = str(key), str(value)          
    print('%s' % (json.dumps(output)))

#Only where and
if len(query['clauses']['and']) > 0 and query['aggregate'] is None:
    for line in sys.stdin:
        line = line.strip().split(',')

        value = False
        for i in range(len(list(get_column_num(query_cols, schema_cols, 2, query_and).values()))):

            if c[i][1][-1] == '=' and int(line[int(c[i][1][0])]) == c[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_and).values()))):
                    if value is False:
                        print("H")
                        value = "pending"
                    elif value == "pending":
                        value = False
                        select_columns[i].append(line[int(get_col_nums_list[i])])
            if c[i][1][-1] == '>' and int(line[int(c[i][1][0])]) < c[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_and).values()))):
                    if value is False:
                        value = "pending"
                    elif value == "pending":
                        select_columns[i].append(line[int(get_col_nums_list[i])])
                        value = False
            if c[i][1][-1] == '<' and int(line[int(c[i][1][0])]) > c[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_and).values()))):
                    if value is False:
                        value = "pending"
                    elif value == "pending":
                        select_columns[i].append(line[int(get_col_nums_list[i])])
                        value = False


    output = dict()
    output['key'] = query['clauses']['and']
    #value = select_columns
    output['value'] = select_columns
    output['type'] = "where_only_and"
    #value = json.loads(value)
    #key, value = str(key), str(value)          
    print('%s' % (json.dumps(output)))


    
    


