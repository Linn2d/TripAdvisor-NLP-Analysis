import streamlit as st
from PIL import Image
import os
from pathlib import Path
def load_css():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .title-container {
            background: linear-gradient(to right, #1e3c72, #2a5298);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }
        .team-card {
            text-align: center;
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stat-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    load_css()

    # Hero Section
    st.markdown("""
        <div class='title-container'>
            <h1>🍽️ Welcome to TripAdvisor NLP Analysis</h1>
            <h3>Découvrez les insights cachés des avis de restaurants</h3>
        </div>
    """, unsafe_allow_html=True)

    # Project Overview
    st.markdown("## 🎯 Notre Mission")
    col1, col2 = st.columns([2,1])
    with col1:
        st.write("""
        Nous utilisons l'intelligence artificielle et le traitement du langage naturel pour :
        - ☁️ Analyser les sentiments des clients
        - 📊 Identifier les tendances
        - 🤖 Assister les utilisateurs
        - 🌟 Montrer des informations cachées
        """)
    with col2:
        # Add project logo or illustration here
        # st.image("https://via.placeholder.com/300", caption="")
        # st.image("https://c.clc2l.com/c/screenshot/d/tripadvisor-resultats-61079ffde3239346241387.jpg")
        # st.image('image.png')
        # Corrected image display
        # st.image('data/image.png')
        IMAGE_PATH = Path(__file__).resolve().parents[1] / "data" / "image.png"
        st.image(str(IMAGE_PATH))
    # Features Section
    st.markdown("## ✨ Fonctionnalités")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>☁️ NLP</h3>
            <p>Analyse avancée des sentiments et des émotions dans les avis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📊 Visualisation</h3>
            <p>Graphiques interactifs et tableaux de bord dynamiques</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3>🤖 ChatBot </h3>
            <p>Assistant intelligent </p>
        </div>
        """, unsafe_allow_html=True)

    # Team Section
    st.markdown("## 👥 Notre Équipe")
    col1, col2, col3 = st.columns(3)

    team_members = [
        {"name": "Edina", "role": "ML Engineer", "skills": ["Machine Learning", "Data Pipelines"]},
        {"name": "Linh nhi", "role": "Data Scientist", "skills": ["NLP", "Data Analysis"]},
        {"name": "Nancy", "role": "Data Analyst", "skills": ["Data Analysis", "Visualization"]}
    ]

    for col, member in zip([col1, col2, col3], team_members):
        with col:
            st.markdown(f"""
            <div class='team-card'>
                <h3>{member['name']}</h3>
                <p><em>{member['role']}</em></p>
                <p>{'• '.join(member['skills'])}</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center'>
            <p>Made with ❤️ by Team TripAdvisor NLP</p>
            <p>Master Data Science - 2024</p>
        </div>
    """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     show()