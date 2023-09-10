# 🎶 Customizable Music Recommendation System 🎶

This web app is a prototype for a music recommendation system unlike any other. Most traditional systems are not very transparent about why a recommendation is made, and seem like magical black boxes. What sets apart this customizable music recommendation system from the rest, is that it aims to clearly convey the reason behind each recommendation, and put all the control in the hands of the user so that they can pick and choose what kind of recommendations they'd like, and hence personalize the system just as they want.

## Features
### Core features
- 2 modes of recommendations between which the user can toggle anytime:
  - Keep up with what's trending (suggests more popular songs)
  - Discover hidden gems (suggests less popular songs)
- A total of 6 types of recommendations:
  - by same artist
  - lyrically similar (not seen in most popular music streaming services)
  - similar energy
  - similar mood
  - released around the same time
  - random
- User can choose to see any, all, or none of the aforementioned recommendation types
- User can set the number of recommendations of each chosen type in the range of 1 to 10
### UX related features
- Ability to show or hide the lyrics for each song
- Youtube video linked for each song
- Viewing a recommended song by clicking on the listen button, will then lead to recommendations based on that song
- Ability to switch the width of the main content area
- Ability to choose between a custom (pastel), light and dark theme.
- Handy hamburger menu with options to report a bug, share the web app, view source code, read about it, see credits, etc
- Cross Platform & Responsive - The site works and looks pretty on any device it is viewed on, irrespective of screen shape and size

## Use Case Examples:
- Suppose User A has been out of the loop and wants to get up to speed with the most popular music. They can use the (default) "keep up with what's trending mode". If another User B already knows most of the popular songs and would rather listen to lesser known tracks, the "discover hidden gems" mode is for them. These modes are clearly differentiated based on the songs' popularity.
- If User C doesn't care much about the lyrics of a song but only their overall energy and mood, they can turn off the "lyrically similar" recommendations, while if User D treats songs like poetry and primarily focuses on just the lyrics, they can do the opposite.
- User E is interested in songs of a particular era, so they can turn on just the "released around the same time" recommendations" to explore contemporary songs
- User F has just discovered their new favourite artist and wants to explore their discography, be it their popular hits or underrated songs, so they can turn on the "by same artist" recommendations alone.
- User G knows that they get easily distracted when faced with too many choices of recommendations to choose from, so they can reduce the number of recommendations shown down to 1, while if User H likes variety they can turn up the number of recommendations of each type to up to 10!
- User I is feeling adventurous and would like to stumble upon music without any relation to their usual taste. The random recommendations are perfect for them!

## Technologies Used

Python was used throughout along with the following modules:
- Pandas
- Numpy
- Scikit Learn
- Streamlit (for frontend)

## Local Set Up

After cloning the repository and firing up a virtual environment, run the following commands:
```
pip install -r requirements.txt    # installs dependencies
streamlit run app.py               # runs the frontend locally in browser
```
For running tests, ensure you have pytest installed via pip, then simply run the command `pytest`

## Folder Organization

    ├── .github/workflows/test.yml          # CI pipeline to automatically test code
    ├── .streamlit/config.toml              # Custom theming for frontend
    ├── pickles                             # Data used to make recommendations 
    │   ├── data.pkl                     
    │   ├── energy_similarity_mapping.pkl 
    │   ├── lyric_similarity_mapping.pkl
    │   └── mood_similarity_mapping.pkl
    ├── .gitignore 
    ├── app.py                              # frontend using streamlit
    ├── preprocessing.py                    # cleans data and generates pickles
    ├── recommender.py                      # code for core recommendation system
    ├── recommender.ipynb                   # initial testing of system
    ├── requirements.txt 
    ├── spotify_songs.csv                   # raw sourced data
    └── test_recommender.py                 # tests for recommender using pytest

The 3 main files of interest (with relevant code) are `preprocessing.py`, `app.py` and `recommender.py`

Sidenote: One may think that the pickle files should have been gitignored, as running `preprocessing.py` would generate them anyway, but they had to be pushed since the deployment is from this repository, so they need to be present here. The jupyter notebook too is not needed for the code to work at any stage, however it is included here to show and document the progress of this project - I worked solely on the notebook initially, and only later broke it into 2 files when I had a clearer idea of where this project was headed.

## Testing and CI

The core functionality of the recommender is tested using `pytest` and the tests are in the `test_recommender.py` file. Using GitHub Actions a workflow (`.github/workflows/test.yml`) has been set up that runs these tests everytime code is pushed or a pull request is made to the repository.

## CD
The streamlit frontend is hosted at https://share.streamlit.io/n-shar-ma/customizable-music-recommendation-system/app.py, where anytime changes are pushed to the master branch, the site is updated.

## Development Process

Being completely new to ML, I spent the 1st 5 days simply doing research on the internet. I scoured through several technical blogs, lots of library specific documentation, browsed through GitHub repositories, and made a lot of Google Searches to understand how traditional recommendation systems actually work. Once I understood common jargon like content based, collaborative based and hybrid recommendation systems, and ML terms like cosine similarity and euclidean distance, I started forming opinions on what kind of system I'd like to build and what features would make it stand out and appeal to a large userbase... The answer I came up with was: customizability!

In the same 5 days, after lots of fruitless search for a suitable dataset, I finally narrowed down on [this one from Kaggle](https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs)

The next 3 days were spent exploring, experimenting with and visualising the data in a Jupyter Notebook, writing the code for several types and modes of recommendations (both the search and sort algorithms for the system), and then also tying them together as a hybrid system. Once I had these basics set up and functional, I spent my 4th day of coding in splitting all this Jupyter Notebook code into 2 appropriate `.py` files, where the first processed and pickled necessary data which the second used to give recommendations.

Over the next 3 days, I worked on the streamlit frontend, initially focusing on displaying all the recommendations appropriately, then on increasing customizability, and finally on cosmetic features like adding YouTube thumbnails and links for each song, making a custom pastel theme, adding credits for the dataset used in the about section, and so on. During this time I also set up the CD pipeline, for which I'd need my pickle files to be stored in the repository as well, but then I realised that they were way too large for that. I was indeed in a pickle 😅. Before long though, it struck me that I was pickling much more data than necessary, so I tweaked the code to make it much more space efficient and fast. In the end, this roadblock was crossed and helped me improve my code's performance as well!

The last 3 days were spent in researching how testing in Python works (I'm already familiar with it in JavaScript), implementing it in my project, automating it through GitHub Actions, and in documenting everything in this README. I habitually comment my code as I write it and clean it at regular intervals, so I didn't have to take out time specially for that. On my mentor's advice I also created a power point [presentation](https://docs.google.com/presentation/d/1yXCtetw0YwBJQNKG5RkCuCG6ZSvpV31Zhqp854nvV28/edit?usp=sharing) for the [video demo](https://www.youtube.com/watch?v=adggmFChcag)