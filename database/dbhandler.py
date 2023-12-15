import sqlite3

class DatabaseHandler():
    def __init__(self, path_to_sqlite: str):
        """Establishes the connection to the given sqlite3 database.

            args: path_to_sqlite (str)
        """
        self.connection = sqlite3.connect(path_to_sqlite)
        self.cursor = self.connection.cursor()

    def query(self, query_string: str) -> tuple:
        """Commands a query to the sqlite3 database.

            args: query_string (str)

            returns: (passed_with_no_errors (bool), answer (list) / exception (sqlite3.OperationalError)) (tuple)"""
        try:
            answer = self.cursor.execute(query_string)
            answer = answer.fetchall()

            # reformatting all possible sql injection attempts
            for row in answer:
                for column in row:
                    if type(column) == str:
                        # SQL injection prevention
                        column.replace('%27', "'")
                        column.replace('%22', '"')
                        column.replace('%60', '`')

                        # XSS prevention
                        column.replace('%8B', "<")
                        column.replace('%9B', ">")
                        column.replace('%F7', "/")

            return (True, answer)

        except Exception as exception:
            return (False, exception)

    def secure(self, unsecure_string: str) -> str:
        """Prevent sql injection and cross-site-scripting.
            Takes in a possible unsecure string and reformats it to be safley fed into the query.

            args: unsecure_string (str)

            returns: secure_string (str)
        """
        # SQL injection prevention
        unsecure_string.replace("'", '%27')
        unsecure_string.replace('"', '%22')
        unsecure_string.replace('`', '%60')

        # XSS prevention
        unsecure_string.replace("<", '%8B')
        unsecure_string.replace(">", '%9B')
        unsecure_string.replace("/", '%F7')

        # retuning safe string
        return unsecure_string

    def close(self) -> int:
        """Closes the sqlite3 connection.
            Returns 0 if successful else if not.

            returns 0 if successful (int)
        """
        self.connection.close()

        return 0


# === TESTING PRUPOSES ONLY ===
def main():
    database = DatabaseHandler(input("Enter path to database: "))

    try:
        while True:
            answer = database.query(input(">>> "))

            for row in answer[1]:
                print(row)

    except KeyboardInterrupt:
        database.close()
        # exit ...

if __name__ == "__main__":
    main()
