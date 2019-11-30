from os import system, name
import sys
import subprocess

class Console:
    parser = None
    our_name = None
    database = None
    parsed_query = None

    debug = None
    home_dir = None

    """
        Constructor function.
        Optional: Provide Parser
    """

    def __init__(self, parser=None, debug=False):
        self.parser = parser or SimpleSQLParser(strict=False)
        self.our_name = "bd-sql-parser"
        self.debug = debug

    """
        Logger Functon.
    """

    def log(self, *what):
        if self.debug: 
            for i in range(0, len(what)):
                print(what[i], end=" ")
            print()

    """
        Function to set default home path.
    """

    def setHomeDir(self, path):
        print("Setting home path:", path)
        self.home_dir = path
        print("Checking if path exists...")
        put = subprocess.call(["hdfs dfs -test -e " + self.home_dir], shell=True)
        if int(put):
            print("Making a new path...")
            put = subprocess.call(["hdfs dfs -mkdir " + self.home_dir], shell=True)
            print("Testing if path was created...")
            put = subprocess.call(["hdfs dfs -test -e " + self.home_dir], shell=True)
            if int(put):
                print("There was an error making the home directory.")
                sys.exit(1)
            print("Path created succesfully. Let's Go!")
        else:
            print("Home directory exists. Let's Go!")
    """
        Function to clear the console screen.
    """ 

    def clear(self): 
    
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear')

    """
        Function to make a new schema and write
        it to the hdfs.
    """

    def makeSchema(self):
        # This function should go through
        # each column of the LOAD query,
        # and make it into this format:
        # col_name  | col_type  | col_index | col_location
        # "example" | "int"     | 0         | home_dir+"/"+col_name+".format"


  
        return 0

    """
        Function to check if the new DB exists,
        if not, then creates one.
    """

    def checkAndChangeDB(self):
        if('type' in self.parsed_query and self.parsed_query['type'].startswith("load") and (self.database != self.parsed_query['database'] or self.parsed_query['type'] == "load")):
            self.database = self.parsed_query['database']
            put = subprocess.call(["hdfs dfs -test -e " + self.home_dir + "/" + self.database + ".json"], shell=True)
            if int(put):
                if self.parsed_query['type'] == "load_existing":
                    print("ERROR: Database does not exist.")
                    self.database = None
                elif self.parsed_query['type'] == "load":
                    if self.makeSchema():
                        print("New database created.")
                    else:
                        self.database = None
                        print("ERROR: Database could not be made.")
            else:
                if self.parsed_query['type'] == "load":
                    print("ERROR: Database already exists.")
                    self.database = None
                elif self.parsed_query['type'] == "load_existing":
                    print("Switched to database:", self.database)
    
    """
        Main function to execute the given query.
    """

    def runQuery(self):
        if 'error' in self.parsed_query:
            print("ERROR:", self.parsed_query['error'])
        elif self.database is None and not self.parsed_query['type'].startswith("load"):
            print("ERROR: No database active.")
        else:
            self.checkAndChangeDB()


    """
        Function to continuously display prompt,
        and get queries.
    """
    
    def start(self):
        if self.home_dir is None:
            print("No hdfs HOME DIR specified. Exiting.")
            sys.exit(1)

        self.clear()
        print("==========")
        welcome = "Welcome to Simple SQL Engine!\nWe use map-reduce to do simple\ncalculations and parse SQL queries.\n\n\n1. \"clear\" or \"cls\" to clear the screen.\n2. \"\\q\" to quit."
        print(welcome)
        print("==========")
        print()
        print()
        while 1:
            query = input((self.database or "home") + "@" + self.our_name + "$ ")
            if query.strip(" ") == "":
                continue
            if query == "clear" or query == "cls":
                self.clear()
                continue
            if query == "\\q":
                break
            self.parser.parseQuery(query)
            self.parsed_query = self.parser.getParsedQuery()
            self.log(self.parsed_query)
            self.runQuery()
