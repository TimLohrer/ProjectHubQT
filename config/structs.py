class UserStruct():
    def __init__(self, id, fristname=None, surname=None, username=None, email=None):
        self.id          = id
        self.first_name  = fristname if fristname is not None else ""
        self.sur_name    = surname if surname is not None else ""
        self.username    = username if username is not None else ""
        self.email       = email if email is not None else ""

class ProjectStruct():
    def __init__(self, id, name=None, description=None):
        self.id          = id
        self.name        = name if name is not None else ""
        self.description = description if description is not None else ""

class ComponentStruct():
    def __init__(self, id, leader_id, name=None):
        self.id          = id
        self.name        = name if name is not None else ""
        self.leader_id   = leader_id

class TaskStruct():
    def __init__(self, id, project_id, creator_id, create_date, type=None, priority=None, title=None, description=None, asignee_id=None, due_date=None, status=None):
        self.id            = id
        self.project_id    = project_id
        self.type          = type if type is not None else "TASK"
        self.priority      = priority if priority is not None else "MEDIUM"
        self.title         = title if title is not None else ""
        self.description   = description if description is not None else ""
        self.creator_id    = creator_id
        self.asignee_id    = asignee_id
        self.creation_date = create_date
        self.due_date      = due_date if due_date is not None else ""
        self.status        = status if status is not None else "BACKLOG"
