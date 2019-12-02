from os import system, name
from subprocess import Popen, PIPE
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
        Function to run a system command. Command Output
    """

    def runCommand(self, cmd, returnValue=False):
        self.log("Ran Command:", cmd)
        if not returnValue:
            p = Popen(cmd.split(" "), stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            output = output.decode('utf-8')
            self.log("Command Output", output)
            rc = p.returncode
            return output

        return subprocess.call([cmd], shell=True)

    """
        Function to check if path exists on HDFS.
        Returns 1 if path exists, else 0.
    """

    def checkIfExistsOnHDFS(self, path):
        test = self.runCommand("hdfs dfs -test -e " + path, returnValue=True)
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
                    self.log("Got the schema:", self.schema)
                    print("Switched to database:", self.database)
   
    """
        Function to verify column names.
    """
    
    def checkColumnNames(self):
        
        if self.schema is None:
            print("ERROR: No database schema available. Please LOAD again.")
            return 0

        for i in range(len(self.parsed_query['columns'])):
            if self.parsed_query['columns'][i] == "agg_column" or self.parsed_query['columns'][i] == "*":
                continue

            found = False
            for j in range(len(self.schema['column_types'])):
                if self.parsed_query['columns'][i] == self.schema['column_types'][j]['name']:
                    found = True
                    break
            if not found:
                print("ERROR: No column named", self.parsed_query['columns'][i] + " found.")
                return 0
        
        # All columns are available to us.
        return 1
    
    """
        Function to check if aggregates are ONLY
        on Integer values.
    """

    def checkAggColComp(self):
        if self.schema is None:
            print("ERROR: No database schema available. Please LOAD again.")
            return 0

        if self.parsed_query['aggregate'] is not None and self.parsed_query['agg_column'] is not None and len(self.parsed_query['columns']) > 1:
            print("WARNING: Columns other than agg_column will be dropped.")

        for i in range(len(self.schema['column_types'])):
            if self.parsed_query['agg_column'] == self.schema['column_types'][i]['name']:
                if self.schema['column_types'][i]['datatype'] != "integer":
                    print("ERROR: Cannot aggregate over column", self.parsed_query['agg_column'], "of type <" + str(self.schema['column_types'][i]['datatype']) + ">.")
                    return 0
                break

        # Column passed the test.
        return 1
   
    """
        Main function to execute the given query.
    """

    def runQuery(self):
        if 'error' in self.parsed_query:
            print("ERROR:", self.parsed_query['error'])
            return 0
        
        # First check if database is selected.
        if self.database is None:
            if not self.parsed_query['type'].startswith("load"):
                print("ERROR: No database active.")
            else:
                self.checkAndChangeDB()
        else:
            # Database is active.
            if self.parsed_query['type'].startswith("load"):
                self.checkAndChangeDB()
            else:
                if self.checkColumnNames():
                    # Checks were succesfull, now do something.
                    if self.checkAggColComp():
                        self.runCommand("hdfs dfs -cat " + self.home_dir + "/" + self.schema['csv_file_name'] + " | python3 mapper.py \'" + json.dumps(self.schema) + "\' \'" + json.dumps(self.parsed_query) + "\' | python3 reducer.py", returnValue=True)


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
