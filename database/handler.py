import sqlite3

class DatabaseHandler():
    def __init__(self, path_to_sqlite: str):
        """Establishes the connection to the given sqlite3 database.

            args: path_to_sqlite (str)
        """
        self.path_to_sqlite = path_to_sqlite

        self.projects = Projects(self)
        self.tasks = Tasks(self)

    def query(self, query_string: str) -> tuple:
        """Commands a query to the sqlite3 database.

            args: query_string (str)

            returns: (passed_with_no_errors (bool), answer (list) / exception (sqlite3.OperationalError)) (tuple)
        """
        connection = sqlite3.connect(self.path_to_sqlite)
        cursor = connection.cursor()

        try:
            answer = cursor.execute(query_string)
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

            connection.close()  # safley terminate the connection
            return (True, answer)

        except Exception as exception:
            connection.close()  # safley terminate the connection
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


class Projects():
    def __init__(self, db_handler: object):
        self.db_handler = db_handler

    def fetch_all(self):
        # query
        answer = self.db_handler.query("SELECT * FROM Project;")
        # return answer if correct else empty list
        return answer[1] if answer[0] else []

class Tasks():
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def fetch_condition(self, user_id: int, project_id: int, list_type: str):
        # securing each element which has the slightest possibility of being messed with
        secure_user_id = self.db_handler.secure(str(user_id))
        secure_project_id = self.db_handler.secure(str(project_id))
        secure_list_type = self.db_handler.secure(list_type)

        # query
        answer = self.db_handler.query(f"""
            SELECT * FROM Task WHERE
                (reporterID = {secure_user_id} OR asigneeId = {secure_user_id})
                AND projectID = {secure_project_id}
                AND type = '{secure_list_type}';
            """)

        # return answer if correct else empty list
        return answer[1] if answer[0] else []



# === TESTING PRUPOSES ONLY ===
def main():
    database = DatabaseHandler(input("Enter path to database: "))

    try:
        while True:
            answer = database.query(input(">>> "))

            if answer[0]:
                for row in answer[1]:
                    print(row)
            else:
                print(answer[1])

    except KeyboardInterrupt:
        pass
        # exit ...

if __name__ == "__main__":
    main()
