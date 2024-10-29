import arturas_k_library.modules.library as lb
import arturas_k_library.modules.user as usr

lib = lb.Library
user_in = usr.User

file_name = "db_objeckt.pkl"
db_name = "library.db"

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

BOOK_FROM = 1800