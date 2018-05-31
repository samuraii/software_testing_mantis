import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.session import SessionHelper
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

@pytest.fixture
def app(request):
    global fixture
    browser = pytest.config.getoption('--browser')
    web_config = load_config(pytest.config.getoption('--config'))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, url=web_config['url'])
    return fixture


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def finalize():
        fixture.session.logout()
        fixture.complete()
    request.addfinalizer(finalize)
    return fixture
