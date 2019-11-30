from os import system, name
import sys
import subprocess
import json

class Console:
    parser = None
    our_name = None
    database = None
    schema = None
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
        Function to run a system command.
    """

    def runCommand(self, cmd):
        self.log("Ran Command:", cmd)
        return subprocess.call([cmd], shell=True)

    """
        Function to check if path exists on HDFS.
        Returns 1 if path exists, else 0.
    """

    def checkIfExistsOnHDFS(self, path):
        test = self.runCommand("hdfs dfs -test -e " + path)
        return 0 if int(test) else 1

    """
        Function to set default home path.
    """

    def setHomeDir(self, path):
        print("Setting home path:", path)
        self.home_dir = path
        print("Checking if path exists...")
        if not self.checkIfExistsOnHDFS(self.home_dir):
            print("Making a new path...")
            self.runCommand("hdfs dfs -mkdir " + self.home_dir)
            print("Testing if path was created...")
            if not self.checkIfExistsOnHDFS(self.home_dir):
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
        db_file_name = self.database + ".json"
        
        if not self.checkIfExistsOnHDFS(self.home_dir + "/" + db_file_name):
            for index in range(len(self.parsed_query['column_types'])):
                self.parsed_query['column_types'][index]['index'] = index

            with open(db_file_name,"w") as f:
                f.write(json.dumps(self.parsed_query))
    
            self.runCommand("hdfs dfs -put " + db_file_name + " " + self.home_dir)

            if self.checkIfExistsOnHDFS(self.home_dir + "/" + db_file_name):
                self.runCommand("rm " + db_file_name)
                self.runCommand("hdfs dfs -put " + self.parsed_query['csv_file_name'] + " " + self.home_dir)
                if self.checkIfExistsOnHDFS(self.home_dir + "/" + self.parsed_query['csv_file_name']):
                    self.schema = self.parsed_query
                    return 1
                else:
                    self.log("Could not transfer csv to HDFS.")
                    return 0
            else:
                self.log("Could not transfer database to HDFS.")
                return 0
        else:
            print("ERROR: Database already exists. Use only LOAD to switch.")
            self.database = None
            return 0

    """
        Function to check if the new DB exists,
        if not, then creates one.
    """

    def checkAndChangeDB(self):
        if('type' in self.parsed_query and self.parsed_query['type'].startswith("load") and (self.database != self.parsed_query['database'] or self.parsed_query['type'] == "load")):
            self.database = self.parsed_query['database']

            if not self.checkIfExistsOnHDFS(self.home_dir + "/" + self.database + ".json"):
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
                    self.schema = json.loads(self.runCommand("hdfs dfs -cat " + self.home_dir + "/" + self.database + ".json"))
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
