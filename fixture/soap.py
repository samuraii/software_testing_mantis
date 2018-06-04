from suds.client import Client
from suds import WebFault

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client('http://localhost/api/soap/mantisconnect.php?wsdl')
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def project_exists(self, username, password, project_name):
        client = Client('http://localhost/api/soap/mantisconnect.php?wsdl')
        try:
            client.service.mc_project_get_id_from_name(username, password, project_name)
            return True
        except WebFault:
            return False

    def get_all_projects(self, username, password):
        client = Client('http://localhost/api/soap/mantisconnect.php?wsdl')
        return client.service.mc_enum_projections(username, password)
