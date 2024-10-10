import arturas_k_library.config as config

from arturas_k_library.functions.import_books import import_to_class as im
from arturas_k_library.modules import user as usr

import pickle
import os

def init(lib):
    if os.path.isfile(config.file_name):
        lib = read_from_library()
        return lib
    else:
        print("Įveskite iBibliotekos administratorių:")
        name    = input(" Vardas: ")
        last    = input(" Pavardė: ")
        pasword = input(" Slaptažodis: ")
        lib.add_user(usr.User("admin", name, last, pasword))
        print("Ar importuoti testinią biblioteką?")
        imp_lib = input(" (taip/ne) -> ")
        if (imp_lib=="taip"):
            im(lib)
        print (lib)
        write_to_library(lib)
        return lib

def write_to_library(lib):
    try:
        with open(config.file_name, "wb") as file:
            pickle.dump(lib, file)
    except FileNotFoundError:
        print("KLAIDA: Failas nerastas!")
    except EOFError:
        print("KLAIDA: {EOFError}!")
    except:
        print("KLAIDA: Nežinoma!")
    
def read_from_library():
    try:
        with open(config.file_name, "rb") as file:
            return pickle.load(file)
    except:
        print("KLAIDA: negalima adidaryti failo!")