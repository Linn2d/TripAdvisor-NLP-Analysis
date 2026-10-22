import streamlit as st
import pandas as pd
import plotly.express as px
from manager import read_restaurant, read_location, get_db, read_review, read_date
import os, manager
from utils import database
from model import models

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
@st.cache_data(ttl=3600)
def load_data():
    db = next(get_db())
    with db:
        df_restaurant = read_restaurant(db)
        df_date = read_date(db)
        df_review = read_review(db)
        df_location = read_location(db)
    return df_restaurant, df_date, df_review, df_location

df_restaurant, df_date, df_review, df_location = load_data()

def show():
    st.markdown("""
        <div class='title-container'>
            <h1> ☁️ Analyse des performances des restaurants</h1>    
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Analyse Globale", "Analyse des Avis"])
    st.write("URL base :", str(database.engine.url))

    data_dir = os.path.join(os.path.dirname(manager.__file__), "data")
    st.write("data_dir :", data_dir, "| existe :", os.path.isdir(data_dir))

    if os.path.isdir(data_dir):
        files = manager.get_data_list(data_dir)
        st.write("Nombre de JSON :", len(files))
        if files:
            p = os.path.join(data_dir, files[0])
            st.write("Taille du 1er fichier :", os.path.getsize(p))
            st.code(open(p, encoding="utf-8").read(200))
            st.write("Clés :", list(manager.read_json_file(p).keys()))

    db = next(manager.get_db())
    st.write("Restaurants en base :", db.query(models.DimRestaurant).count())   
 
    # Onglet 1 : Analyse Globale
    with tab1:
        st.header("Analyse Globale des Performances")
        
        # Créer deux colonnes : une pour les filtres et une pour les graphiques
        col1, col2 = st.columns([1, 3])

        with col1:
            st.write("##### Filtres")
            
            # Filtre restaurant via une fenêtre contextuelle
            if st.checkbox("Tous les restaurants", value=True):
                selected_restaurants = df_restaurant['nom'].unique()
            else:
                # Créer une fenêtre contextuelle pour afficher les restaurants avec des checkboxes
                selected_restaurants = []
                restaurant_names = df_restaurant['nom'].unique()
                with st.expander("Sélectionnez des restaurants"):
                    for restaurant in restaurant_names:
                        if st.checkbox(restaurant, value=False):
                            selected_restaurants.append(restaurant)

            # Filtre pour le critère
            critere = st.selectbox(
                "Critère de comparaison",
                ["note_globale", "note_cuisine", "note_service", "note_rapportqualiteprix", "note_ambiance"]
            )

            # Filtre pour afficher les restaurants
            classement_option = st.selectbox(
                "Afficher les classements",
                ["Tous les restaurants", "5 meilleurs restaurants", "5 pires restaurants"]
            )

        with col2:
            # Filtrer les données
            filtered_df = df_restaurant[df_restaurant['nom'].isin(selected_restaurants)]
            
            # Calcul des statistiques
            stats = filtered_df.groupby('nom')[['note_globale', 'note_cuisine', 'note_service', 'note_rapportqualiteprix', 'note_ambiance']].mean().reset_index()

            if stats.empty:
                st.warning("Aucune donnée disponible pour les restaurants sélectionnés.")
            else:
                # Filtrer en fonction du classement sélectionné
                if classement_option == "5 meilleurs restaurants":
                    stats = stats.nlargest(5, critere)
                elif classement_option == "5 pires restaurants":
                    stats = stats.nsmallest(5, critere)

                # Graphique par critère
                fig = px.bar(
                    stats,
                    x="nom",
                    y=critere,
                    title=f"Comparaison des restaurants selon {critere}",
                    labels={"nom": "Restaurant", critere: "Note"},
                    color="nom",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Radar chart pour un aperçu global
                radar_df = stats.melt(id_vars=["nom"], var_name="Critère", value_name="Note")
                fig_radar = px.line_polar(
                    radar_df,
                    r="Note",
                    theta="Critère",
                    color="nom",
                    line_close=True,
                    title="Performance globale par critères"
                )
                st.plotly_chart(fig_radar, use_container_width=True)



    with tab2:
        st.header("📊 Analyse des Avis")
        
        # Data processing
        avis_data = df_review.merge(df_restaurant, on="id_restaurant", how="left")
        avis_data = avis_data.merge(df_date, on="id_date", how="left")
        
        mois_ordre = [
            "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        
        avis_data["mois"] = pd.Categorical(avis_data["mois"], categories=mois_ordre, ordered=True)
        avis_data = avis_data.sort_values(by=["annee", "mois"])
        avis_data["période"] = avis_data["mois"].str.capitalize() + " " + avis_data["annee"].astype(str)

        # Layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Analysis selector
            selected_critere = st.selectbox(
                "Type d'analyse",
                ["Nombre d'avis", "Note moyenne", "Répartition des avis"]
            )
            
            # Filters with no defaults
            years = sorted(avis_data["annee"].unique())
            selected_years = st.multiselect(
                "Années",
                options=years,
                default=None,
                placeholder="Toutes les années"
            )
            
            selected_months = st.multiselect(
                "Mois",
                options=mois_ordre,
                default=None,
                placeholder="Tous les mois"
            )
            
            restaurants = sorted(avis_data["nom"].unique())
            selected_restaurants = st.multiselect(
                "Restaurants",
                options=restaurants,
                default=None,
                placeholder="Tous les restaurants"
            )

        with col2:
            # Apply filters only if selections are made
            filtered_avis = avis_data.copy()
            
            if selected_years:
                filtered_avis = filtered_avis[filtered_avis["annee"].isin(selected_years)]
            if selected_months:
                filtered_avis = filtered_avis[filtered_avis["mois"].isin(selected_months)]
            if selected_restaurants:
                filtered_avis = filtered_avis[filtered_avis["nom"].isin(selected_restaurants)]
            
            if filtered_avis.empty:
                st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
            else:
                # Metrics
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Total avis", len(filtered_avis))
                with m2:
                    st.metric("Note moyenne", f"{filtered_avis['nb_etoiles'].mean():.1f} ⭐")
                with m3:
                    st.metric("Restaurants", len(filtered_avis['nom'].unique()))

                # Visualizations based on selected criteria
                if selected_critere == "Nombre d'avis":
                    avis_par_periode = (filtered_avis.groupby("période")
                                                   .agg(nb_avis=("id_avis", "count"))
                                                   .reset_index())
                    
                    fig = px.line(avis_par_periode, x="période", y="nb_avis",
                                title="📈 Evolution du nombre d'avis",
                                labels={"période": "Période", "nb_avis": "Nombre d'avis"})
                    fig.update_traces(mode="lines+markers")
                    st.plotly_chart(fig, use_container_width=True)

                elif selected_critere == "Note moyenne":
                    notes_par_periode = (filtered_avis.groupby("période")
                                                    .agg(note_moyenne=("nb_etoiles", "mean"))
                                                    .reset_index())
                    
                    fig = px.line(notes_par_periode, x="période", y="note_moyenne",
                                title="⭐ Evolution des notes moyennes",
                                labels={"période": "Période", "note_moyenne": "Note moyenne"})
                    fig.update_traces(mode="lines+markers")
                    st.plotly_chart(fig, use_container_width=True)

                else:  # Répartition des avis
                    avis_categorie = filtered_avis.groupby("période").agg({
                        "nbExcellent": "sum",
                        "nbTresbon": "sum",
                        "nbMoyen": "sum",
                        "nbMediocre": "sum",
                        "nbHorrible": "sum"
                    }).reset_index()
                    
                    avis_melt = pd.melt(avis_categorie, 
                                       id_vars=["période"],
                                       value_vars=["nbExcellent", "nbTresbon", "nbMoyen", 
                                                 "nbMediocre", "nbHorrible"])
                    
                    fig = px.bar(avis_melt, x="période", y="value", color="variable",
                                title="📊 Distribution des avis",
                                labels={"période": "Période", "value": "Nombre d'avis", 
                                       "variable": "Type d'avis"},
                                color_discrete_map={
                                    "nbExcellent": "#2ecc71",
                                    "nbTresbon": "#3498db",
                                    "nbMoyen": "#f1c40f",
                                    "nbMediocre": "#e67e22",
                                    "nbHorrible": "#e74c3c"
                                })
                    st.plotly_chart(fig, use_container_width=True)

# if __name__ == "__main__":
#     show()