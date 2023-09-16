import uuid
import pytest
import swiftclient
from verifier import Verifier
from workloader import Workloader

MEAN_SIZE = 1 * 1024 # 1 KB
MAX_SIZE = 10 * 1024 # 10 KB
MIN_SIZE = 512 # 512 Bytes
STDEV_SIZE = 1 * 1024 # 1 KB
RETENTION_TIME = 24 * 60 * 60 # 24 hours

PROXY_BASE_URL = 'http://192.168.100.50:5000'
AUTH_URL = f"{PROXY_BASE_URL}/v3"
AUTH_VERSION = '3'
USER = "achilles"
KEY = "CHANGEME"
PROJECT = 'demo'
DEFAULT_VALUE = 'Default'
OS_OPTIONS = {
    'user_domain_name': DEFAULT_VALUE,
    'project_domain_name': DEFAULT_VALUE,
    'project_name': PROJECT
}


@pytest.fixture(scope="session")
def connection():
    _connection = swiftclient.Connection(
        authurl=AUTH_URL,
        user=USER,
        key=KEY,
        os_options=OS_OPTIONS,
        auth_version=AUTH_VERSION
    )
    return _connection


@pytest.fixture
def container(connection):
    random_name = 'the-test-container' # str(uuid.uuid4())
    connection.put_container(random_name)
    yield random_name
    # connection.delete_container(random_name)


def run_workload_test(mean_size, max_size, min_size, stdev_size, retention_time,
                     upload_interval, total_uploads, batch_size, connection, container):
   workloader = Workloader(mean_size, max_size, min_size, stdev_size,
                           retention_time, upload_interval, total_uploads,
                           batch_size, connection)
   uploaded_objects = workloader.create_workload(container)
   verifier = Verifier(connection, container)
   verifier.verify(uploaded_objects)


def test_tiny_workload(connection, container):
    run_workload_test(MEAN_SIZE, MAX_SIZE, MIN_SIZE, STDEV_SIZE,
                     RETENTION_TIME, upload_interval=0, total_uploads=2,
                     batch_size=100, connection=connection, container=container)


# Continuously and slowly upload files without stopping, e.g. a live server that accepts occasional files from many clients
def test_continuous_workload(connection, container):
    run_workload_test(MEAN_SIZE, MAX_SIZE, MIN_SIZE, STDEV_SIZE,
                     RETENTION_TIME, upload_interval=5, total_uploads=10000,
                     batch_size=100, connection=connection, container=container)


# Upload a large amount of objects intermittently, e.g. a live server that accepts batches of files from many clients
def test_burst_workload(connection, container):
    run_workload_test(MEAN_SIZE, MAX_SIZE, MIN_SIZE, STDEV_SIZE,
                     RETENTION_TIME, upload_interval=1800, total_uploads=40,
                     batch_size=25_000, connection=connection, container=container)


# Upload a huge amount of objects at once, e.g. a user is uploading a backup of their file-system.
def test_all_at_once_workload(connection, container):
    run_workload_test(MEAN_SIZE, MAX_SIZE, MIN_SIZE, STDEV_SIZE,
                     RETENTION_TIME, upload_interval=0, total_uploads=1,
                     batch_size=1_000_000, connection=connection, container=container)
