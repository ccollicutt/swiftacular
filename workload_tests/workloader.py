from object_metadata import ObjectMetadata
import swiftclient
import random
import uuid
import time


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
    def __init__(self, mean_size, max_size, min_size, stdev_size,
                 retention_time, upload_interval=0, total_uploads=0, batch_size=0, connection=None):
        self._mean_size = mean_size
        self._max_size = max_size
        self._min_size = min_size
        self._stdev_size = stdev_size
        self._retention_time = retention_time
        self._connection = connection
        self._upload_interval = upload_interval
        self._total_uploads = total_uploads
        self._batch_size = batch_size

    def create_workload(self, container_name):
        created_objects = []
        for batch in range(self._total_uploads):
            print(f"Starting upload of batch {batch + 1}")
            for _ in range(self._batch_size):
                object_metadata = self._create_and_upload_object(container_name)
                created_objects.append(object_metadata)
            print(f"Uploaded {self._batch_size} objects, sleeping for {self._upload_interval}s")
            time.sleep(self._upload_interval)

        print(f"Uploaded {len(created_objects)} objects to container '{container_name}'")
        return created_objects

    def _create_and_upload_object(self, container_name):
        object_name = str(uuid.uuid4())
        object_size = self._generate_object_size()
        object_content = "A" * object_size
        print(f"Uploading object of size: {object_size}")
        self._upload_object(container_name, object_name, object_content)
        object_metadata = ObjectMetadata(name=object_name,
                                                content_length=object_size,
                                                content_hash=hash(object_content))
                                        
        return object_metadata

    @retry(tries=3)
    def _upload_object(self, container_name, object_name, object_content):
        metadata = {"X-Delete-After": str(self._retention_time)}
        self._connection.put_object(container_name, object_name, object_content, headers=metadata)

    def _generate_object_size(self):
        random_size = int(random.normalvariate(self._mean_size, self._stdev_size))
        bound_size = min(self._max_size, max(self._min_size, random_size))
        return bound_size
