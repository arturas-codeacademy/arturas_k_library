import arturas_k_library.config as config
import pandas as pd
import arturas_k_library.functions.file_manager as manager
import arturas_k_library.functions.helper as helper
import arturas_k_library.modules.book as bk
import arturas_k_library.modules.user as usr

from arturas_k_library.web.auth import authenticate_user, logged_in, logged_out, check_login

def show_table(st):
    # Knygų sąrašą paverčiame pandas DataFrame
    df_books = pd.DataFrame(config.lib.get_books_list(), columns=["ISBN", "Knygos pavadinimas", "Autorius", "Leidybos metai", "Miestas: Leidykla", "Žanras", "Kiekis"])


    # Vartotojo įvestis knygos pavadinimui ar autoriui
    search_input = st.text_input("Ieškokite pagal knygos pavadinimą arba autorių")
    
    # Filtruoti knygas pagal vartotojo įvestį
    if search_input:
        result = df_books.loc[
            df_books['Knygos pavadinimas'].str.contains(search_input, case=False) |
            df_books['Autorius'].str.contains(search_input, case=False)
        ]
        st.write("Paieškos rezultatai:", result)
    else:
        # Puslapiavimo nustatymai
        items_per_page = config.items_per_page  # Knygų skaičius viename puslapyje
        total_pages = len(df_books) // items_per_page + (len(df_books) % items_per_page > 0)

        # Puslapio valdymas su "Next" ir "Previous" mygtukais
        if 'page' not in st.session_state:
            st.session_state.page = 1

        prev_button, next_button = st.columns([1, 1])

        with prev_button:
            if st.button("Previous"):
                if st.session_state.page > 1:
                    st.session_state.page -= 1

        with next_button:
            if st.button("Next"):
                if st.session_state.page < total_pages:
                    st.session_state.page += 1

        # Knygų indeksų skaičiavimas
        start_idx = (st.session_state.page - 1) * items_per_page
        end_idx = start_idx + items_per_page

        # Rodyti pasirinkto puslapio duomenis
        st.write(f"Rodomi knygų įrašai nuo {start_idx + 1} iki {min(end_idx, len(df_books))} iš {len(df_books)}")
        st.dataframe(df_books.iloc[start_idx:end_idx])

def show_over(st):
    st.markdown("### Veluojančių knygų sąrašas")
    df_books = pd.DataFrame(config.lib.get_overdue_books(), columns=["Skaitytojo ID","ISBN", "Knygos pavadinimas", "Autorius", "Leidybos metai", "Miestas: Leidykla", "Žanras"])
    st.dataframe(df_books)
        
def show_borrowed(st):
    df_books = pd.DataFrame(config.lib.get_borrowed_books(), columns=["Skaitytojo ID","Grąžinimo data","ISBN", "Knygos pavadinimas", "Autorius", "Leidybos metai", "Miestas: Leidykla", "Žanras"])
    st.dataframe(df_books)

def show_user_borrowed(st):
    df_books = pd.DataFrame(config.lib.get_user_borrowed_books(config.user_in), columns=["Grąžinimo data","ISBN", "Knygos pavadinimas", "Autorius", "Leidybos metai", "Miestas: Leidykla", "Žanras"])
    st.dataframe(df_books)

def show_users(st):
    st.markdown("### Visi įBiblioteką vartotojai")
    df_books = pd.DataFrame(config.lib.get_user_list(), columns=["Rolė","Skaitytojo ID","Vardas", "Pavardė", "Slaptažodis"])
    st.dataframe(df_books)
    
def show_add_book(st):
    st.markdown("### Įveskite knygos duomenis")
    book = config.book_title.copy()
    for i, j in book.items():
        book[i]= st.text_input(f"{j}")
    if st.button("Pridėti knygą"):
        if helper.add_single_book(config.lib,book):
            manager.write_to_library()
            st.write("Knyga įtraukta sėkmingai!")
        else:
            st.write("Įvyko klaida prašome pabandyti dar kartą!")
def show_del_book(st):
    st.markdown("### Ištrinti knygą pagal ISBN")
    isbn_in = st.text_input(f"Įveskite ISBN")
    if st.button("Ištrinti knygą"):
        st.write(config.lib.remove_single_book(isbn_in))
        manager.write_to_library()

def show_del_books(st):
    st.markdown("### Ištrinti knygas pagal datą")
    years_in = st.text_input(f"Įveskite metus")
    if st.button("Ištrinti knygas"):
        st.write(config.lib.remove_old_books(years_in))
        manager.write_to_library()

def show_user_list(st):
    first_name = st.sidebar.text_input(f"Įveskite vardą")
    last_name = st.sidebar.text_input(f"Įveskite pavardę")
    if_admin = st.sidebar.checkbox('Ar bibliotininkas?')
    if st.sidebar.button("Pridėti vartotoją"):
        if if_admin:
            role = "admin"
        else:
            role = "reader"
        new_user = helper.add_new_user(role, first_name, last_name)
        if (new_user):
            st.sidebar.text(new_user.get_new_user())
            manager.write_to_library()
        else:
            st.write("Įvyko klaida prašome pabandyti dar kartą!")
            
def show_borrow_book(st):
    try:
        book_in=str(st.sidebar.text_input(f"Knygos ISBN"))
        user_in=str(st.sidebar.text_input(f"Skaitytojo ID"))
    except:
        st.write("Įvyko klaida prašome pabandyti dar kartą!")
    try: 
        days_in=int(st.sidebar.text_input(f"Laikotarpis"))
    except:
        days_in=14
    if st.sidebar.button("Pridėti į sąrašą"):
        print("1")
        try:
            book = config.lib.get_book_by_isbn(book_in)
            user = config.lib.get_user_by_cn(user_in)
        except:
            st.write("Įvyko klaida prašome pabandyti dar kartą!")
        if isinstance(book,bk.Book) and isinstance(user,usr.User):
            result = user.borrow_book(book, days_in)
            st.text(result)
        else:
            st.write("Įvyko klaida prašome pabandyti dar kartą!")
        
        manager.write_to_library()

def show_login(st):
    card_number = st.sidebar.text_input("Vartotojo ID")
    password = st.sidebar.text_input("Slaptažodis", type="password")

    if st.sidebar.button("Prisijungti"):
        if authenticate_user(card_number, password, st):
            config.user_in = config.lib.get_user_by_cn(card_number)
            st.session_state.logged_in = logged_in()
            st.rerun()
        else:
            st.sidebar.error("Neteisingas vartotojo vardas arba slaptažodis")  
            
def show_role(st):
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
    st.sidebar.write(f"įBiblioteką esate kaip: {user_role}")
    if (user_role=="admin"):
        options = ["Visos knygos",
                   "Vartotojų sąrašas",
                   "-----------------", 
                   "Pridėti knygą", 
                   "Ištrinti knygą",
                   "Ištrinti knygas",
                   "-----------------", 
                   "Priskirti knygą",
                   "Grąžinti knygą",
                   "-----------------",
                   "Veluojančios knygos",
                   "Paimtos knygos",
                   "-----------------",
                   "Statistika"
                   ]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
             
    elif(user_role=="reader"):
        if(config.user_in.has_overdue_books()):
            st.sidebar.error(f"Dėmesio turite negrąžintų knygų!") 
        
        options = ["Visos knygos",
                   "Jūsų paimtos knygos"]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
        
    else:
        options = ["Visos knygos"]
        selected_option = st.sidebar.selectbox("Pasirinkite:", options)
        
    return user_role, selected_option

def show_greetings(st):
    st.write("# Sveiki atvykę įBiblioteką 👋")
    st.markdown(f"Didžiausia bibliotekų sistema Lietuvoje, net {config.lib.get_count()} skirtingų knygų.")
    
def show_statistics(st):
    data = {'Return Date': config.lib.get_all_dates()}
    from datetime import datetime
    df_books = pd.DataFrame(data)
    df_books['Return Date'] = pd.to_datetime(df_books['Return Date'])
    df_books['Late'] = df_books['Return Date'] < datetime.today()
    avg_late_books = df_books['Late'].mean() * len(df_books)
    st.write(f"Vidutinis vėluojančių knygų kiekis: {round(avg_late_books)}")