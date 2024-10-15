import arturas_k_library.config as config
import arturas_k_library.modules.library as lb

import arturas_k_library.functions.file_manager as manager
import arturas_k_library.functions.helper as helper
from arturas_k_library.web.auth import authenticate_user, logged_in, logged_out, check_login
import arturas_k_library.web.table as web
import streamlit as st
import pandas as pd


config.lib = lb.Library()
manager.init()

st.session_state.logged_in = check_login()

st.set_page_config(page_title="įBiblioteka", page_icon="")

if not st.session_state.logged_in:
    web.show_login(st)    
else:
    user_role, selected_option = web.show_role(st)

if not st.session_state.logged_in:
    web.show_greetings(st)
    web.show_table(st)
else:
    if (user_role=="admin"):
        # print(selected_option)
        if selected_option == "Visos knygos":
            web.show_greetings(st)
            web.show_table(st) 
        if selected_option == "Pridėti knygą":
            web.show_add_book(st)
        if selected_option == "Ištrinti knygą":
            web.show_del_book(st)
        if selected_option == "Ištrinti knygas":
            web.show_del_books(st)
        if selected_option == "Vartotojų sąrašas":
            web.show_users(st)
            web.show_user_list(st)
        if selected_option == "Priskirti knygą":
            st.markdown("### Knygų sąrašas")
            web.show_table(st) 
            web.show_borrow_book(st)
        if selected_option == "Veluojančios knygos":    
            web.show_over(st)
        if selected_option == "Paimtos knygos":    
            st.markdown("### Visos paimtos knygos")
            if (config.lib.view_overdue_books()):
                st.error("Sąraše yra skaitytojų negražintų knygų")
            web.show_borrowed(st)     
        if selected_option == "Statistika":
            web.show_statistics(st)         
    elif(user_role=="reader"): 
        if selected_option == "Visos knygos":
            web.show_greetings(st)
            web.show_table(st) 
        if selected_option == "Jūsų paimtos knygos":
            st.markdown("### Jūsų paimtos knygos")
            web.show_user_borrowed(st)
        
    else:
        if selected_option == "Visos knygos":
            web.show_greetings(st)
            web.show_table(st)
            
    if st.sidebar.button("Atsijungti"):
        manager.write_to_library()
        st.session_state.logged_in = logged_out()
        # print(st.session_state.logged_in)
        st.rerun()
    
    