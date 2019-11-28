import sys, os
sys.path.insert(0, os.getcwd())

from console import Console
from simpleSQLParser import SimpleSQLParser

console = Console(SimpleSQLParser())
console.start()
