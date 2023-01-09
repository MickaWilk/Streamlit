import streamlit as st
import requests
import re
import json
CATEGORY = {"people": "characters", "planets": "planets", "starships": "starships", "films": "films", "vehicles": "vehicles", "species": "species"}

# Recherche de l'id dans l'url

def draw_background_image():
  st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://lumiere-a.akamaihd.net/v1/images/star-wars-backgrounds-25_bc15ec98.jpeg");
        background-size: cover;
        background-repeat: repeat;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True)

@st.cache
def parse_url_id(url):
  item_id_match = re.search(r'/api/\w+/(\d+)/', url)
  if item_id_match:
    item_id = item_id_match.group(1)
    return item_id
  else:
    print("Impossible de trouver l'identifiant de l'élément.")

# Fonction pour réaliser une recherche avec l'API SWAPI
@st.cache
def search(category, query):
    results = []
    next = True
    url = f"https://swapi.dev/api/{category}?search={query}"
    while next:
        response = requests.get(url)
        data = json.loads(response.text)
        results.extend(data['results'])
        next = data['next'] is not None
        if next:
            url = data['next']
    return results

# Parcourir la liste de résultats et afficher les images
def draw_results(results, key):
    st.empty()
    st.title(f"Résultats de la recherche pour '{query}' dans la catégorie '{category}' :")
    cols = [i for i in st.columns(len(results))]
    for index, result in enumerate(results):
        with cols[index]:
            id = parse_url_id(result['url'])
            if requests.get(f"https://starwars-visualguide.com/assets/img/{CATEGORY[category]}/{id}.jpg").status_code == 200:
                st.image(f"https://starwars-visualguide.com/assets/img/{CATEGORY[category]}/{id}.jpg")
            else:
                st.image(f"https://starwars-visualguide.com/assets/img/placeholder.jpg")
            st.write(f"- **{result[key]}**")


# Effectuer la requête
def do_query(category, query):
  if query:
    results = search(category, query)
    key = next(iter(results[0]))
    if len(results) == 0: st.markdown("# Pas de résultats pour votre recherche :disappointed_relieved:")
    elif len(results) < 3: draw_results(results, key)
    else:
      results_per_page = st.sidebar.slider("Nombre de résultats par page", 1, len(results) // 2)
      total_pages = len(results) // results_per_page if len(results) > 0 else 1
      current_page = st.sidebar.selectbox("Page", [i for i in range(1, total_pages + 1)])
      start_index = (current_page - 1) * results_per_page
      end_index = start_index + results_per_page
      draw_results(results[start_index:end_index], key)

# Streamlit
st.set_page_config(
page_title="Starwars Search Page",
page_icon="👀",
layout="centered",
initial_sidebar_state="expanded",
menu_items={
    'Get help': 'https://github.com/MickaWilk',
    'Report a bug': "https://github.com/MickaWilk/Streamlit/issues"})
draw_background_image()
st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Star_Wars_Logo..png/640px-Star_Wars_Logo..png')
st.audio("https://www.cjoint.com/doc/21_05/KEhhYBEVF5L_Star-Wars-Theme-Song-.mp3")
st.sidebar.title("Options de recherche")
category = st.sidebar.selectbox("Choisissez une catégorie", ["people", "planets", "starships", "films", "vehicles", "species"])
query = st.sidebar.text_input("Entrez votre recherche")
do_query(category, query)
