from pprint import pprint
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup


# Obtain list of 100 top songs from a given year
year = input("What year you would like to travel to in YYYY-MM-DD format: ")
url = "https://www.billboard.com/charts/hot-100/"

response = requests.get(url+year)
soup = BeautifulSoup(response.text, "html.parser")

titles_tags = soup.find_all(name="h3", class_="a-no-trucate")
artists_tags = soup.find_all(name="span", class_="a-font-primary-s")

song_titles = [title.getText().strip() for title in titles_tags]
artists = [artist.getText().strip() for artist in artists_tags if artist.getText(
).strip() not in ["RIAA Certification:"]]

tracks = []
i = 0
for song in song_titles:
    tracks.append({'song': song, 'artist': artists[i]})
    i += 1

# Authenticate spotify API
scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id="#########", client_secret="########", redirect_uri="#######", scope=scope, show_dialog=True,
                              cache_path="music-timemachine/token.txt"))
user_id = sp.current_user()["id"]

# Search for the songs on Spotify
search_results = []
for track in tracks:
    search_results.append(sp.search(
        q='artist:' + track['artist'] + 'track:' + track['song'] + "year:" + year[:4], limit=1, type="track"))

track_RDIs = []

for result in search_results:
    try:
        track_RDIs.append(result['tracks']['items'][0]['uri'])
    except IndexError:
        print("Sorry, unable to find that song on Spotify")


playlist = sp.user_playlist_create(
    user=user_id, name=f"{year} Billboard Top 100", public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=track_RDIs)
