import arturas_k_library.config as config
import arturas_k_library.functions.file_manager as manager

def authenticate_user(card_number, password, st):
    config.user_in = config.lib.get_user_by_cn(card_number)
    if(config.user_in is not False):
        if (config.user_in.user_pasword == password):
            st.session_state.logged_in = True
            return True
        else:
            st.error("Neteisingas slaptažodis.")
            return False
    else:
        st.error("Vartotojas nerastas.")
        return False
