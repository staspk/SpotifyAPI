## SpotifyAPI
- See your all-time favorites
- Generate lost song candidates
- Programmatically create playlists

### Example Use
Ever lose a beloved song? Create a Spotify playlist of lost song candidates (lifetime_most_listened - liked_songs):
```
lost_song_candidates = SpotifyUser(PATH_TO_USER_DATA).getLostSongCandidates(min_mins_listened=60)

SaveToPlaylistRequest.New_Playlist(
	access_token,
	user_name,
	playlist_name,
	description
).Handle(lost_song_candidates).Result(True)
```

### Steps to run above code: 
- Spotify Data, where:
  	- https://www.spotify.com/us/account/privacy/ - USA Accounts Direct Link
  	- https://www.spotify.com/account - Scroll down, click on 'Account Privacy', otherwise.
- Spotify Data, types:
	- **Account Data**:  				wait time: ~several days. ***[REQUIRED]***
	- **Extended Streaming History**:  	wait time: <=week.         ***[REQUIRED]***
	- Technical Log:				wait time: ~2-4 weeks
- `py ./import_spotify_data.py {name}`
    - `name`: owner of the Spotify Data. separate `*.zips` will be categorized under this name
    - find a Spotify Data `*.zip` file through the File Chooser
 - **Generate Secrets**
 	- Register your app on [Developer Dashboard](https://developer.spotify.com/dashboard)
    	- *Redirect URI*: *`http://127.0.0.1:8080/callback`*
  	- After registration, use values to complete the template file: `./.env/.env`:
	    ```
		client_id={Client ID}
		client_secret={Client secret}
	    ```