class Type():
    TASK = "TASK"
    PROBLEM = "PROBLEM"
    INITIATIVE = "INITIATIVE"

    def beautify(self, type):
        if type == self.TASK:
            return "Task"
        elif type == self.PROBLEM:
            return "Problem"
        elif type == self.INITIATIVE:
            return "Initiative"
        else:
            return "UNKNOWN"