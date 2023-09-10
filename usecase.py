import graphviz

dot = graphviz.Digraph()

dot.node('User', shape='ellipse')
dot.node('MusicRecommendationSystem', shape='ellipse')
dot.node('Admin', shape='ellipse')

dot.node('SelectSong', shape='rectangle', label='Select a song for recommendations')
dot.node('SelectOptions', shape='rectangle', label='Select options for recommendations:\n- Lyrics\n- Mood\n- Energy\n- Same year\n- Same artist\n- Popular/Underrated')
dot.node('ChangeThemes', shape='rectangle', label='Change themes:\n- Light\n- Dark\n- Custom')
dot.node('SeeAboutMe', shape='rectangle', label='See the about me of admins')


dot.node('ChangeSongDataset', shape='rectangle', label='Change song dataset')
dot.node('RestrictUsage', shape='rectangle', label='Restrict usage')
dot.node('ReinventUI', shape='rectangle', label='Reinvent user interface')

dot.edge('User', 'SelectSong')
dot.edge('SelectSong', 'MusicRecommendationSystem')
dot.edge('MusicRecommendationSystem', 'SelectOptions')
dot.edge('SelectOptions', 'MusicRecommendationSystem')
dot.edge('MusicRecommendationSystem', 'ChangeThemes')
dot.edge('MusicRecommendationSystem', 'SeeAboutMe')

dot.edge('Admin', 'MusicRecommendationSystem')
dot.edge('Admin', 'ChangeSongDataset')
dot.edge('Admin', 'RestrictUsage')
dot.edge('Admin', 'ReinventUI')

dot.render('music_recommendation_system_use_case_diagram', view=True)
