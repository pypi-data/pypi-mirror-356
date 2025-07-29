from typing                                             import List
from memory_fs.file_fs.actions.File_FS__Create             import File_FS__Create
from osbot_utils.type_safe.decorators.type_safe         import type_safe
from memory_fs.file_fs.actions.File_FS__Paths              import File_FS__Paths
from memory_fs.schemas.Schema__Memory_FS__File          import Schema__Memory_FS__File
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

# todo: Refactor methods to Storage_FS__*
class Memory_FS__Edit(Type_Safe):
    storage     : Memory_FS__Storage

    def memory_fs__paths(self, file__config : Schema__Memory_FS__File__Config):
        return File_FS__Paths(file__config=file__config)

    def clear(self) -> None:                                                                    # Clear all files and directories
        self.storage.storage_fs.clear()
        # self.storage.files       ().clear()         # todo: refactor this logic to storage
        # self.storage.content_data().clear()

    @type_safe
    def delete(self, file_config: Schema__Memory_FS__File__Config):          # todo: refactor with logic in delete_content since 90% of the code is the same

        raise NotImplementedError  # todo: detect when this is being used, and remove when no exception is thrown

        file_fs__create = File_FS__Create(file__config=file_config, storage=self.storage)
        return file_fs__create.delete__config()

    @type_safe
    def delete_content(self, file_config: Schema__Memory_FS__File__Config):
        raise NotImplementedError  # todo: detect when this is being used, and remove when no exception is thrown
        file_fs__create = File_FS__Create(file__config=file_config, storage=self.storage)
        return file_fs__create.delete__content()


    # todo: this file needs to be removed from here, since we should be using the file_fs__* files here
    @type_safe
    def save(self, file_config: Schema__Memory_FS__File__Config,
                   file       : Schema__Memory_FS__File             # todo: remove this, and add a new method/workflow to add the metadata
              ) -> List[Safe_Str__File__Path]:

        raise NotImplementedError                                   # todo: detect when this is being used, and remove when no exception is thrown

        file_fs__create = File_FS__Create(file__config=file_config, storage=self.storage)
        return file_fs__create.create__config()

        # files_to_save = self.memory_fs__paths(file__config=file_config).paths()
        #
        # for file_to_save in files_to_save:
        #     self.storage.files()[file_to_save] = file                        # Store the file # todo: this needs to be moved into the storage class
        #
        # return files_to_save

    def save__content(self, file_config: Schema__Memory_FS__File__Config,
                      content : bytes
                      ) -> List[Safe_Str__File__Path]:
        raise NotImplementedError  # todo: detect when this is being used, and remove when no exception is thrown

        from memory_fs.file_fs.actions.File_FS__Create import File_FS__Create      # due to circular imports
        file_fs__create = File_FS__Create(file__config=file_config, storage=self.storage)
        return file_fs__create.create__content(content)                                         # todo: fix the inconsistency between save and create

        # files_to_save = self.memory_fs__paths(file__config=file_config).paths__content()
        # for file_to_save in files_to_save:
        #     self.storage.content_data()[file_to_save] = content                                          # Store the file # todo: this needs to be moved into the storage class
        # return files_to_save



    # todo: see if we need this, since now that we have multiple paths support, the logic in the copy is more complicated
    # def copy(self, source      : Safe_Str__File__Path ,                                        # Copy a file from source to destination
    #                destination : Safe_Str__File__Path
    #           ) -> bool:
    #     if source not in self.storage.files():
    #         return False
    #
    #     file = self.storage.file(source)
    #     self.save(destination, file)
    #
    #     # Also copy content if it exists
    #     if source in self.storage.content_data():                                               # todo: need to refactor the logic of the files and the support files
    #         self.save_content(destination, self.storage.file__content(source))
    #
    #     return True

    # todo: see if we need this, since now that we have multiple paths support, the logic in the move is more complicated
    # def move(self, source      : Safe_Str__File__Path ,                                        # Move a file from source to destination
    #                destination : Safe_Str__File__Path
    #           ) -> bool:
    #     if source not in self.storage.files():
    #         return False
    #
    #     file = self.storage.file(source)
    #     self.save(destination, file)
    #     self.delete(source)
    #
    #     # Also move content if it exists
    #     if source in self.storage.content_data():
    #         self.save_content(destination, self.storage.file__content(source))
    #         self.delete_content(source)
    #
    #     return True