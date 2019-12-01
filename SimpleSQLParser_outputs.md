# SimpleSQL Parser Outputs

## The Output

```text

> {'error': 'Please enter a query.'}
LOAD bigdata/project_list.csv AS (student_name: string, year: integer, cgpa:integer)
> {'type': 'load', 'database': 'bigdata', 'csv_file_name': 'project_list.csv', 'column_types': [{'name': 'student_name', 'datatype': 'string'}, {'name': 'year', 'datatype': 'integer'}, {'name': 'cgpa', 'datatype': 'integer'}]}
LOAD bigdata/project_list.csv AS (student_name:)
> {'error': 'Incorrect syntax.'}
LOAD bigdata/project_list.csv AS (: string)
> {'error': 'Incorrect syntax.'}
LOAD bigdata/project_list.csv AS (:)
> {'error': 'Incorrect syntax.'}
LOAD bigdata/project_list.csv AS ()
> {'error': 'Incorrect syntax.'}
LOAD bigdata/project_list.csv AS
> {'error': 'Incomplete LOAD query.'}
LOAD bigdata/project_list.csv
> {'error': 'No need to specify file name for just LOAD database.'}
LOAD bigdata
> {'type': 'load_existing', 'database': 'bigdata'}
LOAD /project_list.csv
> {'error': 'No need to specify file name for just LOAD database.'}
LOAD bigdata/
> {'error': 'No need to specify file name for just LOAD database.'}
LOAD bigdata/ AS ()
> {'error': 'Incorrect Syntax. (incomplete file name)'}
LOAD /project_list.csv AS ()
> {'error': 'Incorrect Syntax. (incomplete database name)'}
SELECT col1 FROM table1
> {'type': 'select', 'columns': ['col1'], 'clauses': {'and': [], 'or': []}}
SELECT col1, FROM table1
> {'error': 'Incorrect Syntax. (incomplete column names)'}
SELECT col1,col2, col3 FROM table1
> {'type': 'select', 'columns': ['col1', 'col2', 'col3'], 'clauses': {'and': [], 'or': []}}
SELECT col1,col2 FROM table1 WHERE col1 = 2
> {'type': 'select', 'columns': ['col1', 'col2'], 'clauses': {'and': ['col1 = 2'], 'or': []}}
SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3
> {'type': 'select', 'columns': ['col1', 'col2'], 'clauses': {'and': [], 'or': ['col1 = 2', 'col1 = 3']}}
SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3 AND col4 = 5
> {'type': 'select', 'columns': ['col1', 'col2'], 'clauses': {'and': ['col4 = 5', 'col1 = 3'], 'or': ['col1 = 2']}}
SELECT col1,col2 FROM table1 WHERE col1 = 3 AND col4 = 5
> {'type': 'select', 'columns': ['col1', 'col2'], 'clauses': {'and': ['col1 = 3', 'col4 = 5'], 'or': []}}
SELECT col1,col2 FROM table1 WHERE 
> {'error': 'Incorrect Syntax.'}
SELECT *
> {'type': 'select', 'columns': ['*'], 'clauses': {'and': [], 'or': []}}
SELECT FROM table1
> {'error': 'Incomplete SELECT Query.'}
SELECT , WHERE col1 = 2
> {'error': 'Incorrect Syntax. (incomplete column names)'}
SELECT col1 WHERE (col1 = 2 OR col2= 1) AND col3 =3
> {'error': 'This parser does not support brackets.'}
SELECT col1 Where a1 = 2 Or a2 = 3 And b = 4;
> {'type': 'select', 'columns': ['col1'], 'clauses': {'and': ['b = 4', 'a2 = 3'], 'or': ['a1 = 2']}}
SELECT COUNT(col1), col2
> {'type': 'select', 'columns': ['agg_column', 'col2'], 'clauses': {'and': [], 'or': []}, 'aggregate': 'count', 'agg_column': 'col1'}
SELECT COUNT(), col2
> {'error': 'Incomplete aggregate function.'}
SELECT (col1), col2
> {'error': 'Incomplete aggregate function.'}
SELECT SUM(col1), col2
> {'type': 'select', 'columns': ['agg_column', 'col2'], 'clauses': {'and': [], 'or': []}, 'aggregate': 'sum', 'agg_column': 'col1'}
SELECT AVG(col1), col1, col2
> {'type': 'select', 'columns': ['agg_column', 'col1', 'col2'], 'clauses': {'and': [], 'or': []}, 'aggregate': 'avg', 'agg_column': 'col1'}
SELECT AVG(col1), SUM(col2) WHERE col1 > 3
> {'error': 'Only one aggregate function allowed.'}
```

## The code

```python
parser = SimpleSQLParser(strict=False)

q = ""
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/project_list.csv AS (student_name: string, year: integer, cgpa:integer)"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/project_list.csv AS (student_name:)"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/project_list.csv AS (: string)"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/project_list.csv AS (:)"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/project_list.csv AS ()"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/project_list.csv AS"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/project_list.csv"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD /project_list.csv"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD bigdata/ AS ()"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "LOAD /project_list.csv AS ()"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1 FROM table1"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1, FROM table1"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1,col2, col3 FROM table1"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1,col2 FROM table1 WHERE col1 = 2"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3 AND col4 = 5"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1,col2 FROM table1 WHERE col1 = 3 AND col4 = 5"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1,col2 FROM table1 WHERE "
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT *"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT FROM table1"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT , WHERE col1 = 2"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1 WHERE (col1 = 2 OR col2= 1) AND col3 =3"
parser = SimpleSQLParser(strict=False)
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT col1 Where a1 = 2 Or a2 = 3 And b = 4;"
parser = SimpleSQLParser(strict=True)
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT COUNT(col1), col2"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT COUNT(), col2"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT (col1), col2"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT SUM(col1), col2"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT AVG(col1), col1, col2"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())

q = "SELECT AVG(col1), SUM(col2) WHERE a > 3"
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
```
