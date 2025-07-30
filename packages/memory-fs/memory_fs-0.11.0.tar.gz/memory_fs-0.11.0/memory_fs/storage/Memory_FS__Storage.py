from typing import List

from memory_fs.storage_fs.Storage_FS                    import Storage_FS
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

# todo: this class needs to be refactored with the code that is now on storage_fs
#       also see if we shouldn't be using the Storage_FS directly, once the data is captured in the Storage_FS__Memory.py class

class Memory_FS__Storage(Type_Safe):
    storage_type : Safe_Id = Safe_Id('memory')              # todo: see if we still need this storage_type
    storage_fs   : Storage_FS                               # todo: to implement this class and wire it below

    def file__content(self, path):
        return self.storage_fs.file__bytes(path)

        #return self.content_data().get(path)

    def file__delete(self, path: Safe_Str__File__Path) -> bool:
        return self.storage_fs.file__delete(path=path)

    def file__exist(self, path):
        return self.storage_fs.file__exists(path)

    def file__save(self, path: Safe_Str__File__Path, data: bytes) -> bool:
        return self.storage_fs.file__save(path=path, data=data)


    def files__paths(self):                                 # todo: see if we need this method
        return self.storage_fs.files__paths()


    # todo
    def list_files(self, prefix : Safe_Str__File__Path = None                                  # List all files, optionally filtered by prefix
                    ) -> List[Safe_Str__File__Path]:                                           # todo: see if we need this method
        if prefix is None:
            return list(self.storage_fs.files__paths())

        prefix_str = str(prefix)
        if not prefix_str.endswith('/'):
            prefix_str += '/'

        return [path for path in self.files__paths()
                if str(path).startswith(prefix_str)]

