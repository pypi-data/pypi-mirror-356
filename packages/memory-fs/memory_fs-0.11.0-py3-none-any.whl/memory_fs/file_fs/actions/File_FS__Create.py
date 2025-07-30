from osbot_utils.type_safe.decorators.type_safe import type_safe

from osbot_utils.utils.Json                             import json_to_bytes
from memory_fs.file_fs.actions.File_FS__Exists             import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Paths              import File_FS__Paths
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

# todo: move the note below to https://github.com/owasp-sbot/Memory-FS/blob/dev/docs/memory_fs/file/actions/Memory_FS__File__Create.md
#       this is where we are going to be storing details about each class

# note: config file can only be created or deleted (it cannot be edited)

class File_FS__Create(Type_Safe):                                                       # todo: refactor to file_fs__create
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage

    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file__config, storage=self.storage)

    @cache_on_self
    def file_fs__paths(self):                                                                      # todo: refactor to file_fs__paths
        return File_FS__Paths(file__config=self.file__config)

    # todo: we will need a top level create(content, metadata) method

    def create__config(self):
        if self.exists() is False:
            files_to_save = self.file_fs__paths().paths__config()
            files_saved   = []
            for file_to_save in files_to_save:
                content__data  = self.file__config.json()
                content__bytes = json_to_bytes(content__data)
                if self.storage.file__save(file_to_save, content__bytes):
                    files_saved.append(file_to_save)
            return files_saved
            #return self.file__edit().create__config()              # todo: see if the exists check should not be inside create__config
        return []

    @type_safe
    def create__content(self, content: bytes):                      # todo: need to updated the metadata file (with for example to save the length of the file, and update timestamp)
        files_to_save = self.file_fs__paths().paths__content()
        files_saved   = []
        for file_to_save in files_to_save:
            if self.storage.file__save(file_to_save, content):
                files_saved.append(file_to_save)
        return files_saved

    def delete__config(self):                                   # todo: # refactor to File_FS__Delete
        files_deleted = []                                      # todo: refactor with delete__content since the code is just about the same
        for file_path in self.file_fs__paths().paths__config():
            if self.storage.file__delete(path=file_path):
                files_deleted.append(file_path)
        return files_deleted

    def delete__content(self):                                  # todo: refactor to File_FS__Delete
        files_deleted = []
        for file_path in self.file_fs__paths().paths__content():
            if self.storage.file__delete(path=file_path):
                files_deleted.append(file_path)
        return files_deleted

        # files_deleted = []
        # content_files = self.storage.content_data()
        # for file_path in self.memory_fs__paths(file__config=file_config).paths__content():
        #     if file_path in content_files:
        #         del content_files[file_path]                         # todo: this needs to be abstracted out in the storage class
        #         files_deleted.append(file_path)
        # return files_deleted
    def exists(self):
        return self.file_fs__exists().config()
        #return self.file__data().exists()