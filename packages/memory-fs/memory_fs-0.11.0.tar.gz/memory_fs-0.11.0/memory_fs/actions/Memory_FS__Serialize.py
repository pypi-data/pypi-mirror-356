import json
from typing                                             import Any
from memory_fs.schemas.Enum__Memory_FS__Serialization   import Enum__Memory_FS__Serialization
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

# todo: refactor this into a new file utils area , since this class has nothing to do with storage (which only sees bytes)
#       this should have the file__config object and be called File__FS__Serialize
class Memory_FS__Serialize(Type_Safe):

    # todo: change name to not have '_'
    def _serialize_data(self, data: Any, file_type) -> bytes:                                   # Serialize data based on file type's serialization method
        serialization = file_type.serialization

        if serialization == Enum__Memory_FS__Serialization.STRING:
            if isinstance(data, str):
                return data.encode(file_type.encoding.value)
            else:
                return str(data).encode(file_type.encoding.value)

        elif serialization == Enum__Memory_FS__Serialization.JSON:
            if type(data) is bytes:                                                             # todo: review this usage, since it doesn't look right to be doing this conversation from bytes to str here
                data = data.decode(file_type.encoding.value)
            json_str = json.dumps(data, indent=2)
            return json_str.encode(file_type.encoding.value)

        elif serialization == Enum__Memory_FS__Serialization.BINARY:
            if isinstance(data, bytes):
                return data
            else:
                raise ValueError(f"Binary serialization expects bytes, got {type(data)}")

        elif serialization == Enum__Memory_FS__Serialization.BASE64:
            import base64
            if isinstance(data, bytes):
                return base64.b64encode(data)
            else:
                return base64.b64encode(str(data).encode('utf-8'))

        elif serialization == Enum__Memory_FS__Serialization.TYPE_SAFE:
            if hasattr(data, 'json'):
                json_str = data.json()
                return json_str.encode(file_type.encoding.value)
            else:
                raise ValueError(f"TYPE_SAFE serialization requires object with json() method, got {type(data)}")

        else:
            raise ValueError(f"Unknown serialization method: {serialization}")