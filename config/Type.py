class Type():
    TASK = "TASK"
    PROBLEM = "PROBLEM"
    INITIATIVE = "INITIATIVE"

    TASK_STRING = "Task"
    PROBLEM_STRING = "Problem"
    INITIATIVE_STRING = "Initiative"

    @staticmethod
    def parse(status_type):
        match status_type:
            case Type.TASK_STRING:
                return Type.TASK
            case Type.PROBLEM_STRING:
                return Type.PROBLEM
            case Type.INITIATIVE_STRING:
                return Type.INITIATIVE
            case _:
                return "UNKNOWN"

    @staticmethod
    def stringify(status_type):
        match status_type:
            case Type.TASK:
                return Type.TASK_STRING
            case Type.PROBLEM:
                return Type.PROBLEM_STRING
            case Type.INITIATIVE:
                return Type.INITIATIVE_STRING
            case _:
                return "UNKNOWN"

    @staticmethod
    def emojify(status_type):
        match status_type:
            case Type.TASK:
                return "📋"
            case Type.PROBLEM:
                return "⚠️"
            case Type.INITIATIVE:
                return "💡"
            case _:
                return "❓"
