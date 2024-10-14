import arturas_k_library.config as config
import pandas as pd

def show_table(lib, st):
    # Knygų sąrašą paverčiame pandas DataFrame
    df_books = pd.DataFrame(lib.get_books_list(), columns=["ISBN", "Knygos pavadinimas", "Autorius", "Leidybos metai", "Miestas: Leidykla", "Žanras"])

    # Puslapiavimo nustatymai
    items_per_page = config.items_per_page  # Knygų skaičius viename puslapyje
    total_pages = len(df_books) // items_per_page + (len(df_books) % items_per_page > 0)

    # Puslapio valdymas su "Next" ir "Previous" mygtukais
    if 'page' not in st.session_state:
        st.session_state.page = 1

    prev_button, next_button = st.columns([1, 1])

    with prev_button:
        if st.button("Atgal"):
            if st.session_state.page > 1:
                st.session_state.page -= 1

    with next_button:
        if st.button("Pirmyn"):
            if st.session_state.page < total_pages:
                st.session_state.page += 1

    # Knygų indeksų skaičiavimas
    start_idx = (st.session_state.page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    # Rodyti pasirinkto puslapio duomenis
    st.write(f"Rodomi knygų įrašai nuo {start_idx + 1} iki {min(end_idx, len(df_books))} iš {len(df_books)}")
    st.dataframe(df_books.iloc[start_idx:end_idx].reset_index(drop=True))  # Pašaliname indeksus

    # Rodomas dabartinis puslapis
    st.write(f"Puslapis {st.session_state.page} iš {total_pages}")
