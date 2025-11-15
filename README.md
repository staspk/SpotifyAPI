## SpotifyAPI
- See your all-time favorites
- Generate lost song candidates
- Programmatically create playlists

### Example Use
Ever lose a beloved song? Create a Spotify playlist of lost song candidates (lifetime_listening_record - liked_songs):
```
NAME = "Stan"	# same name from import step: `py ./import_spotify_data.py {name}`
lost_song_candidates = SpotifyUser(NAME).lost_song_candidates(minimum_listen_time_in_minutes=60)

SaveToPlaylistRequest.New_Playlist(
	playlist_name,
	description="",
	public=True
).Handle(lost_song_candidates).Result()
```

### Steps to run above code: 
- Spotify Data, types:
	- **Account Data** - ***[REQUIRED]***
	- **Extended Streaming History** - ***[REQUIRED]***
	- Technical Log
- Spotify Data, where:
  	- https://www.spotify.com/us/account/privacy/ - USA Accounts Direct Link
- `py ./import_spotify_data.py {name}`
    - `name`: owner of the Spotify Data. separate `*.zips` will be categorized under this name
    - find `my_spotify_data.zip` through the File Chooser
 - **Enable Spotify Web Api Interactions**
 	- click on (**Create app**) on the [Developer Dashboard](https://developer.spotify.com/dashboard)
    	- *Redirect URI*: *`http://127.0.0.1:8080/callback`*
  	- The new App's `Client ID` and `client secret` need to be copy/pasted into the template `./.env`:
	    ```
		client_id=
		client_secret=
	    ```
