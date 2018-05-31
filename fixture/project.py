from model.project import Project
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith('/manage_proj_page.php') and len(wd.find_elements_by_name('name')) > 0):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        wd.find_element_by_link_text("Proceed").click()
        WebDriverWait(wd, 1).until(EC.url_contains('manage_proj_page'))

    def delete_first_project(self):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_css_selector('.row-1 a').click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        WebDriverWait(wd, 3).until(EC.url_contains('manage_proj_delete'))
        wd.find_element_by_css_selector("input[value='Delete Project']").click()

    def delete_by_project_name(self, project_name):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_link_text(project_name).click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        WebDriverWait(wd, 1).until(EC.url_contains('manage_proj_delete'))
        wd.find_element_by_css_selector("input[value='Delete Project']").click()

    def count(self):
        wd = self.app.wd
        self.open_projects_page()
        table_with_projects = wd.find_elements_by_tag_name('table')[2]
        # Возвращаем все ряды за исключением 2х верхних
        return len(table_with_projects.find_elements_by_tag_name('tr')) - 2

    def get_projects_list(self):
        wd = self.app.wd
        projects = []
        count = self.count()
        table_with_projects = wd.find_elements_by_tag_name('table')[2]
        for i in range(2, 2 + count):
            text = table_with_projects.find_elements_by_css_selector('tr')[i].text
            projects.append(Project(name=text.split()[0]))
        return projects