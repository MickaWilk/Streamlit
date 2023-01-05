import streamlit as st
import requests

# Fonction pour réaliser une recherche avec l'API SWAPI
def search(category, query):
  # Construire l'URL de l'API en fonction de la catégorie et de la requête
  url = f"https://swapi.dev/api/{category}?search={query}"

  # Effectuer une requête GET à l'API
  response = requests.get(url)

  # Extraire les résultats de la réponse
  results = response.json()['results']

  return results

# Créer un menu déroulant pour sélectionner la catégorie de recherche
st.sidebar.title("Options de recherche")
category = st.sidebar.selectbox("Choisissez une catégorie", ["people", "planets", "starships"])

# Créer un champ de saisie pour entrer la requête de recherche
query = st.sidebar.text_input("Entrez votre recherche")

# Si l'utilisateur a saisi une requête, effectuer la recherche et afficher les résultats
if query:
  results = search(category, query)
  st.title(f"Résultats de la recherche pour '{query}' dans la catégorie '{category}' :")
  for result in results:
    st.markdown(f"- **{result['name']}**")
