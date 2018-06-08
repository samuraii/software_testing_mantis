import allure
from model.project import Project


@allure.feature('Проекты')
@allure.story('Удаление проекта из списка')
def test_delete_first_project(app):
    with allure.step('Открываю страницу проектов'):
        app.project.open_projects_page()
    before_remove_project = len(app.project.get_projects_list())
    if before_remove_project == 0:
        # Если в списке групп нет, то создаем одну для удаления
        app.project.create(Project(name='ThisWillBeRemoved'))
        before_remove_project += 1
    with allure.step('Удаляю первый проект в списке'):
        app.project.delete_first_project()
    with allure.step('Проверяю количество проектов в списке'):
        after_remove_project = len(app.project.get_projects_list())
        assert before_remove_project - after_remove_project == 1
