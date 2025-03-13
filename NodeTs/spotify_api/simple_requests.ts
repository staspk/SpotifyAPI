function printRed(msg: string): void {
	console.error(`\x1b[31m${msg}\x1b[0m`);
}

export async function getPlaylist(playlistId: string, accessToken: string): Promise<void> {
	const endpoint = `https://api.spotify.com/v1/playlists/${playlistId}`;
  
	const headers = {
	  'Authorization': `Bearer ${accessToken}`
	};
  
	try {
		const response = await fetch(endpoint, { headers });
		if (response.status === 200) {
			const data = await response.json();
			console.log(JSON.stringify(data, null, 4));
		} else {
			printRed(`response.status_code: ${response.status}`);
			const errorData = await response.json();
			printRed(`error message: ${errorData.error?.message}`);
		}
	} catch (error) {
		printRed(`An error occurred: ${error}`);
	}
}