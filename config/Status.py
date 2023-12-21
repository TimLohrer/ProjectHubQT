class Status():
    """Unnötig."""

    BACKLOG = "BACKLOG"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    BACKLOG_STRING = "Backlog"
    TODO_STRING = "ToDo"
    IN_PROGRESS_STRING = "In Progress"
    DONE_STRING = "Done"

    @staticmethod
    def parse(status):
        match status:
            case Status.BACKLOG_STRING:
                return Status.BACKLOG
            case Status.TODO_STRING:
                return Status.TODO
            case Status.IN_PROGRESS_STRING:
                return Status.IN_PROGRESS
            case Status.DONE_STRING:
                return Status.DONE
            case _:
                return "UNKNOWN"

    @staticmethod
    def stringify(status):
        match status:
            case Status.BACKLOG:
                return Status.BACKLOG_STRING
            case Status.TODO:
                return Status.TODO_STRING
            case Status.IN_PROGRESS:
                return Status.IN_PROGRESS_STRING
            case Status.DONE:
                return Status.DONE_STRING
            case _:
                return "UNKNOWN"

    @staticmethod
    def emojify(status):
        match status:
            case Status.BACKLOG:
                return "📚"
            case Status.TODO:
                return "📝"
            case Status.IN_PROGRESS:
                return "🕥"
            case Status.DONE:
                return "✅"
            case _:
                return "❓"
