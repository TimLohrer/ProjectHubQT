import sqlite3
import time

if not __name__ == "__main__":
    from config.structs import *
    from config.Status import Status
    from config.Type import Type
    from config.Priority import Priority


def secure(arguments: dict):
    def decorator(func):
        def wrapper(*args, **kwargs):
            secure_kwargs = {argument: kwargs[argument] if not isinstance(kwargs[argument], str) else safe_string(kwargs[argument])
                for argument in arguments.keys() if argument in kwargs and isinstance(kwargs[argument], arguments[argument]["type"])}

            return func(*args, **secure_kwargs)
        return wrapper
    return decorator

def safe_string(string: str):
    # SQL injection prevention
    string.replace("'", '%27')
    string.replace('"', '%22')
    string.replace('`', '%60')

    # XSS prevention
    string.replace("<", '%8B')
    string.replace(">", '%9B')
    string.replace("/", '%F7')

    safe_string = f"'{ string }'"

    return safe_string



class DatabaseHandler():
    def __init__(self, path_to_sqlite: str):
        """Establishes the connection to the given sqlite3 database.

            args: path_to_sqlite (str)
        """
        self.path_to_sqlite = path_to_sqlite

        self.tasks = Tasks(self)
        self.projects = Projects(self)
        self.users = Users(self)

    # general
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
            connection.commit()

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

    # specialized
    def select(self, table: object, object: object = None, **kwargs) -> list:
        # inquiry
        condition = self.__convert_defintion_based(table, **kwargs)
        answer = self.query(f"SELECT * FROM { table.name }" + (";" if len(kwargs) == 0 else f" WHERE { " AND ".join(condition) };"))

        # answer formatting (either direct answer or object formatted answer)
        return answer[1] if object is None else [object(*row) for row in answer[1]]

    def insert(self, table: object, **kwargs):
        # inquiry
        variables = self.__convert_order_based(table, **kwargs)
        answer = self.query(f"INSERT INTO { table.name } ({ ", ".join(variables["names"]) }) VALUES ({ ", ".join(variables["values"]) });")

    def update(self, table: object, id: int, **kwargs):
        # inquiry
        variables = self.__convert_defintion_based(table, **kwargs)
        answer = self.query(f"UPDATE { table.name } SET { ",".join(variables) } WHERE ID = { id };")

    def delete(self, table: object, id: int):
        # inquiry
        answer = self.query(f"DELETE FROM { table.name } WHERE ID = { id };")

    # __private
    def __convert_defintion_based(self, table: object, **kwargs) -> list:
        return [f"{ table.arguments[argument]["col_name"] } = { str(kwargs[argument]) }" for argument in table.arguments.keys() if argument in kwargs and kwargs[argument] is not None]

    def __convert_order_based(self, table: object, **kwargs) -> tuple:
        return {
            "names": [table.arguments[argument]["col_name"] for argument in table.arguments.keys() if argument in kwargs and kwargs[argument] is not None],
            "values": [str(kwargs[argument]) for argument in table.arguments.keys() if argument in kwargs and kwargs[argument] is not None]
        }


class Tasks():
    arguments = {
        "id": {
            "type": int,
            "col_name": "ID"
        },
        "project_id": {
            "type": int,
            "col_name": "projectID"
        },
        "creator_id": {
            "type": int,
            "col_name": "creatorID"
        },
        "asignee_id": {
            "type": int,
            "col_name": "asigneeID"
        },
        "title": {
            "type": str,
            "col_name": "title"
        },
        "description": {
            "type": str,
            "col_name": "description"
        },
        "type": {
            "type": str,
            "col_name": "type"
        },
        "status": {
            "type": str,
            "col_name": "status"
        },
        "priority": {
            "type": str,
            "col_name": "priority"
        },
        "due_date": {
            "type": int,
            "col_name": "dueDate"
        },
        "create_date": {
            "type": int,
            "col_name": "createDate"
        }
    }

    def __init__(self, db_handler: object):
        self.db_handler = db_handler

        # constants
        self.name = "Task"

    @secure(arguments)
    def fetch(self, project_id: int, status: str, object: object = None if __name__ == "__main__" else TaskStruct):
        return self.db_handler.select(self, object, project_id=project_id, status=status)

    @secure(arguments)
    def create(self, **kwargs):
        self.db_handler.insert(self, create_date=int(time.time()), **kwargs)

    @secure(arguments)
    def update(self, id: int, **kwargs):
        self.db_handler.update(self, id, **kwargs)

    @secure(arguments)
    def delete(self, id: int):
        self.db_handler.delete(self, id)

class Projects():
    arguments = {
        "id": {
            "type": int,
            "col_name": "ID"
        },
        "name": {
            "type": str,
            "col_name": "name"
        },
        "description": {
            "type": str,
            "col_name": "description"
        }
    }

    def __init__(self, db_handler: object):
        self.db_handler = db_handler

        # constants
        self.name = "Project"

    @secure(arguments)
    def fetch(self, object: object = None if __name__ == "__main__" else ProjectStruct):
        return self.db_handler.select(self, object)

    @secure(arguments)
    def create(self, **kwargs):
        self.db_handler.insert(self, **kwargs)

    @secure(arguments)
    def update(self, id: int, **kwargs):
        self.db_handler.update(self, id, **kwargs)

    @secure(arguments)
    def delete(self, id: int):
        self.db_handler.delete(self, id)

class Users():
    arguments = {
        "id": {
            "type": int,
            "col_name": "ID"
        },
        "firstname": {
            "type": str,
            "col_name": "firstname"
        },
        "surname": {
            "type": str,
            "col_name": "surname"
        },
        "username": {
            "type": str,
            "col_name": "username"
        },
        "email": {
            "type": str,
            "col_name": "email"
        }
    }

    def __init__(self, db_handler: object):
        self.db_handler = db_handler

        # contants
        self.name = "User"

    @secure(arguments)
    def fetch(self, object: object = None if __name__ == "__main__" else UserStruct):
        return self.db_handler.select(self, object)

    @secure(arguments)
    def create(self, **kwargs):
        self.db_handler.insert(self, **kwargs)

    @secure(arguments)
    def update(self, id: int, **kwargs):
        self.db_handler.update(self, id, **kwargs)

    @secure(arguments)
    def delete(self, id: int):
        self.db_handler.delete(self, id)




# === TESTING PRUPOSES ONLY ===
def main():
    ACCESS_MODE = False

    try:
        database = DatabaseHandler(input("Enter path to database: "))

        if ACCESS_MODE:
            while True:
                answer = database.query(input(">>> "))

                if answer[0]:
                    for row in answer[1]:
                        print(row)
                else:
                    print(answer[1])
        else:
            # code here ...
            pass
            print(database.tasks.fetch(project_id=3, status="BACKLOG"))
            print(database.projects.fetch())
            # print(database.users.fetch())

    except KeyboardInterrupt:
        pass
        # exit ...

if __name__ == "__main__":
    main()
