class UserStruct():
    def __init__(self, id, fristname, surname, username, email):
        self.id          = id
        self.first_name  = fristname if fristname is not None else ""
        self.sur_name    = surname if surname is not None else ""
        self.username    = username if username is not None else ""
        self.email       = email if email is not None else ""

class ProjectStruct():
    def __init__(self, id, name, description):
        self.id          = id
        self.name        = name if name is not None else ""
        self.description = description if description is not None else ""

class ComponentStruct():
    def __init__(self, id, name, leader_id):
        self.id          = id
        self.name        = name if name is not None else ""
        self.leader_id   = leader_id

class TaskStruct():
    def __init__(self, id, project_id, type, priority, title, description, creator_id, asignee_id, create_date, due_date, status):
        self.id            = id
        self.project_id    = project_id
        self.type          = type if type is not None else ""
        self.priority      = priority if priority is not None else ""
        self.title         = title if title is not None else ""
        self.description   = description if description is not None else ""
        self.creator_id    = creator_id
        self.asignee_id    = asignee_id
        self.creation_date = create_date
        self.due_date      = due_date
        self.status        = status if status is not None else ""
