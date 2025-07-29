from memory_fs.storage_fs.Storage_FS                    import Storage_FS
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from memory_fs.core.Memory_FS__File_System              import Memory_FS__File_System
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

# todo: this class needs to be refactored with the code that is now on storage_fs
#       also see if we shouldn't be using the Storage_FS directly, once the data is captured in the Storage_FS__Memory.py class

class Memory_FS__Storage(Type_Safe):
    storage_type : Safe_Id = Safe_Id('memory')              # todo: see if we still need this storage_type
    file_system  : Memory_FS__File_System                   # todo: we need to refactor this into class that has all the methods below, but has no access to the memory object (since each provider will have it's own version of it)
    storage_fs   : Storage_FS                               # todo: to implement this class and wire it below

    # def content_data(self):
    #     return self.file_system.content_data

    def file(self, path):
        return self.files().get(path)

    def file__content(self, path):
        return self.storage_fs.file__bytes(path)

        #return self.content_data().get(path)

    def file__delete(self, path: Safe_Str__File__Path) -> bool:
        return self.storage_fs.file__delete(path=path)

    def file__exist(self, path):
        return self.storage_fs.file__exists(path)

    def file__save(self, path: Safe_Str__File__Path, data: bytes) -> bool:
        return self.storage_fs.file__save(path=path, data=data)


    # def files(self):
    #     return self.storage_fs.files__names()
    #     return self.file_system.files

    # def files__contents(self):                              # todo: see if we need this, this could be lots of data
    #     return self.files().values()

    def files__paths(self):                                 # todo: see if we need this method
        return self.storage_fs.files__paths()
        #return list(self.file_system.files.keys())


