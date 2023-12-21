import sqlite3
import time

from config.structs import *
from config.Status import Status
from config.Type import Type
from config.Priority import Priority

class DatabaseHandler():
    def __init__(self, path_to_sqlite: str):
        """Establishes the connection to the given sqlite3 database.

            args: path_to_sqlite (str)
        """
        self.path_to_sqlite = path_to_sqlite

        self.system = System(self)
        self.projects = Projects(self)
        self.tasks = Tasks(self)

    def query(self, query_string: str, update: bool = False) -> tuple:
        """Commands a query to the sqlite3 database.

            args: query_string (str)

            returns: (passed_with_no_errors (bool), answer (list) / exception (sqlite3.OperationalError)) (tuple)
        """
        connection = sqlite3.connect(self.path_to_sqlite)
        cursor = connection.cursor()

        try:
            answer = cursor.execute(query_string)

            if update:
                connection.commit()
                connection.close()
                self.system.set_update()
                return (True, None)


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


class System():
    def __init__(self, db_handler: object):
        self.db_handler = db_handler

    def fetch_update(self):
        # query
        answer = self.db_handler.query("SELECT username FROM User WHERE ID == 0;")
        # return answer if correct else empty list
        return answer

    def set_update(self):
        # query
        answer = self.db_handler.query(f"UPDATE User SET username = 'update={int(time.time())}' WHERE ID == 0;", True)
        # return answer if correct else empty list
        return answer

class Projects():
    def __init__(self, db_handler: object):
        self.db_handler = db_handler

    def fetch_all(self):
        # query
        answer = self.db_handler.query("SELECT * FROM Project;")
        # return answer if correct else empty list
        return [ProjectStruct(project) for project in answer[1]] if answer[0] else []

class Tasks():
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def fetch_condition(self, project_id: int, status: str):
        # securing each element which has the slightest possibility of being messed with
        secure_project_id = self.db_handler.secure(str(project_id))
        secure_status = self.db_handler.secure(status)

        # query
        answer = self.db_handler.query(f"""
            SELECT * FROM Task WHERE
                projectID = {secure_project_id}
                AND status = '{secure_status}';
            """)

        # return answer if correct else empty list
        return [TaskStruct(task) for task in answer[1]] if answer[0] else []

    def create(self, project_id: int, creator_id: int, asignee_id: int, title: str, description: str = "", type: str = Type.TASK, status: str = Status.BACKLOG, priority: str = Priority.MEDIUM, due_date: str = ""):
        # securing each element which has the slightest possibility of being messed with
        secure_project_id = self.db_handler.secure(str(project_id))
        secure_creator_id = self.db_handler.secure(str(creator_id))
        secure_asignee_id = self.db_handler.secure(str(asignee_id))
        secure_title = self.db_handler.secure(str(title))
        secure_description = self.db_handler.secure(str(description))
        secure_type = self.db_handler.secure(str(type))
        secure_status = self.db_handler.secure(str(status))
        secure_priority = self.db_handler.secure(str(priority))
        secure_due_date = self.db_handler.secure(str(due_date))

        create_date = ""

        # query
        answer = self.db_handler.query(f"""
            INSERT INTO Task
                (projectID, type, priority, title, description, creatorID, asigneeID, createDate, dueDate, status)
                VALUES ({int(secure_project_id)}, '{secure_type}', '{secure_priority}', '{secure_title}', '{secure_description}', {int(secure_creator_id)}, {int(secure_asignee_id)}, '{secure_due_date}', '{create_date}', '{secure_status}');
            """, True)

        return answer



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
