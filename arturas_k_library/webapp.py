import arturas_k_library.config as config
import arturas_k_library.modules.library as lb
import arturas_k_library.modules.book as bk
import arturas_k_library.modules.user as usr
import arturas_k_library.functions.file_manager as manager
import arturas_k_library.functions.helper as helper
from arturas_k_library.web.auth import authenticate_user
import arturas_k_library.web.table as web
import streamlit as st
import pandas as pd

# Inicializuojame biblioteką
config.lib = lb.Library()
manager.init()

# Patikriname prisijungimo būseną
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Nustatome puslapio konfigūraciją
st.set_page_config(page_title="iBiblioteka", page_icon="")



# SIDEBAR -------------------------------------------------------------------------------------------
if not st.session_state.logged_in:
    username = st.sidebar.text_input("Vartotojo ID")
    password = st.sidebar.text_input("Slaptažodis", type="password")

    if st.sidebar.button("Prisijungti"):
        if authenticate_user(username, password, st):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.sidebar.error("Neteisingas vartotojo vardas arba slaptažodis")       
            
else:
    # Prisijungus rodome pagrindinį puslapį
    st.sidebar.success(f"Jūs sėkmingai prisijungėte: {config.user_in.get_first_name()}!")
    user_role=config.user_in.get_library_role()
    st.sidebar.write(f"iBibliotekoje esate kaip: {user_role}")
    
    if (user_role=="admin"):
        options = ["Visos knygos", 
                   "Pridėti knygą", 
                   "Ištrinti knygą",
                   "Ištrinti knygas", 
                   "Return Book"]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
        
        if selected_option == "Pridėti knygą":
            pass         
    elif(user_role=="reader"):
        options = ["Visos knygos"]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
        pass
    else:
        pass
    # Galimybė atsijungti
    if st.sidebar.button("Atsijungti"):
        st.session_state.logged_in = False
        st.rerun()
        

# BODY ----------------------------------------------------------------------------------------------

# Puslapio turinys
st.write("# Sveiki atvykę į iBiblioteką 👋")
st.markdown(f"Didžiausia bibliotekų sistema Lietuvoje, net {config.lib.get_count()} skirtingų knygų.")

if not st.session_state.logged_in:
    web.show_table(st)
else:
    if (user_role=="admin"):
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
        if selected_option == "Ištrinti knygas":
            years_in = st.text_input(f"Įveskite metus")
            if st.button("Ištrinti knygas"):
                 st.write(config.lib.remove_old_books(years_in))
    elif(user_role=="reader"):        
        if selected_option == "Visos knygos":
                web.show_table(st)
    else:
        pass
    
