import arturas_k_library.config as config

import arturas_k_library.modules.library as lb
import arturas_k_library.modules.book as bk
import arturas_k_library.modules.user as usr
import arturas_k_library.functions.file_manager as manager
import arturas_k_library.functions.helper as helper

lib = lb.Library()

lib = manager.init(lib)

msg = "\nPasirinkite funkcijas:\n"
msg += " pr     : pridėti knygą\n"
msg += " tr     : ištrinti knygą (pagal ISBN)\n"
msg += " inv    : pašalinti knygas (pagal metus)\n"
msg += " test   : importuoti testinius duomenis\n"
msg += " print  : atspausdina visą objektą\n"
msg += " i      : išeiti iš programos"

print(msg)

while True:
    str_in = input(" -> ")
    if str_in == "i":
        manager.write_to_library(lib)
        print("Programa baigta ir biudžetas išsaugotas.")
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
        lib.remove_old_books(2000)
    elif str_in == "print":
        print(lib)
    elif str_in == "reset":
        lib.books = []
        lib = manager.init(lib)
        print(lib, "Testiniai duomenys suimportuoti!\n")
    else:
        print(msg)

