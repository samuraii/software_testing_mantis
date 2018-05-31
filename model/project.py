class Project:

    def __init__(self, name=None, status=None, view_status=None, description=''):
        self.name = name
        self.status = status
        self.view_status = view_status
        self.description = description

    def __repr__(self):
        return "Project({}, {}, {}, {})".format(self.name, self.status, self.view_status, self.description)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name
