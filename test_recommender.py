import pytest

from recommender import MusicRecommender


@pytest.fixture(scope='module')
def engine():
    return MusicRecommender('spotify_songs.csv')


def test_recommendation_counts(engine):
    result = engine.recommend(100, count=4, prioritise_popular=True)
    assert set(result) == {
        'by same artist',
        'lyrically similar',
        'similar energy',
        'similar mood',
        'released around same time',
        'random'
    }
    assert all(len(songs) <= 4 for songs in result.values())


def test_metadata(engine):
    metadata = engine.get_metadata(100)
    assert {
        'track_id',
        'track_name',
        'track_artist',
        'lyrics',
        'spotify_url',
        'youtube_url'
    }.issubset(metadata)
    assert metadata['spotify_url'].startswith('https://open.spotify.com/track/')


def test_recommendations_exclude_source_song(engine):
    result = engine.recommend(100, count=5, prioritise_popular=False)
    returned_indexes = [song['index'] for songs in result.values() for song in songs]
    assert 100 not in returned_indexes


def test_popularity_modes_change_ranking(engine):
    popular = engine.recommend(100, count=5, prioritise_popular=True)['lyrically similar']
    hidden = engine.recommend(100, count=5, prioritise_popular=False)['lyrically similar']
    assert [song['index'] for song in popular] != [song['index'] for song in hidden]
