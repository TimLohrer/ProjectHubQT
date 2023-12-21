import sqlite3
import time

from config.structs import *
from config.Status import Status
from config.Type import Type
from config.Priority import Priority

def secure(func):
    """Prevent sql injection and cross-site-scripting.
        Takes in a possible unsecure string and reformats it to be safley fed into the query.

        args: func (function object)

        This is intended to be a decorator.
    """
    def wrapper(*args, **kwargs):
        """Modifies and parses sql safe arguemts to a given function."""
        # replaces critical chars with its safe counterparts
        secure_arg = lambda unsecure: unsecure.replace("'", "%27").replace('"', "%22").replace("`", "%60").replace("<", "%8B").replace(">", "%9B").replace("/", "%F7") # <--- i'm not super proud of that

        # securing
        secure_args = [secure_arg(arg) if isinstance(arg, str) else arg for arg in args]
        secure_kwargs = {key: secure_arg(arg) if isinstance(arg, str) else arg for arg in kwargs.items()}

        # call the function
        return func(*secure_args, **secure_kwargs)
    return wrapper

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


class Projects():
    def __init__(self, db_handler: object):
        self.db_handler = db_handler

    @secure
    def fetch_all(self):
        query = """SELECT * FROM Project;"""

        answer = self.db_handler.query(query)
        # return answer if correct else empty list
        return [ProjectStruct(project) for project in answer[1]] if answer[0] else []

class Tasks():
    def __init__(self, db_handler: object):
        self.db_handler = db_handler

    @secure
    def fetch_by(self, project_id: int, status: str):
        query = f"""
            SELECT * FROM Task WHERE
                projectID = {project_id}
                AND status = '{status}';
            """

        answer = self.db_handler.query(query)
        # return answer if correct else empty list
        return [TaskStruct(task) for task in answer[1]] if answer[0] else []

    @secure
    def create(self,
            project_id: int,
            creator_id: int,
            asignee_id: int,
            title: str,
            description: str = "",
            task_type: str = Type.TASK,
            status: str = Status.BACKLOG,
            priority: str = Priority.MEDIUM,
            due_date: int = None
        ):
        create_date = time.time()
        query = f"""
            INSERT INTO Task (
                    projectID,
                    type,
                    priority,
                    title,
                    description,
                    creatorID,
                    asigneeID,
                    createDate,
                    dueDate,
                    status
                ) VALUES (
                    {int(project_id)},
                    '{task_type}',
                    '{priority}',
                    '{title}',
                    '{description}',
                    {int(creator_id)},
                    {int(asignee_id)},
                    {int(due_date)},
                    {int(create_date)},
                    '{status}');
        """

        # query
        answer = self.db_handler.query(query)

        print(query)

        return answer



# === TESTING PRUPOSES ONLY ===
def main():
    try:
        database = DatabaseHandler(input("Enter path to database: "))

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
