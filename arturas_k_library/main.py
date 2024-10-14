import arturas_k_library.config as config

import arturas_k_library.modules.library as lb
import arturas_k_library.modules.book as bk
import arturas_k_library.modules.user as usr
import arturas_k_library.functions.file_manager as manager
import arturas_k_library.functions.helper as helper

config.lib = lb.Library()
manager.init()

msg = "\nPasirinkite funkcijas:\n"

msg += " pr      : pridėti knygą\n"
msg += " tr      : ištrinti knygą (pagal ISBN)\n"
msg += " inv     : pašalinti knygas (pagal metus)\n"
msg += " search  : ieško knygos (pagal pavadinimą ar autorių)\n"
msg += " import  : importuoti testinius knygų duomenis\n"
msg += " view    : peržiūrėti visas veluojančias knygas\n\n"

msg += " var     : naujas vartotojas\n"
msg += " user    : vartotojo informacija\n"
msg += " book    : knyga priskiriama vartotojui (pagal ISBN ir kortelės nr.)\n"
msg += " over    : sarašas veluojančių knygų (pagal kortelės nr.) \n\n"

msg += " print   : atspausdina visą objektą\n"
msg += " init    : trinti duomenis ir inicijuoti programą iš naujo\n"
msg += " i       : išeiti iš programos"

print(msg)

while True:
    str_in = input("\n -> ")
    if str_in == "i":
        manager.write_to_library()
        print("\nPrograma uždaroma...")
        break
    elif str_in == "pr":
        book = config.book_title.copy()
        for i, j in book.items():
            book[i]=input(f"{j} :")
        print("Knyga įtraukta sėkmingai!" if helper.add_single_book(config.lib,book) 
              else "Įvyko klaida prašome pabandyti dar kartą!")
        print(msg)
    elif str_in == "tr":
        print(config.lib.remove_single_book(input(" ISBN: ")))
    elif str_in == "inv":
        print(config.lib.remove_old_books(input(" Metai: ")))
    elif str_in == "print":
        print(config.lib)
    elif str_in == "search":
        text=input(" ieškoti -> ")
        print("Paieškos rezultatas: \n", config.lib.search_books(text,text))
    elif str_in == "import":
        config.lib.books = []
        helper.import_to_class(config.lib)
        manager.write_to_library()
        print(config.lib, "\nTestiniai duomenys suimportuoti!\n")
    elif str_in == "init":
        if (input(" tikrai? (taip/ne) -> ")=="taip"):
            config.lib.books=[]
            config.lib.users=[]
            manager.delete_reset()
            manager.init()
    elif str_in == "var":
        name = input(" vardas -> ")
        last_name = input(" pavardė -> ")
        config.lib.add_user(usr.User("reader", name, last_name))
    elif str_in == "book":
        book_in=input(" ISBN -> ")
        user_in=input(" Kortelės numeris -> ")
        days_in=int(input(" Dienų skaičius -> "))
        book = config.lib.get_book_by_isbn(book_in)
        user = config.lib.get_user_by_cn(user_in)
        print(user.borrow_book(book, days_in))
        print(user)
    elif(str_in=="user"):
        user_in=input(" Kortelės numeris -> ")
        user = config.lib.get_user_by_cn(user_in)
        print(user)
    elif(str_in=="over"):
        user_in=input(" Kortelės numeris -> ")
        user = config.lib.get_user_by_cn(user_in)
        print(user.check_overdue_books())
        # print("Simuliuojame datą, 2024-12-01, tai???")
        # user.check_overdue_books("2024-12-01")
    elif(str_in=="view"):
        config.lib.view_overdue_books()
    else:
        print(msg)

