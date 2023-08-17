import swiftclient
import random
import uuid

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

MEAN_SIZE = 1 * 1024 # 1 KB
MAX_SIZE = 10 * 1024 # 10 KB
MIN_SIZE = 512 # 512 Bytes
STDEV_SIZE = 1 * 1024 # 1 KB

RETENTION_TIME = 60 * 60 # 1 hour

OBJECT_COUNT = 150

def retry(tries, delay=0):
    def _retry(function):
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < tries:
                try:
                    result = function(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Attempt {retry_count + 1} failed with exception: {e}")
                    retry_count += 1
            raise Exception(f"{function.__name__} failed after {tries} tries")
        return wrapper
    return _retry


class Workloader:
    def __init__(self, object_count=OBJECT_COUNT, mean_size=MEAN_SIZE, 
                 max_size=MAX_SIZE, min_size=MIN_SIZE, stdev_size=STDEV_SIZE,
                 retention_time=RETENTION_TIME, connection=None):
        self._object_count = object_count
        self._mean_size = mean_size
        self._max_size = max_size
        self._min_size = min_size
        self._stdev_size = stdev_size
        self._retention_time = retention_time
        self._setup_connection(connection)

    def _setup_connection(self, connection):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = swiftclient.Connection(
                authurl=AUTH_URL,
                user=USER,
                key=KEY,
                os_options=OS_OPTIONS,
                auth_version=AUTH_VERSION
            )

    def create_workload(self, container_name):
        for _ in range(self._object_count):
            object_name = str(uuid.uuid4())
            object_size = self._generate_object_size()
            object_content = "A" * object_size
            print(f"Uploading object of size: {object_size}")
            self._upload_object(container_name, object_name, object_content)

        print(f"Uploaded {self._object_count} objects to container '{container_name}'")

    @retry(tries=3)
    def _upload_object(self, container_name, object_name, object_content):
        metadata = {"X-Delete-After": str(self._retention_time)}
        self._connection.put_object(container_name, object_name, object_content, headers=metadata)

    def _generate_object_size(self):
        random_size = int(random.normalvariate(self._mean_size, self._stdev_size))
        bound_size = min(self._max_size, max(self._min_size, random_size))
        return bound_size

container = "testcontainer"
workloader = Workloader()
print(f"Creating workload on container {container}")
workloader.create_workload(container)
