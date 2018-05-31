from model.project import Project


def test_delete_first_project(app):
    app.project.open_projects_page()
    before_remove_project = app.project.count()
    if before_remove_project == 0:
        # Если в списке групп нет, то создаем одну для удаления
        app.project.create(Project(name='ThisWillBeRemoved'))
        before_remove_project += 1
    app.project.delete_first_project()
    after_remove_project = app.project.count()
    assert before_remove_project - after_remove_project == 1
