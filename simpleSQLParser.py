class SimpleSQLParser():
    QUERY = None
    DICTIONARY = None

    def __init__(self):
        self.QUERY = None
        self.DICTIONARY = dict()

    def addQuery(self, query):
        self.QUERY = query

    def clearAndMakeError(self, error):
        self.DICTIONARY = dict()
        self.DICTIONARY['error'] = error
        return 0
        
    def checkSyntax(self, query, syntax_to_be_checked=None):
        if(syntax_to_be_checked is None or syntax_to_be_checked == "type"):
            if(not self.DICTIONARY['type'].lower() == "select" and not self.DICTIONARY['type'].lower() == "load"):
                return self.clearAndMakeError("Supported only SELECT/UPDATE queries.")
        if(syntax_to_be_checked == "select_column_names"):
            if(query.strip(" ").endswith(",")):
                print("\"" + query + "\"")
                return self.clearAndMakeError("Incorrect Syntax. (incomplete column names)") 
        
        return 1

    def parseQueryType(self):
        type_of_query = self.QUERY.split(" ")[0]
        self.DICTIONARY['type'] = type_of_query

    def getSelectedColumnNames(self, query):
        columns = list()
        column_query = query[len(self.DICTIONARY['type']):query.lower().index("from", len(self.DICTIONARY['type']))]
        if(self.checkSyntax(column_query, syntax_to_be_checked="select_column_names")):
            columns = column_query.strip(" ").split(",")
            self.DICTIONARY['columns'] = list()
            for index in range(len(columns)):
                if(len(columns[index]) == 0):
                    return self.clearAndMakeError("Incomplete SELECT Query.")
                self.DICTIONARY['columns'].append(columns[index].strip())


        return 1


    def parseQuery(self, query):
        self.addQuery(query)
        self.parseQueryType()
        if(self.checkSyntax(self.QUERY)):
            if(self.DICTIONARY['type'].lower() == "select"):
                if(self.getSelectedColumnNames(self.QUERY)):
                    print("Got column Names.")
