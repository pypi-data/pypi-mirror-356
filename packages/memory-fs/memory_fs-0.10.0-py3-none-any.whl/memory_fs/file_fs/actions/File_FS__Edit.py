from memory_fs.file_fs.actions.File_FS__Paths              import File_FS__Paths
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.actions.Memory_FS__Edit                  import Memory_FS__Edit
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class File_FS__Edit(Type_Safe):
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage

    @cache_on_self
    def file_fs__paths(self):
        return File_FS__Paths(file__config=self.file__config)

    # @cache_on_self
    # def storage_data(self):
    #     return Memory_FS__Data(storage=self.storage)

    @cache_on_self                  # todo: see if we still needs this class here
    def storage_fs__edit(self):
        return Memory_FS__Edit(storage=self.storage)

    def storage_paths(self):                # todo: remove since this is covered by file__paths
        return File_FS__Paths(file__config=self.file__config)

    def load__content(self) -> bytes:
        paths = self.storage_paths().paths__content()
        for path in paths:
            content = self.storage.storage_fs.file__bytes(path)                 # todo: refactor, since this logic already exists in the current codebase (and it should only exist once)
            if content:
                return content

    def save__content(self, content: bytes):
        files_saved = []
        paths = self.storage_paths().paths__content()
        for path in paths:
            if self.storage.storage_fs.file__save(path, content):
                files_saved.append(path)
        return files_saved

    # def save__content(self, content: bytes):
    #     files_to_save = self.file__paths().paths__content()
    #     files_saved   = []
    #     for file_to_save in files_to_save:
    #         if self.storage.file__save(file_to_save, content):
    #             files_saved.append(file_to_save)
    #     return files_saved

    # def create__config(self) -> List[Safe_Str__File__Path]:
    #     files_to_save = self.file__paths().paths__config()
    #     files_saved   = []
    #     for file_to_save in files_to_save:
    #         content__data  = self.file__config.json()
    #         content__bytes = json_to_bytes(content__data)
    #         if self.storage.file__save(file_to_save, content__bytes):
    #             files_saved.append(file_to_save)
    #     return files_saved

