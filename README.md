# Simple SQL Engine with Hadoop
This project performs SQL operations on a CSV input in HDFS, using Hadoop's Map-Reduce. 

## How to Start

### TL;DR: Run `main.py`

We have a console hosted at `console.py`. In order to begin, please make sure you have the current directory as a working directory. Then, import the console and your parser. This console's default parser is [SimpleSQLParser](/simpleSQLParser.py).

```python
import sys, os
sys.path.insert(0, os.getcwd())

from console import Console
from simpleSQLParser import SimpleSQLParser

console = Console(SimpleSQLParser())
console.start()
```

## How to use SimpleSQLParser

**Note: This parser has been stripped down for simplicity and takes only AND with no logic attached. No syntax checking is done.** For a more elaborate version, check the `old-code` branch.

Follow this short snippet, the function `parseQuery("Query")` parses the query, and then we can use `getParsedQuery()` which will return a dictionary of the parsed SQL.

```python
q = "SELECT col1, col2 FROM WHERE col5 = \"Awesome\";"
parser = SimpleSQLParser()
parser.parseQuery(q)
print(parser.getParsedQuery())
```
