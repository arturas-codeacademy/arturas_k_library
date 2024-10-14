import arturas_k_library.config as config

from arturas_k_library.modules import library as lb
from arturas_k_library.modules import user as usr
from arturas_k_library.functions.file_manager import init

import arturas_k_library.web.table as web

import streamlit as st
import pandas as pd

lib = lb.Library()
lib = init(lib)

st.set_page_config(
    page_title="iBiblioteka",
    page_icon="",
)

st.write("# Sveiki atvykę į iBiblioteką👋")

user = usr.User()
st.sidebar.success(f"Jūs prisijungęs kaip: {user.get_library_role()}")

st.markdown(
    f"""
    Didžiausia bibliotekų sistema Lietuvoje, net {lib.get_count()} skirtingų knygų.
    """
)

web.show_table(lib, st)
