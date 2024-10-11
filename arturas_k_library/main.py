import arturas_k_library.config as config

import arturas_k_library.modules.library as lb
import arturas_k_library.modules.book as bk
import arturas_k_library.modules.user as usr
import arturas_k_library.functions.file_manager as manager
import arturas_k_library.functions.helper as helper

lib = lb.Library()

manager.init(lib)

msg = "\nPasirinkite funkcijas:\n"
msg += " pr      : pridėti knygą\n"
msg += " tr      : ištrinti knygą (pagal ISBN)\n"
msg += " inv     : pašalinti knygas (pagal metus)\n"
msg += " reset   : importuoti testinius duomenis\n"
msg += " print   : atspausdina visą objektą\n"
msg += " search  : ieško knygos (pagal pavadinimą ar autorių)\n"
msg += " i       : išeiti iš programos"

print(msg)

while True:
    str_in = input(" -> ")
    if str_in == "i":
        manager.write_to_library(lib)
        print("Programa baigta ir informacija išsaugota.")
        break
    elif str_in == "pr":
        book = config.book_title.copy()
        for i, j in book.items():
            book[i]=input(f"{j} :")
        print("Knyga įtraukta sėkmingai!" if helper.add_single_book(lib,book) 
              else "Įvyko klaida prašome pabandyti dar kartą!")
        print(msg)
    elif str_in == "tr":
        print(lib.remove_single_book(input(" ISBN: ")))
    elif str_in == "inv":
        print(lib.remove_old_books(input(" Metai: ")))
    elif str_in == "print":
        print(lib)
    elif str_in == "search":
        text=input(" ieškoti -> ")
        print("Paieškos rezultatas: \n", lib.search_books(text,text))
    elif str_in == "reset":
        lib.books = []
        helper.import_to_class(lib)
        manager.write_to_library(lib)
        print(lib, "\nTestiniai duomenys suimportuoti!\n")
    else:
        print(msg)

