import arturas_k_library.config as config
import arturas_k_library.modules.library as lb
import arturas_k_library.modules.book as bk
import arturas_k_library.modules.user as usr
import arturas_k_library.functions.file_manager as manager
import arturas_k_library.functions.helper as helper
from arturas_k_library.web.auth import authenticate_user, logged_in, logged_out, check_login
import arturas_k_library.web.table as web
import streamlit as st
import pandas as pd

# Inicializuojame biblioteką
config.lib = lb.Library()
manager.init()

# Patikriname prisijungimo būseną
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = logged_in()
# else:

st.session_state.logged_in = check_login()

# Nustatome puslapio konfigūraciją
st.set_page_config(page_title="įBiblioteka", page_icon="")

# SIDEBAR -------------------------------------------------------------------------------------------
if not st.session_state.logged_in:
    card_number = st.sidebar.text_input("Vartotojo ID")
    password = st.sidebar.text_input("Slaptažodis", type="password")

    if st.sidebar.button("Prisijungti"):
        if authenticate_user(card_number, password, st):
            config.user_in = config.lib.get_user_by_cn(card_number)
            st.session_state.logged_in = logged_in()
            st.rerun()
        else:
            st.sidebar.error("Neteisingas vartotojo vardas arba slaptažodis")       
            
else:
    # Prisijungus rodome pagrindinį puslapį
    try:
        name_in = config.user_in.get_first_name()
    except:
        name_in = "svečias"
    if (name_in != "svečias"):
        st.sidebar.success(f"Jūs sėkmingai prisijungėte: {name_in}!")
    try:
        user_role=config.user_in.get_library_role()
    except:
        user_role="svečias"
    st.sidebar.write(f"iBibliotekoje esate kaip: {user_role}")
    
    if (user_role=="admin"):
        options = ["Visos knygos", 
                   "Pridėti knygą", 
                   "Ištrinti knygą",
                   "Ištrinti knygas",
                   "-----------------", 
                   "Pridėtį vartotoją",
                   "Vartotojų sąrašas",
                   "Priskirti knygą",
                   "Veluojančios knygos",
                   "Paimtos knygos"
                   ]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
        
        if selected_option == "Pridėti knygą":
            pass         
    elif(user_role=="reader"):
        options = ["Visos knygos"]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
        pass
    else:
        options = ["Visos knygos"]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
    # Galimybė atsijungti
    if st.sidebar.button("Atsijungti"):
        manager.write_to_library()
        st.session_state.logged_in = logged_out()
        print(st.session_state.logged_in)
        st.rerun()
        

# BODY ----------------------------------------------------------------------------------------------

# Puslapio turinys
st.write("# Sveiki atvykę įBiblioteką 👋")
st.markdown(f"Didžiausia bibliotekų sistema Lietuvoje, net {config.lib.get_count()} skirtingų knygų.")

if not st.session_state.logged_in:
    web.show_table(st)
else:
    if (user_role=="admin"):
        if selected_option == "Visos knygos":
            web.show_table(st) 
        if selected_option == "Pridėti knygą":
            st.write("Įveskite knygos duomenis:")
            book = config.book_title.copy()
            for i, j in book.items():
                book[i]= st.text_input(f"{j}")
            if st.button("Pridėti knygą"):
                if helper.add_single_book(config.lib,book):
                    manager.write_to_library()
                    st.write("Knyga įtraukta sėkmingai!")
                else:
                    st.write("Įvyko klaida prašome pabandyti dar kartą!")
        if selected_option == "Ištrinti knygą":
            isbn_in = st.text_input(f"Įveskite ISBN")
            if st.button("Ištrinti knygą"):
                 st.write(config.lib.remove_single_book(isbn_in))
                 manager.write_to_library()
        if selected_option == "Ištrinti knygas":
            years_in = st.text_input(f"Įveskite metus")
            if st.button("Ištrinti knygas"):
                 st.write(config.lib.remove_old_books(years_in))
                 manager.write_to_library()
        if selected_option == "Pridėtį vartotoją":
            first_name = st.sidebar.text_input(f"Įveskite vardą")
            last_name = st.sidebar.text_input(f"Įveskite pavardę")
            if_admin = st.sidebar.checkbox('Ar bibliotininkas?')
            if st.sidebar.button("Pridėti skaitytoją"):
                if if_admin:
                    role = "admin"
                else:
                    role = "reader"
                new_user = usr.User(role, first_name, last_name)
                config.lib.add_user(new_user)
                st.sidebar.write(new_user.get_new_user())
                manager.write_to_library()
        if selected_option == "Priskirti knygą":
            web.show_table(st) 
            book_in=st.sidebar.text_input(f"Knygos ISBN")
            user_in=st.sidebar.text_input(f"Skaitytojo ID")
            try: 
                days_in=int(st.sidebar.text_input(f"Laikotarpis"))
            except:
                days_in=14
            if st.sidebar.button("Pridėti į sąrašą"):
                book = config.lib.get_book_by_isbn(book_in)
                user = config.lib.get_user_by_cn(user_in)
                st.sidebar.write(user.borrow_book(book, days_in))
                manager.write_to_library()
        if selected_option == "Veluojančios knygos":    
            st.write("Veluojančių knygų sąrašas")
            web.show_over(st)
        if selected_option == "Paimtos knygos":    
            st.write("Visos paimtos knygos")
            web.show_borrowed(st)
        if selected_option == "Vartotojų sąrašas":    
            st.write("Vartotojų duomenys")
            web.show_users(st)
    elif(user_role=="reader"):        
        if selected_option == "Visos knygos":
            web.show_table(st) 
    else:
        if selected_option == "Visos knygos":
            web.show_table(st)
    
