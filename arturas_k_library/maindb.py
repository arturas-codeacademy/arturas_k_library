import arturas_k_library.config as config

import arturas_k_library.modules.library as lb
import arturas_k_library.modules.book as bk
import arturas_k_library.modules.user as usr
import arturas_k_library.functions.sql_manager as manager
import arturas_k_library.functions.helper as helper

config.lib = lb.Library()
manager.init()

msg = "\nPasirinkite funkcijas:\n"

msg += " add     : pridėti knygą\n"
msg += " del     : ištrinti knygą (pagal ISBN)\n"
msg += " inv     : pašalinti knygas (pagal metus)\n"
msg += " search  : ieško knygos (pagal pavadinimą ar autorių)\n\n"

msg += " new     : naujas vartotojas\n"
msg += " user    : vartotojo informacija\n"
msg += " book    : knyga priskiriama vartotojui (pagal ISBN ir kortelės nr.)\n"
msg += " return  : grąžinama knyga (pagal ISBN ir kortelės nr.)\n\n"

msg += " list    : peržiūrėti visas paimtas knygas\n"
msg += " view    : peržiūrėti visas veluojančias knygas\n"
msg += " over    : sarašas veluojančių knygų (pagal kortelės nr.) \n\n"

msg += " print   : atspausdina visą objektą\n"
msg += " import  : importuoti testinius knygų duomenis\n"
msg += " init    : trinti duomenis ir inicijuoti programą iš naujo\n"
msg += " i,e     : išeiti iš programos"

print(msg)

while True:
    str_in = input("\n -> ")
    if str_in == "i" or str_in == "e":
        print("\nPrograma uždaroma...")
        break
    elif str_in == "add":
        helper.prideti_knyga()
    elif str_in == "del":
        helper.trinti_knyga()
    elif str_in == "inv":
        helper.inventorizacija()
    elif str_in == "print":
        print(config.lib)
    elif str_in == "search":
        text=input(" ieškoti -> ")
        print("Paieškos rezultatas: \n", config.lib.search_books(text,text))
    elif str_in == "import":
        config.lib.books = []
        helper.import_to_class(config.lib)
        print(config.lib, "\nTestiniai duomenys suimportuoti!\n")
    elif str_in == "init":
        if (input(" tikrai? (taip/ne) -> ")=="taip"):
            config.lib.books=[]
            config.lib.users=[]
            manager.delete_reset()
            manager.init()
    elif str_in == "new":
        helper.prideti_vartotoja()
    elif str_in == "book":
        helper.priskirti_knyga()
    elif str_in == "return":
        helper.grazinti_knyga()
    elif(str_in=="user"):
        user_in=input(" Kortelės numeris -> ")
        user = config.lib.get_user_by_cn(user_in)
        print(user)
    elif(str_in=="over"):
        user_in=input(" Kortelės numeris -> ")
        user = config.lib.get_user_by_cn(user_in)
        print(user.check_overdue_books())
    elif(str_in=="view"):
        config.lib.view_overdue_books()
    elif(str_in=="list"):
        helper.print_bowerred_books()
    elif(str_in=="all"):
         helper.print_all_books()
    else:
        print(msg)

