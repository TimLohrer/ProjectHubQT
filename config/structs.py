class UserStruct():
    def __init__(self, project):
        self.id          = user[0]
        self.first_name  = user[1]
        self.sur_name    = user[2]
        self.username    = user[3]
        self.email       = user[4]

class ProjectStruct():
    def __init__(self, project):
        self.id          = project[0]
        self.name        = project[1]
        self.description = project[2]

class ComponentStruct():
    def __init__(self, component):
        self.id          = component[0]
        self.name        = component[1]
        self.leader_id   = component[2]

class TaskStruct():
    def __init__(self, task):
        self.id            = task[0]
        self.project_id    = task[1]
        self.type          = task[2]
        self.priority      = task[3]
        self.title         = task[4]
        self.description   = task[5]
        self.reporter_id   = task[6]
        self.asignee_id    = task[7]
        self.creation_date = task[8]
        self.due_date      = task[9]
        self.status        = task[10]
