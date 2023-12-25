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
    string = string.replace("'", '%27')
    string = string.replace('"', '%22')
    string = string.replace('`', '%60')

    # XSS prevention
    string = string.replace("<", '%8B')
    string = string.replace(">", '%9B')
    string = string.replace("/", '%F7')

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

            answer = [list(row) for row in answer]

            # reformatting all possible sql injection attempts
            for row_index in range(len(answer)):
                for column_index in range(len(answer[row_index])):
                    if isinstance(answer[row_index][column_index], str):

                        # SQL injection prevention
                        answer[row_index][column_index] = answer[row_index][column_index].replace('%27', "'")
                        answer[row_index][column_index] = answer[row_index][column_index].replace('%22', '"')
                        answer[row_index][column_index] = answer[row_index][column_index].replace('%60', '`')

                        # XSS prevention
                        answer[row_index][column_index] = answer[row_index][column_index].replace('%8B', "<")
                        answer[row_index][column_index] = answer[row_index][column_index].replace('%9B', ">")
                        answer[row_index][column_index] = answer[row_index][column_index].replace('%F7', "/")

            connection.close()  # safley terminate the connection
            return (True, answer)

        except Exception as exception:
            print(exception)
            connection.close()  # safley terminate the connection
            return (False, exception)

    def check_update(self, timestamp: int) -> tuple:
        answer = self.query(f"SELECT username FROM User WHERE ID = 0;")
        new_timestamp = int(answer[1][0][0].split("=")[1])

        return (new_timestamp > timestamp, new_timestamp)

    def __update(self):
        self.query(f"UPDATE User SET username = 'update={ int(time.time()) }' WHERE ID = 0;")

    # specialized
    def select(self, table: object, object: object = None, **kwargs) -> list:
        # inquiry
        condition = self.__convert_defintion_based(table, **kwargs)
        answer = self.query(f"SELECT * FROM { table.name }" + (";" if len(kwargs) == 0 else f" WHERE { ' AND '.join(condition) };"))

        # answer formatting (either direct answer or object formatted answer (**kwargs))
        return answer[1] if object is None else [object(**self.__convert_python_based(table, *args)) for args in answer[1]]

    def insert(self, table: object, **kwargs):
        self.__update()
        # inquiry
        variables = self.__convert_order_based(table, **kwargs)
        answer = self.query(f"INSERT INTO { table.name } ({ ', '.join(variables['names']) }) VALUES ({ ', '.join(variables['values']) });")

    def update(self, table: object, id: int, **kwargs):
        self.__update()
        # inquiry
        variables = self.__convert_defintion_based(table, **kwargs)
        answer = self.query(f"UPDATE { table.name } SET { ','.join(variables) } WHERE ID = { id };")

    def delete(self, table: object, id: int):
        self.__update()
        # inquiry
        answer = self.query(f"DELETE FROM { table.name } WHERE ID = { id };")

    # __private
    def __convert_defintion_based(self, table: object, **kwargs) -> list:
        return [f"{ table.arguments[argument]['col_name'] } = { str(kwargs[argument]) }" for argument in table.arguments.keys() if argument in kwargs and kwargs[argument] is not None]

    def __convert_order_based(self, table: object, **kwargs) -> tuple:
        return {
            "names": [table.arguments[argument]["col_name"] for argument in table.arguments.keys() if argument in kwargs and kwargs[argument] is not None],
            "values": [str(kwargs[argument]) for argument in table.arguments.keys() if argument in kwargs and kwargs[argument] is not None]
        }

    def __convert_python_based(self, table: object, *args) -> set:
        return {list(table.arguments.keys())[arg_index]: list(table.arguments.values())[arg_index]["type"](args[arg_index]) if args[arg_index] is not None else None for arg_index in range(len(args))}


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
        "type": {
            "type": str,
            "col_name": "type"
        },
        "priority": {
            "type": str,
            "col_name": "priority"
        },
        "title": {
            "type": str,
            "col_name": "title"
        },
        "description": {
            "type": str,
            "col_name": "description"
        },
        "creator_id": {
            "type": int,
            "col_name": "creatorID"
        },
        "asignee_id": {
            "type": int,
            "col_name": "asigneeID"
        },
        "create_date": {
            "type": int,
            "col_name": "createDate"
        },
        "due_date": {
            "type": str,
            "col_name": "dueDate"
        },
        "status": {
            "type": str,
            "col_name": "status"
        }
    }

    def __init__(self, db_handler: object):
        self.db_handler = db_handler

        # constants
        self.name = "Task"

    @secure(arguments)
    def fetch(self, object: object = None if __name__ == "__main__" else TaskStruct, **kwargs):
        return self.db_handler.select(self, object, **kwargs)

    @secure(arguments)
    def fetch_all(self, object: object = None if __name__ == "__main__" else TaskStruct):
        return self.db_handler.select(self, object)

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
    def fetch(self, object: object = None if __name__ == "__main__" else ProjectStruct, **kwargs):
        return self.db_handler.select(self, object, **kwargs)

    @secure(arguments)
    def fetch_all(self, object: object = None if __name__ == "__main__" else TaskStruct):
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
    def fetch(self, object: object = None if __name__ == "__main__" else UserStruct, **kwargs):
        return self.db_handler.select(self, object, **kwargs)

    @secure(arguments)
    def fetch_all(self, object: object = None if __name__ == "__main__" else UserStruct):
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
    ACCESS_MODE = True

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

    except KeyboardInterrupt:
        pass
        # exit ...

if __name__ == "__main__":
    main()
