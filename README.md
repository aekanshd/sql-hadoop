# sql-hadoop
This project performs SQL operations on a CSV input in HDFS, using Hadoop's Map-Reduce. 

## How to use SimpleSQLParser

Follow this short snippet, the function `parseQuery("Query")` returns a dictionary of the parsed SQL.

```python
q = "SELECT col1, col2 FROM WHERE col5 = \"Awesome\";"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(parser.DICTIONARY)
```
