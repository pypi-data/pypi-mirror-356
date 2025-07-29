from typing                                              import Dict
from osbot_utils.helpers.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from memory_fs.schemas.Schema__Memory_FS__File           import Schema__Memory_FS__File

# todo: find better name for this class since this is the one that simulates the actually File System (and this is in the 'core' folder)
class Memory_FS__File_System(Type_Safe):                                                # In-memory file system that maintains directory structure and file storage
    files          : Dict[Safe_Str__File__Path, Schema__Memory_FS__File]                                  # Path -> File metadata mapping
    content_data   : Dict[Safe_Str__File__Path, bytes]                                           # Path -> Raw content mapping







