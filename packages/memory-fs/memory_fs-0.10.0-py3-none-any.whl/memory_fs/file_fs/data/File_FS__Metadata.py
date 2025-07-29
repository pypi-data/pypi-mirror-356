from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self
from memory_fs.file_fs.data.File_FS__Content                   import File_FS__Content
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: implement the logic to create, load and save the metadata file
class File_FS__Metadata(Type_Safe):
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage


    @cache_on_self
    def file_fs__content(self):                                                                             # todo: see if we should have this dependency here (or if this class should receive the file's bytes, data, and config)
        return File_FS__Content(file__config=self.file__config, storage=self.storage)

    def metadata(self) -> Schema__Memory_FS__File__Metadata:
        content_bytes = self.file_fs__content().bytes()
        metadata      = Schema__Memory_FS__File__Metadata()
        if content_bytes:
            metadata.content__hash = safe_str_hash(content_bytes.decode())                                    # todo: this should be calculated on create/edit (and saved to storage), and this need refactored into separate method (if not class)
        return metadata