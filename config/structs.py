class UserStruct():
    def __init__(self, id: int, firstname: str = "", surname: str = "", username: str = "", email: str = ""):
        self.id          = id
        self.firstname   = firstname
        self.surname     = surname
        self.username    = username
        self.email       = email

class ProjectStruct():
    def __init__(self, id: int, name: str = "", description: str = ""):
        self.id          = id
        self.name        = name
        self.description = description

class ComponentStruct():
    def __init__(self, id: int, leader_id: int, name: str = ""):
        self.id          = id
        self.name        = name
        self.leader_id   = leader_id

class TaskStruct():
    def __init__(self, id: int, project_id: int, creator_id: int, create_date: int, type: str = "TASK", priority: str = "MEDIUM", title: str = "", description: str = "", asignee_id: int = "", due_date: str = "", status: str = "BACKLOG"):
        self.id            = id
        self.project_id    = project_id
        self.type          = type
        self.priority      = priority
        self.title         = title
        self.description   = description
        self.creator_id    = creator_id
        self.asignee_id    = asignee_id
        self.creation_date = create_date
        self.due_date      = due_date
        self.status        = status
