from random import randint
from recommender import hybrid_recommend, get_metadata, songs_count

random_song_index = randint(0, songs_count-1)

# test if number of each recommendation is less than or equal to the given count
def test_recommend_output():
    hybrid_recommend_output = hybrid_recommend(random_song_index, 5, True)
    for songs in hybrid_recommend_output.values():
        assert len(songs) <= 5

# test if metadata for a song includes the necessary keys
def test_metadata_output():
    get_metadata_output = get_metadata(random_song_index)
    assert {'track_name', 'track_artist', 'lyrics'}.issubset(get_metadata_output)
