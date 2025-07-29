from typing                                                 import List, Dict, Any
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: I think most of these Memory_FS__* classes should be refactored to the Storage_FS__* classes
class Memory_FS__Data(Type_Safe):
    storage     : Memory_FS__Storage


    def list_files(self, prefix : Safe_Str__File__Path = None                                  # List all files, optionally filtered by prefix
                    ) -> List[Safe_Str__File__Path]:                                           # todo: see if we need this method
        if prefix is None:
            return list(self.storage.storage_fs.files__paths())

        prefix_str = str(prefix)
        if not prefix_str.endswith('/'):
            prefix_str += '/'

        return [path for path in self.storage.files__paths()
                if str(path).startswith(prefix_str)]
