import requests
from flask import Flask, render_template
import time

app = Flask(__name__)
PC_IP = "192.168.1.1" 
URL = f"http://{PC_IP}:5000/now-playing"

def fetch_now_playing():
    try:
        response = requests.get(URL)
        data = response.json()
        return data.get('now_playing', "No song playing")
    except Exception as e:
        return(str(e))

# Im using itunes as it doesnt need an api key hehe
def fetch_album_art(song_details):

    # Url dosnt like spaces
    query = song_details.replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Ensure something is there
        if data["resultCount"] > 0:
            artwork_url = data["results"][0]["artworkUrl100"]

            #Increase resolution to fit pannel
            artwork_url = artwork_url.replace("100x100", "600x600")
            return artwork_url
        else:
            return None
    else:
        return None
    
@app.route('/')
def index():
    now_playing = fetch_now_playing()
    album_art_url = fetch_album_art(now_playing)
    # This is Flask passing now_playing and the album art url to the index.html (Kinda like passing in variables if you want to think of it like that)
    return render_template('index.html', now_playing=now_playing, album_art_url=album_art_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)



