import arturas_k_library.config as config
import arturas_k_library.functions.file_manager as manager

import pickle, os

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

def logged_in():
    try: 
        with open("user.pkl", "wb") as file:
            pickle.dump(config.user_in, file)
        print("Informacija išsaugota.")
        return True
    except:
        return False

def check_login():
    if os.path.exists("user.pkl"):
        with open("user.pkl", "rb") as file:
            config.user_in = pickle.load(file)
            return True
    else:
        return False

def logged_out():
    if os.path.exists("user.pkl"):
        os.remove("user.pkl")
        return False
    else:
        return False