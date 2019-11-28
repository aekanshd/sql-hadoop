from os import system, name 

class Console:
    parser = None
    our_name = None
    database = None
    parsed_query = None

    """
        Constructor function.
        Optional: Provide Parser
    """

    def __init__(self, parser=parser):
        self.parser = parser or SimpleSQLParser()
        self.our_name = "bd-sql-parser"

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
        Function to change the database.
    """
    def checkAndChangeDB(self):
        # Only change DB if:
        # 1. Type == "load"
        # 2. Current DB Name != New DB Name
        if('type' in self.parsed_query and self.parsed_query['type'].startswith("load") and self.database != self.parsed_query['database']):
            self.database = self.parsed_query['database']
            self.checkNewDB()

    """
        Function to check if the new DB exists,
        if not, then creates one.
    """
    def checkNewDB(self):
        # Code to check for new database.
        pass

    """
        Main function to parse the given query.
    """
    def parseQuery(self):
        self.checkAndChangeDB()


    """
        Function to continuously display prompt,
        and get queries.
    """
    def start(self):
        self.clear()
        print("==========")
        welcome = "Welcome to Simple SQL Engine!\nWe use map-reduce to do simple\ncalculations and parse SQL queries.\n\n\n1. \"clear\" or \"cls\" to clear the screen.\n2. \"\\q\" to quit."
        print(welcome)
        print("==========")
        print()
        print()
        while 1:
            query = input((self.database or "home") + "@" + self.our_name + "$ ")
            if query == "clear" or query == "cls":
                self.clear()
                continue
            if query == "\\q":
                break
            self.parser.parseQuery(query)
            self.parsed_query = self.parser.getParsedQuery()
            self.parseQuery()
