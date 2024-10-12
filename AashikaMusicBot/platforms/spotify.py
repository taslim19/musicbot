"""Module for Spotify API integration to manage music playback."""

import logging
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython.__future__ import VideosSearch
import config

class SpotifyAPI:
    """Class to interact with the Spotify API for music playback."""

    def __init__(self):
        """Initialize Spotify API client."""
        self.regex = r"^(https:\/\/open.spotify.com\/)(.*)$"
        self.client_id = config.SPOTIFY_CLIENT_ID
        self.client_secret = config.SPOTIFY_CLIENT_SECRET
        if self.client_id and self.client_secret:
            self.client_credentials_manager = SpotifyClientCredentials(
                self.client_id, self.client_secret
            )
            self.spotify = spotipy.Spotify(
                client_credentials_manager=self.client_credentials_manager
            )
        else:
            self.spotify = None

    async def valid(self, link: str):
        """Validate if the link is a valid Spotify URL."""
        return bool(re.search(self.regex, link))

    async def track(self, link: str):
        """Fetch track details from Spotify."""
        track = self.spotify.track(link)
        info = track["name"]
        for artist in track["artists"]:
            fetched = f' {artist["name"]}'
            if "Various Artists" not in fetched:
                info += fetched
        results = VideosSearch(info, limit=1)
        for result in (await results.next())["result"]:
            ytlink = result["link"]
            title = result["title"]
            vidid = result["id"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": ytlink,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def play_track(self, link: str):
        """Play a track from the provided Spotify link."""
        logging.info("Received link: %s", link)
        if await self.valid(link):
            track_details, _ = await self.track(link)
            logging.info("Playing track: %s", track_details)
            await self.start_playback(track_details)  # Ensure this method exists
            return track_details
        logging.warning("Invalid link: %s", link)
        return None

    async def start_playback(self, track_details):
        """Start playing the provided track details."""
        # Your playback logic here
        pass  # Replace with actual implementation

    async def playlist(self, url):
        """Fetch tracks from a Spotify playlist."""
        playlist = self.spotify.playlist(url)
        playlist_id = playlist["id"]
        results = []
        for item in playlist["tracks"]["items"]:
            music_track = item["track"]
            info = music_track["name"]
            for artist in music_track["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)
        return results, playlist_id

    async def album(self, url):
        """Fetch tracks from a Spotify album."""
        album = self.spotify.album(url)
        album_id = album["id"]
        results = []
        for item in album["tracks"]["items"]:
            info = item["name"]
            for artist in item["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)

        return results, album_id

    async def artist(self, url):
        """Fetch top tracks for a Spotify artist."""
        artistinfo = self.spotify.artist(url)
        artist_id = artistinfo["id"]
        results = []
        artisttoptracks = self.spotify.artist_top_tracks(url)
        for item in artisttoptracks["tracks"]:
            info = item["name"]
            for artist in item["artists"]:
                fetched = f' {artist["name"]}'
                if "Various Artists" not in fetched:
                    info += fetched
            results.append(info)

        return results, artist_id
