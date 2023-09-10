import streamlit as st
from recommender import hybrid_recommend, get_metadata
from youtubesearchpython import VideosSearch

dataset_url = 'https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs'
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title='Mellifluous - Music Recommendation Engine 🎶', 
    page_icon='🎶',
    menu_items={
        'Get Help': None,
        'About': f"### Mini Project ❣ - SEM IV! \n #### By Anushaka Patil, Harkeerat Dhunda, Mohammad Adil, Riya Sudrik \n#### Music Data sourced from [Kaggle]({dataset_url})"
    }
)
st.write(st.config.get_option("server.enableCORS"))
   
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             font-family:  "Lucida Handwriting", cursive;
             line-spacing: 1.1;
             background-attachment: fixed;
             background-size: cover;
             background: linear-gradient(rgba(255,255,255,.1), rgba(255,255,255,.1)), url("https://static.vecteezy.com/system/resources/previews/005/489/284/non_2x/beautiful-purple-color-gradient-background-free-vector.jpg");

         }}
         </style>
         """,
         unsafe_allow_html=True
     )
add_bg_from_url()

def grad():
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-image: linear-gradient(to bottom, #EE82EE,#9400D3 );
                color: white;
                backdrop-filter: blur(10px);
                
        }
    </style>
    """, unsafe_allow_html=True)
grad()
# Persistent app state managment

def change_song(index):
    st.session_state['current_song_index'] = index

if 'current_song_index' not in st.session_state:
    change_song(10000)

# Sidebar with customizing options
st.sidebar.image("https://rare-gallery.com/uploads/posts/4585585-vinyl-music-gramophone.jpg", use_column_width=True)
st.sidebar.title('Choose:')

option1 = 'Keep up with what\'s trending'
option2 = 'Discover hidden gems'
mode = st.sidebar.selectbox('Your mode of recommendations:', (option1, option2))
if(mode == option1):
    prioritisePopular = True
else:
    prioritisePopular = False

recommendations_count = st.sidebar.slider('Upto how many of each kind of recommendations would you like '
'(lesser means more accurate but more means more variety!)', min_value=1, max_value=10, value=3)

st.sidebar.write('Which kinds of recommendations you\'d like') # options added later below when adding songs

# Main Content:

# Showing current song

current_song = get_metadata(st.session_state['current_song_index'])

st.write(f'## {current_song["track_name"]} - {current_song["track_artist"]}')

youtube_search = VideosSearch(f'## {current_song["track_name"]} - {current_song["track_artist"]}', limit = 1)
youtube_id = youtube_search.result()['result'][0]['id'] # getting youtube link
thumbnail_url = youtube_search.result()['result'][0]['thumbnails'][0]['url'] # getting youtube thumbnail

st.write(f'[![YouTube thumbnail]({thumbnail_url})](https://www.youtube.com/watch?v={youtube_id})')
st.write(f'[Hear on YouTube](https://www.youtube.com/watch?v={youtube_id})')

with st.expander('Show lyrics'):
    st.write(current_song['lyrics'])


# Retreiving and showing recommendations as per user's choices

recommendations = hybrid_recommend(st.session_state['current_song_index'], recommendations_count, prioritisePopular=prioritisePopular)

for recommendation_type, songs in recommendations.items():
    if not st.sidebar.checkbox(recommendation_type, value=True):
        continue
    if(len(songs) == 0): # do not show a recommendation type if it has no songs
        continue
    st.write(f'<u><h3>{recommendation_type.title()}:</h3></u>', unsafe_allow_html=True)

    with st.container():
        for i, song in enumerate(songs):
            st.write(f'#### {i+1}. <em>{song["track_name"]}</em> - <em>{song["track_artist"]}</em>', unsafe_allow_html=True)
            st.button("listen", key=str(song['index'])+recommendation_type, on_click=change_song, args=(song['index'],))
