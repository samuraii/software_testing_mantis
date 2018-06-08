import pytest
import json
import os.path
import ftputil
from fixture.application import Application

fixture = None
config = None


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome', action='store')
    parser.addoption('--config', default='config.json', action='store')
    parser.addoption('--check_ui', action='store_true')


def load_config(file):
    global config
    if config is None:
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file_path) as config_file:
            config = json.load(config_file)
    return config


@pytest.fixture(scope='session')
def configuration(request):
    return load_config(request.config.getoption('--config'))


# @pytest.fixture(scope='session', autouse=True)
# def configure_server(request, configuration):
#     install_server_configuration(configuration['ftp']['host'], configuration['ftp']['username'], configuration['ftp']['password'])
#     def fin():
#         restore_server_configuration(configuration['ftp']['host'], configuration['ftp']['username'], configuration['ftp']['password'])
#     request.addfinalizer(fin)


# def install_server_configuration(host, username, password):
#     with ftputil.FTPHost(host, username, password) as remote:
#         if remote.path.isfile('config_inc.php.bak'):
#             remote.remove('config_inc.php.bak')
#         if remote.path.isfile('config_inc.php'):
#             remote.rename('config_inc.php', 'config_inc.php.bak')
#         remote.upload(os.path.join(os.path.dirname(__file__),'resources/config_inc.php'), 'config_inc.php')
#
#
# def restore_server_configuration(host, username, password):
#     with ftputil.FTPHost(host, username, password) as remote:
#         if remote.path.isfile('config_inc.php'):
#             remote.remove('config_inc.php')
#         if remote.path.isfile('config_inc.php.bak'):
#             remote.rename('config_inc.php.bak', 'config_inc.php')
#         remote.upload(os.path.join(os.path.dirname(__file__),'resources/config_inc.php'), 'config_inc.php')


@pytest.fixture
def app(request, configuration):
    global fixture
    browser = request.config.getoption('--browser')
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, configuration=configuration)
    fixture.session.ensure_login(configuration['admin']['username'], configuration['admin']['password'])
    return fixture


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def finalize():
        fixture.session.logout()
        fixture.complete()
    request.addfinalizer(finalize)
    return fixture
