from .object_metadata import ObjectMetadata

class Verifier:
   def __init__(self, connection=None) -> None:
       self._connection = connection
  
   def verify(self, objects_metadata):
       for obj in objects_metadata:
           assert self._verify_object(obj), f"Failed to verify object {obj}"
  
   def _verify_object(self, expected_object) -> bool:
       try:
           object_match = self._connection.get_object(expected_object.name)
       except Exception as e:
           return False, f"Failed to retrieve object with name {expected_object.name}"
      
       object_content = object_match['content']
       actual_object = ObjectMetadata(name=expected_object.name,
                                      content_length=len(object_content),
                                      content_hash=hash(object_content))
       return actual_object == expected_object
