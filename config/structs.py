class UserStruct():
    def __init__(self, project):
        self.id          = user[0]
        self.first_name  = user[1] if user[1] is not None else ""
        self.sur_name    = user[2] if user[2] is not None else ""
        self.username    = user[3] if user[3] is not None else ""
        self.email       = user[4] if user[4] is not None else ""

class ProjectStruct():
    def __init__(self, project):
        self.id          = project[0]
        self.name        = project[1] if project[1] is not None else ""
        self.description = project[2] if project[2] is not None else ""

class ComponentStruct():
    def __init__(self, component):
        self.id          = component[0]
        self.name        = component[1] if component[1] is not None else ""
        self.leader_id   = component[2]

class TaskStruct():
    def __init__(self, task):
        self.id            = task[0]
        self.project_id    = task[1]
        self.type          = task[2] if task[2] is not None else ""
        self.priority      = task[3] if task[3] is not None else ""
        self.title         = task[4] if task[4] is not None else ""
        self.description   = task[5] if task[5] is not None else ""
        self.creator_id    = task[6]
        self.asignee_id    = task[7]
        self.creation_date = task[8]
        self.due_date      = task[9]
        self.status        = task[10] if task[10] is not None else ""
