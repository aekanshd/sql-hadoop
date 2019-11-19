# SimpleSQL Parser Outputs

## The Output

```text
LOAD bigdata/project_list.csv AS (student_name: string, year: integer, cgpa:integer)
> {'type': 'LOAD', 'database': 'bigdata', 'csv_file_name': 'project_list.csv', 'column_types': [{'name': 'student_name', 'datatype': 'string'}, {'name': 'year', 'datatype': 'integer'}, {'name': 'cgpa', 'datatype': 'integer'}]}
LOAD bigdata/project_list.csv
> {'error': 'No need to specify file name for just LOAD database.'}
SELECT col1 FROM table1
> {'type': 'SELECT', 'columns': ['col1'], 'CLAUSES': {'AND': [], 'OR': []}}
SELECT col1, FROM table1
> {'error': 'Incorrect Syntax. (incomplete column names)'}
SELECT col1,col2, col3 FROM table1
> {'type': 'SELECT', 'columns': ['col1', 'col2', 'col3'], 'CLAUSES': {'AND': [], 'OR': []}}
SELECT col1,col2 FROM table1 WHERE col1 = 2
> {'type': 'SELECT', 'columns': ['col1', 'col2'], 'CLAUSES': {'AND': ['col1 = 2'], 'OR': []}}
SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3
> {'type': 'SELECT', 'columns': ['col1', 'col2'], 'CLAUSES': {'AND': [], 'OR': ['col1 = 2', 'col1 = 3']}}
SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3 AND col4 = 5
> {'type': 'SELECT', 'columns': ['col1', 'col2'], 'CLAUSES': {'AND': ['col4 = 5', 'col1 = 2'], 'OR': ['col1 = 3']}}
SELECT col1,col2 FROM table1 WHERE col1 = 3 AND col4 = 5
> {'type': 'SELECT', 'columns': ['col1', 'col2'], 'CLAUSES': {'AND': ['col1 = 3', 'col4 = 5'], 'OR': []}}
SELECT col1,col2 FROM table1 WHERE 
> {'error': 'Incorrect Syntax.'}
SELECT *
> {'type': 'SELECT', 'columns': ['*'], 'CLAUSES': {'AND': [], 'OR': []}}
SELECT FROM table1
> {'error': 'Incomplete SELECT Query.'}
SELECT , WHERE col1 = 2
> {'error': 'Incorrect Syntax. (incomplete column names)'}
SELECT col1 WHERE (col1 = 2 OR col2= 1) AND col3 =3
> {'error': 'This parser does not support brackets.'}
SELECT col1
> {'error': 'Syntax error. [STRICT ON]'}
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
q = "SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1,col2 FROM table1 WHERE col1 = 2 OR col1 = 3 AND col4 = 5"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(q)
print(">",parser.getParsedQuery())
q = "SELECT col1,col2 FROM table1 WHERE col1 = 3 AND col4 = 5"
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
q = "SELECT col1"
parser = SimpleSQLParser()
parser.parseQuery(q, strict=True)
print(q)
print(">",parser.getParsedQuery())
```