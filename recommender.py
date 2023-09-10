# Importing the needed installed libraries

import pickle
import pandas as pd
import numpy as np


# Loading all the pickled data for making recommendations 

data = pickle.load(open('pickles/data.pkl', 'rb'))
songs_count = data.shape[0]
lyric_similarity_mapping = pickle.load(open('pickles/lyric_similarity_mapping.pkl', 'rb'))
energy_similarity_mapping = pickle.load(open('pickles/energy_similarity_mapping.pkl', 'rb'))
mood_similarity_mapping = pickle.load(open('pickles/mood_similarity_mapping.pkl', 'rb'))


# Utility functions

def sort_by_popularity(songs, descending=True):
    if descending:
        return songs.sort_values(by=['track_popularity'])[::-1]
    else:
        return songs.sort_values(by=['track_popularity'])

def get_similar(track_index, count, comparison_matrix, select_smallest):
    similar_songs_indexes = np.argsort(np.array(comparison_matrix[track_index]))
    similar_songs_indexes = np.delete(similar_songs_indexes, np.where(similar_songs_indexes == track_index))
    similar_songs_indexes = similar_songs_indexes[:count] if select_smallest else similar_songs_indexes[::-1][:count]
    return data.iloc[similar_songs_indexes].copy()

def recommendations_as_list(songs, include_fields):
    songs = songs[include_fields].copy()
    songs['index'] = songs.index
    return songs.to_dict(orient='records')

def get_closest_n(track_index, count):
    if track_index >= count//2 and track_index < songs_count-count//2:
        return pd.concat([data.iloc[track_index-count//2 : track_index], data.iloc[track_index+1 : track_index+count//2+1]])
    elif track_index < count//2:
        return data.head(count+1).drop(track_index)
    else:
        return data.tail(count+1).drop(track_index)

def get_metadata(track_index):
    return data.iloc[track_index][['track_name', 'track_artist', 'lyrics']].to_dict()

# Getters for recommendation subsystems

def get_by_same_artist(track_index, count):
    return data[data['track_artist'] == data.iloc[track_index]['track_artist']].drop(track_index)[:count]

def get_lyrically_similar(track_index, count):
    similar_songs_indexes = lyric_similarity_mapping[track_index][:count]
    return data.iloc[similar_songs_indexes].copy()

def get_energy_similar(track_index, count):
    similar_songs_indexes = energy_similarity_mapping[track_index][:count]
    return data.iloc[similar_songs_indexes].copy()

def get_mood_similar(track_index, count):
    similar_songs_indexes = mood_similarity_mapping[track_index][:count]
    return data.iloc[similar_songs_indexes].copy()

def get_released_around_same_time(track_index, count):
    return get_closest_n(track_index, count)


# Recommendation subsytems

def recommend_by_same_artist(track_index, count, prioritisePopular, include_fields):
    songs_by_same_artist = get_by_same_artist(track_index, count*2)
    songs_by_same_artist = sort_by_popularity(songs_by_same_artist, prioritisePopular)[:count]
    return recommendations_as_list(songs_by_same_artist, include_fields)

def recommend_lyrically_similar(track_index, count, prioritisePopular, include_fields):
    similar_songs = get_lyrically_similar(track_index, count*2)
    similar_songs = sort_by_popularity(similar_songs, prioritisePopular)[:count]
    return recommendations_as_list(similar_songs, include_fields)

def recommend_energy_similar(track_index, count, prioritisePopular, include_fields):
    similar_songs = get_energy_similar(track_index, count*2)
    similar_songs = sort_by_popularity(similar_songs, prioritisePopular)[:count]
    return recommendations_as_list(similar_songs, include_fields)

def recommend_mood_similar(track_index, count, prioritisePopular, include_fields):
    similar_songs = get_mood_similar(track_index, count*2)
    similar_songs = sort_by_popularity(similar_songs, prioritisePopular)[:count]
    return recommendations_as_list(similar_songs, include_fields) 

def recommend_released_around_same_time(track_index, count, prioritisePopular, include_fields):
    contemporary_songs = get_released_around_same_time(track_index, count*2)
    contemporary_songs = sort_by_popularity(contemporary_songs, prioritisePopular)[:count]
    return recommendations_as_list(contemporary_songs, include_fields)



# Hybrid recommendation system

def hybrid_recommend(track_index, count=5, prioritisePopular=True):
    include_fields = ['track_name', 'track_artist']
    all_recommendations = dict()
    all_recommendations['by same artist'] = recommend_by_same_artist(track_index, count, prioritisePopular, include_fields)
    all_recommendations['lyrically similar'] = recommend_lyrically_similar(track_index, count, prioritisePopular, include_fields)
    all_recommendations['similar energy'] = recommend_energy_similar(track_index, count, prioritisePopular, include_fields)
    all_recommendations['similar mood'] = recommend_mood_similar(track_index, count, prioritisePopular, include_fields)
    all_recommendations['released around same time'] = recommend_released_around_same_time(track_index, count, prioritisePopular, include_fields)
    return all_recommendations
