from pathlib import Path
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


class MusicRecommender:
    def __init__(self, data_path='spotify_songs.csv'):
        self.data_path = Path(data_path)
        self.data = self._load_data()
        self.songs_count = len(self.data)
        self._build_models()

    def _load_data(self):
        data = pd.read_csv(self.data_path)
        data = data[data['language'].eq('en')].copy()
        data = data.drop_duplicates(subset=['track_name', 'track_artist'])
        data['lyrics'] = data['lyrics'].fillna('')
        data['track_id'] = data['track_id'].fillna('').astype(str)
        data['track_popularity'] = pd.to_numeric(data['track_popularity'], errors='coerce').fillna(0)
        data['track_album_release_date'] = pd.to_datetime(data['track_album_release_date'], errors='coerce')
        data = data.sort_values(['track_album_release_date', 'track_name'], na_position='last')
        return data.reset_index(drop=True)

    def _build_models(self):
        self.lyric_vectorizer = TfidfVectorizer(stop_words='english', max_features=30000, min_df=2)
        self.lyric_vectors = self.lyric_vectorizer.fit_transform(self.data['lyrics'])
        self.lyric_model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.lyric_model.fit(self.lyric_vectors)

        self.energy_features = ['danceability', 'energy', 'tempo', 'acousticness', 'loudness']
        self.mood_features = ['valence', 'mode', 'key', 'energy', 'danceability']

        self.energy_scaler = StandardScaler()
        energy_values = self.data[self.energy_features].fillna(0)
        self.energy_vectors = self.energy_scaler.fit_transform(energy_values)
        self.energy_model = NearestNeighbors(metric='euclidean')
        self.energy_model.fit(self.energy_vectors)

        self.mood_scaler = StandardScaler()
        mood_values = self.data[self.mood_features].fillna(0)
        self.mood_vectors = self.mood_scaler.fit_transform(mood_values)
        self.mood_model = NearestNeighbors(metric='euclidean')
        self.mood_model.fit(self.mood_vectors)

    def song_options(self):
        labels = self.data['track_name'].astype(str) + ' — ' + self.data['track_artist'].astype(str)
        return labels.tolist()

    def get_metadata(self, track_index):
        row = self.data.iloc[int(track_index)]
        release = row['track_album_release_date']
        track_id = row['track_id']
        return {
            'index': int(track_index),
            'track_id': track_id,
            'track_name': row['track_name'],
            'track_artist': row['track_artist'],
            'lyrics': row['lyrics'],
            'track_popularity': float(row['track_popularity']),
            'release_date': None if pd.isna(release) else release.date().isoformat(),
            'spotify_url': self.spotify_url(track_id),
            'youtube_url': self.youtube_search_url(row['track_name'], row['track_artist'])
        }

    @staticmethod
    def spotify_url(track_id):
        return f'https://open.spotify.com/track/{track_id}'

    @staticmethod
    def youtube_search_url(track_name, track_artist):
        query = quote_plus(f'{track_name} {track_artist} official audio')
        return f'https://www.youtube.com/results?search_query={query}'

    def _rerank(self, indexes, count, prioritise_popular):
        indexes = [int(i) for i in indexes]
        candidates = self.data.iloc[indexes].copy()
        candidates['_index'] = indexes
        candidates = candidates.sort_values('track_popularity', ascending=not prioritise_popular)
        return candidates.head(count)['_index'].astype(int).tolist()

    def _nearest(self, model, matrix, track_index, count, prioritise_popular):
        pool = min(self.songs_count, max(count * 8 + 1, 41))
        _, indexes = model.kneighbors(matrix[int(track_index)].reshape(1, -1), n_neighbors=pool)
        candidates = [i for i in indexes[0] if int(i) != int(track_index)]
        return self._rerank(candidates, count, prioritise_popular)

    def _nearest_lyrics(self, track_index, count, prioritise_popular):
        pool = min(self.songs_count, max(count * 8 + 1, 41))
        _, indexes = self.lyric_model.kneighbors(self.lyric_vectors[int(track_index)], n_neighbors=pool)
        candidates = [i for i in indexes[0] if int(i) != int(track_index)]
        return self._rerank(candidates, count, prioritise_popular)

    def _same_artist(self, track_index, count, prioritise_popular):
        artist = self.data.iloc[int(track_index)]['track_artist']
        indexes = self.data.index[self.data['track_artist'].eq(artist)].tolist()
        indexes = [i for i in indexes if i != int(track_index)]
        return self._rerank(indexes, count, prioritise_popular)

    def _released_around_same_time(self, track_index, count, prioritise_popular):
        target = self.data.iloc[int(track_index)]['track_album_release_date']
        if pd.isna(target):
            return []
        delta = (self.data['track_album_release_date'] - target).abs().dt.days
        candidates = delta.drop(index=int(track_index)).nsmallest(max(count * 8, 40)).index.tolist()
        return self._rerank(candidates, count, prioritise_popular)

    def _random(self, track_index, count):
        candidates = self.data.index[self.data.index != int(track_index)]
        if len(candidates) <= count:
            return candidates.astype(int).tolist()
        seed = int(track_index) * 1009 + count * 9176
        rng = np.random.default_rng(seed)
        return rng.choice(candidates.to_numpy(), size=count, replace=False).astype(int).tolist()

    def _records(self, indexes, reason):
        records = []
        for index in indexes:
            row = self.data.iloc[int(index)]
            release = row['track_album_release_date']
            track_id = row['track_id']
            records.append({
                'index': int(index),
                'track_id': track_id,
                'track_name': row['track_name'],
                'track_artist': row['track_artist'],
                'track_popularity': float(row['track_popularity']),
                'release_date': None if pd.isna(release) else release.date().isoformat(),
                'reason': reason,
                'spotify_url': self.spotify_url(track_id),
                'youtube_url': self.youtube_search_url(row['track_name'], row['track_artist'])
            })
        return records

    def recommend(self, track_index, count=3, prioritise_popular=True):
        track_index = int(track_index)
        return {
            'by same artist': self._records(
                self._same_artist(track_index, count, prioritise_popular),
                'More from the same artist'
            ),
            'lyrically similar': self._records(
                self._nearest_lyrics(track_index, count, prioritise_popular),
                'Closest match in lyric TF-IDF space'
            ),
            'similar energy': self._records(
                self._nearest(self.energy_model, self.energy_vectors, track_index, count, prioritise_popular),
                'Similar danceability, energy, tempo, acousticness and loudness'
            ),
            'similar mood': self._records(
                self._nearest(self.mood_model, self.mood_vectors, track_index, count, prioritise_popular),
                'Similar valence, mode, key, energy and danceability'
            ),
            'released around same time': self._records(
                self._released_around_same_time(track_index, count, prioritise_popular),
                'Released closest in time'
            ),
            'random': self._records(
                self._random(track_index, count),
                'A deliberate wildcard'
            )
        }
