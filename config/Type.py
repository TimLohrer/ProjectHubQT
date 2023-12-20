class Type():
    TASK = "TASK"
    PROBLEM = "PROBLEM"
    INITIATIVE = "INITIATIVE"

    TASK_STRING = "Task"
    PROBLEM_STRING = "Problem"
    INITIATIVE_STRING = "Initiative"

    def parse(self, type):
        match type:
            case self.TASK_STRING:
                return self.TASK
            case self.PROBLEM_STRING:
                return self.PROBLEM
            case self.INITIATIVE_STRING:
                return self.INITIATIVE
            case _:
                return "UNKNOWN"

    def stringify(self, type):
        match type:
            case self.TASK:
                return self.TASK_STRING
            case self.PROBLEM:
                return self.PROBLEM_STRING
            case self.INITIATIVE:
                return self.INITIATIVE_STRING
            case _:
                return "UNKNOWN"

    def emojify(self, type):
        match type:
            case self.TASK:
                return "📋"
            case self.PROBLEM:
                return "⚠️"
            case self.INITIATIVE:
                return "💡"
            case _:
                return "❓"