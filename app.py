from html import escape
from pathlib import Path
import random

import requests
import streamlit as st
import streamlit.components.v1 as components

from recommender import MusicRecommender


st.set_page_config(
    page_title='Mellifluous · Music Recommendation Engine',
    page_icon='🎶',
    layout='wide',
    menu_items={'About': 'A customizable, explainable music recommendation prototype.'}
)

st.markdown(
    '''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Poppins:wght@400;500;600;700&display=swap');

    :root {
        --bg: #DDC9F0;
        --bg-deep: #D2B8EA;
        --surface: #EEE1F8;
        --surface-strong: #F5ECFB;
        --surface-soft: #E7D5F4;
        --text: #21172B;
        --muted: #62546D;
        --muted-soft: #796985;
        --accent: #72449D;
        --accent-deep: #57306F;
        --accent-soft: #DCC6EE;
        --line: #C8A9DD;
        --line-strong: #B98FD3;
        --sidebar-top: #86509B;
        --sidebar-mid: #5B286B;
        --sidebar-bottom: #21102C;
        --sidebar-text: #FBF6FF;
        --sidebar-muted: #E3D2EB;
        --shadow: 0 12px 30px rgba(68, 39, 83, .13);
        --shadow-hover: 0 16px 38px rgba(68, 39, 83, .19);
    }

    html, body, .stApp {
        font-family: 'Poppins', sans-serif;
        color: var(--text);
    }

    .stApp {
        background:
            radial-gradient(circle at 9% 7%, rgba(245, 231, 255, .46), transparent 26%),
            radial-gradient(circle at 91% 9%, rgba(180, 143, 214, .22), transparent 30%),
            linear-gradient(155deg, #E5D3F4 0%, var(--bg) 48%, var(--bg-deep) 100%);
    }

    .block-container {
        max-width: 1240px;
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4, h5, h6,
    .hero-title,
    .song-title,
    .card-title,
    .sidebar-song-title {
        font-family: 'Fraunces', serif !important;
        color: var(--text) !important;
        letter-spacing: -.025em;
    }

    p, label, button, input, textarea,
    [data-testid="stCaptionContainer"],
    [data-testid="stMarkdownContainer"] {
        font-family: 'Poppins', sans-serif;
    }

    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 16% 6%, rgba(239, 192, 252, .34), transparent 24%),
            radial-gradient(circle at 91% 31%, rgba(168, 91, 190, .28), transparent 31%),
            radial-gradient(circle at 34% 79%, rgba(107, 48, 132, .24), transparent 35%),
            linear-gradient(148deg, var(--sidebar-top) 0%, #713982 25%, var(--sidebar-mid) 52%, #3B1848 76%, var(--sidebar-bottom) 100%) !important;
        border-right: 1px solid rgba(255,255,255,.14) !important;
    }

    section[data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div {
        background: transparent !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: .65rem !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: .55rem !important;
        padding-bottom: .55rem !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: var(--sidebar-text) !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: var(--sidebar-muted) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.18) !important;
        margin-top: .55rem !important;
        margin-bottom: .55rem !important;
    }

    [data-testid="stSidebar"] [data-testid="stImage"] {
        max-width: 285px;
        margin-left: auto;
        margin-right: auto;
    }

    [data-testid="stSidebar"] img {
        border-radius: 16px;
        box-shadow: 0 12px 28px rgba(28, 12, 35, .25);
        border: 1px solid rgba(255,255,255,.18);
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"],
    [data-testid="stSidebar"] [data-testid="stSlider"],
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        margin-bottom: -.2rem;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        min-height: 1.5rem;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] label {
        gap: .42rem;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
        font-size: 1rem !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="input"] > div {
        background: rgba(252, 246, 255, .95) !important;
        border-color: rgba(255,255,255,.25) !important;
        border-radius: 11px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #2E1D35 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #D8BDE9 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #38203F !important;
    }

    [data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
        background: #DABDEF !important;
        border-color: #DABDEF !important;
    }

    [data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #F0E1F9 0%, #DABCEB 100%) !important;
        border: 1px solid rgba(255, 255, 255, .45) !important;
        color: #24102E !important;
        box-shadow: 0 7px 18px rgba(22, 8, 30, .24) !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] div.stButton > button p,
    [data-testid="stSidebar"] div.stButton > button span,
    [data-testid="stSidebar"] div.stButton > button div {
        color: #24102E !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #24102E !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #F7ECFC 0%, #E4CBF1 100%) !important;
        border-color: rgba(255, 255, 255, .65) !important;
        color: #180920 !important;
        transform: translateY(-1px);
    }

    [data-testid="stSidebar"] div.stButton > button:hover p,
    [data-testid="stSidebar"] div.stButton > button:hover span,
    [data-testid="stSidebar"] div.stButton > button:hover div {
        color: #180920 !important;
        -webkit-text-fill-color: #180920 !important;
    }

    .hero {
        text-align: center;
        padding: .7rem .5rem 1.45rem;
    }

    .hero-title {
        font-size: clamp(2.75rem, 5vw, 4.7rem);
        font-weight: 700;
        line-height: .98;
        margin: 0;
        color: #27182F !important;
    }

    .hero-accent {
        color: var(--accent);
    }

    .hero p {
        max-width: 760px;
        margin: .85rem auto 0;
        color: #584763;
        font-size: 1rem;
        line-height: 1.72;
    }

    .now-playing-head {
        padding: .12rem .1rem .72rem;
    }

    .now-playing-head .eyebrow {
        text-transform: uppercase;
        letter-spacing: .14em;
        font-size: .70rem;
        font-weight: 700;
        color: var(--accent-deep);
        margin-bottom: .28rem;
    }

    .now-playing-head .song-title {
        font-size: clamp(1.7rem, 2.5vw, 2.35rem);
        font-weight: 700;
        line-height: 1.04;
        margin: 0;
    }

    .now-playing-head .artist {
        display: inline;
        font-size: .98rem;
        color: var(--muted);
        font-weight: 500;
    }

    .now-playing-head .meta {
        display: inline;
        color: var(--muted-soft);
        font-size: .83rem;
        margin-left: .48rem;
    }

    .st-key-now_playing {
        background: linear-gradient(135deg, rgba(240,224,249,.97), rgba(216,189,234,.97));
        border: 1px solid var(--line-strong) !important;
        border-radius: 24px !important;
        box-shadow: var(--shadow);
        padding: 1.05rem 1.15rem .72rem;
        margin-bottom: .8rem;
    }

    .st-key-now_playing div[data-testid="stVerticalBlockBorderWrapper"] {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    .section-kicker {
        color: #5D4B67;
        margin-top: -.42rem;
        margin-bottom: 1.05rem;
        font-size: .91rem;
        line-height: 1.6;
        max-width: 760px;
    }

    .lyrics {
        white-space: pre-wrap;
        font-family: 'Poppins', sans-serif;
        line-height: 1.9;
        font-size: .96rem;
        color: #302038;
        background: #E8D7F4;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.3rem 1.4rem;
        max-height: 500px;
        overflow-y: auto;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(239, 225, 248, .94);
        border: 1px solid var(--line) !important;
        border-radius: 20px !important;
        box-shadow: var(--shadow);
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
        overflow: hidden;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
        border-color: var(--line-strong) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] img {
        border-radius: 14px;
    }

    .card-title {
        font-size: 1.14rem;
        font-weight: 700;
        line-height: 1.22;
        margin-top: .25rem;
    }

    .card-artist {
        color: var(--muted);
        font-size: .89rem;
        margin-top: .16rem;
        min-height: 1.35rem;
        font-weight: 500;
    }

    .card-meta {
        color: var(--muted-soft);
        font-size: .76rem;
        margin-top: .4rem;
        min-height: 1.2rem;
    }

    .card-badge {
        display: inline-flex;
        align-items: center;
        width: fit-content;
        margin-top: .55rem;
        margin-bottom: .65rem;
        padding: .24rem .55rem;
        border-radius: 999px;
        background: rgba(111, 66, 139, .11);
        border: 1px solid rgba(111, 66, 139, .22);
        color: #5B336D;
        font-size: .69rem;
        font-weight: 600;
        letter-spacing: .015em;
    }

    .mode-note {
        color: var(--sidebar-muted);
        font-size: .79rem;
        line-height: 1.45;
        margin-top: -.2rem;
        margin-bottom: .15rem;
    }

    div.stButton > button,
    div[data-testid="stLinkButton"] > a {
        border-radius: 999px !important;
        border: 1px solid var(--line-strong) !important;
        background: #F3E8FA !important;
        color: #33203D !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        box-shadow: 0 3px 10px rgba(67, 46, 91, .07);
        transition: transform .15s ease, background .15s ease, color .15s ease, border-color .15s ease;
    }

    div.stButton > button:hover,
    div[data-testid="stLinkButton"] > a:hover {
        transform: translateY(-1px);
        background: #DCC4ED !important;
        border-color: #A879C7 !important;
        color: #4E2A62 !important;
    }

    div.stButton > button:focus,
    div[data-testid="stLinkButton"] > a:focus {
        box-shadow: 0 0 0 3px rgba(114, 68, 157, .18) !important;
    }

    [data-testid="stSelectbox"] label,
    [data-testid="stSlider"] label,
    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {
        color: var(--text) !important;
        font-weight: 500;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    input {
        background: rgba(245, 236, 251, .94) !important;
        color: var(--text) !important;
        border-color: var(--line-strong) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] {
        background: #F3E8FA !important;
        color: var(--text) !important;
    }

    [data-baseweb="slider"] [role="slider"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    [data-baseweb="slider"] > div > div > div {
        background: var(--accent) !important;
    }

    div[data-testid="stExpander"] {
        background: rgba(235, 217, 246, .94);
        border: 1px solid var(--line);
        border-radius: 18px;
    }

    div[data-testid="stExpander"] summary {
        color: var(--text) !important;
        font-weight: 600;
    }

    [data-testid="stAlert"] {
        background: #DFC8EF;
        color: var(--text);
        border-color: var(--line-strong);
        border-radius: 16px;
    }

    hr {
        border-color: rgba(109, 72, 128, .26) !important;
        margin-top: 1.55rem !important;
        margin-bottom: 1.25rem !important;
    }

    .sidebar-song-title {
        font-size: 1.22rem;
        font-weight: 700;
        line-height: 1.08;
        margin-top: .25rem;
        color: var(--sidebar-text) !important;
    }

    .sidebar-artist {
        color: var(--sidebar-muted);
        font-size: .80rem;
        margin-top: .08rem;
    }

    .sidebar-discovery-title {
        color: var(--sidebar-text);
        font-size: 1.04rem;
        font-weight: 600;
        margin-top: .48rem;
        margin-bottom: .18rem;
    }

    .footer {
        text-align: center;
        margin-top: 2.8rem;
        padding: 1.65rem .5rem .9rem;
        color: #4A3157;
        font-size: 1.18rem;
        font-weight: 600;
        letter-spacing: .015em;
    }

    @media (max-height: 820px) {
        [data-testid="stSidebar"] > div:first-child {
            padding-top: .35rem !important;
        }

        [data-testid="stSidebar"] [data-testid="stImage"] {
            max-width: 225px;
        }

        .sidebar-song-title {
            font-size: 1.08rem;
        }

        [data-testid="stSidebar"] hr {
            margin-top: .35rem !important;
            margin-bottom: .35rem !important;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            font-size: .80rem;
        }

        [data-testid="stSidebar"] [data-testid="stCheckbox"] {
            min-height: 1.3rem;
        }
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .st-key-now_playing {
            padding: .85rem;
        }
    }
    </style>
    ''',
    unsafe_allow_html=True
)


@st.cache_resource(show_spinner='Building recommendation indexes…')
def load_recommender():
    return MusicRecommender(Path(__file__).with_name('spotify_songs.csv'))


@st.cache_data(ttl=86400, show_spinner=False)
def spotify_artwork(track_id):
    if not track_id:
        return None
    try:
        response = requests.get(
            'https://open.spotify.com/oembed',
            params={'url': f'https://open.spotify.com/track/{track_id}'},
            timeout=3
        )
        response.raise_for_status()
        return response.json().get('thumbnail_url')
    except requests.RequestException:
        return None


def choose_song(label):
    st.session_state['song_selector'] = label
    st.session_state['scroll_to_player'] = True


def surprise_me(song_options):
    current = st.session_state.get('song_selector')
    choices = [song for song in song_options if song != current]
    st.session_state['song_selector'] = random.choice(choices or song_options)
    st.session_state['scroll_to_player'] = True


def advance_section(state_key, pool_length, count):
    if pool_length <= count:
        return
    current_offset = st.session_state.get(state_key, 0)
    st.session_state[state_key] = (current_offset + count) % pool_length


def scroll_to_now_playing():
    components.html(
        '''
        <script>
        const root = window.parent.document;
        setTimeout(() => {
            const target = root.querySelector('.st-key-now_playing');
            if (target) {
                target.scrollIntoView({behavior: 'smooth', block: 'start'});
            } else {
                window.parent.scrollTo({top: 0, behavior: 'smooth'});
            }
        }, 120);
        </script>
        ''',
        height=0
    )


@st.dialog('How Mellifluous ♪ works', width='large')
def show_how_it_works():
    st.markdown('### A content-based recommender where *you* choose the similarity function')
    st.markdown(
        '''
Mellifluous first filters the dataset to **English-language tracks** and removes duplicate
`(track_name, track_artist)` pairs. It then builds different mathematical representations
of each song depending on what you ask “similar” to mean.

#### 1. Lyrically similar — TF-IDF + cosine distance

Lyrics are converted into a sparse TF-IDF vector. For term $t$ in song $d$:
        '''
    )
    st.latex(r"\mathrm{tfidf}(t,d)=\mathrm{tf}(t,d)\times\log\left(\frac{N}{\mathrm{df}(t)}\right)")
    st.markdown(
        '''
The vectorizer removes English stop words, ignores terms appearing in fewer than 2 songs,
and keeps at most 30,000 features.

Two lyric vectors $x$ and $y$ are compared using cosine distance:
        '''
    )
    st.latex(r"d_{\mathrm{cos}}(x,y)=1-\frac{x\cdot y}{\lVert x\rVert_2\lVert y\rVert_2}")
    st.markdown(
        '''
So songs can be close because they use related words/themes even when their audio features
are completely different.

#### 2. Similar energy — standardized audio vector + Euclidean distance

Each song becomes the feature vector:
        '''
    )
    st.latex(r"x_E=[\mathrm{danceability},\ \mathrm{energy},\ \mathrm{tempo},\ \mathrm{acousticness},\ \mathrm{loudness}]")
    st.markdown('Because these features live on different numeric scales, each feature is standardized:')
    st.latex(r"z_j=\frac{x_j-\mu_j}{\sigma_j}")
    st.markdown('Nearest neighbours are then found with Euclidean distance:')
    st.latex(r"d_E(a,b)=\sqrt{\sum_{j=1}^{5}(z_{a,j}-z_{b,j})^2}")

    st.markdown(
        '''
#### 3. Similar mood — a different feature space

Mood deliberately uses a different vector:
        '''
    )
    st.latex(r"x_M=[\mathrm{valence},\ \mathrm{mode},\ \mathrm{key},\ \mathrm{energy},\ \mathrm{danceability}]")
    st.markdown(
        '''
It is standardized independently and also searched with Euclidean nearest neighbours.
The important part is that **“energy similarity” and “mood similarity” are not the same
distance function over the same features**.

#### 4. Same artist & same era — deterministic rules

**Same artist** is an exact artist match.

For **same era**, the distance between two songs is simply the absolute difference between
their release dates:
        '''
    )
    st.latex(r"d_{\mathrm{era}}(a,b)=\left|\mathrm{date}_a-\mathrm{date}_b\right|\quad\text{(in days)}")
    st.markdown(
        '''
The songs with the smallest date differences become the candidate set.

#### 5. Trending vs hidden gems — two-stage retrieval + reranking

For lyric, mood and energy searches, Mellifluous does **not** mix popularity into the
similarity equation. It first retrieves a neighbourhood based only on similarity.

For $k$ requested recommendations, the nearest-neighbour candidate pool is:
        '''
    )
    st.latex(r"P=\min\left(N,\ \max(8k+1,\ 41)\right)")
    st.markdown(
        '''
That pool is then reranked by Spotify's `track_popularity` field:

- **Keep up with what's trending:** sort popularity **descending**
- **Discover hidden gems:** sort popularity **ascending**

So this is a **two-stage recommender**:

**content similarity → candidate pool → popularity reranking**

That separation is intentional: your definition of *similar* stays intact while you can
independently control whether the final results skew mainstream or obscure.

#### 6. Wildcard

Wildcard bypasses the similarity models entirely and samples songs without replacement.
The random generator is deterministically seeded from the selected track index and requested
count, so the result is reproducible for a given state.

---

**In short:** Mellifluous is a transparent **content-based recommendation system**, not
collaborative filtering. The user explicitly chooses the representation and distance notion
instead of receiving one opaque recommendation score.
        '''
    )
    st.caption(
        'Implementation: scikit-learn TF-IDF, StandardScaler and NearestNeighbors; '
        'recommendations are computed locally from the included dataset.'
    )


def format_lyrics(text):
    text = str(text or '').strip()
    if not text:
        return 'Lyrics unavailable for this track.'
    if '\n' in text:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
    else:
        words = text.split()
        lines = []
        current = []
        for word in words:
            current.append(word)
            if len(current) >= 8:
                lines.append(' '.join(current))
                current = []
        if current:
            lines.append(' '.join(current))
    blocks = []
    for start in range(0, len(lines), 4):
        blocks.append('\n'.join(lines[start:start + 4]))
    return '\n\n'.join(blocks)


def render_spotify_embed(track_id):
    components.html(
        f'''
        <iframe
            style="border-radius:18px; display:block;"
            src="https://open.spotify.com/embed/track/{escape(track_id)}?utm_source=generator&theme=0"
            width="100%"
            height="152"
            frameborder="0"
            allowfullscreen=""
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy">
        </iframe>
        ''',
        height=168
    )


section_copy = {
    'by same artist': (
        'More by the same artist',
        'Stay in the same discography, then let your discovery mode decide whether to surface familiar favourites or deeper cuts.'
    ),
    'lyrically similar': (
        'Lyrically similar',
        'Matched through lyric similarity, so the language and themes of the song drive this set.'
    ),
    'similar energy': (
        'Similar energy',
        'Matched using danceability, energy, tempo, acousticness and loudness.'
    ),
    'similar mood': (
        'Similar mood',
        'Matched using valence, mode, key, energy and danceability.'
    ),
    'released around same time': (
        'From the same era',
        'Songs released closest in time to the track you picked.'
    ),
    'random': (
        'Wildcard',
        'No similarity rules here — just a deliberate jump somewhere else in the catalogue.'
    )
}

recommender = load_recommender()
options = recommender.song_options()


if 'song_selector' not in st.session_state:
    default_song = next(
        (song for song in options if 'Billie Jean' in song),
        options[0]
    )
    st.session_state['song_selector'] = default_song

st.markdown(
    '''
    <div class="hero">
        <div class="hero-title"><span class="hero-accent">♪</span> Mellifluous <span class="hero-accent">♪</span></div>
        <p>One day, I got tired of Spotify’s recommendation black box. So I built my own: one where you decide what “similar” actually means: lyrics, mood, energy, era, artist, or random chaos!</p>
    </div>
    ''',
    unsafe_allow_html=True
)

song_col, surprise_col = st.columns([5, 1.3], vertical_alignment='bottom')
with song_col:
    selected_label = st.selectbox('Start with a song', options, key='song_selector')
with surprise_col:
    st.button(
        'Surprise me ✦',
        width='stretch',
        on_click=surprise_me,
        args=(options,)
    )
track_index = options.index(selected_label)
current = recommender.get_metadata(track_index)
current_art = spotify_artwork(current['track_id'])

with st.sidebar:
    if current_art:
        st.image(current_art, width=265)
    st.markdown(
        f'''
        <div class="sidebar-song-title">{escape(str(current['track_name']))}</div>
        <div class="sidebar-artist">{escape(str(current['track_artist']))}</div>
        ''',
        unsafe_allow_html=True
    )
    st.divider()
    mode = st.selectbox(
        'Recommendation mode',
        ['Keep up with what’s trending', 'Discover hidden gems']
    )
    mode_note = (
        'Leans toward the more popular songs among your closest matches.'
        if mode == 'Keep up with what’s trending'
        else 'Pushes lower-popularity matches upward so deeper cuts surface first.'
    )
    st.markdown(f'<div class="mode-note">{mode_note}</div>', unsafe_allow_html=True)
    count = st.slider(
        'Recommendations per section',
        min_value=1,
        max_value=10,
        value=3
    )
    st.markdown('<div class="sidebar-discovery-title">What kind of discovery?</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        same_artist = st.checkbox('Same artist', True)
        energy = st.checkbox('Energy', True)
        same_era = st.checkbox('Same era', True)
    with right:
        lyrics = st.checkbox('Lyrics', True)
        mood = st.checkbox('Mood', True)
        random_pick = st.checkbox('Wildcard', False)
    st.caption('Audio features + English lyrics · recommendations computed locally')
    if st.button('How it works ✦', width='stretch'):
        show_how_it_works()

enabled = {
    'by same artist': same_artist,
    'lyrically similar': lyrics,
    'similar energy': energy,
    'similar mood': mood,
    'released around same time': same_era,
    'random': random_pick
}

meta = []
if current['release_date']:
    meta.append(f'Released {current["release_date"]}')
meta.append(f'Popularity {current["track_popularity"]:.0f}/100')

with st.container(border=True, key='now_playing'):
    st.markdown(
        f'''
        <div class="now-playing-head">
            <div class="eyebrow">Now exploring</div>
            <div class="song-title">{escape(str(current['track_name']))}</div>
            <div>
                <span class="artist">{escape(str(current['track_artist']))}</span>
                <span class="meta">{' · '.join(meta)}</span>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    render_spotify_embed(current['track_id'])

if st.session_state.pop('scroll_to_player', False):
    scroll_to_now_playing()

action_left, action_right, spacer = st.columns([1, 1, 3.4])
with action_left:
    st.link_button('Open in Spotify ↗', current['spotify_url'], width='stretch')
with action_right:
    st.link_button('Watch on YouTube ↗', current['youtube_url'], width='stretch')

with st.expander('Show lyrics'):
    formatted_lyrics = escape(format_lyrics(current['lyrics']))
    st.markdown(f'<div class="lyrics">{formatted_lyrics}</div>', unsafe_allow_html=True)

prioritise_popular = mode == 'Keep up with what’s trending'
pool_count = min(max(count * 3, count + 6), 30)
recommendation_pool = recommender.recommend(track_index, pool_count, prioritise_popular)
visible_types = [name for name, is_enabled in enabled.items() if is_enabled]

if not visible_types:
    st.info('Choose at least one recommendation type in the sidebar.')

def recommendation_badge(recommendation_type, song, popular_mode):
    popularity = song['track_popularity']
    if recommendation_type == 'random':
        return 'Wildcard'
    if popular_mode and popularity >= 70:
        return 'Popular pick'
    if not popular_mode and popularity <= 35:
        return 'Hidden gem'
    if recommendation_type == 'released around same time':
        return 'Same era'
    return None


for recommendation_type in visible_types:
    pool = recommendation_pool[recommendation_type]
    if not pool:
        continue

    heading, explanation = section_copy[recommendation_type]
    state_key = f'section_offset::{track_index}::{prioritise_popular}::{count}::{recommendation_type}'
    offset = st.session_state.get(state_key, 0)

    if offset >= len(pool):
        offset = 0
        st.session_state[state_key] = 0

    songs = (pool[offset:] + pool[:offset])[:count]

    st.divider()
    heading_col, refresh_col = st.columns([5, 1.35], vertical_alignment='center')
    with heading_col:
        st.subheader(heading)
    with refresh_col:
        if len(pool) > count:
            st.button(
                'Try another ↻',
                key=f'refresh-{recommendation_type}-{track_index}-{prioritise_popular}-{count}',
                width='stretch',
                on_click=advance_section,
                args=(state_key, len(pool), count)
            )

    st.markdown(
        f'<div class="section-kicker">{escape(explanation)}</div>',
        unsafe_allow_html=True
    )

    for start in range(0, len(songs), 3):
        batch = songs[start:start + 3]
        columns = st.columns(3)

        for column, song in zip(columns, batch):
            with column:
                with st.container(border=True):
                    artwork = spotify_artwork(song['track_id'])
                    if artwork:
                        st.image(artwork, width='stretch')

                    st.markdown(
                        f'<div class="card-title">{escape(str(song["track_name"]))}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="card-artist">{escape(str(song["track_artist"]))}</div>',
                        unsafe_allow_html=True
                    )

                    song_meta = []
                    if song['release_date']:
                        song_meta.append(str(song['release_date']))
                    song_meta.append(f'popularity {song["track_popularity"]:.0f}/100')

                    st.markdown(
                        f'<div class="card-meta">{" · ".join(song_meta)}</div>',
                        unsafe_allow_html=True
                    )

                    badge = recommendation_badge(
                        recommendation_type,
                        song,
                        prioritise_popular
                    )
                    if badge:
                        st.markdown(
                            f'<div class="card-badge">{escape(badge)}</div>',
                            unsafe_allow_html=True
                        )

                    st.button(
                        'Explore this song',
                        key=f'use-{recommendation_type}-{song["index"]}',
                        width='stretch',
                        on_click=choose_song,
                        args=(options[song['index']],)
                    )

                    link_left, link_right = st.columns(2)
                    with link_left:
                        st.link_button('Spotify', song['spotify_url'], width='stretch')
                    with link_right:
                        st.link_button('YouTube', song['youtube_url'], width='stretch')


st.markdown('<div class="footer">💜 Made by Keera 💜</div>', unsafe_allow_html=True)