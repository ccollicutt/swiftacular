import dataclasses


@dataclasses.dataclass(frozen=True)
class ObjectMetadata:
   name: str
   content_length: int
   content_hash: str


   @staticmethod
   def from_object(obj):
       return ObjectMetadata(obj.name, obj.content_length, obj.content_hash)
  
   def __eq__(self, __value: object) -> bool:
       return type(__value) == ObjectMetadata and (self.name == __value.name and
               self.content_length == __value.content_length and
               self.content_hash == __value.content_hash)
