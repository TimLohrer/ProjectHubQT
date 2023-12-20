class Status():
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    BACKLOG_STRING = "Backlog"
    TODO_STRING = "ToDo"
    IN_PROGRESS_STRING = "In Progress"
    DONE_STRING = "Done"

    def parse(self, status):
        match status:
            case self.BACKLOG_STRING:
                return self.BACKLOG
            case self.TODO_STRING:
                return self.TODO
            case self.IN_PROGRESS_STRING:
                return self.IN_PROGRESS
            case self.DONE_STRING:
                return self.DONE
            case _:
                return "UNKNOWN"

    def stringify(self, status):
        match status:
            case self.BACKLOG:
                return self.BACKLOG_STRING
            case self.TODO:
                return self.TODO_STRING
            case self.IN_PROGRESS:
                return self.IN_PROGRESS_STRING
            case self.DONE:
                return self.DONE_STRING
            case _:
                return "UNKNOWN"
