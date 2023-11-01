from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import json
import random

app = FastAPI()


def load_song_data():
    with open('songs.json', 'r') as f:
        return json.load(f)


def load_lyrics_data():
    with open('lyrics.json', 'r') as f:
        return json.load(f)


lana_del_rey_songs = load_song_data()
combined_lyrics_data = load_lyrics_data()


@app.get("/songs")
def get_all_songs():
    return lana_del_rey_songs


@app.get("/songs/{album}")
def get_songs_by_album(album: str):
    if album in lana_del_rey_songs:
        return {album: lana_del_rey_songs[album]}
    else:
        raise HTTPException(status_code=404, detail="Album not found")


@app.get("/lyrics/{album}/{song}")
def get_lyrics(album: str, song: str):
    if album in combined_lyrics_data and song in combined_lyrics_data[album]:
        song_lyrics = combined_lyrics_data[album][song]
        return song_lyrics
    else:
        raise HTTPException(status_code=404, detail="Song or album not found")


@app.get("/random_lyric")
def get_random_lyric():
    album_name = random.choice(list(combined_lyrics_data.keys()))
    song_title = random.choice(list(combined_lyrics_data[album_name].keys()))
    song_lyrics = combined_lyrics_data[album_name][song_title]
    return {"lyric": random.choice(song_lyrics), "song": song_title}


@app.get("/songs/{album}/{song}")
def get_song_details(album: str, song: str):
    if album in lana_del_rey_songs and song in lana_del_rey_songs[album]:
        song_details = lana_del_rey_songs[album][song]
        return song_details
    else:
        raise HTTPException(status_code=404, detail="Song or album not found")


@app.get("/albums")
def get_albums_list():
    albums_list = list(lana_del_rey_songs.keys())
    return albums_list


@app.get("/random_song")
def get_random_song():
    random_album = random.choice(list(combined_lyrics_data.keys()))
    random_song = random.choice(list(combined_lyrics_data[random_album].keys()))
    return {"album": random_album, "song": random_song}


@app.get("/search_lyrics")
def search_lyrics(keyword: str = Query(..., description="Keyword to search in lyrics")):
    matching_lyrics = []

    for album, songs in combined_lyrics_data.items():
        for song, lyrics in songs.items():
            matching_lines = [line for line in lyrics if keyword.lower() in line.lower()]
            if matching_lines:
                matching_lyrics.append({
                    "album": album,
                    "song": song,
                    "lyrics": matching_lines
                })

    return matching_lyrics

