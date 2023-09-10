Class Diagram
--------------
Class: RecommendationSystem
- data: pandas DataFrame
- songs_count: int
- lyric_similarity_mapping: numpy array
- energy_similarity_mapping: numpy array
- mood_similarity_mapping: numpy array
--------------------
+ sort_by_popularity(songs: pandas DataFrame, descending: bool=True): pandas DataFrame
+ get_similar(track_index: int, count: int, comparison_matrix: numpy array, select_smallest: bool): pandas DataFrame
+ recommendations_as_list(songs: pandas DataFrame, include_fields: List[str]): List[Dict[str, Any]]
+ get_closest_n(track_index: int, count: int): pandas DataFrame
+ get_metadata(track_index: int): Dict[str, Any]
+ get_by_same_artist(track_index: int, count: int): pandas DataFrame
+ get_lyrically_similar(track_index: int, count: int): pandas DataFrame
+ get_energy_similar(track_index: int, count: int): pandas DataFrame
+ get_mood_similar(track_index: int, count: int): pandas DataFrame
+ get_released_around_same_time(track_index: int, count: int): pandas DataFrame
+ recommend_by_same_artist(track_index: int, count: int, prioritisePopular: bool, include_fields: List[str]): List[Dict[str, Any]]
+ recommend_lyrically_similar(track_index: int, count: int, prioritisePopular: bool, include_fields: List[str]): List[Dict[str, Any]]
+ recommend_energy_similar(track_index: int, count: int, prioritisePopular: bool, include_fields: List[str]): List[Dict[str, Any]]
+ recommend_mood_similar(track_index: int, count: int, prioritisePopular: bool, include_fields: List[str]): List[Dict[str, Any]]
+ recommend_released_around_same_time(track_index: int, count: int, prioritisePopular: bool, include_fields: List[str]): List[Dict[str, Any]]
+ hybrid_recommend(track_index: int, count: int=5, prioritisePopular: bool=True): Dict[str, List[Dict[str, Any]]]
