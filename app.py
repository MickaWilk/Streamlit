import streamlit as st
import requests
import re
CATEGORY = {"people": "characters", "planets": "planets", "starships": "starships"}

# Recherche de l'id

def parse_url_id(url):
  item_id_match = re.search(r'/api/\w+/(\d+)/', url)
  if item_id_match:
    item_id = item_id_match.group(1)
    print(f"L'identifiant de l'élément est {item_id}.")
    return item_id
  else:
    print("Impossible de trouver l'identifiant de l'élément.")
    
    
    
# Fonction pour réaliser une recherche avec l'API SWAPI
def search(category, query):
  url = f"https://swapi.dev/api/{category}?search={query}"
  response = requests.get(url)
  results = response.json()['results']
  return results


# Streamlit part

st.sidebar.title("Options de recherche")
category = st.sidebar.selectbox("Choisissez une catégorie", ["people", "planets", "starships"])
query = st.sidebar.text_input("Entrez votre recherche")

# Si l'utilisateur a saisi une requête, effectuer la recherche et afficher les résultats
if query:
  results = search(category, query)
  st.title(f"Résultats de la recherche pour '{query}' dans la catégorie '{category}' :")
  for result in results:
    st.markdown(f"- **{result['name']}**")
    id = parse_url_id(result['url'])
    if requests.get(f"https://starwars-visualguide.com/assets/img/{CATEGORY[category]}/{id}.jpg").status_code == 200:
      st.image(f"https://starwars-visualguide.com/assets/img/{CATEGORY[category]}/{id}.jpg")
    else:
      st.image(f"https://starwars-visualguide.com/assets/img/placeholder.jpg")