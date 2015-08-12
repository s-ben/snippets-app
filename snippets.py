import logging
import argparse
import sys
import psycopg2

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='ubuntu' password='thinkful' host='localhost'")
logging.debug("Database connection established.")

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)


def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    # cursor = connection.cursor()
    # command = "insert into snippets values (%s, %s)"
    
    with connection, connection.cursor() as cursor:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
        # row = cursor.fetchone()
    
    # try:
    #     command = "insert into snippets values (%s, %s)"
    #     cursor.execute(command, (name, snippet))
    # except psycopg2.IntegrityError as e:
    #     connection.rollback()
    #     command = "update snippets set message=%s where keyword=%s"
    #     cursor.execute(command, (snippet, name))
        
    # cursor.execute(command, (name, snippet))
    # connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet...Enter snippet now?

    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    # cursor = connection.cursor()
    # command = "select message from snippets where keyword='%s'" % (name)
    # cursor.execute(command, (name))
    # row = cursor.fetchone()
    # connection.commit()
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
        
    if not row:
        # No snippet with that name
        print "No snippet with that name."
    else:    
        return row[0]

def catalog():
    cursor = connection.cursor()
    command = "select * from snippets"
    cursor.execute(command)
    whole_table = cursor.fetchall()
    return whole_table

def search(query):
    """ 
    Searches messages against the text string in 'query' argument 
    """
    logging.info("Querying for snippet {!r}".format(query))
    
    cursor = connection.cursor()
    command = "select * from snippets where message like '%{}%';" .format(query)
    # print command
    cursor.execute(command)
    row = cursor.fetchall()
    
    # whole_table = cursor.fetchall()
    # return whole_table
    
    # with connection, connection.cursor() as cursor:
    #     cursor.execute("select * from snippets where message like %s", (query))
    #     row = cursor.fetchone()
    matches = []
    for item in row:
        matches.append(item[1])
        # print item[1]
        # return row[1]
    return matches
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    # Subparse for the get command
    logging.debug("Constructing the get subparser") 
    get_parser = subparsers.add_parser("get", help="Get a snippet")
    get_parser.add_argument("name", help="The name of the snippet") 

    # Subparse for the search command
    logging.debug("Constructing the search subparser") 
    search_parser = subparsers.add_parser("search", help="Search for a snippet")
    search_parser.add_argument("query", help="The text string searched for in messages") 
    
    # Subparse for the catalog command
    logging.debug("Constructing the catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="List keys in table")
    
    
    arguments = parser.parse_args(sys.argv[1:])

    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog": 
        table_keys = catalog()
        # print type(table_keys)
        keylist = []
        for item in table_keys:
            keylist.append(item[0])
            print item[0]
    elif command == "search":
        
        matches = search(**arguments)
        print matches
        
            
        # [keylist[0] for keylist in table_keys]
        # print keylist
        # print table_keys[:][1]

if __name__ == "__main__":
    main()


