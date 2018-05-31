import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.application import Application
from fixture.db import DbFixture
from fixture.orm import ORMFixture

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
    fixture.session.ensure_login(web_config['username'], web_config['password'])
    return fixture


@pytest.fixture(scope='session')
def db(request):
    db_config = load_config(pytest.config.getoption('--config'))['db']
    dbfixture = DbFixture(
        host=db_config['host'],
        db=db_config['db'],
        user=db_config['user'],
        password=db_config['password']
    )
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture()
def orm(request):
    db_config = load_config(pytest.config.getoption('--config'))['db']
    orm_fixture = ORMFixture(
        host=db_config['host'],
        db=db_config['db'],
        user=db_config['user'],
        password=db_config['password']
    )
    return orm_fixture


@pytest.fixture
def check_ui(request):
    return pytest.config.getoption('--check_ui')


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def finalize():
        fixture.session.logout()
        fixture.complete()
    request.addfinalizer(finalize)
    return fixture


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            test_data = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids = [str(x) for x in test_data])
        elif fixture.startswith("json_"):
            test_data = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids = [str(x) for x in test_data])


def load_from_module(module):
    return importlib.import_module('data.%s' % module).testdata


def load_from_json(json):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/%s.json' % json)) as json_f:
        return jsonpickle.decode(json_f.read())
