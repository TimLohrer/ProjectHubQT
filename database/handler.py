import sqlite3
import time

if not __name__ == "__main__":
    from config.structs import *
    from config.Status import Status
    from config.Type import Type
    from config.Priority import Priority


def secure(arguments: dict):
    """Decorator function securing all arguments parsed to the inclosing function.
        It is of importance that critical values (under critical values one understands
        values that will be parsed along to the database and there could be potentially subject to
        injection attacks - including but not limited to SQL injections)

        Args:
            arguments (dict): dictonary for translating between python values und slq params.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # securues kwargs -> only "defined" params will be changed while parsing "undefined" along.
            secure_kwargs = {argument: kwargs[argument] if not isinstance(kwargs[argument], str) else db_string_format(kwargs[argument])
                for argument in arguments.keys() if argument in kwargs and isinstance(kwargs[argument], arguments[argument]["type"])}

            return func(*args, **secure_kwargs)
        return wrapper
    return decorator

def db_string_format(string: str) -> str:
    """Prepares and formats a string for a safe database query.
        This prevents unwanted and potentially malicious attempts of
        accessing the sql database.

        Args:
            string (str): unsafe string

        Returns:
            (str): seucrly formatted string
    """
    # order in which these values are replaced are of importance
    string = string.replace(";", "%3B;")

    # SQL injection prevention
    string = string.replace("'", "%27;")
    string = string.replace('"', "%22;")
    string = string.replace("`", "%60;")

    safe_string = f"'{ string }'"

    return safe_string

def db_string_format_reverse(string: str) -> str:
    """Reverses the formation required for a safe database query.

        Args:
            string (str): safe database string

        Returns:
            (str): reversed format of given string
    """
    # SQL injection prevention
    string = string.replace("%27;", "'")
    string = string.replace("%22;", '"')
    string = string.replace("%60;", "`")

    # order in which these values are replaced are of importance
    string = string.replace("%3B;", ";")

    return string


class DatabaseHandler():
    def __init__(self, path_to_sqlite: str):
        """Establishes the connection to the given sqlite database.

            args: path_to_sqlite (str)
        """
        self.path_to_sqlite = path_to_sqlite

        self.tasks = Tasks(self)
        self.projects = Projects(self)
        self.users = Users(self)

    # general
    def query(self, query_string: str) -> tuple:
        """Commands a query to the sqlite3 database.

            Args:
                query_string (str)

            Returns:
                (passed_with_no_errors (bool), answer (list) / exception (sqlite3.OperationalError)) (tuple)
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
                # extracting column from table
                column = answer[row_index]

                for column_index in range(len(column)):
                    # extrating cell from column
                    cell = column[column_index]

                    # reverse string changes when type is str
                    if isinstance(cell, str): answer[row_index][column_index] = db_string_format_reverse(cell)

            connection.close()  # safley terminate the connection
            return (True, answer)

        except Exception as exception:
            print(exception)
            connection.close()  # safley terminate the connection
            return (False, exception)

    def check_update(self, timestamp: int) -> tuple:
        """Checking the update parameter (the update parameter
            is understood as to be the username with the user id equal to zero, this will be
            set to update=<unix_timestamp>) and whetever it is greater and therefore
            at a later date of the timestamp being provided.

            Args:
                timstamp (int): unix timestamp from the last update the Window had.

            Returns:
                (bool: whether there is a unaccounted update, int: timestamp form last database update) (tuple)
        """
        answer = self.query(f"SELECT username FROM User WHERE ID = 0;")
        new_timestamp = int(answer[1][0][0].split("=")[1])

        return (new_timestamp > timestamp, new_timestamp)

    def __update(func):
        """This decorator is responsible for setting the update parameter (the update parameter
            is understood as to be the username with the user id equal to zero, this will be
            set to update=<unix_timestamp>) to the current unix timestamp integer.
        """
        def wrapper(self, *args, **kwargs):
            # calling the function
            func(self, *args, **kwargs)

            # setting the update value to current time
            self.query(f"UPDATE User SET username = 'update={ int(time.time()) }' WHERE ID = 0;")
        return wrapper

    # specialized database access
    def select(self, table: object, object: object = None, **kwargs) -> list:
        # inquiry
        condition = self.__convert_defintion_based(table, **kwargs)
        answer = self.query(f"SELECT * FROM { table.name }" + (";" if len(kwargs) == 0 else f" WHERE { ' AND '.join(condition) };"))

        # answer formatting (either direct answer or object formatted answer (**kwargs))
        return answer[1] if object is None else [object(**self.__convert_python_based(table, *args)) for args in answer[1]]

    @__update # changes the db
    def insert(self, table: object, **kwargs):
        # inquiry
        variables = self.__convert_order_based(table, **kwargs)
        answer = self.query(f"INSERT INTO { table.name } ({ ', '.join(variables['names']) }) VALUES ({ ', '.join(variables['values']) });")

    @__update # changes the db
    def update(self, table: object, id: int, **kwargs):
        # inquiry
        variables = self.__convert_defintion_based(table, **kwargs)
        answer = self.query(f"UPDATE { table.name } SET { ','.join(variables) } WHERE ID = { id };")

    @__update # changes the db
    def delete(self, table: object, id: int):
        # inquiry
        answer = self.query(f"DELETE FROM { table.name } WHERE ID = { id };")

    # __private formation function
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
        return self.db_handler.select(table=self, object=object, **kwargs)

    @secure(arguments)
    def create(self, **kwargs):
        self.db_handler.insert(table=self, create_date=int(time.time()), **kwargs)

    @secure(arguments)
    def update(self, id: int, **kwargs):
        self.db_handler.update(table=self, id=id, **kwargs)

    @secure(arguments)
    def delete(self, id: int):
        self.db_handler.delete(table=self, id=id)

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
        return self.db_handler.select(table=self, object=object, **kwargs)

    @secure(arguments)
    def create(self, **kwargs):
        self.db_handler.insert(table=self, **kwargs)

    @secure(arguments)
    def update(self, id: int, **kwargs):
        self.db_handler.update(table=self, id=id, **kwargs)

    @secure(arguments)
    def delete(self, id: int):
        self.db_handler.delete(table=self, id=id)

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
        return self.db_handler.select(table=self, object=object, **kwargs)

    @secure(arguments)
    def create(self, **kwargs):
        self.db_handler.insert(table=self, **kwargs)

    @secure(arguments)
    def update(self, id: int, **kwargs):
        self.db_handler.update(table=self, id=id, **kwargs)

    @secure(arguments)
    def delete(self, id: int):
        self.db_handler.delete(table=self, id=id)


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
            database.projects.fetch()
            pass

    except KeyboardInterrupt:
        pass
        # exit ...

if __name__ == "__main__":
    main()
