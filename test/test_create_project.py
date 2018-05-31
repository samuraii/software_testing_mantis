import string
import random
from model.project import Project

def random_string(max_len=5):
    symbols = string.ascii_letters
    return 'Test-' + ''.join([random.choice(symbols) for i in range(max_len)])

def test_create_project(app):
    app.project.open_projects_page()
    before_add_project = app.project.count()
    projects = app.project.get_projects_list()
    project_to_create = Project(name=random_string(5))
    if project_to_create in projects:
        project_to_create = Project(name=random_string(5))
    app.project.create(project_to_create)
    after_add_project = app.project.count()
    assert after_add_project - before_add_project == 1
