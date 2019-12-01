import re
import traceback

class SimpleSQLParser:
    QUERY = None
    DICTIONARY = None
    strict = None

    """
        Constructor Function.
    """

    def __init__(self, strict=False):
        self.QUERY = None
        self.DICTIONARY = dict()
        self.strict = strict

    """
        Setter function for QUERY.
    """

    def addQuery(self, query):
        self.__init__(strict=self.strict)
        self.QUERY = query

    """
        Getter function for DICTIONARY.
    """

    def getParsedQuery(self):
        return self.DICTIONARY

    """
        Function to clear the DICTIONARY
        and insert the ERROR.
    """

    def clearAndMakeError(self, error):
        self.DICTIONARY = dict()
        self.DICTIONARY['error'] = error
        return 0

    """
        Function to check syntax of query.
    """

    def checkSyntax(self, query, syntax_to_be_checked=None):
        # Check if STRICT mode is ON => In which case, see if the
        # query ends with a semicolon (;)
        if self.QUERY.lower().strip(" ").endswith(";") and not self.strict:
            return self.clearAndMakeError("Please enable strict mode.")
        if syntax_to_be_checked is None and self.strict:
            if not self.QUERY.lower().strip(" ").endswith(";"):
                return self.clearAndMakeError("Syntax error. [STRICT ON]")
            else:
                # If test passed, remove the ending semicolon (;)
                self.QUERY = self.QUERY[:-1]

        # Default check: Allow only SELECT/LOAD queries.
        if syntax_to_be_checked is None or syntax_to_be_checked == "type":
            if not self.DICTIONARY['type'].lower() == "select" and not self.DICTIONARY['type'].lower().startswith("load"):
                return self.clearAndMakeError("Supported only SELECT/LOAD queries.")

        # Check if SELECT queries end with a comma
        if syntax_to_be_checked == "select_column_names":
            if query.strip(" ").endswith(","):
                return self.clearAndMakeError("Incorrect Syntax. (incomplete column names)")

        return 1

    """
        Function to detect the type of query based 
        on first word.
    """

    def parseQueryType(self):
        type_of_query = self.QUERY.split(" ")[0].lower()
        self.DICTIONARY['type'] = type_of_query

    """
        Function to parse the QUERY.
    """

    def parseQuery(self, query):
        # If no query, silently return
        if query == "":
            return self.clearAndMakeError("Please enter a query.")
        # First, set the QUERY variable.
        self.addQuery(query)
        # Then, set the QUERY TYPE.
        self.parseQueryType()
        # Check if all default syntax tests pass.
        if self.checkSyntax(self.QUERY):
            # If it is a SELECT query, then enter this flow.
            if self.DICTIONARY['type'].lower() == "select":
                # Get selected Columns and their names in an array.
                if self.getSelectedColumnNames(self.QUERY):
                    # Get optional WHERE Clauses in a dictionary.
                    if self.getWHEREClauses(self.QUERY):
                        # Finally, parse aggregate functions:
                        if self.getAggregateFunctions():
                            return self.DICTIONARY
            elif self.DICTIONARY['type'].lower().startswith("load"):
                # This is a load query, enter this flow.
                if self.parseLOADDatabase(self.QUERY):
                    return self.DICTIONARY

    """
        Function to define the WHERE clauses dictionary.
        This function returns two keys: AND, OR - both
        of which are arrays, and contain clauses under them.
    """

    def getWHEREClauses(self, query):
        clauses = dict()
        clauses['and'] = list()
        clauses['or'] = list()

        # Immediately exit if there is already an error.
        # TODO: Why does this condition arrive in the first place?
        if 'error' in self.DICTIONARY:
            return 0

        try:
            # Check if there is WHERE clause.
            len_where = len(query[:query.lower().index("where", len(self.DICTIONARY['type']))])

            try:
                # Check if the query has any brackets,
                # If yes - immediately raise an error.
                bracket_open = query[len_where + 5:].index("(", 0)
                bracket_close = query[len_where + 5:].index(")", 0)

                return self.clearAndMakeError("This parser does not support brackets.")
            except ValueError:
                # All basic tests passed, proceed to
                # get the WHERE query.
                clause_query = query[len_where + 5:]

                # Split the WHERE query based on ANDs.
                clauses['and'] = clause_query.lower().split(" and ")

                # Loop through each elements of the AND array.
                for index in range(len(clauses['and'])):
                    # Strip empty spaces from both ends.
                    clauses['and'][index] = clauses['and'][index].strip(" ")

                    # Further divide the query using OR clause.
                    or_clauses = clauses['and'][index].lower().split(" or ")

                    # If only ONE OR clause exists,
                    # Just append them into OR array.
                    # Example: "... WHERE this = that OR that = this;"
                    if len(clauses['and']) == 1:
                        if len(or_clauses) > 1:
                            clauses['and'] = list()
                            clauses['or'] = or_clauses
                        else:
                            clauses['and'] = or_clauses
                            clauses['or'] = list()
                    else:
                        # This means we have either 0, or
                        # more than 2 elements.
                        # (1 was already covered)
                        if len(or_clauses) == 2:
                            # If length is 2, then delete this
                            # element in the AND array.
                            # Add the left most bit to the
                            # AND Array, and the remaining
                            # in the OR Array.
                            # Example: "... WHERE a = b AND c = d OR d = e;"
                            # Here, AND: {"a = b", "c = d"}
                            # OR = {"d = e"}
                            del clauses['and'][index]
                            clauses['and'] = clauses['and'] + or_clauses[1:]
                            # del or_clauses[0] => Commented because (a or b and c) => a or (b and c)
                            clauses['or'] = clauses['or'] + or_clauses[0:1]
                        elif len(or_clauses) > 2:
                            # If more than 2 elements,
                            # just append to OR array.
                            del clauses['and'][index]
                            clauses['or'] = clauses['or'] + or_clauses

                # This loop goes through every element of
                # AND array, and strips their ";"s, and also
                # checks for dummy elements: in which case
                # exit, and show error.
                for index in range(len(clauses['and'])):
                    if clauses['and'][index].endswith(";"):
                        clauses['and'][index] = clauses['and'][index][:len(clauses['and'][index]) - 1]

                    if len(clauses['and'][index]) == 0:
                        return self.clearAndMakeError("Incorrect Syntax.")

                # Same loop as above, but for OR array.
                for index in range(len(clauses['or'])):
                    if clauses['or'][index].endswith(";"):
                        clauses['or'][index] = clauses['or'][index][:len(clauses['or'][index]) - 1]

                    if len(clauses['or'][index]) == 0:
                        return self.clearAndMakeError("Incorrect Syntax.")

        except ValueError:
            # This condition happens when there is NO where clause.
            # In this case, just pass an empty dictionary.
            pass

        # Everything went as expected, add dictionary
        # to the array.
        self.DICTIONARY['clauses'] = clauses
        return 1

    """
        Function to get column names.	
    """

    def getSelectedColumnNames(self, query):
        columns = list()
        len_type = len(self.DICTIONARY['type'])

        # First check if the keyword "FROM" exists.
        # In this case, our indexing length would be
        # different - we will use WHERE.
        try:
            column_query = query[len_type:query.lower().index("from", len_type)]
        except ValueError:
            try:
                column_query = query[len_type:query.lower().index("where", len_type)]
            except ValueError:
                # This means there is no FROM and WHERE.
                # Which means, get entire query!
                column_query = query[len_type:]

        # Check basic syntax - ending with comma's,
        # Incomplete column names, etc.
        if self.checkSyntax(column_query, syntax_to_be_checked="select_column_names"):
            # Split the column names by comma.
            columns = column_query.strip(" ").split(",")

            # Make a new list of columns.
            self.DICTIONARY['columns'] = list()

            # Iterate through each column,
            # remove extra spaces, and also check
            # If column name is empty - raise error if True.
            for index in range(len(columns)):
                if len(columns[index]) == 0:
                    return self.clearAndMakeError("Incomplete SELECT Query.")
                self.DICTIONARY['columns'].append(columns[index].strip())

        # All went as expected, return with no error.
        return 1

    """
        Function to parse LOAD queries.
    """

    def parseLOADDatabase(self, query):
        spaced_query = query.lower().split(" ")

        # If there are only two words,
        # We assume it is "LOAD database".
        if len(spaced_query) == 2:
            self.DICTIONARY['database'] = query.lower()[len("load"):].strip(" ")
            
            if self.DICTIONARY['database'] == "":
                return self.clearAndMakeError("Syntax error.")

            try:
                idex = self.DICTIONARY['database'].index("/", 0)
                return self.clearAndMakeError("No need to specify file name for just LOAD database.")
            except ValueError:
                self.DICTIONARY['type'] = "load_existing"
                return 1

        else:
            # Get the database name.
            self.DICTIONARY['database'] = query.lower()[len("load"):query.lower().index("/")].strip(" ")
            
            if self.DICTIONARY['database'] == "":
                return self.clearAndMakeError("Incorrect Syntax. (incomplete database name)")

            # Get the CSV file name.
            self.DICTIONARY['csv_file_name'] = query.lower()[query.lower().index("/") + 1:query.lower().index(" as")].strip(" ")

            if self.DICTIONARY['csv_file_name'] == "":
                return self.clearAndMakeError("Incorrect Syntax. (incomplete file name)")
                
            # Get the columns array string
            # within the brackets.
            try:
                column_array_string = query.lower()[query.lower().index(" as ", 0) + 4:].strip("(").strip(")")
            except ValueError:
                return self.clearAndMakeError("Incomplete LOAD query.")

            columns_array = column_array_string.split(",")

            # This is the columns array that will
            # get added to the DICTIONARY.
            columns = list()
            for index in range(len(columns_array)):
                # Strip the sentence of any extra spaces.
                columns_array[index] = columns_array[index].strip(" ")

                # Throw error if anything is empty.
                if columns_array[index] == "":
                    return self.clearAndMakeError("Incorrect syntax.")

                # Extract key:value pair.
                column_string = columns_array[index].split(":")

                # Loop through each such pair array.
                for second_index in range(len(column_string)):
                    # Strip all spaces.
                    # Ex => key:pair vs key: pair, etc
                    column_string[second_index] = column_string[second_index].strip(" ")

                    # Throw error if anything is empty.
                    if column_string[second_index] == "":
                        return self.clearAndMakeError("Incorrect syntax.")

                # Make a columnn dictionary.
                column = dict()

                # Add name, and datatype for that column.
                column['name'] = column_string[0]
                column['datatype'] = column_string[1]

                # Append this column to the columns array.
                columns.append(column)

            # All went well, insert into main dictionary.
            self.DICTIONARY['column_types'] = columns

            if 'column_types' not in self.DICTIONARY:
                self.clearAndMakeError("Incomplete query.")

        return 1

    """
        Function to get aggregate functions in the query.
        Adds the following keys:

        aggregate: Function to perform.
        agg_column: Column to perform above on.
        
        Removed original column, and adds a special
        column called: "agg_column" to the column list.
    """

    def getAggregateFunctions(self):
        
        # If not select query, just exit
        if not self.DICTIONARY['type'] == "select":
            return 1
        else:

            # Predefine both keys as null
            self.DICTIONARY['aggregate'] = None
            self.DICTIONARY['agg_column'] = None
            
            # Loop through each column
            for i in range(len(self.DICTIONARY['columns'])):
                
                # First check if they are empty brackets
                try:
                    self.DICTIONARY['columns'][i].index("()", 0)
                    
                    # Found! Return with error.
                    return self.clearAndMakeError("Incomplete aggregate function.")
                except ValueError:
                    pass
                
                # Search for "(word)" regex, where word != NULL or only spaces
                try:
                    # Special case: func(*)
                    try:
                        self.DICTIONARY['columns'][i].index("(*)", 0)
                        
                        # Found! Set all appropriate keys manually.
                        self.DICTIONARY['agg_column'] = "*"
                        self.DICTIONARY['aggregate'] = self.DICTIONARY['columns'][i].replace("(" + self.DICTIONARY['agg_column'] + ")", "").lower().strip(" ")
                        self.DICTIONARY['columns'][i] = "agg_column"
                        continue
                    except ValueError:
                        pass

                    # Get column name between brackets
                    self.DICTIONARY['agg_column'] = re.search(r"\((\w+)\)", self.DICTIONARY['columns'][i]).group(0)[1:-1].lower().strip(" ")
                    # Get function name
                    self.DICTIONARY['aggregate'] = self.DICTIONARY['columns'][i].replace("(" + self.DICTIONARY['agg_column'] + ")", "").lower().strip(" ")

                    # Safe check if either of the above are empty.
                    if self.DICTIONARY['agg_column'] == "" or self.DICTIONARY['aggregate'] == "":
                        return self.clearAndMakeError("Incomplete aggregate function.")

                    # Only replace original column name if agg_column is NOT empty.
                    if self.DICTIONARY['agg_column'] is not None:
                        self.DICTIONARY['columns'][i] = "agg_column" 

                except AttributeError:

                    # Regex NOT found - either not there, or brackets with spaces
                    try:
                        # Check if the column has any brackets,
                        # If yes - immediately raise an error.
                        self.DICTIONARY['columns'][i].index("(", 0)
                        self.DICTIONARY['columns'][i].index(")", 0)

                        return self.clearAndMakeError("Incomplete aggregate function.")
                    except ValueError:
                        # No regex, no spaces, no empty brackets
                        # Just move on to the next column
                        continue
                except Exception:
                    # There was some weird error.
                    return self.clearAndMakeError("Could not parse aggregate function(s).")
                    
            # All went well - return.
            return 1