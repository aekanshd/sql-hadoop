import sys


rough_schema = {'type': 'load', 'database': 'bigdata', 'csv_file_name': 'project_list.csv', 'column_types': [{'name': 'batsman', 'datatype': 'string'}, {'name': 'bowler', 'datatype': 'string'}, {'name': 'wickets', 'datatype': 'integer'}, {'name': 'runs', 'datatype': 'integer'}], 'aggregate': 'avg', 'agg_columns': 'student_name'}
query = {'type': 'select', 'aggregate': None, 'agg_columns': None, 'columns': ['batsman'], 'clauses': {'and': [], 'or': []}}


#'wickets = 5', 'runs = 29'
#Get column names from schema 
schema_cols = [rough_schema['column_types'][i]['name'] for i in range(0,len(rough_schema['column_types']))]
query_cols = query['columns']
query_and = query['clauses']['or']
query_agg = query['agg_columns']
get_col_nums, get_col_nums1, get_col_nums2 = {}, {}, {}
get_col_nums_list, get_col_nums_list1, get_col_nums_list2 = [], [], []
#get_col_nums = [get_col_nums.append(int(schema_cols.index(str(query_cols[i])))) for i in range(len(query_cols))]
#key, value = [], []


def get_column_num(query_cols, schema_cols, aggregate, query_and) :    
    if aggregate == 0:
        for i in range(len(query_cols)):
            a = schema_cols.index(str(query_cols[i]))
            get_col_nums.update({query_cols[i] : int(a)})
            get_col_nums_list.append(int(a))
        return get_col_nums
    if aggregate == 1:
        a = int(schema_cols.index(query['agg_columns']))
        get_col_nums_list1.append(a)
        get_col_nums1.update({'aggregate' : a})
        return get_col_nums1
    if aggregate == 2:
        for i in range(len(query['clauses']['and'])):
            want = [ query['clauses']['and'][i].split(' ') for i in range(len(query['clauses']['and'])) ]
            a = schema_cols.index(str(want[i][0]))
            get_col_nums2.update({want[i][0] : [int(a), int(want[i][2]), str(want[i][1])]})
            get_col_nums_list2.append([int(a), int(want[i][2])])
        return get_col_nums2


'''def purify(l):
    return [i for i in l if not i & 1]'''




select_columns = [[] for i in range(len(query_cols))]

#Get WHERE column names and list of position with value : [('year', [1, 2]), ('cgpa', [2, 3])]
c = sorted(get_column_num(query_cols, schema_cols, 2, query_and).items(), key = lambda x: x[1])
print(c)
"""
| col1 | col2 | col3 |
1,2,3
3,2,1
1,1,1


[[1,3,1], [2,2,1]]
"""

#Check for PROJECT query. Enter this loop if true.            
if len(query['clauses']['and']) == 0 and query['aggregate'] is None: 
    for line in sys.stdin:
        line = line.strip().split(',')
        #print(line)
        
        for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_and).values()))):
            select_columns[i].append(line[int(get_col_nums_list[i])])
    
    key = select_columns
    a, b = get_column_num(query_cols, schema_cols, 0, query_and), get_column_num(query_cols, schema_cols, 2, query_and)
    value = [query['type']]
    key = str(key)
    value = str(value)            
    print('%s:%s' % (key, value))

#check for SELECT and WHERE. Enter loop if true.
else:
    for line in sys.stdin:
        line = line.strip().split(',')

        for i in range(len(list(get_column_num(query_cols, schema_cols, 2, query_and).values()))):
            #print(int(line[int(c[i][1][0])]), c[i][1][1])
            '''x = int(line[(c[i][1][0])])
            x = [True if int(line[(c[i][1][0])]) == c[i][1][1] else False for i in range(len(c))]
            print(x)'''


            if c[i][1][-1] == '=' and int(line[int(c[i][1][0])]) == c[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_and).values()))):
                    #print("\t",line[int(get_col_nums_list[i])])
                    select_columns[i].append(line[int(get_col_nums_list[i])])
            if c[i][1][-1] == '>' and int(line[int(c[i][1][0])]) < c[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_and).values()))):
                    select_columns[i].append(line[int(get_col_nums_list[i])])
            if c[i][1][-1] == '<' and int(line[int(c[i][1][0])]) > c[i][1][1]:
                for i in range(len(list(get_column_num(query_cols, schema_cols, 0, query_and).values()))):
                    select_columns[i].append(line[int(get_col_nums_list[i])])



    '''if(query['aggregate'] is None):
        key = select_columns
        value = [ query['type'], get_column_num(query_cols, schema_cols, 0, query_and), c ]
        key, value = str(key), str(value)          
        print('%s:%s' % (key, value))'''


    key = select_columns
    value = [ query['type'], get_column_num(query_cols, schema_cols, 0, query_and), c]
    key, value = str(key), str(value)            
    print('%s:%s' % (key, value))

    


    


