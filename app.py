import streamlit as st
import requests
import re
CATEGORY = {"people": "characters", "planets": "planets", "starships": "starships"}

# Recherche de l'id dans l'url
@st.cache
def parse_url_id(url):
  item_id_match = re.search(r'/api/\w+/(\d+)/', url)
  if item_id_match:
    item_id = item_id_match.group(1)
    return item_id
  else:
    print("Impossible de trouver l'identifiant de l'élément.")
    
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
    unsafe_allow_html=True
)
    
# Fonction pour réaliser une recherche avec l'API SWAPI
@st.cache
def search(category, query):
  url = f"https://swapi.dev/api/{category}?search={query}"
  response = requests.get(url)
  results = response.json()['results']
  return results

# Parcourir la liste de résultats et afficher les images
def draw_results(results):
    st.empty()
    st.title(f"Résultats de la recherche pour '{query}' dans la catégorie '{category}' :")
    for result in results:
      st.write(f"- **{result['name']}**")
      id = parse_url_id(result['url'])
      if requests.get(f"https://starwars-visualguide.com/assets/img/{CATEGORY[category]}/{id}.jpg").status_code == 200:
        st.image(f"https://starwars-visualguide.com/assets/img/{CATEGORY[category]}/{id}.jpg")
      else:
        st.image(f"https://starwars-visualguide.com/assets/img/placeholder.jpg")


# Effectuer la requête
def do_query(category, query):
  if query:
    results = search(category, query)
    if len(results) == 0: st.markdown("# Pas de résultats pour votre recherche :disappointed_relieved:")
    elif len(results) < 3: draw_results(results)
    else:
      results_per_page = st.sidebar.slider("Nombre de résultats par page", 1, len(results) // 2)
      total_pages = len(results) // results_per_page if len(results) > 0 else 0
      current_page = st.sidebar.selectbox("Page", [i for i in range(1, total_pages + 1)])
      start_index = (current_page - 1) * results_per_page
      end_index = start_index + results_per_page
      draw_results(results[start_index:end_index])

# Streamlit
draw_background_image()
st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Star_Wars_Logo..png/640px-Star_Wars_Logo..png')
st.sidebar.title("Options de recherche")
category = st.sidebar.selectbox("Choisissez une catégorie", ["people", "planets", "starships"])
query = st.sidebar.text_input("Entrez votre recherche")
do_query(category, query)