import sys, os
sys.path.insert(0, os.getcwd())

from console import Console
from simpleSQLParser import SimpleSQLParser

home_dir = "/BD_649_692_1744_1808"

console = Console(SimpleSQLParser(strict=True), debug=True)
console.setHomeDir(home_dir)
console.start()
