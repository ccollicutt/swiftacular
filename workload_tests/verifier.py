from object_metadata import ObjectMetadata

class Verifier:
    def __init__(self, connection, container) -> None:
        self._connection = connection
        self._container = container
  
    def verify(self, objects_metadata):
        print(f"Verifying {len(objects_metadata)} objects...")
        for obj in objects_metadata:
           assert self._verify_object(obj), f"Failed to verify object {obj}"
        print(f"Verified successfully!")
  
    def _verify_object(self, expected_object) -> bool:
        try:
            _, object_content = self._connection.get_object(self._container, expected_object.name)
        except Exception as e:
            return False, f"Failed to retrieve object with name {expected_object.name}: {e}"
        actual_object = ObjectMetadata(name=expected_object.name,
                                      content_length=len(object_content),
                                      content_hash=hash(object_content))
        return actual_object == expected_object
