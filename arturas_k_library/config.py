import arturas_k_library.modules.library as lb

lib = lb.Library

file_name = "db_objeckt.pkl"

book_title = {"title":"Pavadinimas", 
              "author":"Autorius", 
              "year":"Metai",
              "details":"Informacija", 
              "genre":"Žanras", 
              "isbn":"ISBN", 
              "quantity":"Kiekis"
              }

roles={"admin":"01","reader":"18", "guest":""}

items_per_page = 10