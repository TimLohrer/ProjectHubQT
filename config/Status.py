class Status():
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    def beautify(self, status):
        if status == self.BACKLOG:
            return "Backlog"
        elif status == self.TODO:
            return "ToDo"
        elif status == self.IN_PROGRESS:
            return "In Progress"
        elif status == self.DONE:
            return "Done"
        else:
            return "UNKNOWN"
