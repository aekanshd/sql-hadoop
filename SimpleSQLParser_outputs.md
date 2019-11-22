# SimpleSQL Parser Outputs

## The Output

```text
LOAD bigdata/project_list.csv AS (student_name: string, year: integer, cgpa:integer)
> {'type': 'load', 'database': 'bigdata', 'csv_file_name': 'project_list.csv', 'column_types': [{'name': 'student_name', 'datatype': 'string'}, {'name': 'year', 'datatype': 'integer'}, {'name': 'cgpa', 'datatype': 'integer'}]}
LOAD bigdata/project_list.csv
> {'error': 'No need to specify file name for just LOAD database.'}
LOAD bigdata
> {'type': 'load_existing', 'database': 'bigdata'}
SELECT col1 FROM table1
> {'type': 'select', 'columns': ['col1'], 'clauses': {'and': []}}
SELECT col1, FROM table1
> {'error': 'Incorrect Syntax. (incomplete column names)'}
SELECT col1,col2, col3 FROM table1
> {'type': 'select', 'columns': ['col1', 'col2', 'col3'], 'clauses': {'and': []}}
SELECT col1,col2 FROM table1 WHERE col1 = 2
> {'type': 'select', 'columns': ['col1', 'col2'], 'clauses': {'and': ['col1 = 2']}}
SELECT col1,col2 FROM table1 WHERE col1 = 2 AND col1 = 3
> {'type': 'select', 'columns': ['col1', 'col2'], 'clauses': {'and': ['col1 = 2', 'col1 = 3']}}
SELECT col1,col2 FROM table1 WHERE col1 = 2 AND col1 = 3 AND col4 = 5
> {'type': 'select', 'columns': ['col1', 'col2'], 'clauses': {'and': ['col1 = 2', 'col1 = 3', 'col4 = 5']}}
SELECT col1,col2 FROM table1 WHERE 
> {'error': 'Incorrect Syntax.'}
SELECT *
> {'type': 'select', 'columns': ['*'], 'clauses': {'and': []}}
SELECT FROM table1
> {'error': 'Incomplete SELECT Query.'}
SELECT , WHERE col1 = 2
> {'error': 'Incorrect Syntax. (incomplete column names)'}
SELECT col1 WHERE (col1 = 2 OR col2= 1) AND col3 =3
> {'type': 'select', 'columns': ['col1'], 'clauses': {'and': ['(col1 = 2 or col2= 1)', 'col3 =3']}}
SELECT col1 Where a1 = 2 And a2 = 3 And b = 4;
> {'type': 'select', 'columns': ['col1'], 'clauses': {'and': ['a1 = 2', 'a2 = 3', 'b = 4']}}
```

## The code

```python
parser = SimpleSQLParser()
q = "LOAD bigdata/project_list.csv AS (student_name: string, year: integer, cgpa:integer)"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "LOAD bigdata/project_list.csv"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "LOAD bigdata"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1 FROM table1"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1, FROM table1"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1,col2, col3 FROM table1"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1,col2 FROM table1 WHERE col1 = 2"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1,col2 FROM table1 WHERE col1 = 2 AND col1 = 3"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1,col2 FROM table1 WHERE col1 = 2 AND col1 = 3 AND col4 = 5"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1,col2 FROM table1 WHERE "
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT *"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT FROM table1"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT , WHERE col1 = 2"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1 WHERE (col1 = 2 OR col2= 1) AND col3 =3"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1 Where a1 = 2 And a2 = 3 And b = 4;"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
```
