import streamlit as st
from interface import (
    accueil, 
    navbar, 
    dashbord, 
    cartographie, 
    analyse_nlp2, 
    scrapper_restaurant, 
    chatbot
)
from typing import Optional
from manager import InitialisationBD
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

st.set_page_config(
    page_title="Tripadvisor Scraper",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def init_database() -> bool:
    InitialisationBD()
    return True

try:
    init_database()
except Exception as e:
    st.error(f"Initialisation de la base impossible : {e}")
    st.stop()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Accueil"

PAGES = {
    "Accueil": accueil,
    "Analyse NLP2": dashbord,
    "Cartographie": cartographie,
    "Analyse NLP": analyse_nlp2,
    "chatbot": chatbot,
    "Ajouter Restaurant": scrapper_restaurant,
}

def main():
    current_page = navbar.show()
    if current_page in PAGES:
        PAGES[current_page].show()
    else:
        st.error(f"Page {current_page} not found")

main()