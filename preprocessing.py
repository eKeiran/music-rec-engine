# Importing the installed libraries and their required modules

import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances


# Reading and cleaning the music data 

data = pd.read_csv('spotify_songs.csv')
data = data[data['language'] == 'en']
data.drop(columns=['language', 'playlist_name', 'playlist_id'], inplace=True)
data = data.drop_duplicates(subset=['track_name', 'track_artist'])
data['track_album_release_date'] = pd.to_datetime(data['track_album_release_date'], infer_datetime_format=True)
data = data.sort_values(by=['track_album_release_date'])
data.reset_index(drop=True, inplace=True)
songs_count = data.shape[0]


# Sectioning off data for recommendation subsystems

lyrics_data = data['lyrics']
energy_data = data[['danceability', 'tempo', 'acousticness']]
mood_data = data[['mode', 'key', 'valence']]


# Utility function

def get_similar_indices(track_index, count, comparison_matrix, select_smallest):
    similar_songs_indexes = np.argsort(np.array(comparison_matrix[track_index]))
    similar_songs_indexes = np.delete(similar_songs_indexes, np.where(similar_songs_indexes == track_index))
    return similar_songs_indexes[:count] if select_smallest else similar_songs_indexes[::-1][:count]


# Using cosine similarity and Tfidf for making lyrics comparable, and mapping each song to 20 most similar

lyrics_data = TfidfVectorizer(stop_words='english').fit_transform(lyrics_data)
lyric_similarity_matrix = cosine_similarity(lyrics_data)
lyric_similarity_mapping = dict()
for i in range(songs_count):
    lyric_similarity_mapping[i] = get_similar_indices(i, 20, lyric_similarity_matrix, False)


# Using euclidean distance for making energy and mood comparable, and mapping each song to 20 most similar

energy_difference_matrix = euclidean_distances(energy_data)
energy_similarity_mapping = dict()
for i in range(songs_count):
    energy_similarity_mapping[i] = get_similar_indices(i, 20, energy_difference_matrix, True)

mood_similarity_matrix = euclidean_distances(mood_data)
mood_similarity_mapping = dict()
for i in range(songs_count):
    mood_similarity_mapping[i] = get_similar_indices(i, 20, lyric_similarity_matrix, True)


# pickling all data and similarity mappings needed for making recommendations

pickle.dump(data, open('pickles/data.pkl', 'wb'))
pickle.dump(lyric_similarity_mapping, open('pickles/lyric_similarity_mapping.pkl', 'wb'))
pickle.dump(energy_similarity_mapping, open('pickles/energy_similarity_mapping.pkl', 'wb'))
pickle.dump(mood_similarity_mapping, open('pickles/mood_similarity_mapping.pkl', 'wb'))

print('preprocessing done')
