from typing                                                 import Optional, Dict, Any
from memory_fs.file_fs.data.File_FS__Data                      import File_FS__Data
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                        import Type_Safe


class File_FS__Info(Type_Safe):
    file__config: Schema__Memory_FS__File__Config
    storage     : Memory_FS__Storage

    @cache_on_self
    def file_fs__data(self):
        return File_FS__Data(file__config=self.file__config, storage= self.storage)


    # todo: this method should return a strongly typed class (ideally one from the file)
    def info(self) -> Optional[Dict[Safe_Id, Any]]:

        if self.file_fs__data().not_exists():
            return None

        config   = self.file_fs__data().config()
        metadata = self.file_fs__data().metadata()


        content_size = int(metadata.content__size)                                # Get size from metadata
        return {Safe_Id("exists")       : True                                          ,
                Safe_Id("size")         : content_size                                  ,
                Safe_Id("content_hash") : metadata.content__hash                   ,
                Safe_Id("timestamp")    : metadata.timestamp                       ,
                Safe_Id("content_type") : config.file_type.content_type.value      }