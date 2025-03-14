## SpotifyAPI
- See your all-time favorites
- Generate lost song candidates
- Programatically create playlists

### Example Use
```
lost_song_candidates = SpotifyUser(PATH_TO_USER_DATA).getLostSongCandidates(60)

SaveToPlaylistRequest.New_Playlist(
	access_token,
	'staspk',
	"Bronze - Duplicate",
	'For deleting songs'
).Handle(lost_song_candidates).Result(True)
```

### Get your Lifetime Listening Data
- https://www.spotify.com/us/account/privacy/ - My Direct Link
- https://www.spotify.com/account
	- Click on: 'Account Privacy'
	- Scroll down to section: 'Download your data'. Your Choices:
		- Account Data:  				wait time: ~several days
		- Extended Streaming History:  	wait time: ~week
		- Technical Log:				wait time: ~2-4 weeks
	- Do not forget to respond to your confirmation link.

