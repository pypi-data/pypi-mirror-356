from memory_fs.file_fs.File_FS                          import File_FS
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Target_FS(Type_Safe):
    file_config : Schema__Memory_FS__File__Config                                   # todo: rename to file__config (for consistency with other classes)
    storage     : Memory_FS__Storage

    @cache_on_self
    def file_fs(self):
        return File_FS(file_config=self.file_config, storage=self.storage)          # todo: refactor this so that we pass a schema object (for example Schema__Target_FS) that has the references to the file_config and storage objects