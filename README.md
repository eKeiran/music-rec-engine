# Mellifluous — Customizable Music Recommendation Engine 🎶

Mellifluous is an explainable music recommendation prototype built around one idea: users should be able to decide what “similar music” means to them.

Instead of returning one opaque ranked list, the app separates recommendations into understandable signals such as lyrics, mood, energy, artist and release period. Users can turn signals on or off, choose how many suggestions they want, and switch between popular tracks and lesser-known alternatives.

## What makes it different

The app supports:

- Same-artist recommendations
- Lyrically similar songs using TF-IDF and cosine distance
- Similar-energy songs using normalized audio features
- Similar-mood songs using valence, mode, key, energy and danceability
- Songs released around the same period
- Random wildcard recommendations
- “Keep up with what’s trending” and “Discover hidden gems” ranking modes
- 1–10 recommendations per category
- Searchable song selection
- Spotify artwork and an embedded Spotify player
- Reformatted lyrics display
- Direct Spotify and YouTube links
- Section-level explanations for why each recommendation group exists

## How it works

The dataset is filtered to English-language tracks and deduplicated by track and artist.

Lyrics are transformed into sparse TF-IDF vectors and queried with cosine nearest neighbors. Energy and mood use standardized audio-feature vectors with nearest-neighbor search. Release-period recommendations use date distance, while same-artist and random modes use deterministic filtering and sampling.

The popularity mode is applied as a reranking step over a pool of nearby candidates. This preserves the selected similarity signal while letting the user choose whether the final results lean mainstream or obscure.

Spotify track IDs already present in the dataset power the player and artwork without requiring Spotify authentication. YouTube is kept as a direct search link rather than a scraping dependency.

## Tech stack

- Python
- Pandas
- NumPy
- scikit-learn
- Streamlit
- Spotify Embeds / oEmbed
- pytest
- GitHub Actions

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows, activate the environment with `.venv\\Scripts\\activate` instead.

## Run tests

```bash
python -m pytest -q
```

Using `python -m pytest` ensures the test runner uses the same Python interpreter as the active virtual environment.

## Repository structure

```text
.
├── .github/workflows/test.yml
├── .streamlit/config.toml
├── app.py
├── recommender.py
├── requirements.txt
├── spotify_songs.csv
└── test_recommender.py
```

## Dataset

The project uses the Kaggle dataset “Audio Features and Lyrics of Spotify Songs.” The dataset is included for reproducibility of the demo.

## Revival notes

The first version precomputed and pickled large similarity mappings. The revived version keeps lyrics as a sparse TF-IDF matrix and uses nearest-neighbor search at query time. This removes fragile serialized model artifacts, simplifies deployment and keeps the recommendation logic inspectable.

The mood path also now uses the intended mood/audio features rather than the lyric similarity representation, and the advertised random recommendation mode is implemented.

The frontend keeps the purple/pastel identity of the original project while adding richer cards, album artwork and an embedded player.

## CI

GitHub Actions runs the test suite on pushes and pull requests to `main` using Python 3.11.
