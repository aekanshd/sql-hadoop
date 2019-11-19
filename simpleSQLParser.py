class SimpleSQLParser:
    QUERY = None
    DICTIONARY = None

    def __init__(self):
        self.QUERY = None
        self.DICTIONARY = dict()

    def addQuery(self, query):
        self.QUERY = query

    def getParsedQuery(self):
        return self.DICTIONARY

    def clearAndMakeError(self, error):
        self.DICTIONARY = dict()
        self.DICTIONARY['error'] = error
        return 0

    def checkSyntax(self, query, strict=False, syntax_to_be_checked=None):
        if syntax_to_be_checked is None and strict:
            if not self.QUERY.lower().strip(" ").endswith(";"):
                return self.clearAndMakeError("Syntax error. [STRICT ON]")
            elif self.QUERY.lower().strip(" ").endswith(";"):
                self.QUERY = self.QUERY[:-1]
        if syntax_to_be_checked is None or syntax_to_be_checked == "type":
            if not self.DICTIONARY['type'].lower() == "select" and not self.DICTIONARY['type'].lower() == "load":
                return self.clearAndMakeError("Supported only SELECT/UPDATE queries.")
        if syntax_to_be_checked == "select_column_names":
            if query.strip(" ").endswith(","):
                return self.clearAndMakeError("Incorrect Syntax. (incomplete column names)")

        return 1

    def parseQueryType(self):
        type_of_query = self.QUERY.split(" ")[0]
        self.DICTIONARY['type'] = type_of_query

    def parseQuery(self, query, strict=False):
        self.addQuery(query)
        self.parseQueryType()
        if self.checkSyntax(self.QUERY, strict=strict):
            if self.DICTIONARY['type'].lower() == "select":
                if self.getSelectedColumnNames(self.QUERY):
                    if self.getWHEREClauses(self.QUERY):
                        print("Got WHERE clause.")

    def getWHEREClauses(self, query):
        clauses = dict()
        clauses['AND'] = list()
        clauses['OR'] = list()

        if 'error' in self.DICTIONARY:
            return 0

        try:
            len_where = len(query[:query.lower().index("where", len(self.DICTIONARY['type']))])

            try:
                bracket_open = query[len_where+5:].index("(", 0)
                bracket_close = query[len_where + 5:].index(")", 0)

                return self.clearAndMakeError("This parser does not support brackets.")
            except ValueError:
                clause_query = query[len_where + 5:]
                clauses['AND'] = clause_query.lower().split(" and ")

                for index in range(len(clauses['AND'])):
                    clauses['AND'][index] = clauses['AND'][index].strip(" ")
                    or_clauses = clauses['AND'][index].lower().split(" or ")
                    if len(clauses['AND']) == 1:
                        clauses['AND'] = list()
                        clauses['OR'] = or_clauses
                    else:
                        if len(or_clauses) == 2:
                            del clauses['AND'][index]
                            clauses['AND'] = clauses['AND'] + or_clauses[0:1]
                            del or_clauses[0]
                            clauses['OR'] = clauses['OR'] + or_clauses
                        elif len(or_clauses) > 2:
                            del clauses['AND'][index]
                            clauses['OR'] = clauses['OR'] + or_clauses

                for index in range(len(clauses['AND'])):
                    if clauses['AND'][index].endswith(";"):
                        clauses['AND'][index] = clauses['AND'][index][:len(clauses['AND'][index]) - 1]

                    if len(clauses['AND'][index]) == 0:
                        return self.clearAndMakeError("Incorrect Syntax.")

                for index in range(len(clauses['OR'])):
                    if clauses['OR'][index].endswith(";"):
                        clauses['OR'][index] = clauses['OR'][index][:len(clauses['OR'][index]) - 1]

                    if len(clauses['OR'][index]) == 0:
                        return self.clearAndMakeError("Incorrect Syntax.")

        except ValueError:
            pass

        self.DICTIONARY['CLAUSES'] = clauses
        return 1

    def getSelectedColumnNames(self, query):
        columns = list()
        len_type = len(self.DICTIONARY['type'])
        try:
            column_query = query[len_type:query.lower().index("from", len_type)]
        except ValueError:
            try:
                column_query = query[len_type:query.lower().index("where", len_type)]
            except ValueError:
                column_query = query[len_type:]
        if self.checkSyntax(column_query, syntax_to_be_checked="select_column_names"):
            columns = column_query.strip(" ").split(",")
            self.DICTIONARY['columns'] = list()
            for index in range(len(columns)):
                if len(columns[index]) == 0:
                    return self.clearAndMakeError("Incomplete SELECT Query.")
                self.DICTIONARY['columns'].append(columns[index].strip())

        return 1
