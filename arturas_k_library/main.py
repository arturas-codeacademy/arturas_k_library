import arturas_k_library.config as config

from arturas_k_library.modules import library as lb
from arturas_k_library.modules import book as bk
from arturas_k_library.modules import user as usr
from arturas_k_library.functions.file_manager import init, write_to_library

lib = lb.Library()

lib = init(lib)

print(lib)

# write_object(lib: object, file_name:str):A
