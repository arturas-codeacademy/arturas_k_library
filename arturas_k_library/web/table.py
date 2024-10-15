import arturas_k_library.config as config
import pandas as pd

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
    # print(config.lib.get_overdue_books())
    df_books = pd.DataFrame(config.lib.get_overdue_books(), columns=["Skaitytojo ID","ISBN", "Knygos pavadinimas", "Autorius", "Leidybos metai", "Miestas: Leidykla", "Žanras"])
    st.dataframe(df_books)
        
def show_borrowed(st):
    df_books = pd.DataFrame(config.lib.get_borrowed_books(), columns=["Skaitytojo ID","Grąžinimo data","ISBN", "Knygos pavadinimas", "Autorius", "Leidybos metai", "Miestas: Leidykla", "Žanras"])
    st.dataframe(df_books)

def show_users(st):
    df_books = pd.DataFrame(config.lib.get_user_list(), columns=["Skaitytojo ID","Rolė","Vardas", "Pavardė", "Slaptažodis"])
    st.dataframe(df_books)
    